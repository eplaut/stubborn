from typing import Dict, Optional

from litestar import Request, HttpMethod, Controller, post, route, Response as LitestarResponse
from litestar.exceptions import NotFoundException
from litestar.datastructures import State

from .response import Response


class Stubborn(Controller):
    @post("/_register")
    async def register(self, state: State, request: Request) -> Dict[str, str]:
        res = await request.json()
        if res["path"] not in state:
            state[res["path"]] = {}
        state[res["path"]][res["method"].lower()] = Response(res)
        return {"result": "success"}

    @route("{path:path}", http_method=list(HttpMethod))
    def replay(self, path: str, state: State, request: Request) -> LitestarResponse:
        response: Optional[Response] = state.get(path, {}).get(request.method.lower())
        if response is None:
            raise NotFoundException
        return response.response
