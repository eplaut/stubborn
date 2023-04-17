from typing import Dict

from litestar.exceptions import NotFoundException, MethodNotAllowedException

from .response import Response


class PathResponsePool:
    def __init__(self):
        self._pool: Dict[str, Response] = {}  # method -> Response

    def register(self, method: str, response: Response) -> None:
        self._pool[method.lower()] = response

    def get(self, method: str) -> Response:
        method = method.lower()
        if method not in self._pool:
            raise MethodNotAllowedException
        try:
            return self._pool[method]
        except NotFoundException:
            del self._pool[method]
            raise

    def __bool__(self):
        return bool(self._pool)


class ResponsePool:
    def __init__(self):
        self._pool: Dict[str, PathResponsePool] = {}  # path -> PathResponsePool

    def register(self, path: str, method: str, response: Response) -> None:
        if path not in self._pool:
            self._pool[path] = PathResponsePool()
        self._pool[path].register(method, response)

    def get(self, path: str, method: str) -> Response:
        method = method.lower()
        if path not in self._pool:
            raise NotFoundException
        try:
            return self._pool[path].get(method)
        except NotFoundException:
            if not self._pool[path]:
                del self._pool[path]
            raise
