from instruction_set import InstructionSet
from instruction import opcode_to_str


def disassemble(input_code):
    ins = InstructionSet()
    source = []

    for ip, val in enumerate(input_code):
        source.append(opcode_to_str(ip, val, ins))

    return source

