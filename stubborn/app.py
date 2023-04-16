from typing import Dict

from litestar import Litestar, Request, HttpMethod, Controller, post, route, Response
from litestar.exceptions import NotFoundException
from litestar.datastructures import State


class Stubborn(Controller):
    @post("/_register")
    async def register(self, state: State, request: Request) -> Dict[str, str]:
        res = await request.json()
        if res["path"] not in state:
            state[res["path"]] = {}
        state[res["path"]][res["method"].lower()] = (
            float(res.get("count", "inf")),
            res["response"],
            int(res.get("status_code", 200)),
        )
        return {"result": "success"}

    @route("{path:path}", http_method=list(HttpMethod))
    def replay(self, path: str, state: State, request: Request) -> Response:
        res = state.get(path, {}).get(request.method.lower())
        if res is None:
            raise NotFoundException
        count, response, status_code = res
        if count == 0:
            raise NotFoundException
        state[path][request.method.lower()] = (count - 1, response, status_code)
        return Response(response, status_code=status_code)


app = Litestar(route_handlers=[Stubborn])
