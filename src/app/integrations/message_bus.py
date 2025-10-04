import asyncio
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any

from app.core.singleton import SingletonMeta


Subscriber = Callable[[Any], Awaitable[None]]


class MessageBus(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._queue: asyncio.Queue[tuple[str, Any]] = asyncio.Queue()
        self._subscribers: dict[str, list[Subscriber]] = defaultdict(list)
        self._worker_task: asyncio.Task | None = None

    async def start(self) -> None:
        if self._worker_task is None:
            self._worker_task = asyncio.create_task(self._worker())

    async def publish(self, topic: str, payload: Any) -> None:
        await self._queue.put((topic, payload))
        if self._worker_task is None:
            await self.start()

    def subscribe(self, topic: str, handler: Subscriber) -> None:
        self._subscribers[topic].append(handler)

    async def _worker(self) -> None:
        while True:
            topic, payload = await self._queue.get()
            handlers = self._subscribers.get(topic, [])
            for handler in handlers:
                await handler(payload)
            self._queue.task_done()
