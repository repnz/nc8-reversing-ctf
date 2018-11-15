from parse import parse
from simpleeval import simple_eval
from collections import defaultdict
from instruction_set import InstructionSet
from errors import SourceAssemblyError


def evaluate_variable(variable, variable_type):
    item = simple_eval(variable, functions={'len': len})

    if isinstance(item, int):
        item = [item]
    else:
        item = map(ord, item)

    if variable_type == 'db':
        for b in item:
            yield b

    elif variable_type == 'dw':
        for b in item:
            yield (b >> 8) & 0xFF
            yield b & 0xFF
    else:
        raise Exception


def add_name(line, names, current_address, missing_name_users):

    values = line.split(' ', 1)

    names[values[0][1:]] = current_address

    if len(values) == 1:
        return

    others = values[1]
    var_type, var_value = others.split(' ', 1)

    if not var_value.startswith('.'):
        # a value declaration
        for value in evaluate_variable(variable=var_value, variable_type=var_type):
            yield value

        return

    var_value = var_value[1:]

    if var_value not in names:
        # put the index of that user
        missing_name_users[var_value].append(current_address)

        # There supposed to be a value here
        yield line
        yield -1
        return

    else:
        yield (names[var_value] >> 8) & 0xFF
        yield (names[var_value]) & 0xFF


def parse_offset(thing, names, current_address, missing_names):
    if thing.startswith('.'):
        if thing[1:] in names:
            val = int(names[thing[1:]])
            x = val - current_address

            if not (-8 <= x <= 7):
                raise SourceAssemblyError("Offset not in range! trying to jump to " + thing[1:])

            return str(x)
        else:
            missing_names[thing[1:]].append(current_address)
    return thing

offset_instructions = [
    'push [{offset}]',
    'jmp {offset}',
    'jz {offset}',
    'jnz {offset}'
]


def line_remove_name(names, line, missing_name_users, current_address):
    if line.startswith('.'):
        for b in add_name(line, names, current_address, missing_name_users):
            yield b
        return

    for offset_instruction in offset_instructions:

        offset = parse(format=offset_instruction, string=line)

        if offset is None:
            continue

        offset = offset['offset']
        offset = parse_offset(offset, names, current_address, missing_name_users)
        yield offset_instruction.format(offset=offset)
        break

    else:
        yield line


def remove_names(lines, offset=0):
    instructions_str = []
    names = {}
    missing_name_users = defaultdict(lambda: [])

    for line in lines:
        for b in line_remove_name(names, line, missing_name_users, offset+len(instructions_str)):
            instructions_str.append(b)

    handle_missing_names(instructions_str, missing_name_users, names, offset)

    return instructions_str, names


def handle_missing_names(instructions_str, missing_name_users, names, offset):
    for missing_name in missing_name_users:
        if missing_name not in names:
            raise Exception("Missing name " + missing_name)

        for missing_user_address in missing_name_users[missing_name]:
            original_line = instructions_str[missing_user_address-offset]
            address = missing_user_address

            for value in line_remove_name(names, original_line, missing_name_users, missing_user_address):
                instructions_str[address-offset] = value
                address += 1


def remove_comments_and_whitespace(lines):
    after_removal = []

    for line in lines:
        line = line.split(';')[0]
        line = " ".join(line.split())

        if not line.strip():
            continue

        after_removal.append(line)

    return after_removal


def remove_macros(lines):
    macros = {}
    after_macros = []

    for line in lines:
        for macro_name, macro_value in macros.iteritems():
            line = line.replace(macro_name, macro_value)

        if line.startswith("#define"):
            macro_name, macro_value = line.split(' ')[1:]
            macros['$'+macro_name] = macro_value
            continue

        after_macros.append(line)

    return after_macros, macros


def assemble(lines, offset=0):
    instruction_set = InstructionSet()
    lines = remove_comments_and_whitespace(lines)
    lines, macros = remove_macros(lines)
    instructions_str, names = remove_names(lines, offset)
    instructions_bytes = []

    for ins_str in instructions_str:
        if isinstance(ins_str, int):
            instructions_bytes.append(ins_str)
            continue

        ins_byte = instruction_set.encode(ins_str)

        if not (0 <= ins_byte < 0xFF):
            raise Exception("Error in instruction " + ins_str)

        instructions_bytes.append(ins_byte)

    return instructions_str, instructions_bytes, names, macros
