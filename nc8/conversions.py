from regs import regs
from errors import SourceAssemblyError


def convert_to_reg_value(reg_str):
    return regs.index(reg_str)


def convert_to_offset_value(offset_str):
    offset = int(offset_str)

    if not (-8 <= offset <= 7):
        raise SourceAssemblyError("Not in range!")
    if offset < 0:
        return 0x10 + offset

    return offset-2


def convert_offset(arg):
    if not (0 <= arg <= 0xf):
        raise SourceAssemblyError("Argument not in range")
    if arg >= 8:
        return -1 * (0x10 - arg)
    return arg + 2


def convert_offset_str(offset):
    if offset >= 0:
        return '+' + str(offset)
    return str(offset)


def convert_arg_to_reg(arg):
    return regs[arg]


def convert_arg_to_dst_src(arg):
    src = arg & 0b11
    dst = (arg >> 2) & 0b11
    return regs[dst], regs[src]


def encode_regs(dst, src):
    dst = convert_to_reg_value(dst)
    src = convert_to_reg_value(src)

    if not ((0 <= dst <= 3) and (0 <= src <= 3)):
        raise SourceAssemblyError("Not in range")

    return (dst << 2) + src