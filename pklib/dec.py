import ast
import sys

import pklib.bc as bc
import pklib.ty as ty

bin_ops = (
    (ast.Add),
    (ast.BitAnd),
    (ast.FloorDiv),
    (ast.LShift),
    (ast.MatMult),
    (ast.Mult),
    (ast.Mod),
    (ast.BitOr),
    (ast.Pow),
    (ast.RShift),
    (ast.Sub),
    (ast.Div),
    (ast.BitXor),
    (ast.Add),  # AugAssign
    (ast.BitAnd),
    (ast.FloorDiv),
    (ast.LShift),
    (ast.MatMult),
    (ast.Mult),
    (ast.Mod),
    (ast.BitOr),
    (ast.Pow),
    (ast.RShift),
    (ast.Sub),
    (ast.Div),
    (ast.BitXor),
)


class Postfix312(ast.NodeTransformer):
    def visit_For(self, node: ast.For):
        if isinstance(node.body[-1], ast.Continue):
            node.body.pop()
        return self.generic_visit(node)


def arguments_from_codeobj(co):
    posonly = co.co_posonlyargcount
    pos = co.co_argcount
    kwonly = co.co_kwonlyargcount

    names = co.co_varnames

    idx = 0
    posonlyargs = [ast.arg(arg=names[i]) for i in range(idx, idx + posonly)]
    idx += posonly

    args = [ast.arg(arg=names[i]) for i in range(idx, idx + pos)]
    idx += pos

    vararg = None
    if co.co_flags & 8:
        vararg = ast.arg(arg=names[idx])
        idx += 1

    kwonlyargs = [ast.arg(arg=names[i]) for i in range(idx, idx + kwonly)]
    idx += kwonly

    kwarg = None
    if co.co_flags & 8:
        kwarg = ast.arg(arg=names[idx])

    return ast.arguments(
        posonlyargs=posonlyargs,
        args=args,
        vararg=vararg,
        kwonlyargs=kwonlyargs,
        kw_defaults=[None] * kwonly,
        kwarg=kwarg,
        defaults=[],
    )


