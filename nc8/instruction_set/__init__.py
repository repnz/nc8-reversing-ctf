from int_instruction import IntInstruction
from jmp_instructions import JumpInstruction, JumpZeroInstruction, JumpNotZeroInstruction
from math_instructions import AddInstruction, XorInstruction, DivInstruction
from mov_instructions import MoveImmToRegInstruction, MoveMemToRegInstruction, MoveRegToMemInstruction
from stack_instructions import PushMemoryInstruction, PushRegisterInstruction, PopRegisterInstruction
from math_instructions import OrInstruction, AndInstruction, MulInstruction

from nc8.errors import SourceAssemblyError


class OpcodeError(Exception):
    def __init__(self, opcode):
        self.opcode = opcode
        super(OpcodeError, self).__init__(hex(self.opcode) + ' is not known')


class InstructionSet(object):
    def __init__(self):

        self.__instruction_set = [
            IntInstruction(),
            MoveMemToRegInstruction(),
            PushRegisterInstruction(),
            PopRegisterInstruction(),
            PushMemoryInstruction(),
            JumpZeroInstruction(),
            AddInstruction(),
            JumpInstruction(),
            MoveImmToRegInstruction(),
            XorInstruction(),
            MoveRegToMemInstruction(),
            DivInstruction(),
            OrInstruction(),
            MulInstruction(),
            AndInstruction(),
            JumpNotZeroInstruction()
        ]

        self.__opcode_set = {}

        for instruction in self.__instruction_set:
            for opcode in instruction.generate_opcodes():
                self.__opcode_set[opcode.value] = opcode

    def decode(self, opcode):
        try:
            return self.__opcode_set[opcode]
        except KeyError:
            raise OpcodeError(opcode)

    def encode(self, line):
        for instruction in self.__instruction_set:
            try:
                return instruction.encode(line)

            except SourceAssemblyError:
                raise
            except:
                continue

        raise Exception("Cannot encode " + line)