import re

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
import pytest

from dkc.core.exceptions import MaxFolderDepthExceeded
from dkc.core.models.folder import Folder


@pytest.fixture
def limited_tree_height():
    original, Folder.MAX_TREE_HEIGHT = Folder.MAX_TREE_HEIGHT, 3
    yield Folder.MAX_TREE_HEIGHT
    Folder.MAX_TREE_HEIGHT = original


def test_folder_name_invalid(folder_factory):
    folder = folder_factory.build(name='name / withslash')

    # Since the folder is not saved and added to a tree, other validation errors are also present,
    # so it's critical to match the error by string content
    with pytest.raises(ValidationError, match='Name may not contain forward slashes'):
        folder.full_clean()


def test_is_root_root(folder_factory):
    folder = folder_factory.build()
    assert folder.is_root is True


def test_is_root_child(folder_factory):
    folder = folder_factory.build()
    child = folder_factory.build(parent=folder)
    assert child.is_root is False


@pytest.mark.django_db
def test_ancestors(folder, folder_factory):
    child = folder_factory(parent=folder)
    grandchild = folder_factory(parent=child)
    assert list(grandchild.ancestors) == [grandchild, child, folder]


@pytest.mark.django_db
def test_root_folder_depth_is_zero(folder):
    assert folder.depth == 0


@pytest.mark.django_db
def test_child_folder_depth_computed(folder, folder_factory):
    child = folder_factory(parent=folder)
    assert child.depth == folder.depth + 1


@pytest.mark.django_db
def test_folder_max_depth_enforced(folder, folder_factory, limited_tree_height):
    for _ in range(limited_tree_height):
        folder = folder_factory(parent=folder)

    with pytest.raises(MaxFolderDepthExceeded):
        folder_factory(parent=folder)


@pytest.mark.django_db
def test_folder_root_self_reference(folder):
    assert folder.root_folder == folder


@pytest.mark.django_db
def test_root_folder_inherited(folder, folder_factory):
    child = folder_factory(parent=folder)
    grandchild = folder_factory(parent=child)
    assert child.root_folder == folder
    assert grandchild.root_folder == folder


@pytest.mark.django_db
def test_folder_sibling_names_unique(folder, folder_factory):
    child = folder_factory(parent=folder)
    with pytest.raises(IntegrityError):
        folder_factory(name=child.name, parent=folder)


@pytest.mark.django_db
def test_folder_sibling_names_unique_files(file, folder_factory):
    escaped = re.escape(file.name)
    sibling_folder = folder_factory.build(parent=file.folder, name=file.name)
    with pytest.raises(
        ValidationError, match=fr'There is already a file here with the name "{escaped}"\.'
    ):
        sibling_folder.full_clean()


@pytest.mark.django_db
def test_root_folder_names_unique(folder, folder_factory):
    other_root = folder_factory.build(name=folder.name)
    with pytest.raises(IntegrityError):
        other_root.save()


@pytest.mark.django_db
def test_folder_names_not_globally_unique(folder_factory):
    root = folder_factory()
    child = folder_factory(name=root.name, parent=root)
    assert child


@pytest.mark.parametrize('amount', [-10, 0, 10])
@pytest.mark.django_db
def test_increment_size(folder_factory, amount):
    initial_size = 100
    root = folder_factory(size=initial_size)
    child = folder_factory(parent=root, size=initial_size)
    grandchild = folder_factory(parent=child, size=initial_size)

    grandchild.increment_size(amount)

    # Local references to other objects "root", "child" are stale
    # We can only guarantee integrity from the mutated object
    new_size = initial_size + amount
    assert grandchild.size == new_size
    assert grandchild.parent.size == new_size
    assert grandchild.parent.parent.size == new_size


@pytest.mark.django_db
def test_increment_size_negative(folder_factory):
    # Make the root too small
    root = folder_factory(size=5)
    child = folder_factory(parent=root, size=10)

    # Increment the child, which tests enforcement across propagation
    with pytest.raises(IntegrityError, match=r'size'):
        child.increment_size(-10)
