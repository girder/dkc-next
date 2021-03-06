from hashlib import md5

import pytest

from dkc.core.models import TermsAgreement
from dkc.core.permissions import Permission, PermissionGrant


@pytest.mark.django_db
def test_terms_checksum_computed(terms_factory):
    terms = terms_factory(text='hello')
    assert terms.checksum == md5(b'hello').hexdigest()


@pytest.mark.django_db
def test_terms_get(admin_api_client, terms):
    resp = admin_api_client.get(f'/api/v2/folders/{terms.tree.root_folder.id}/terms')
    assert resp.status_code == 200
    assert resp.data['text'] == terms.text
    assert resp.data['checksum'] == terms.checksum


@pytest.mark.django_db
def test_terms_agreement_get(admin_api_client, terms):
    resp = admin_api_client.get(f'/api/v2/folders/{terms.tree.root_folder.id}/terms/agreement')
    assert resp.status_code == 200
    assert resp.data['text'] == terms.text
    assert resp.data['checksum'] == terms.checksum


@pytest.mark.django_db
def test_terms_agreement_unauthenticated(api_client, terms):
    terms.tree.public = True
    terms.tree.save()
    resp = api_client.get(f'/api/v2/folders/{terms.tree.root_folder.id}/terms/agreement')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_terms_agreement_get_existing(api_client, terms_agreement):
    user = terms_agreement.user
    terms_agreement.terms.tree.grant_permission(
        PermissionGrant(user_or_group=user, permission=Permission.read)
    )
    api_client.force_authenticate(user=user)
    resp = api_client.get(
        f'/api/v2/folders/{terms_agreement.terms.tree.root_folder.id}/terms/agreement'
    )
    assert resp.status_code == 204


@pytest.mark.django_db
def test_terms_agreement_get_updated(api_client, terms_agreement):
    # Updated terms should require re-agreement
    terms_agreement.terms.text += 'extra content'
    terms_agreement.terms.save()

    user = terms_agreement.user
    terms_agreement.terms.tree.grant_permission(
        PermissionGrant(user_or_group=user, permission=Permission.read)
    )
    api_client.force_authenticate(user=user)
    resp = api_client.get(
        f'/api/v2/folders/{terms_agreement.terms.tree.root_folder.id}/terms/agreement'
    )
    assert resp.status_code == 200
    assert resp.data['text'] == terms_agreement.terms.text


@pytest.mark.django_db
def test_terms_agreement_post(api_client, terms, user):
    terms.tree.public = True
    terms.tree.save()
    api_client.force_authenticate(user=user)
    resp = api_client.post(
        f'/api/v2/folders/{terms.tree.root_folder.id}/terms/agreement',
        data={'checksum': terms.checksum},
    )
    assert resp.status_code == 204

    agreement = TermsAgreement.objects.get(terms=terms, user=user)
    assert agreement.checksum == terms.checksum


@pytest.mark.django_db
def test_terms_agreement_post_invalid_checksum(api_client, terms, user):
    terms.tree.public = True
    terms.tree.save()
    api_client.force_authenticate(user=user)
    resp = api_client.post(
        f'/api/v2/folders/{terms.tree.root_folder.id}/terms/agreement', data={'checksum': 'invalid'}
    )
    assert resp.status_code == 400
    assert resp.json()['checksum'] == 'Mismatched checksum. Your terms may be out of date.'


@pytest.mark.django_db
def test_terms_agreement_post_invalid_folder(api_client, folder, user):
    folder.tree.public = True
    folder.tree.save()
    api_client.force_authenticate(user=user)
    resp = api_client.post(f'/api/v2/folders/{folder.id}/terms/agreement', data={'checksum': 'x'})
    assert resp.status_code == 400
    assert resp.json()['folder'] == 'This folder has no associated terms of use.'
