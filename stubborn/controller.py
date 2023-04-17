from typing import Dict

from litestar import Request, HttpMethod, Controller, post, route, Response as LitestarResponse
from litestar.datastructures import State

from .pool import ResponsePool
from .response import Response


class Stubborn(Controller):
    @classmethod
    def setup_state(cls, state: State) -> None:
        state["responses"] = ResponsePool()

    @post("/_register")
    async def register(self, state: State, request: Request) -> Dict[str, str]:
        res = await request.json()
        state["responses"].register(res["path"], res["method"], Response(res))
        return {"result": "success"}

    @route("{path:path}", http_method=list(HttpMethod))
    def replay(self, path: str, state: State, request: Request) -> LitestarResponse:
        return state["responses"].get(path, request.method).response
