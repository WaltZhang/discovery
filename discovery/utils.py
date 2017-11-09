import requests

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
