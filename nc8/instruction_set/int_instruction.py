from nc8.instruction import Instruction
from simpleeval import simple_eval
import random


class IntInstruction(Instruction):
    def __init__(self):
        super(IntInstruction, self).__init__('int',
                                             base_opcode=0x00,
                                             argument_range=(0x00, 0xf),
                                             instruction_format='int {0}')
        self.available_int_numbers = {0, 1, 2, 4, 10, 11}

    def parse_arguments(self, arg_value):
        return int(arg_value)

    def encode_arg(self, int_number):
        i = simple_eval(int_number)
        if i not in self.available_int_numbers:
            raise Exception("Cannot encode this int number")
        return i

    def run(self, machine, int_number):

        def read_char_handler():
            c = machine.read_char()
            machine.regs['r0'] = c

        def write_char_handler():
            c = machine.regs['r0']
            machine.write_char(c)

        def put_challenge_handler():
            challenge_address = machine.regs['r0']

            for i in xrange(32):
                machine.memory[challenge_address+i] = random.randrange(255)

            print '[nc8] Putting challenge data..'

        def validate_challenge_handler():
            challenge_address = machine.regs['r0']
            challenge_data = machine.memory.load(challenge_address, 32)

            def is_sorted(l):
                return all(l[i] <= l[i+1] for i in xrange(len(l)-1))

            if is_sorted(challenge_data):
                print '[nc8] Correct!'
            else:
                print '[nc8] Incorrect!'

        def do_something():
            print '[nc8] Called int 4!'
            challenge_address = machine.regs['r0']
            machine.memory.store(challenge_address, map(ord, 'FLAG-AAAAAAAAAAAAAAAAAAAAA'))


        {
            0: machine.exit,
            1: read_char_handler,
            2: write_char_handler,
            4: do_something,
            10: put_challenge_handler,
            11: validate_challenge_handler
        }[int_number]()