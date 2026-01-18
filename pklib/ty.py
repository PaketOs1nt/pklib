import types as _ts
import typing as _t

ARGS = _t.ParamSpec("ARGS")
RETURN = _t.TypeVar("RETURN")

cb = _t.Callable[ARGS, RETURN]

type func = _ts.FunctionType
type any = _t.Any
type iter[T] = _t.Iterable[T]
type map[K, V] = _t.Mapping[K, V]
type code = _ts.CodeType
