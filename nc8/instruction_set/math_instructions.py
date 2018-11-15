from nc8.instruction import Instruction
import nc8.conversions


class AddInstruction(Instruction):
    def __init__(self):
        super(AddInstruction, self).__init__('add',
                                             base_opcode=0x40,
                                             argument_range=(0x0, 0xf),
                                             instruction_format='add {0}, {1}')

    def encode_arg(self, dst, src):
        return nc8.conversions.encode_regs(dst, src)

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_arg_to_dst_src(arg_value)

    def run(self, machine, dst, src):
        machine.regs[dst] += machine.regs[src]
        machine.regs[dst] &= 0xFFFF


class XorInstruction(Instruction):
    def __init__(self):
        super(XorInstruction, self).__init__('xor',
                                             base_opcode=0x50,
                                             argument_range=(0x0, 0xf),
                                             instruction_format='xor {0}, {1}')

    def encode_arg(self, dst, src):
        return nc8.conversions.encode_regs(dst, src)

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_arg_to_dst_src(arg_value)

    def run(self, machine, dst, src):
        machine.regs[dst] ^= machine.regs[src]
        machine.regs[dst] &= 0xFFFF


class AndInstruction(Instruction):
    def __init__(self):
        super(AndInstruction, self).__init__('and',
                                             base_opcode=0x60,
                                             argument_range=(0x0, 0xf),
                                             instruction_format='and {0}, {1}')

    def encode_arg(self, dst, src):
        return nc8.conversions.encode_regs(dst, src)

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_arg_to_dst_src(arg_value)

    def run(self, machine, dst, src):
        machine.regs[dst] &= machine.regs[src]


class OrInstruction(Instruction):
    def __init__(self):
        super(OrInstruction, self).__init__('or',
                                            base_opcode=0x70,
                                            argument_range=(0x0, 0xf),
                                            instruction_format='or {0}, {1}')

    def encode_arg(self, dst, src):
        return nc8.conversions.encode_regs(dst, src)

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_arg_to_dst_src(arg_value)

    def run(self, machine, dst, src):
        machine.regs[dst] |= machine.regs[src]


class MulInstruction(Instruction):
    def __init__(self):
        super(MulInstruction, self).__init__('mul',
                                             base_opcode=0x80,
                                             argument_range=(0, 0xf),
                                             instruction_format='mul {0}, {1}')

    def encode_arg(self, dst, src):
        return nc8.conversions.encode_regs(dst, src)

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_arg_to_dst_src(arg_value)

    def run(self, machine, dst, src):
        machine.regs[dst] *= machine.regs[src]
        machine.regs[dst] &= 0xFFFF


class DivInstruction(Instruction):
    def __init__(self):
        super(DivInstruction, self).__init__('div',
                                             base_opcode=0x90,
                                             argument_range=(0, 0xf),
                                             instruction_format='div {0}, {1}')

    def encode_arg(self, dst, src):
        return nc8.conversions.encode_regs(dst, src)

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_arg_to_dst_src(arg_value)

    def run(self, machine, dst, src):
        dst_value = machine.regs[dst]
        src_value = machine.regs[src]

        machine.regs[src] = dst_value % src_value
        machine.regs[dst] = dst_value / src_value
