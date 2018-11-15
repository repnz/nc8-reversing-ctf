from parse import parse


def display_opcode(ip, val, s):
    print opcode_to_str(ip, val, s)


class Opcode(object):
    def __init__(self, name, value, instruction, arguments=()):
        self.name = name
        self.value = value
        self.instruction = instruction
        self.arguments = arguments
        self.str_value = self.instruction.opcode_str(*arguments)

    def __str__(self):
        return self.str_value

    def run(self, machine):
        self.instruction.run(machine, *self.arguments)


def opcode_to_str(ip, value, instruction_set):
    op_str = "0x%02x 0x%02x " % (ip, value)

    try:
        s = instruction_set.decode(value)
    except:
        op_str += "'" + chr(value) + "'"
    else:
        op_str += str(s)

    return op_str


class Instruction(object):

    def __init__(self, name, base_opcode, argument_range, instruction_format):
        self.name = name
        self.instruction_format = instruction_format
        self.base_opcode = base_opcode
        self.argument_range = argument_range

    def encode_arg(self, *args):
        raise NotImplementedError

    def encode(self, line):
        result = parse(
            format=self.instruction_format,
            string=line
        )

        if result is None:
            raise Exception

        args = tuple(result)
        value = self.base_opcode

        if not args:
            return value

        return value+self.encode_arg(*args)

    def parse_arguments(self, arg_value):
        return ()

    def generate_opcodes(self):
        min, max = self.argument_range[0], self.argument_range[1]

        for arg_value in xrange(min, max + 1):
            args = self.parse_arguments(arg_value)

            if not hasattr(args, '__iter__'):
                args = [args]
            yield Opcode(
                name=self.name,
                value=self.base_opcode+arg_value,
                instruction=self,
                arguments=args
            )

    def opcode_str(self, *args):
        return self.instruction_format.format(*map(str, args))


