from typing import Any, TypedDict, Optional

from litestar import Response as LitestarResponse
from litestar.exceptions import NotFoundException


class ResponseData(TypedDict):
    path: str
    method: str
    status_code: int
    count: Optional[int]
    response: Any


class Response:
    def __init__(self, data: ResponseData):
        self.count = float(data.get("count") or "inf")  # 0 or None interpreted as infinity
        self.status_code = data.get("status_code", 200)
        self._response = data["response"]

    @property
    def response(self) -> LitestarResponse:
        if self.count <= 0:
            raise NotFoundException
        self.count -= 1
        return LitestarResponse(self._response, status_code=self.status_code)
