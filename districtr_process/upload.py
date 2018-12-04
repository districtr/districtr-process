from time import sleep

import mapbox

from .exceptions import MapboxError


def attempt_upload(uploader, filename, upload_id):
    with open(filename, "rb") as source:
        upload_response = uploader.upload(source, upload_id)
    return upload_response


def retry(f, retries, pause, succeeded):
    result = f()
    if succeeded(result):
        return result

    for i in range(retries):
        sleep(pause)
        result = f()
        if succeeded(result):
            return result


def succeeded(resp):
    return resp.status_code != 422


def upload(filename, upload_id):
    uploader = mapbox.Uploader()

    def attempt():
        return attempt_upload(uploader, filename, upload_id)

    response = retry(attempt, retries=5, pause=5, succeeded=succeeded)

    if response.status_code != 201:
        raise MapboxError(response)

    return response
