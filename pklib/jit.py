"""
v1.04

PYTHON 3.12 / 3.14

pklib.jit - python jit bytecode translator+optimizator by PaketSoftware

features:
    @struct     register class as struct
    @enum       register class as enum

    @structs    jit struct2tuple compilation
    @enums      jit enum inlining
    @fastnop    jit nops skipping aptimization

code doubling used for pref (im so lazy)

MY GITHUB: https://github.com/PaketOs1nt
MY TELEGRAM: @paketls
MY TELEGRAM CHANNEL: @paketpksoftware

MIT LICENSE
"""

import sys
from types import FunctionType
from typing import Any

import pklib.bc as bc

_structs: dict[str, tuple[str, ...]] = {}
_structs_fast: dict[str, dict[str, int]] = {}

_enums = set()
_enums_fast: dict[str, dict[str, Any]] = {}


class _gotos:
    __slots__ = ()

    def __getattribute__(self, name: str, /) -> Any:
        raise RuntimeError("You cant use goto.* / label.* without @pklib.jit.gotos !")


label = _gotos()
goto = _gotos()


def struct(cls: type):
    n = cls.__name__
    ans = cls.__annotations__.keys()

    _structs[n] = tuple(ans)
    _structs_fast[n] = {a: i for i, a in enumerate(ans)}
    return cls


def enum(cls: type):
    n = cls.__name__
    ans = {k: v for k, v in cls.__dict__.items() if not k.startswith("__")}

    _enums.add(n)
    _enums_fast[n] = dict(ans)
    return cls


# для типизации норм
def enums(f: FunctionType) -> FunctionType:
    return f


def structs(f: FunctionType) -> FunctionType:
    return f


def gotos(f: FunctionType) -> FunctionType:
    return f


def _inject_const(consts: list, obj):
    if obj in consts:
        return consts.index(obj)

    idx = len(consts)
    consts.append(obj)
    return idx


def fastnop(f: FunctionType) -> FunctionType:
    n_code = bytearray(f.__code__.co_code)

    # удаляем весь мусор + оптимизирует NOPы
    nop_c = 0
    start = 0
    for _, opcode, _, pos in bc.unpack(n_code):
        if opcode in (bc.NOP, bc.CACHE):
            if nop_c == 0:
                start = pos

            n_code[pos] = bc.NOP
            nop_c += 1

        elif nop_c > 2:
            n_code[start] = bc.JUMP_FORWARD
            n_code[start + 1] = nop_c - 1
            nop_c = 0

    f.__code__ = f.__code__.replace(co_code=bytes(n_code))
    return f


if sys.version_info.minor == 12:

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

        for _, opcode, arg, pos in bc.unpack(n_code):
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
                o_strct = None

            # патч при работе с обьектом структуры
            elif load_s:
                if opcode == bc.LOAD_ATTR:
                    name = names[arg >> 1]

                    # индекс tuple val у аттрибта текущей struct
                    idx = _structs_fast[detected[load_s]][name]
                    const_idx = _inject_const(consts, idx)

                    n_code[pos] = bc.LOAD_CONST
                    n_code[pos + 1] = const_idx
                    n_code[pos + 2] = bc.BINARY_SUBSCR
                    load_s = None

            else:
                strct = None

        # удаляем весь мусор после обхода нашего + оптимизирует NOPы
        nop_c = 0
        start = 0
        for _, opcode, arg, pos in bc.unpack(n_code):
            if opcode in (bc.NOP, bc.CACHE):
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

    def enums(f: FunctionType):
        varnames = f.__code__.co_varnames
        names = f.__code__.co_names
        consts = list(f.__code__.co_consts)
        n_code = bytearray(f.__code__.co_code)

        enm: str | None = None

        for _, opcode, arg, pos in bc.unpack(n_code):
            if opcode == bc.LOAD_FAST:
                name = varnames[arg]
                if name in _enums:
                    enm = name
                    n_code[pos] = bc.NOP
                    n_code[pos + 1] = bc.NOP

            elif opcode == bc.LOAD_GLOBAL:
                name = names[arg >> 1]
                if name in _enums:
                    enm = name
                    n_code[pos] = bc.NOP
                    n_code[pos + 1] = bc.NOP

            elif enm and opcode == bc.LOAD_ATTR:
                name = names[arg >> 1]
                const = _enums_fast[enm][name]
                idx = _inject_const(consts, const)

                n_code[pos] = bc.LOAD_CONST
                n_code[pos + 1] = idx
                enm = None

        # удаляем весь мусор после обхода нашего + оптимизирует NOPы
        nop_c = 0
        start = 0
        for _, opcode, arg, pos in bc.unpack(n_code):
            if opcode in (bc.NOP, bc.CACHE):
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

    def gotos(f: FunctionType):
        names = f.__code__.co_names
        n_code = bytearray(f.__code__.co_code)

        c_label = 0
        c_goto = 0

        cleanext = False

        labels: dict[str, int] = {}

        # первый проход, запись всех label.*
        for _, opcode, arg, pos in bc.unpack(n_code):
            if opcode == bc.LOAD_GLOBAL and names[arg >> 1] == "label":
                c_label = pos

            elif c_label:
                if opcode == bc.LOAD_ATTR:
                    labels[names[arg >> 1]] = c_label
                    n_code[c_label] = bc.NOP
                    n_code[c_label + 1] = bc.NOP
                    n_code[pos] = bc.NOP
                    n_code[pos + 1] = bc.NOP

                    # POP_TOP нахуй убираем
                    cleanext = True

                c_label = 0

            elif cleanext:
                n_code[pos] = bc.NOP
                n_code[pos + 1] = bc.NOP
                cleanext = False

        # второй проход, работа с goto.*
        for _, opcode, arg, pos in bc.unpack(n_code):
            if opcode == bc.LOAD_GLOBAL:
                if names[arg >> 1] == "goto":
                    c_goto = pos

            elif c_goto:
                if opcode == bc.LOAD_ATTR:
                    n_pos = labels[names[arg >> 1]]

                    if n_pos > pos:
                        n_code[c_goto] = bc.JUMP_FORWARD
                        n_code[c_goto + 1] = (n_pos - (c_goto - 2)) // 2
                    else:
                        n_code[c_goto] = bc.JUMP_BACKWARD
                        n_code[c_goto + 1] = (c_goto - (n_pos - 2)) // 2

                    n_code[pos] = bc.NOP
                    n_code[pos + 1] = bc.NOP

                    # POP_TOP нахуй убираем
                    cleanext = True

                c_goto = 0

            elif cleanext:
                n_code[pos] = bc.NOP
                n_code[pos + 1] = bc.NOP
                cleanext = False

        # удаляем весь мусор после обхода нашего + оптимизируем NOPы
        nop_c = 0
        start = 0
        for _, opcode, arg, pos in bc.unpack(n_code):
            if opcode in (bc.NOP, bc.CACHE):
                if nop_c == 0:
                    start = pos

                n_code[pos] = bc.NOP
                nop_c += 1

            elif nop_c > 2:
                n_code[start] = bc.JUMP_FORWARD
                n_code[start + 1] = nop_c - 1
                nop_c = 0

        f.__code__ = f.__code__.replace(co_code=bytes(n_code))
        return f