def dec312(c: ty.code) -> str:
    module = ast.Module([], [])
    obj = module

    # ctx: list[Context] = []
    stack: list[ast.expr | ty.any] = [ast.Constant(None) for _ in range(512)]
    stack_ptr = 0

    def push(x: ast.expr | ty.any):
        nonlocal stack_ptr
        stack_ptr += 1
        stack[stack_ptr] = x

    def pop() -> ast.expr | ty.any:
        nonlocal stack_ptr
        stack_ptr -= 1
        return stack[stack_ptr + 1]

    for opcode, op, arg, pos in bc.unpack(c.co_code):
        # print(pos, opcode, op, arg)
        match op:
            case bc.IMPORT_NAME:
                pop()
                push(ast.Import([ast.alias(c.co_names[arg])]))

            case bc.IMPORT_FROM:
                imp: ast.Import | ty.any = stack[stack_ptr]
                push(ast.ImportFrom(imp.names[0].name, [ast.alias(c.co_names[arg])], 0))

            case bc.LOAD_CONST:
                push(ast.Constant(c.co_consts[arg]))

            case bc.LOAD_NAME:
                push(ast.Name(c.co_names[arg], ctx=ast.Load()))

            case bc.LOAD_FAST:
                push(ast.Name(c.co_varnames[arg], ctx=ast.Load()))

            case bc.LOAD_GLOBAL:
                push(ast.Name(c.co_names[arg >> 1], ctx=ast.Load()))

            case bc.CALL:
                args = [pop() for _ in range(arg)][::-1]
                func = pop()
                push(ast.Call(func, args, []))

            case bc.POP_TOP:
                d = pop()
                if not isinstance(d, ast.Import):
                    obj.body.append(ast.Expr(d))

            case bc.LOAD_ATTR:
                push(ast.Attribute(pop(), c.co_names[arg >> 1], ast.Load()))

            case bc.BINARY_OP:
                b, a = pop(), pop()
                push(ast.BinOp(a, bin_ops[arg](), b))

            case bc.RETURN_VALUE:
                obj.body.append(ast.Return(pop()))
                if hasattr(obj, "_back"):
                    obj = obj._back  # type: ignore

            case bc.RETURN_CONST:
                const = c.co_consts[arg]
                if const is None:
                    if not isinstance(obj, ast.Module):
                        obj.body.append(ast.Return())
                else:
                    obj.body.append(ast.Return(ast.Constant(const)))

                if hasattr(obj, "_back"):
                    obj = obj._back  # type: ignore

            case bc.FOR_ITER:
                pass

            case bc.BUILD_TUPLE:
                push(ast.Tuple([pop() for _ in range(arg)][::-1], ast.Load()))

            case bc.BUILD_LIST:
                push(ast.List([pop() for _ in range(arg)][::-1], ast.Load()))

            case bc.BUILD_SET:
                push(ast.Set([pop() for _ in range(arg)][::-1]))

            case bc.GET_ITER:
                nf = ast.For(ast.Name("<?>"), pop(), [], [], lineno=-1)
                nf._back = obj  # type: ignore
                obj = nf

            case bc.JUMP_BACKWARD:
                if isinstance(obj, ast.For):
                    obj.body.append(ast.Continue())

            case bc.STORE_NAME:
                val = pop()

                if isinstance(obj, ast.For) and obj.target.id == "<?>":
                    obj.target.id = c.co_names[arg]
                    continue

                if isinstance(val, ast.Import):
                    name = c.co_names[arg]
                    # if name != val.names[0].name:
                    #     val.names[0].asname = name
                    obj.body.append(val)

                elif isinstance(val, ast.ImportFrom):
                    name = c.co_names[arg >> 1]
                    # print(val.names[0].name, val.module)
                    # if name != val.names[0]:
                    #     val.names[0].asname = name
                    obj.body.append(val)

                elif isinstance(val, ast.FunctionDef):
                    obj.body.append(val)

                else:
                    obj.body.append(
                        ast.Assign([ast.Name(c.co_names[arg])], val, lineno=-1)
                    )

            case bc.END_FOR:
                ff = obj
                obj = obj._back  # type: ignore
                obj.body.append(ff)

            case bc.STORE_FAST:
                val = pop()

                if isinstance(obj, ast.For) and obj.target.id == "<?>":
                    obj.target.id = c.co_varnames[arg]
                    continue

                if isinstance(val, ast.Import):
                    name = c.co_varnames[arg]
                    # if name != val.names[0].name:
                    #     val.names[0].asname = name
                    obj.body.append(val)

                elif isinstance(val, ast.ImportFrom):
                    name = c.co_varnames[arg]
                    # print(val.names[0].name, val.module)
                    # if name != val.names[0]:
                    #     val.names[0].asname = name
                    obj.body.append(val)

                elif isinstance(val, ast.FunctionDef):
                    obj.body.append(val)
                else:
                    obj.body.append(
                        ast.Assign([ast.Name(c.co_varnames[arg])], val, lineno=-1)
                    )

            case bc.MAKE_FUNCTION:
                f: ty.code = pop().value  # type: ignore

                push(
                    ast.FunctionDef(
                        f.co_name,
                        arguments_from_codeobj(f),
                        ast.parse(dec312(f)).body,
                        [],
                        None,
                        None,
                        [],
                        lineno=-1,
                    )
                )

            case bc.PUSH_NULL:
                pass

            case bc.RESUME:
                pass

            case other:
                obj.body.append(
                    ast.Expr(ast.Constant(f"UNKNOWN OPCODE: {bc.fast_name(other)}"))
                )

    pfix = Postfix312()
    return ast.unparse(pfix.visit(module))


def dec(file: str):
    with open(file, "rb") as f:
        pyc = f.read()

    if sys.version_info.minor == 12:
        print(dec312(bc.code_from_pyc(pyc)))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: python {sys.argv[0]} <file>")

    file = sys.argv[1]
    dec(file)
