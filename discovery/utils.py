import requests
import json

from discovery import settings


def get_service_url(service):
    url = '{}://{}:{}/services/api/{}'.format(
        settings.SERVICE_PROTOCOL,
        settings.SERVICE_HOST,
        settings.SERVICE_PORT,
        service
    )
    response = requests.get(url)
    return response.json().get('url')


def get_connector():
    url = get_service_url('connector')
    print('url:', url)
    response = requests.get(url)
    return json.loads(response.text)
