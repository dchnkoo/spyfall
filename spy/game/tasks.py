from contextvars import Context

import typing as _t
import asyncio
import sys


_T = _t.TypeVar("_T")


type Task = _t.Coroutine[_t.Any, _t.Any, _T]
type task_name = str


class Tasks(list[asyncio.Task]):

    @property
    def current_task(self):
        if len(self) > 0:
            return self[-1]

    @current_task.setter
    def current_task(self, value):
        assert isinstance(
            value, asyncio.Task
        ), f"You cannot set {type(value)} to tasks list."
        self.insert(len(self), value)

    @property
    def previous_task(self):
        if len(self) > 1:
            return self[-2]

    @property
    def active(self):
        return self.__class__([task for task in self if self._done(task) is False])

    @property
    def cancelled(self):
        return self.__class__(
            [task for task in self if task.cancelled() or task.cancelling() > 0]
        )

    @property
    def finished(self):
        return self.__class__([task for task in self if task._state == "FINISHED"])

    def _done(self, task: asyncio.Task):
        if not task.done() and not task.cancelled() and task.cancelling() < 1:
            return False
        return True

    def pop(self, index: _t.SupportsIndex = -1) -> asyncio.Task:
        task = self[index]
        if self._done(task) is False:
            raise ValueError("If you want pop not completed task force_pop")
        return super(Tasks, self).pop(index)

    def force_pop(self, index: _t.SupportsIndex = -1) -> asyncio.Task:
        return super(Tasks, self).pop(index)

    def get_task(self, name: str):
        for task in self[::-1]:
            if task.get_name() == name:
                return task

    def append(self, object: asyncio.Task) -> None:
        if self.get_task(object.get_name()) is not None:
            if self._done(object) is False:
                raise ValueError("Cannot add exists task.")
        super(Tasks, self).append(object)

    def index(
        self,
        value: asyncio.Task,
        start: _t.SupportsIndex = 0,
        stop: _t.SupportsIndex = sys.maxsize,
    ) -> int:
        search_start = start
        prev_index = None
        while search_start > -1:
            index = super(Tasks, self).index(value, search_start, stop)
            if index > -1:
                if self._done(self[index]) is False:
                    return index
                elif prev_index == search_start:
                    return index
            prev_index = search_start
            search_start = index
        return search_start

    def insert(self, index: _t.SupportsIndex, object: asyncio.Task) -> None:
        if task := self.get_task(object.get_name()):
            exists_index = self.index(task)
            if index <= exists_index:
                raise ValueError(
                    f"Task index with existed name {task.get_name()} cannot be less or equal {exists_index}"
                )
            if self._done(task) is False:
                raise ValueError("You cannot add the same not completed task.")
        super(Tasks, self).insert(index, object)

    def clear(self) -> None:
        for task in self.active:
            task.cancel()
        return super(Tasks, self).clear()

    def copy(self) -> list[asyncio.Task]:
        return self.__class__(self)

    def remove(self, value: asyncio.Task) -> None:
        task = self.get_task(value.get_name())
        if self._done(task) is False:
            raise ValueError("Cannor remove not completed task, use force_remove")
        super(Tasks, self).remove(value)

    def force_remove(self, value: asyncio.Task) -> None:
        super(Tasks, self).remove(value)

    def count(self, name: task_name) -> int:
        counter = 0
        for task in self:
            if task.get_name() == name:
                counter += 1
        return counter

    def create_task(
        self, coro: Task, name: str, *args, context: Context | None = None, **kw
    ):
        if (task := self.get_task(name=name)) is not None and self._done(task) is False:
            raise ValueError(f"Task with name `{name}` already exists.")

        new_task = asyncio.create_task(coro(*args, **kw), name=name, context=context)
        super(Tasks, self).append(new_task)
        return new_task

    async def wait_until_complete_current_task(self):
        task = self.current_task
        assert task is not None, "Any tasks not found."
        if self._done(task) is False:
            await task

    def cancel_current_task(self):
        if (task := self.current_task) is not None and self._done(task) is False:
            task.cancel()


if __name__ == "__main__":

    async def print_some():
        print("START")
        await asyncio.sleep(1)
        print("END")

    async def main():
        tasks = Tasks()
        new_task = tasks.create_task(print_some, name="first")
        tasks.current_task = new_task

    asyncio.run(main())
