import http.client

import pklib.ty as ty

type _datatype = bytes | ty.iter[ty.any] | ty.any


def conntype(url: str) -> type[http.client.HTTPConnection] | ty.any:
    if url.startswith("https://"):
        return http.client.HTTPSConnection

    return http.client.HTTPConnection


def domain_path(url: str) -> tuple[str, str]:
    sp = url.split("/", maxsplit=3)
    return (sp[2], "/" + sp[3])


def request(
    url: str,
    method: str,
    body: _datatype | str | None = None,
    headers: ty.map[str, ty.any | str | int] = {},
) -> http.client.HTTPResponse:
    dom, path = domain_path(url)
    conn = conntype(url)(dom)
    conn.request(method, path, body=body, headers=headers)
    result = conn.getresponse()
    return result


def get(
    url: str,
    body: _datatype | str | None = None,
    headers: ty.map[str, ty.any | str | int] = {},
):
    return request(url, "GET", body, headers)


def post(
    url: str,
    body: _datatype | str | None = None,
    headers: ty.map[str, ty.any | str | int] = {},
):
    return request(url, "GET", body, headers)
