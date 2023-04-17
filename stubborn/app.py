from litestar import Litestar
from .controller import Stubborn


app = Litestar(route_handlers=[Stubborn], on_startup=[Stubborn.setup_state])
