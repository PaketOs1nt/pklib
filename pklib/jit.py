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
from functools import wraps

import pklib.bc as bc
import pklib.ty as ty

_structs: dict[str, tuple[str, ...]] = {}
_structs_fast: dict[str, dict[str, int]] = {}
_structs_impl: dict[str, dict[str, ty.any]] = {}
_structs_muts: dict[str, bool] = {}

_enums = set()
_enums_fast: dict[str, dict[str, ty.any]] = {}


class _gotos:
    __slots__ = ()

    def __getattribute__(self, name: str, /) -> ty.any:
        raise RuntimeError("You cant use goto.* / label.* without @pklib.jit.gotos !")


label = _gotos()
goto = _gotos()


def struct(cls: type) -> type:
    n = cls.__name__
    ans = cls.__annotations__.keys()

    _structs[n] = tuple(ans)
    _structs_fast[n] = {a: i for i, a in enumerate(ans)}
    _structs_muts[n] = False
    return cls


def mutstruct(cls: type) -> type:
    n = cls.__name__
    ans = cls.__annotations__.keys()

    _structs[n] = tuple(ans)
    _structs_fast[n] = {a: i for i, a in enumerate(ans)}
    _structs_muts[n] = True
    return cls


def impl(target: type) -> ty.func | ty.any:
    @wraps(target)
    def _impl(cls: type) -> type:
        n = target.__name__
        ans = {k: v for k, v in cls.__dict__.items() if not k.startswith("__")}

        _structs_impl[n] = ans

        return cls

    return _impl


def enum(cls: type) -> type:
    n = cls.__name__
    ans = {k: v for k, v in cls.__dict__.items() if not k.startswith("__")}

    _enums.add(n)
    _enums_fast[n] = ans
    return cls


# для типизации норм
def enums(f: ty.func) -> ty.func:
    return f


def structs(f: ty.func) -> ty.func:
    return f


# def inject(f: ty.func) -> ty.func:
#     return f
# ИДЕТ НАХУЙ БЛЯТЬ


def gotos(f: ty.func) -> ty.func:
    return f


def _inject_to_list(space: list, obj):
    if obj in space:
        return space.index(obj)

    idx = len(space)
    space.append(obj)
    return idx


