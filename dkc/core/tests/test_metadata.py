from django.core.exceptions import ValidationError
import pytest


@pytest.mark.parametrize(
    'metadata',
    [
        1,
        [],
        [1],
        True,
        False,
        '',
        'hello',
    ],
)
@pytest.mark.django_db
def test_invalid_metadata(metadata, folder_factory):
    folder = folder_factory(user_metadata=metadata)
    with pytest.raises(ValidationError) as err:
        folder.full_clean()
    assert len(err.value.error_dict['user_metadata']) == 1
    assert err.value.error_dict['user_metadata'][0].message == 'Must be a JSON Object.'


@pytest.mark.xfail
@pytest.mark.parametrize(
    'metadata',
    [
        {},
        {'a': 'b'},
        {2: 3},
        {'nested': {'foo': [1, 2]}},
    ],
)
@pytest.mark.django_db
def test_valid_metadata(metadata, folder_factory):
    folder = folder_factory(user_metadata=metadata)
    folder.full_clean()
