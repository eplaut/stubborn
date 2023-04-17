from typing import Dict

from litestar.exceptions import NotFoundException, MethodNotAllowedException

from .response import Response


class ResponsePool:
    def __init__(self):
        self._pool: Dict[str, Dict[str, Response]] = {}  # path -> method -> response

    def register(self, path: str, method: str, response: Response) -> None:
        if path not in self._pool:
            self._pool[path] = {}
        self._pool[path][method.lower()] = response

    def get(self, path: str, method: str) -> Response:
        method = method.lower()
        if path not in self._pool:
            raise NotFoundException
        if method not in self._pool[path]:
            raise MethodNotAllowedException
        try:
            return self._pool[path][method]
        except NotFoundException:
            del self._pool[path][method]
            raise