def fastnop(f: ty.func) -> ty.func:
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
    # def inject(f: ty.func):
    #     consts = list(f.__code__.co_consts)
    #     names = list(f.__code__.co_names)
    #     varnames = list(f.__code__.co_varnames)
    #     cellvars = list(f.__code__.co_cellvars)
    #     freevars = list(f.__code__.co_freevars)

    #     def wrapper(new: ty.func):
    #         n_code = bytearray(f.__code__.co_code)

    #         iconsts = new.__code__.co_consts
    #         inames = new.__code__.co_names
    #         ivarnames = new.__code__.co_varnames
    #         icellvars = new.__code__.co_cellvars
    #         ifreevars = new.__code__.co_freevars
    #         icode = new.__code__.co_code

    #         consts_remaps = {
    #             src: _inject_to_list(consts, iconsts[src])
    #             for src in range(len(iconsts))
    #         }
    #         names_remaps = {
    #             src: _inject_to_list(names, inames[src]) for src in range(len(inames))
    #         }
    #         varnames_remaps = {
    #             src: _inject_to_list(varnames, ivarnames[src])
    #             for src in range(len(ivarnames))
    #         }
    #         cellvars_remaps = {
    #             src: _inject_to_list(cellvars, icellvars[src])
    #             for src in range(len(icellvars))
    #         }
    #         freevars_remaps = {
    #             src: _inject_to_list(freevars, ifreevars[src])
    #             for src in range(len(ifreevars))
    #         }

    #         const_ops = (
    #             bc.STORE_NAME,
    #             bc.LOAD_NAME,
    #             bc.DELETE_NAME,
    #             bc.LOAD_GLOBAL,
    #             bc.STORE_GLOBAL,
    #             bc.DELETE_GLOBAL,
    #             bc.LOAD_ATTR,
    #             bc.STORE_ATTR,
    #         )

    #         remaps = {
    #             (bc.LOAD_FAST, bc.STORE_FAST, bc.DELETE_FAST): varnames_remaps,
    #             const_ops: names_remaps,
    #             (bc.LOAD_DEREF, bc.STORE_DEREF, bc.DELETE_DEREF): freevars_remaps,
    #             (bc.LOAD_CLOSURE,): cellvars_remaps,
    #             (bc.LOAD_CONST,): consts_remaps,
    #         }

    #         orig_len = len(n_code)
    #         offset = len(n_code) + 2

    #         n_code += n_code[0:2]
    #         n_code += icode

    #         new_offset = len(icode)

    #         for op, opcode, arg, pos in bc.unpack(n_code[orig_len + 2 :]):
    #             pos = pos + offset
    #             print("modify", pos, op, arg)
    #             for ops, remap in remaps.items():
    #                 if opcode in ops:
    #                     print(ops, remap)
    #                     if opcode in const_ops:
    #                         n_code[pos + 1] = remap[arg >> 1] << 1
    #                     else:
    #                         n_code[pos + 1] = remap[arg]

    #                 if opcode in (bc.RETURN_CONST, bc.RETURN_VALUE):
    #                     n_code[pos] = bc.NOP
    #                     n_code[pos + 1] = bc.NOP

    #         n_code[orig_len] = n_code[0]
    #         n_code[orig_len + 1] = n_code[1]
    #         n_code.append(bc.JUMP_BACKWARD)
    #         n_code.append(new_offset // 2 + 2)
    #         n_code[offset - 2 : offset + 2] = [
    #             bc.JUMP_BACKWARD,
    #             orig_len // 2,
    #             n_code[offset - 2],
    #             n_code[offset - 1],
    #         ]
    #         n_code[0] = bc.JUMP_FORWARD
    #         n_code[1] = orig_len // 2

    #         f.__code__ = f.__code__.replace(
    #             co_code=bytes(n_code),
    #             co_consts=tuple(consts),
    #             co_names=tuple(names),
    #             co_varnames=tuple(varnames),
    #             co_cellvars=tuple(cellvars),
    #             co_freevars=tuple(freevars),
    #             co_nlocals=len(varnames),
    #             co_stacksize=f.__code__.co_stacksize + new.__code__.co_stacksize,
    #         )

    #     return wrapper
    # ИДЕТ НАХУЙ БЛЯТЬ

    def structs(f: ty.func):
        # менеьше load_attr == бвстрее код
        varnames = f.__code__.co_varnames
        cellvars = f.__code__.co_cellvars
        freevars = f.__code__.co_freevars
        derefnames = cellvars + freevars

        consts = list(f.__code__.co_consts)
        names = f.__code__.co_names

        strct: str | None = None
        o_strct: str | None = None

        # сразу детектим все аргументы struct
        detected: dict[str, str] = {
            name: t.__name__
            for name, t in f.__annotations__.items()
            if hasattr(t, "__name__") and t.__name__ in _structs
        }

        doc = f.__doc__
        if doc:
            for line in doc.splitlines():
                if line.startswith("jit.ty!"):
                    name, type = line[7:].split("=")
                    detected[name] = type

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

            elif opcode == bc.LOAD_DEREF and not load_s:
                name = derefnames[arg >> 1]
                if name in detected:
                    load_s = name

            # обнаружение работы с готовой структурой

            elif opcode == bc.LOAD_FAST:
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
                    n_code[pos] = (
                        bc.BUILD_LIST if _structs_muts[strct] else bc.BUILD_TUPLE
                    )
                    n_code[pos + 1] = len(_structs[strct])

                    o_strct = strct
                    strct = None

                # эт уже вне контекста выходит
                else:
                    o_strct = strct
                    strct = None

            # точно знает что var такого то типа
            elif o_strct and opcode == bc.STORE_FAST:
                detected[varnames[arg]] = o_strct
                o_strct = None

            # патч при работе с обьектом структуры
            elif load_s:
                if opcode == bc.LOAD_ATTR:
                    name = names[arg >> 1]

                    detect = detected[load_s]
                    # индекс tuple val у аттрибта текущей struct
                    if detect in _structs_impl and name in (
                        detect_impl := _structs_impl[detect]
                    ):
                        func = detect_impl[name]
                        const_idx = _inject_to_list(consts, func)

                        # ебаный фикс, шоб вышло не self(func) а func(self)
                        n_code[pos - 2 : pos + 2] = (
                            bc.LOAD_CONST,
                            const_idx,
                            n_code[pos - 2],
                            n_code[pos - 1],
                        )

                    elif detect in _structs_fast and name in (
                        detect_fast := _structs_fast[detect]
                    ):
                        const_idx = _inject_to_list(consts, detect_fast[name])

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

    def enums(f: ty.func):
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
                idx = _inject_to_list(consts, const)

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

    def gotos(f: ty.func):
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

    def structs(f: ty.func) -> ty.func:
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
                    n_code[pos] = (
                        bc.BUILD_LIST if _structs_muts[strct] else bc.BUILD_TUPLE
                    )
                    n_code[pos + 1] = len(_structs[strct])

                    o_strct = strct
                    strct = None

                # эт уже вне контекста выходит
                else:
                    o_strct = strct
                    strct = None

            # точно знает что var такого то типа
            elif o_strct and opcode == bc.STORE_FAST:
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

    def enums(f: ty.func) -> ty.func:
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
                idx = _inject_to_list(consts, const)

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
