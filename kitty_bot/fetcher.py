from __future__ import annotations

from httpx import Response, get


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

    def get(self) -> Response:
        return get(self.url, params=self.params)

    def get_json(self) -> dict | list[dict]:
        return self.get().json()