elif sys.version_info.minor == 14:

    def structs(f: FunctionType) -> FunctionType:
        # менеьше load_attr == бвстрее код
        varnames = f.__code__.co_varnames
        consts = list(f.__code__.co_consts)
        names = f.__code__.co_names

        strct: str | None = None
        o_strct: str | None = None
        detected: dict[str, str] = {}
        load_s: str | None = None

        n_code = bytearray(f.__code__.co_code)

        for _, opcode, arg, pos in bc.unpack(n_code):
            # "вход" в струткуру
            if opcode == bc.LOAD_GLOBAL:
                name = names[arg >> 1]
                if name in _structs:
                    strct = name
                    n_code[pos] = bc.NOP
                    n_code[pos + 1] = bc.NOP

            # обнаружение работы с готовой структурой
            if opcode == bc.LOAD_FAST or opcode == bc.LOAD_FAST_BORROW:
                name = varnames[arg]
                if name in detected:
                    load_s = name

            if strct:  # патч в контексте структуры
                if opcode in bc.LOADERS_OP:
                    pass

                # что бы убрать ошибки со стеком
                elif opcode == bc.CALL_KW:
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
                o_strct = None

            # патч при работе с обьектом структуры
            elif load_s:
                if opcode == bc.LOAD_ATTR:
                    name = names[arg >> 1]

                    # индекс tuple val у аттрибта текущей struct
                    idx = _structs_fast[detected[load_s]][name]
                    # const_idx = _inject_const(consts, idx) в 3.14 не над константы инжектить
                    # можно через LOAD_SMALL_INT шоб бысьрее

                    n_code[pos] = bc.LOAD_SMALL_INT
                    n_code[pos + 1] = idx
                    n_code[pos + 2] = bc.BINARY_OP
                    n_code[pos + 3] = 26
                    load_s = None

            else:
                strct = None

        # удаляем весь мусор после обхода нашего + оптимизирует NOPы
        nop_c = 0
        start = 0
        for _, opcode, arg, pos in bc.unpack(n_code):
            if opcode in (bc.NOP, bc.CACHE):
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

    def enums(f: FunctionType) -> FunctionType:
        varnames = f.__code__.co_varnames
        names = f.__code__.co_names
        consts = list(f.__code__.co_consts)
        n_code = bytearray(f.__code__.co_code)

        enm: str | None = None

        for _, opcode, arg, pos in bc.unpack(n_code):
            if opcode == bc.LOAD_FAST or opcode == bc.LOAD_FAST_BORROW:
                name = varnames[arg]
                if name in _enums:
                    enm = name
                    n_code[pos] = bc.NOP
                    n_code[pos + 1] = bc.NOP

            elif opcode == bc.LOAD_GLOBAL:
                name = names[arg >> 1]
                if name in _enums:
                    enm = name
                    n_code[pos] = bc.NOP
                    n_code[pos + 1] = bc.NOP

            elif enm and opcode == bc.LOAD_ATTR:
                name = names[arg >> 1]
                const = _enums_fast[enm][name]
                idx = _inject_const(consts, const)

                n_code[pos] = bc.LOAD_CONST
                n_code[pos + 1] = idx
                enm = None

        # удаляем весь мусор после обхода нашего + оптимизирует NOPы
        nop_c = 0
        start = 0
        for _, opcode, arg, pos in bc.unpack(n_code):
            if opcode in (bc.NOP, bc.CACHE):
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


@enum
class Enum:
    A = 1
    B = 2
    C = 3
    D = 4


@struct
class Point:
    x: int
    y: int


@enums
@gotos
@structs
def test():
    a = Enum.C
    if a == Enum.A:
        print("a == Enum.A", a)
    elif a == Enum.C:
        print("a == Enum.C", a)
    else:
        label.imstupidkid
        print("unreal on legit code")
        return

    p = Point(22, 45)
    print("point x", p.x)
    print("point y", p.y)

    print("point", p)

    if p.x + p.y == 67:
        goto.imstupidkid

    return


test()

# with open("dump.pyc", "wb") as f:
#     f.write(bc.code_to_pyc(test.__code__))
