from _thread import allocate_lock
from dataclasses import dataclass

import pklib.ty as ty

type event = type[baseevent]
type listener = ty.cb[[ty.any], ty.any]


@dataclass
class baseevent:
    canceled: bool = False

    def on_error(self, e: Exception):
        pass

    @classmethod
    def on(cls, f: listener):
        eventbus.INSTANCE.subscribe(cls, f)
        return f

    def end(self, result: ty.any):
        pass


class eventbus:
    INSTANCE: "eventbus"

    def __init__(self):
        self.listeners: dict[event, list[listener]] = {}
        self.lock = allocate_lock()

    def subscribe(self, event: event, func: listener):
        with self.lock:
            self.listeners.setdefault(event, []).append(func)

    def post(self, event: baseevent):
        with self.lock:
            listeners = self.listeners.get(type(event), []).copy()

        for f in listeners:
            try:
                res = f(event)
                if res is not None:
                    event.end(res)
                if event.canceled:
                    break

            except Exception as e:
                event.on_error(e)


eventbus.INSTANCE = eventbus()
