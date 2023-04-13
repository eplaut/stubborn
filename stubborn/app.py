from typing import Dict

from litestar import Litestar, Request, HttpMethod, Controller, post, route
from litestar.datastructures import State


class Stubborn(Controller):
    @post("/_register")
    async def register(self, state: State, request: Request) -> Dict[str, str]:
        res = await request.json()
        if res["path"] not in state:
            state[res["path"]] = {}
        state[res["path"]][res["method"]] = (res.get("count", float("inf")), res["response"])
        return {"result": "success"}

    @route("/", http_method=list(HttpMethod))
    def replay(self, state: State) -> Dict[str, str]:
        """Keeping the tradition alive with hello world."""
        return dict(state)


app = Litestar(route_handlers=[Stubborn])
