from dataclasses import dataclass
from types import FunctionType

import pklib.bc as bc

_structs: dict[str, tuple[str, ...]] = {}


def struct(cls: type):
    _structs[cls.__name__] = tuple(cls.__annotations__.keys())
    return cls


def _inject_const(consts: list, obj):
    if obj in consts:
        return consts.index(obj)

    idx = len(consts)
    consts.append(obj)
    return idx


def structs(f: FunctionType):
    # менеьше load_attr == бвстрее код
    varnames = f.__code__.co_varnames
    consts = list(f.__code__.co_consts)
    names = f.__code__.co_names

    strct: str | None = None
    o_strct: str | None = None
    detected: dict[str, str] = {}
    load_s: str | None = None

    n_code = bytearray(f.__code__.co_code)

    for op, opcode, arg, pos in bc.unpack(f.__code__.co_code):
        # "вход" в струткуру
        if opcode == bc.LOAD_GLOBAL:
            name = names[arg >> 1]
            if name in _structs:
                strct = name
                n_code[pos] = bc.NOP
                n_code[pos + 1] = bc.NOP

        # обнаружение работы с готовой структурой
        if opcode == bc.LOAD_FAST:
            name = varnames[arg]
            if name in detected:
                load_s = name

        if strct:  # патч в контексте структуры
            if opcode in bc.LOADERS_OP:
                pass

            # что бы убрать ошибки со стеком
            elif opcode == bc.KW_NAMES:
                n_code[pos] = bc.NOP
                n_code[pos + 1] = bc.NOP

            # заменяем вызов struct(...) на tuple, (...)
            elif opcode == bc.CALL:
                n_code[pos] = bc.BUILD_TUPLE
                n_code[pos + 1] = len(_structs[strct])

                o_strct = strct
                strct = None

            # эт уже вне контекста выходит
            else:
                o_strct = strct
                strct = None

        # точно знает что var такого то типа
        elif o_strct and opcode in (bc.STORE_FAST, bc.STORE_FAST):
            detected[varnames[arg]] = o_strct
            print(f"struct {detected[varnames[arg]]} -> {varnames[arg]}")

        # патч при работе с обьектом структуры
        elif load_s:
            if opcode == bc.LOAD_ATTR:
                name = names[arg >> 1]

                # индекс tuple val у аттрибта текущей struct
                idx = _structs[detected[load_s]].index(name)
                const_idx = _inject_const(consts, idx)

                n_code[pos] = bc.LOAD_CONST
                n_code[pos + 1] = const_idx
                n_code[pos + 2] = bc.BINARY_SUBSCR

                print(f"{load_s}.{name} -> {load_s}[{idx}]")

        else:
            strct = None

    # удаляем весь мусор после обхода нашего + оптимизирует NOPы
    nop_c = 0
    start = 0
    for _, opcode, arg, pos in bc.unpack(n_code):
        if opcode == bc.CACHE:
            if nop_c == 0:
                start = pos

            n_code[pos] = bc.NOP
            nop_c += 1
        elif nop_c > 2:
            n_code[start] = bc.JUMP_FORWARD
            n_code[start + 1] = nop_c - 1
            nop_c = 0

    f.__code__ = f.__code__.replace(co_code=bytes(n_code), co_consts=tuple(consts))
    return f


@struct
class Point:
    x: int
    y: int


@structs
def test():
    def print(x):
        return

    for i in range(3):
        i = int(2)
        b = Point(x=1, y=i)

        print(b)
        p = Point(3, 4)

        print(p)
        print(p.x)
        print(p.y)


bc.dis.dis(test)
test()

with open("dump.pyc", "wb") as f:
    f.write(bc.code_to_pyc(test.__code__))
