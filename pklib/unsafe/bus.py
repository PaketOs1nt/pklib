import pklib.jit as jit
import pklib.ty as ty


@jit.struct
class _bus:
    handlers: tuple[list[ty.cb], ...]


@jit.impl(_bus)
class _ibus:
    @jit.structs
    def add(self: _bus, idx: int, handler: ty.cb):
        self.handlers[idx].append(handler)

    @jit.structs
    def emit(self: _bus, idx: int, event: tuple | ty.any):
        for handler in self.handlers[idx]:
            handler(event)


@jit.structs
def bus(size: int):
    data = tuple([[] for _ in range(size)])
    return _bus(data)
