"""
v1.12

PYTHON 3.12 / 3.14

pklib.bc - python bytecode lib by PaketSoftware

MY GITHUB: https://github.com/PaketOs1nt
MY TELEGRAM: @paketls
MY TELEGRAM CHANNEL: @paketpksoftware

MIT LICENSE
"""

import dis
import importlib._bootstrap_external as imp_b
import sys

import pklib.ty as ty

type instr = tuple[str, int, int, int]  # 3.12 type style


if sys.version_info.minor == 12:
    map = {
        0: "CACHE",
        1: "POP_TOP",
        2: "PUSH_NULL",
        3: "INTERPRETER_EXIT",
        4: "END_FOR",
        5: "END_SEND",
        9: "NOP",
        11: "UNARY_NEGATIVE",
        12: "UNARY_NOT",
        15: "UNARY_INVERT",
        17: "RESERVED",
        25: "BINARY_SUBSCR",
        26: "BINARY_SLICE",
        27: "STORE_SLICE",
        30: "GET_LEN",
        31: "MATCH_MAPPING",
        32: "MATCH_SEQUENCE",
        33: "MATCH_KEYS",
        35: "PUSH_EXC_INFO",
        36: "CHECK_EXC_MATCH",
        37: "CHECK_EG_MATCH",
        49: "WITH_EXCEPT_START",
        50: "GET_AITER",
        51: "GET_ANEXT",
        52: "BEFORE_ASYNC_WITH",
        53: "BEFORE_WITH",
        54: "END_ASYNC_FOR",
        55: "CLEANUP_THROW",
        60: "STORE_SUBSCR",
        61: "DELETE_SUBSCR",
        68: "GET_ITER",
        69: "GET_YIELD_FROM_ITER",
        71: "LOAD_BUILD_CLASS",
        74: "LOAD_ASSERTION_ERROR",
        75: "RETURN_GENERATOR",
        83: "RETURN_VALUE",
        85: "SETUP_ANNOTATIONS",
        87: "LOAD_LOCALS",
        89: "POP_EXCEPT",
        90: "STORE_NAME",
        91: "DELETE_NAME",
        92: "UNPACK_SEQUENCE",
        93: "FOR_ITER",
        94: "UNPACK_EX",
        95: "STORE_ATTR",
        96: "DELETE_ATTR",
        97: "STORE_GLOBAL",
        98: "DELETE_GLOBAL",
        99: "SWAP",
        100: "LOAD_CONST",
        101: "LOAD_NAME",
        102: "BUILD_TUPLE",
        103: "BUILD_LIST",
        104: "BUILD_SET",
        105: "BUILD_MAP",
        106: "LOAD_ATTR",
        107: "COMPARE_OP",
        108: "IMPORT_NAME",
        109: "IMPORT_FROM",
        110: "JUMP_FORWARD",
        114: "POP_JUMP_IF_FALSE",
        115: "POP_JUMP_IF_TRUE",
        116: "LOAD_GLOBAL",
        117: "IS_OP",
        118: "CONTAINS_OP",
        119: "RERAISE",
        120: "COPY",
        121: "RETURN_CONST",
        122: "BINARY_OP",
        123: "SEND",
        124: "LOAD_FAST",
        125: "STORE_FAST",
        126: "DELETE_FAST",
        127: "LOAD_FAST_CHECK",
        128: "POP_JUMP_IF_NOT_NONE",
        129: "POP_JUMP_IF_NONE",
        130: "RAISE_VARARGS",
        131: "GET_AWAITABLE",
        132: "MAKE_FUNCTION",
        133: "BUILD_SLICE",
        134: "JUMP_BACKWARD_NO_INTERRUPT",
        135: "MAKE_CELL",
        136: "LOAD_CLOSURE",
        137: "LOAD_DEREF",
        138: "STORE_DEREF",
        139: "DELETE_DEREF",
        140: "JUMP_BACKWARD",
        141: "LOAD_SUPER_ATTR",
        142: "CALL_FUNCTION_EX",
        143: "LOAD_FAST_AND_CLEAR",
        144: "EXTENDED_ARG",
        145: "LIST_APPEND",
        146: "SET_ADD",
        147: "MAP_ADD",
        149: "COPY_FREE_VARS",
        150: "YIELD_VALUE",
        151: "RESUME",
        152: "MATCH_CLASS",
        155: "FORMAT_VALUE",
        156: "BUILD_CONST_KEY_MAP",
        157: "BUILD_STRING",
        162: "LIST_EXTEND",
        163: "SET_UPDATE",
        164: "DICT_MERGE",
        165: "DICT_UPDATE",
        171: "CALL",
        172: "KW_NAMES",
        173: "CALL_INTRINSIC_1",
        174: "CALL_INTRINSIC_2",
        175: "LOAD_FROM_DICT_OR_GLOBALS",
        176: "LOAD_FROM_DICT_OR_DEREF",
        237: "INSTRUMENTED_LOAD_SUPER_ATTR",
        238: "INSTRUMENTED_POP_JUMP_IF_NONE",
        239: "INSTRUMENTED_POP_JUMP_IF_NOT_NONE",
        240: "INSTRUMENTED_RESUME",
        241: "INSTRUMENTED_CALL",
        242: "INSTRUMENTED_RETURN_VALUE",
        243: "INSTRUMENTED_YIELD_VALUE",
        244: "INSTRUMENTED_CALL_FUNCTION_EX",
        245: "INSTRUMENTED_JUMP_FORWARD",
        246: "INSTRUMENTED_JUMP_BACKWARD",
        247: "INSTRUMENTED_RETURN_CONST",
        248: "INSTRUMENTED_FOR_ITER",
        249: "INSTRUMENTED_POP_JUMP_IF_FALSE",
        250: "INSTRUMENTED_POP_JUMP_IF_TRUE",
        251: "INSTRUMENTED_END_FOR",
        252: "INSTRUMENTED_END_SEND",
        253: "INSTRUMENTED_INSTRUCTION",
        254: "INSTRUMENTED_LINE",
        256: "SETUP_FINALLY",
        257: "SETUP_CLEANUP",
        258: "SETUP_WITH",
        259: "POP_BLOCK",
        260: "JUMP",
        261: "JUMP_NO_INTERRUPT",
        262: "LOAD_METHOD",
        263: "LOAD_SUPER_METHOD",
        264: "LOAD_ZERO_SUPER_METHOD",
        265: "LOAD_ZERO_SUPER_ATTR",
        266: "STORE_FAST_MAYBE_NULL",
    }

    CACHE = 0
    POP_TOP = 1
    PUSH_NULL = 2
    INTERPRETER_EXIT = 3
    END_FOR = 4
    END_SEND = 5
    NOP = 9
    UNARY_NEGATIVE = 11
    UNARY_NOT = 12
    UNARY_INVERT = 15
    RESERVED = 17
    BINARY_SUBSCR = 25
    BINARY_SLICE = 26
    STORE_SLICE = 27
    GET_LEN = 30
    MATCH_MAPPING = 31
    MATCH_SEQUENCE = 32
    MATCH_KEYS = 33
    PUSH_EXC_INFO = 35
    CHECK_EXC_MATCH = 36
    CHECK_EG_MATCH = 37
    WITH_EXCEPT_START = 49
    GET_AITER = 50
    GET_ANEXT = 51
    BEFORE_ASYNC_WITH = 52
    BEFORE_WITH = 53
    END_ASYNC_FOR = 54
    CLEANUP_THROW = 55
    STORE_SUBSCR = 60
    DELETE_SUBSCR = 61
    GET_ITER = 68
    GET_YIELD_FROM_ITER = 69
    LOAD_BUILD_CLASS = 71
    LOAD_ASSERTION_ERROR = 74
    RETURN_GENERATOR = 75
    RETURN_VALUE = 83
    SETUP_ANNOTATIONS = 85
    LOAD_LOCALS = 87
    POP_EXCEPT = 89
    STORE_NAME = 90
    DELETE_NAME = 91
    UNPACK_SEQUENCE = 92
    FOR_ITER = 93
    UNPACK_EX = 94
    STORE_ATTR = 95
    DELETE_ATTR = 96
    STORE_GLOBAL = 97
    DELETE_GLOBAL = 98
    SWAP = 99
    LOAD_CONST = 100
    LOAD_NAME = 101
    BUILD_TUPLE = 102
    BUILD_LIST = 103
    BUILD_SET = 104
    BUILD_MAP = 105
    LOAD_ATTR = 106
    COMPARE_OP = 107
    IMPORT_NAME = 108
    IMPORT_FROM = 109
    JUMP_FORWARD = 110
    POP_JUMP_IF_FALSE = 114
    POP_JUMP_IF_TRUE = 115
    LOAD_GLOBAL = 116
    IS_OP = 117
    CONTAINS_OP = 118
    RERAISE = 119
    COPY = 120
    RETURN_CONST = 121
    BINARY_OP = 122
    SEND = 123
    LOAD_FAST = 124
    STORE_FAST = 125
    DELETE_FAST = 126
    LOAD_FAST_CHECK = 127
    POP_JUMP_IF_NOT_NONE = 128
    POP_JUMP_IF_NONE = 129
    RAISE_VARARGS = 130
    GET_AWAITABLE = 131
    MAKE_FUNCTION = 132
    BUILD_SLICE = 133
    JUMP_BACKWARD_NO_INTERRUPT = 134
    MAKE_CELL = 135
    LOAD_CLOSURE = 136
    LOAD_DEREF = 137
    STORE_DEREF = 138
    DELETE_DEREF = 139
    JUMP_BACKWARD = 140
    LOAD_SUPER_ATTR = 141
    CALL_FUNCTION_EX = 142
    LOAD_FAST_AND_CLEAR = 143
    EXTENDED_ARG = 144
    LIST_APPEND = 145
    SET_ADD = 146
    MAP_ADD = 147
    COPY_FREE_VARS = 149
    YIELD_VALUE = 150
    RESUME = 151
    MATCH_CLASS = 152
    FORMAT_VALUE = 155
    BUILD_CONST_KEY_MAP = 156
    BUILD_STRING = 157
    LIST_EXTEND = 162
    SET_UPDATE = 163
    DICT_MERGE = 164
    DICT_UPDATE = 165
    CALL = 171
    KW_NAMES = 172
    CALL_INTRINSIC_1 = 173
    CALL_INTRINSIC_2 = 174
    LOAD_FROM_DICT_OR_GLOBALS = 175
    LOAD_FROM_DICT_OR_DEREF = 176
    INSTRUMENTED_LOAD_SUPER_ATTR = 237
    INSTRUMENTED_POP_JUMP_IF_NONE = 238
    INSTRUMENTED_POP_JUMP_IF_NOT_NONE = 239
    INSTRUMENTED_RESUME = 240
    INSTRUMENTED_CALL = 241
    INSTRUMENTED_RETURN_VALUE = 242
    INSTRUMENTED_YIELD_VALUE = 243
    INSTRUMENTED_CALL_FUNCTION_EX = 244
    INSTRUMENTED_JUMP_FORWARD = 245
    INSTRUMENTED_JUMP_BACKWARD = 246
    INSTRUMENTED_RETURN_CONST = 247
    INSTRUMENTED_FOR_ITER = 248
    INSTRUMENTED_POP_JUMP_IF_FALSE = 249
    INSTRUMENTED_POP_JUMP_IF_TRUE = 250
    INSTRUMENTED_END_FOR = 251
    INSTRUMENTED_END_SEND = 252
    INSTRUMENTED_INSTRUCTION = 253
    INSTRUMENTED_LINE = 254
    SETUP_FINALLY = 256
    SETUP_CLEANUP = 257
    SETUP_WITH = 258
    POP_BLOCK = 259
    JUMP = 260
    JUMP_NO_INTERRUPT = 261
    LOAD_METHOD = 262
    LOAD_SUPER_METHOD = 263
    LOAD_ZERO_SUPER_METHOD = 264
    LOAD_ZERO_SUPER_ATTR = 265
    STORE_FAST_MAYBE_NULL = 266

    BUILDERS_OP = (
        BUILD_LIST,
        BUILD_MAP,
        BUILD_SET,
        BUILD_TUPLE,
        BUILD_SLICE,
        BUILD_STRING,
        BUILD_CONST_KEY_MAP,
    )
    LOADERS_OP = (
        LOAD_GLOBAL,
        LOAD_NAME,
        LOAD_CONST,
        LOAD_FAST,
        LOAD_DEREF,
        LOAD_ATTR,
        LOAD_METHOD,
        LOAD_SUPER_ATTR,
        LOAD_SUPER_METHOD,
        LOAD_ZERO_SUPER_ATTR,
        LOAD_ZERO_SUPER_METHOD,
    )
    JUMP_OP = (
        JUMP,
        JUMP_BACKWARD,
        JUMP_BACKWARD_NO_INTERRUPT,
        JUMP_FORWARD,
        JUMP_NO_INTERRUPT,
        POP_JUMP_IF_FALSE,
        POP_JUMP_IF_NONE,
        POP_JUMP_IF_NOT_NONE,
        POP_JUMP_IF_TRUE,
    )

    def fast_calc_jump(self: instr) -> int:
        _, opcode, arg, pos = self
        if opcode in (JUMP_BACKWARD, JUMP_BACKWARD_NO_INTERRUPT):
            return pos - arg * 2

        if opcode == JUMP_FORWARD:
            return pos + arg * 2

        return arg * 2

    def calc_jump(self: instr) -> int:
        op, opcode, arg, _ = self
        if opcode not in JUMP_OP:
            raise Exception(f"{op} is not JUMP_OP !")

        if not arg:
            raise Exception(f"{op} without arg :\\")

        return fast_calc_jump(self)

    def op_name(i: int) -> str:
        return map.get(i, "<unknown-opcode>")

    def fast_name(i: int) -> str:
        return map[i]

    def unpack(code: bytes | bytearray, unpacker=fast_name) -> ty.iter[instr]:
        for pos, op, arg in dis._unpack_opargs(code):  # type: ignore
            yield (unpacker(op), op, arg, pos)


