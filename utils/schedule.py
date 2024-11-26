import typing as _t
import asyncio
import inspect


type seconds = float


def call_later[
    F
](delay: seconds, func: _t.Callable | _t.Awaitable, *args: F, **kw,):
    loop = asyncio.get_running_loop()
    is_coro = inspect.iscoroutinefunction(func)
    task = lambda *args: asyncio.create_task(func(*args)) if is_coro else func(*args)
    loop.call_later(delay, task, *args, **kw)
