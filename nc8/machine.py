import nc8.memory
import nc8.stack
import nc8.instruction_set
from regs import regs
import sys


class Machine(object):
    def __init__(self, code):
        self.regs = {reg: 0 for reg in regs}
        self.code = code
        self.memory = nc8.memory.MachineMemory()
        #self.input_buffer = ((0x62,)*2 + (0x10,)*62)*450+(0x61, 0x62)*32*58+(0x50, 0x04, 0xce)+(0x10,)*34+(0x11,)
        self.input_buffer = []
        self.input_buff_index = 0
        self.exited = False

        for i, c in enumerate(code):
            self.memory[i] = c

        self.stack = nc8.stack.MachineStack(self)
        self.instruction_set = nc8.instruction_set.InstructionSet()
        self.regs['sp'] = 0x7FFE

    def run(self):
        while not self.exited:
            op = self.decode_current()
            self.regs['pc'] += 1
            op.run(machine=self)

    def dump_regs(self):
        lines = ''

        for index, reg_name in enumerate(regs):
            lines += reg_name + ': ' + hex(self.regs[reg_name]) + '\t'

            if index % 2 == 1:
                lines += '\n'

        return lines

    def dump(self):
        return 'Regs:\n{regs}\nStack:\n{stack}\nMemory\n{memory}'.format(
            regs=self.dump_regs(),
            stack=self.stack.dump(),
            memory=self.memory.dump()
        )

    def decode_current(self):
        return self.instruction_set.decode(self.memory[self.regs['pc']])

    def read_char(self):
        if self.input_buffer:
            v = self.input_buffer[0]
            self.input_buffer = self.input_buffer[1:]
            return v
        else:
            data = sys.stdin.read(1)
            if data.strip() == '[DEBUG]':
                raise Exception("Back To Debugger")
            self.input_buffer = self.input_buffer = map(ord, data)
            v = self.input_buffer[0]
            self.input_buffer = self.input_buffer[1:]
            return v

    def write_char(self,c):
        sys.stdout.write(chr(c))

    def exit(self):
        self.exited = True
