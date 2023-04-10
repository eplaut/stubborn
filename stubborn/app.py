from typing import Dict

from litestar import Litestar, get, HttpMethod
from litestar.handlers.http_handlers.decorators import HTTPRouteHandler


@HTTPRouteHandler("/", http_method=HttpMethod)
def hello_world() -> Dict[str, str]:
    """Keeping the tradition alive with hello world."""
    return {"hello": "world"}


app = Litestar(route_handlers=[hello_world])
