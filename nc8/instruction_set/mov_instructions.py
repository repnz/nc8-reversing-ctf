from nc8.instruction import Instruction
from nc8.regs import regs
import nc8.conversions


class MoveImmToRegInstruction(Instruction):
    def __init__(self):
        super(MoveImmToRegInstruction, self).__init__('mov',
                                                      base_opcode=0x10,
                                                      argument_range=(0, 0xf),
                                                      instruction_format='mov {0}, {1}')
        self.imm_repr_to_imm = {
            0b11: -1,
            0b10: 2,
            0b00: -2,
            0b01: 1
        }

        self.imm_to_imm_repr = {value:key for key, value in self.imm_repr_to_imm.iteritems()}

    def encode_arg(self, reg, imm):
        imm = int(imm)
        reg = nc8.conversions.convert_to_reg_value(reg)

        if not (0 <= reg <= 0b11):
            raise Exception('Value Not Correct')

        if imm not in self.imm_to_imm_repr:
            raise Exception("Error with value")

        return (reg << 2)+self.imm_to_imm_repr[imm]

    def parse_arguments(self, arg_value):
        return self.convert_to_reg_imm(arg_value)

    def convert_to_reg_imm(self, argument):
        reg = regs[(argument >> 2) & 0b11]

        imm = self.imm_repr_to_imm[argument & 0b11] & 0xFFFF

        return reg, imm

    def run(self, machine, reg, imm):
        machine.regs[reg] = imm


class MoveRegToMemInstruction(Instruction):
    def __init__(self):
        super(MoveRegToMemInstruction, self).__init__('mov',
                                                      base_opcode=0x20,
                                                      argument_range=(0, 0xf),
                                                      instruction_format='mov [{0}], {1}')

    def run(self, machine, dst, src):
        dst_address = machine.regs[dst]
        machine.memory[dst_address] = machine.regs[src] & 0xFF

    def encode_arg(self, dst, src):
        return nc8.conversions.encode_regs(dst, src)

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_arg_to_dst_src(arg_value)


class MoveMemToRegInstruction(Instruction):
    def __init__(self):
        super(MoveMemToRegInstruction, self).__init__('mov',
                                                      base_opcode=0x30,
                                                      argument_range=(0, 0xf),
                                                      instruction_format='mov {0}, [{1}]')

    def encode_arg(self, dst, src):
        return nc8.conversions.encode_regs(dst, src)

    def parse_arguments(self, arg_value):
        return nc8.conversions.convert_arg_to_dst_src(arg_value)

    def run(self, machine, dst, src):
        mem_address = machine.regs[src]
        machine.regs[dst] = machine.memory[mem_address]
