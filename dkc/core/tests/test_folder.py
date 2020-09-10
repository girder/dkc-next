from django.core.exceptions import ValidationError
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
