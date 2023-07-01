import hashlib
import hmac
from http import HTTPStatus

import git
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

w_secret = settings.SECRET_KEY


def is_verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    hash_object = hmac.new(
        secret_token.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)


@csrf_exempt
def pull_repo(request):
    """
    Compare secret key, and pull repo to get changes from GitHub.

    """
    if request.method != 'POST':
        return HttpResponse('Wrong event.', status=HTTPStatus.BAD_REQUEST)
    x_hub_signature = request.headers.get('X-Hub-Signature-256')

    if not is_verify_signature(request.body, w_secret, x_hub_signature):
        return HttpResponse('Wrong event.', status=HTTPStatus.BAD_REQUEST)

    repo = git.Repo('/home/momonline/hmom3')
    repo.remotes.origin.pull()

    return HttpResponse('Updated.', status=HTTPStatus.OK)
