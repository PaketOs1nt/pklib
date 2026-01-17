import pklib.bc
from pklib.jit import enum, enums, goto, gotos, label, struct, structs


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

with open("dump.pyc", "wb") as f:
    f.write(pklib.bc.code_to_pyc(test.__code__))
