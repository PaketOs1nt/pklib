import pklib.bc as bc
import pklib.jit as jit
from pklib.bus import _bus, bus
from pklib.jit import goto, label


@jit.struct
class httpevent:
    method: str
    body: bytes


@jit.structs
def handler(event: httpevent):
    print("handled httpevent", event)


@jit.structs
def main():
    "jit.ty!b=_bus"
    # создаем EventBus с максимальным количеством евентов (НЕ ХЕНДЛЕРОВ) - 1:
    b = bus(1)

    # добавляем слушателя handler к евенту 0
    b.add(0, handler)

    b.emit(0, httpevent("POST", b"example event body 1"))
    b.emit(0, httpevent("POST", b"example event body 2"))
    b.emit(0, httpevent("POST", b"example event body 3"))


main()

# with open("dump.pyc", "wb") as f:
#     f.write(pklib.bc.code_to_pyc(test.__code__))


@jit.gotos
def with_goto():
    for a in range(100):
        for b in range(100):
            for c in range(100):
                if a + b + c == 123:
                    print(a, b, c)
                    goto.fast_exit_loop

    label.fast_exit_loop


with_goto()
