import requests


class Request:
    def __init__(self, base_url):
        self.__base_url = base_url

    def fetch_data(self, forecast, area):
        url = self.__base_url.format(forecast=forecast, area=area)
        response = requests.get(url)

        if response.status_code == 404:
            raise Exception('Could not find the area you searched for')

        return response.text
