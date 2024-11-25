from functools import partial

import typing as _t
import inspect
import asyncio


type seconds = int


async def wait(
    statement: _t.Awaitable[bool] | _t.Callable[[], bool],
    *,
    _for: seconds = 60,
    interval: int = 2,
    **statments_kw,
):
    seconds_left = _for

    is_coro = inspect.iscoroutinefunction(statement)
    func = partial(statement, **statments_kw)

    while seconds_left > 0:
        if seconds_left % interval == 0 and ((await func()) if is_coro else func()):
            return True
        await asyncio.sleep(interval)
    return False
