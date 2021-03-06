from django.core import signing
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from . import factories


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def admin_api_client(user_factory) -> APIClient:
    user = user_factory(is_superuser=True)
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def child_folder(folder, folder_factory):
    return folder_factory(parent=folder)


@pytest.fixture
def hashed_file(file):
    file.compute_sha512()
    file.save()
    return file


@pytest.fixture
def pending_file(file_factory):
    return file_factory(size=42, blob=None, content_type='text/plain')


@pytest.fixture
def public_folder(folder_factory):
    return folder_factory(tree__public=True)


@pytest.fixture
def s3ff_field_value() -> str:
    """Generate a faked S3FileField field_value to pass via REST.

    Because S3FF currently doesn't check that the object was created, this just
    provides a fake signed value rather than mocking the entire S3FF upload process.
    """
    return signing.dumps(
        {
            'object_key': 'key',
            'file_size': 123,
        }
    )


register(factories.AuthorizedUploadFactory, 'authorized_upload')
register(factories.FileFactory)
register(factories.FolderFactory)
register(factories.TermsFactory)
register(factories.TermsAgreementFactory, 'terms_agreement')
register(factories.TreeFactory)
register(factories.TreeWithRootFactory)
register(factories.UserFactory)
