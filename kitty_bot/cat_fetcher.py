from __future__ import annotations

from random import choice

import httpx


class ApiRequestBuilder:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
        self.url_paths: list[str] = []
        self.url_query_params: dict[str, str] = {}

    def paths(self, *paths: str) -> ApiRequestBuilder:
        self.url_paths.extend(paths)
        return self

    def params(self, **params: str) -> ApiRequestBuilder:
        self.url_query_params |= params
        return self

    def build(self) -> ApiRequest:
        return ApiRequest(
            url=self.base_url + '/'.join(self.url_paths),
            params=self.url_query_params,
        )


class ApiRequest:
    @classmethod
    def builder(cls, base_url: str) -> ApiRequestBuilder:
        return ApiRequestBuilder(base_url)

    def __init__(self, url: str, params: dict[str, str]) -> None:
        self.url = url
        self.params = params

    def get(self) -> httpx.Response:
        return httpx.get(self.url, params=self.params)

    def get_json(self) -> dict | list[dict]:
        return self.get().json()


def get_random_animal_url(api_url: str) -> str:
    api_json = (
        ApiRequest.builder(api_url)
        .paths('v1', 'images', 'search')
        .build()
        .get_json()
    )

    if isinstance(api_json, list):
        if not len(api_json):
            raise ValueError('Empty api json')
        api_json = choice(api_json)

    picture_url = api_json.get('url')
    if not picture_url:
        raise ValueError('Picture url is missing')

    return picture_url
