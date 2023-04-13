from typing import Dict

from litestar import Litestar, HttpMethod, Controller, post, route


class Stubborn(Controller):
    @post("/_register")
    def register(self) -> Dict[str, str]:
        """Keeping the tradition alive with hello world."""
        return {"hello": "world"}

    @route("/", http_method=list(HttpMethod))
    def replay(self) -> Dict[str, str]:
        """Keeping the tradition alive with hello world."""
        return {"hello": "world"}


app = Litestar(route_handlers=[Stubborn])