elif sys.version_info.minor == 14:
    # oneline instructions for 3.14 python
    (
        CACHE,
        RESERVED,
        RESUME,
        INSTRUMENTED_LINE,
        ENTER_EXECUTOR,
        BINARY_SLICE,
        BUILD_TEMPLATE,
        CALL_FUNCTION_EX,
        CHECK_EG_MATCH,
        CHECK_EXC_MATCH,
        CLEANUP_THROW,
        DELETE_SUBSCR,
        END_FOR,
        END_SEND,
        EXIT_INIT_CHECK,
        FORMAT_SIMPLE,
        FORMAT_WITH_SPEC,
        GET_AITER,
        GET_ANEXT,
        GET_ITER,
        GET_LEN,
        GET_YIELD_FROM_ITER,
        INTERPRETER_EXIT,
        LOAD_BUILD_CLASS,
        LOAD_LOCALS,
        MAKE_FUNCTION,
        MATCH_KEYS,
        MATCH_MAPPING,
        MATCH_SEQUENCE,
        NOP,
        NOT_TAKEN,
        POP_EXCEPT,
        POP_ITER,
        POP_TOP,
        PUSH_EXC_INFO,
        PUSH_NULL,
        RETURN_GENERATOR,
        RETURN_VALUE,
        SETUP_ANNOTATIONS,
        STORE_SLICE,
        STORE_SUBSCR,
        TO_BOOL,
        UNARY_INVERT,
        UNARY_NEGATIVE,
        UNARY_NOT,
        WITH_EXCEPT_START,
        BINARY_OP,
        BUILD_INTERPOLATION,
        BUILD_LIST,
        BUILD_MAP,
        BUILD_SET,
        BUILD_SLICE,
        BUILD_STRING,
        BUILD_TUPLE,
        CALL,
        CALL_INTRINSIC_1,
        CALL_INTRINSIC_2,
        CALL_KW,
        COMPARE_OP,
        CONTAINS_OP,
        CONVERT_VALUE,
        COPY,
        COPY_FREE_VARS,
        DELETE_ATTR,
        DELETE_DEREF,
        DELETE_FAST,
        DELETE_GLOBAL,
        DELETE_NAME,
        DICT_MERGE,
        DICT_UPDATE,
        END_ASYNC_FOR,
        EXTENDED_ARG,
        FOR_ITER,
        GET_AWAITABLE,
        IMPORT_FROM,
        IMPORT_NAME,
        IS_OP,
        JUMP_BACKWARD,
        JUMP_BACKWARD_NO_INTERRUPT,
        JUMP_FORWARD,
        LIST_APPEND,
        LIST_EXTEND,
        LOAD_ATTR,
        LOAD_COMMON_CONSTANT,
        LOAD_CONST,
        LOAD_DEREF,
        LOAD_FAST,
        LOAD_FAST_AND_CLEAR,
        LOAD_FAST_BORROW,
        LOAD_FAST_BORROW_LOAD_FAST_BORROW,
        LOAD_FAST_CHECK,
        LOAD_FAST_LOAD_FAST,
        LOAD_FROM_DICT_OR_DEREF,
        LOAD_FROM_DICT_OR_GLOBALS,
        LOAD_GLOBAL,
        LOAD_NAME,
        LOAD_SMALL_INT,
        LOAD_SPECIAL,
        LOAD_SUPER_ATTR,
        MAKE_CELL,
        MAP_ADD,
        MATCH_CLASS,
        POP_JUMP_IF_FALSE,
        POP_JUMP_IF_NONE,
        POP_JUMP_IF_NOT_NONE,
        POP_JUMP_IF_TRUE,
        RAISE_VARARGS,
        RERAISE,
        SEND,
        SET_ADD,
        SET_FUNCTION_ATTRIBUTE,
        SET_UPDATE,
        STORE_ATTR,
        STORE_DEREF,
        STORE_FAST,
        STORE_FAST_LOAD_FAST,
        STORE_FAST_STORE_FAST,
        STORE_GLOBAL,
        STORE_NAME,
        SWAP,
        UNPACK_EX,
        UNPACK_SEQUENCE,
        YIELD_VALUE,
        INSTRUMENTED_END_FOR,
        INSTRUMENTED_POP_ITER,
        INSTRUMENTED_END_SEND,
        INSTRUMENTED_FOR_ITER,
        INSTRUMENTED_INSTRUCTION,
        INSTRUMENTED_JUMP_FORWARD,
        INSTRUMENTED_NOT_TAKEN,
        INSTRUMENTED_POP_JUMP_IF_TRUE,
        INSTRUMENTED_POP_JUMP_IF_FALSE,
        INSTRUMENTED_POP_JUMP_IF_NONE,
        INSTRUMENTED_POP_JUMP_IF_NOT_NONE,
        INSTRUMENTED_RESUME,
        INSTRUMENTED_RETURN_VALUE,
        INSTRUMENTED_YIELD_VALUE,
        INSTRUMENTED_END_ASYNC_FOR,
        INSTRUMENTED_LOAD_SUPER_ATTR,
        INSTRUMENTED_CALL,
        INSTRUMENTED_CALL_KW,
        INSTRUMENTED_CALL_FUNCTION_EX,
        INSTRUMENTED_JUMP_BACKWARD,
        ANNOTATIONS_PLACEHOLDER,
        JUMP,
        JUMP_IF_FALSE,
        JUMP_IF_TRUE,
        JUMP_NO_INTERRUPT,
        LOAD_CLOSURE,
        POP_BLOCK,
        SETUP_CLEANUP,
        SETUP_FINALLY,
        SETUP_WITH,
        STORE_FAST_MAYBE_NULL,
    ) = (
        0,
        17,
        128,
        254,
        255,
        1,
        2,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        58,
        59,
        60,
        61,
        62,
        63,
        64,
        65,
        66,
        67,
        68,
        69,
        70,
        71,
        72,
        73,
        74,
        75,
        76,
        77,
        78,
        79,
        80,
        81,
        82,
        83,
        84,
        85,
        86,
        87,
        88,
        89,
        90,
        91,
        92,
        93,
        94,
        95,
        96,
        97,
        98,
        99,
        100,
        101,
        102,
        103,
        104,
        105,
        106,
        107,
        108,
        109,
        110,
        111,
        112,
        113,
        114,
        115,
        116,
        117,
        118,
        119,
        120,
        234,
        235,
        236,
        237,
        238,
        239,
        240,
        241,
        242,
        243,
        244,
        245,
        246,
        247,
        248,
        249,
        250,
        251,
        252,
        253,
        256,
        257,
        258,
        259,
        260,
        261,
        262,
        263,
        264,
        265,
        266,
    )

    BUILDERS_OP = (
        BUILD_LIST,
        BUILD_MAP,
        BUILD_SET,
        BUILD_TUPLE,
        BUILD_SLICE,
        BUILD_STRING,
        BUILD_TEMPLATE,
        BUILD_INTERPOLATION,
    )
    LOADERS_OP = (
        LOAD_COMMON_CONSTANT,
        LOAD_BUILD_CLASS,
        LOAD_FAST_BORROW_LOAD_FAST_BORROW,
        LOAD_FROM_DICT_OR_DEREF,
        LOAD_SPECIAL,
        LOAD_GLOBAL,
        LOAD_NAME,
        LOAD_CONST,
        LOAD_FAST,
        LOAD_DEREF,
        LOAD_ATTR,
        LOAD_SUPER_ATTR,
        LOAD_SMALL_INT,
        LOAD_FAST_BORROW,
        LOAD_FAST_AND_CLEAR,
        LOAD_FAST_LOAD_FAST,
    )
    JUMP_OP = (
        JUMP,
        JUMP_BACKWARD,
        JUMP_BACKWARD_NO_INTERRUPT,
        JUMP_FORWARD,
        JUMP_NO_INTERRUPT,
        POP_JUMP_IF_FALSE,
        POP_JUMP_IF_NONE,
        POP_JUMP_IF_NOT_NONE,
        POP_JUMP_IF_TRUE,
    )

    # instr map for 3.14 python
    map = {
        0: "CACHE",
        17: "RESERVED",
        128: "RESUME",
        254: "INSTRUMENTED_LINE",
        255: "ENTER_EXECUTOR",
        1: "BINARY_SLICE",
        2: "BUILD_TEMPLATE",
        4: "CALL_FUNCTION_EX",
        5: "CHECK_EG_MATCH",
        6: "CHECK_EXC_MATCH",
        7: "CLEANUP_THROW",
        8: "DELETE_SUBSCR",
        9: "END_FOR",
        10: "END_SEND",
        11: "EXIT_INIT_CHECK",
        12: "FORMAT_SIMPLE",
        13: "FORMAT_WITH_SPEC",
        14: "GET_AITER",
        15: "GET_ANEXT",
        16: "GET_ITER",
        18: "GET_LEN",
        19: "GET_YIELD_FROM_ITER",
        20: "INTERPRETER_EXIT",
        21: "LOAD_BUILD_CLASS",
        22: "LOAD_LOCALS",
        23: "MAKE_FUNCTION",
        24: "MATCH_KEYS",
        25: "MATCH_MAPPING",
        26: "MATCH_SEQUENCE",
        27: "NOP",
        28: "NOT_TAKEN",
        29: "POP_EXCEPT",
        30: "POP_ITER",
        31: "POP_TOP",
        32: "PUSH_EXC_INFO",
        33: "PUSH_NULL",
        34: "RETURN_GENERATOR",
        35: "RETURN_VALUE",
        36: "SETUP_ANNOTATIONS",
        37: "STORE_SLICE",
        38: "STORE_SUBSCR",
        39: "TO_BOOL",
        40: "UNARY_INVERT",
        41: "UNARY_NEGATIVE",
        42: "UNARY_NOT",
        43: "WITH_EXCEPT_START",
        44: "BINARY_OP",
        45: "BUILD_INTERPOLATION",
        46: "BUILD_LIST",
        47: "BUILD_MAP",
        48: "BUILD_SET",
        49: "BUILD_SLICE",
        50: "BUILD_STRING",
        51: "BUILD_TUPLE",
        52: "CALL",
        53: "CALL_INTRINSIC_1",
        54: "CALL_INTRINSIC_2",
        55: "CALL_KW",
        56: "COMPARE_OP",
        57: "CONTAINS_OP",
        58: "CONVERT_VALUE",
        59: "COPY",
        60: "COPY_FREE_VARS",
        61: "DELETE_ATTR",
        62: "DELETE_DEREF",
        63: "DELETE_FAST",
        64: "DELETE_GLOBAL",
        65: "DELETE_NAME",
        66: "DICT_MERGE",
        67: "DICT_UPDATE",
        68: "END_ASYNC_FOR",
        69: "EXTENDED_ARG",
        70: "FOR_ITER",
        71: "GET_AWAITABLE",
        72: "IMPORT_FROM",
        73: "IMPORT_NAME",
        74: "IS_OP",
        75: "JUMP_BACKWARD",
        76: "JUMP_BACKWARD_NO_INTERRUPT",
        77: "JUMP_FORWARD",
        78: "LIST_APPEND",
        79: "LIST_EXTEND",
        80: "LOAD_ATTR",
        81: "LOAD_COMMON_CONSTANT",
        82: "LOAD_CONST",
        83: "LOAD_DEREF",
        84: "LOAD_FAST",
        85: "LOAD_FAST_AND_CLEAR",
        86: "LOAD_FAST_BORROW",
        87: "LOAD_FAST_BORROW_LOAD_FAST_BORROW",
        88: "LOAD_FAST_CHECK",
        89: "LOAD_FAST_LOAD_FAST",
        90: "LOAD_FROM_DICT_OR_DEREF",
        91: "LOAD_FROM_DICT_OR_GLOBALS",
        92: "LOAD_GLOBAL",
        93: "LOAD_NAME",
        94: "LOAD_SMALL_INT",
        95: "LOAD_SPECIAL",
        96: "LOAD_SUPER_ATTR",
        97: "MAKE_CELL",
        98: "MAP_ADD",
        99: "MATCH_CLASS",
        100: "POP_JUMP_IF_FALSE",
        101: "POP_JUMP_IF_NONE",
        102: "POP_JUMP_IF_NOT_NONE",
        103: "POP_JUMP_IF_TRUE",
        104: "RAISE_VARARGS",
        105: "RERAISE",
        106: "SEND",
        107: "SET_ADD",
        108: "SET_FUNCTION_ATTRIBUTE",
        109: "SET_UPDATE",
        110: "STORE_ATTR",
        111: "STORE_DEREF",
        112: "STORE_FAST",
        113: "STORE_FAST_LOAD_FAST",
        114: "STORE_FAST_STORE_FAST",
        115: "STORE_GLOBAL",
        116: "STORE_NAME",
        117: "SWAP",
        118: "UNPACK_EX",
        119: "UNPACK_SEQUENCE",
        120: "YIELD_VALUE",
        234: "INSTRUMENTED_END_FOR",
        235: "INSTRUMENTED_POP_ITER",
        236: "INSTRUMENTED_END_SEND",
        237: "INSTRUMENTED_FOR_ITER",
        238: "INSTRUMENTED_INSTRUCTION",
        239: "INSTRUMENTED_JUMP_FORWARD",
        240: "INSTRUMENTED_NOT_TAKEN",
        241: "INSTRUMENTED_POP_JUMP_IF_TRUE",
        242: "INSTRUMENTED_POP_JUMP_IF_FALSE",
        243: "INSTRUMENTED_POP_JUMP_IF_NONE",
        244: "INSTRUMENTED_POP_JUMP_IF_NOT_NONE",
        245: "INSTRUMENTED_RESUME",
        246: "INSTRUMENTED_RETURN_VALUE",
        247: "INSTRUMENTED_YIELD_VALUE",
        248: "INSTRUMENTED_END_ASYNC_FOR",
        249: "INSTRUMENTED_LOAD_SUPER_ATTR",
        250: "INSTRUMENTED_CALL",
        251: "INSTRUMENTED_CALL_KW",
        252: "INSTRUMENTED_CALL_FUNCTION_EX",
        253: "INSTRUMENTED_JUMP_BACKWARD",
        256: "ANNOTATIONS_PLACEHOLDER",
        257: "JUMP",
        258: "JUMP_IF_FALSE",
        259: "JUMP_IF_TRUE",
        260: "JUMP_NO_INTERRUPT",
        261: "LOAD_CLOSURE",
        262: "POP_BLOCK",
        263: "SETUP_CLEANUP",
        264: "SETUP_FINALLY",
        265: "SETUP_WITH",
        266: "STORE_FAST_MAYBE_NULL",
    }

    def fast_calc_jump(self: instr) -> int:
        _, opcode, arg, pos = self
        if opcode in (JUMP_BACKWARD, JUMP_BACKWARD_NO_INTERRUPT):
            return pos - arg * 2

        if opcode == JUMP_FORWARD:
            return pos + arg * 2

        return arg * 2

    def calc_jump(self: instr) -> int:
        op, opcode, arg, _ = self
        if opcode not in JUMP_OP:
            raise Exception(f"{op} is not JUMP_OP !")

        if not arg:
            raise Exception(f"{op} without arg :\\")

        return fast_calc_jump(self)

    def op_name(i: int) -> str:
        return map.get(i, "<unknown-opcode>")

    def fast_name(i: int) -> str:
        return map[i]

    def unpack(code: bytes | bytearray, unpacker=fast_name) -> ty.iter[instr]:
        for pos, _, op, arg in dis._unpack_opargs(code):  # type: ignore
            yield (unpacker(op), op, arg, pos)


def code_to_pyc(code: ty.code) -> bytes:
    return imp_b._code_to_timestamp_pyc(code)  # type: ignore
