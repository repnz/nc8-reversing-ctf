from nc8.instruction import Instruction
import nc8.conversions


class JumpInstruction(Instruction):
    def __init__(self):
        super(JumpInstruction, self).__init__('jmp',
                                              base_opcode=0xc0,
                                              argument_range=(0, 0xf),
                                              instruction_format='jmp {0}')

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_offset(arg_value)

    def encode_arg(self, offset_str):
        return nc8.conversions.convert_to_offset_value(offset_str)

    def run(self, machine, offset):
        machine.regs['pc'] += offset - 1

    def opcode_str(self, offset):
        return 'jmp ' + nc8.conversions.convert_offset_str(offset)


class JumpZeroInstruction(Instruction):
    def __init__(self):
        super(JumpZeroInstruction, self).__init__("jz",
                                                  base_opcode=0xa0,
                                                  argument_range=(0, 0xf),
                                                  instruction_format='jz {0}')

    def encode_arg(self, offset_str):
        return nc8.conversions.convert_to_offset_value(offset_str)

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_offset(arg_value)

    def run(self, machine, offset):
        if machine.regs['r0'] == 0:
            machine.regs['pc'] += offset - 1

    def opcode_str(self, argument):
        return 'jz {offset}'.format(offset=nc8.conversions.convert_offset_str(argument))


class JumpNotZeroInstruction(Instruction):
    def __init__(self):
        super(JumpNotZeroInstruction, self).__init__("jnz",
                                                     base_opcode=0xb0,
                                                     argument_range=(0, 0xf),
                                                     instruction_format='jnz {0}')

    def encode_arg(self, offset_str):
        return nc8.conversions.convert_to_offset_value(offset_str)

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_offset(arg_value)

    def run(self, machine, offset):
        if machine.regs['r0'] != 0:
            machine.regs['pc'] += offset - 1

    def opcode_str(self, argument):
        return 'jnz {offset}'.format(offset=nc8.conversions.convert_offset_str(argument))
