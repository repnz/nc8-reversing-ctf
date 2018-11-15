from nc8.instruction import Instruction
import nc8.conversions


class PushRegisterInstruction(Instruction):
    def __init__(self):
        super(PushRegisterInstruction, self).__init__("push",
                                                      base_opcode=0xd0,
                                                      argument_range=(0, 0xf),
                                                      instruction_format='push {0}')

    def encode_arg(self, reg):
        return nc8.conversions.convert_to_reg_value(reg)

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_arg_to_reg(arg_value)

    def run(self, machine, reg):
        machine.stack.push(machine.regs[reg])


class PopRegisterInstruction(Instruction):
    def __init__(self):
        super(PopRegisterInstruction, self).__init__("pop",
                                                     base_opcode=0xf0,
                                                     argument_range=(0, 0xf),
                                                     instruction_format='pop {0}')

    def encode_arg(self, reg):
        return nc8.conversions.convert_to_reg_value(reg)

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_arg_to_reg(arg_value)

    def run(self, machine, reg):

        if reg == 'pc':
            machine.regs['r13'] = machine.regs['pc']

        machine.regs[reg] = machine.stack.pop()


class PushMemoryInstruction(Instruction):
    def __init__(self):
        super(PushMemoryInstruction, self).__init__("push",
                                                    base_opcode=0xe0,
                                                    argument_range=(0, 0xf),
                                                    instruction_format='push [{0}]')

    def encode_arg(self, offset):
        return nc8.conversions.convert_to_offset_value(offset)

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_offset(arg_value)

    def run(self, machine, offset):
        val_to_push = machine.memory.load_word(machine.regs['pc'] + offset - 1)
        machine.stack.push(val_to_push)

    def opcode_str(self, offset):
        return "push [{offset}]".format(offset=nc8.conversions.convert_offset_str(offset))