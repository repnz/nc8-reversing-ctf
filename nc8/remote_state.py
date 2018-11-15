import nc8


def parse_remote_state(data):
    regs = extract_registers(data)
    memory = extract_memory(data)
    return regs, memory


def get_first_nonspace(s, start_i=0, step=1):

    for i in xrange(start_i, len(s), step):
        if s[i] != ' ':
            return i

    return -1


def extract_registers(data):
    trace_str = 'Trace:'
    stack_str = 'Stack:'
    trace_start_index = data.index(trace_str) + len(trace_str)

    regs_str = data[trace_start_index:data.index(stack_str, trace_start_index)]

    regs = {}

    i = 0

    while True:
        reg_name_start = get_first_nonspace(regs_str, i)

        if reg_name_start == -1:
            break

        reg_name_end_index = regs_str.index(': ')
        reg_name = regs_str[reg_name_start:reg_name_end_index]
        reg_value_str = regs_str[reg_name_end_index+2:reg_name_end_index+2+4]
        reg_value = int(reg_value_str, 16)
        regs[reg_name] = reg_value
        i = reg_name_end_index+2+4

    return regs


def extract_memory(data):
    mem_dump_str = 'Mem dump:'

    data = data[data.index(mem_dump_str)+len(mem_dump_str):]
    dump = []

    for line in data.split('\n'):
        start_index = line.index(': ') + 2
        hex_values = line[start_index:start_index + 79].split(' ', )

        dump.append(int(hex_values[:2], 16))
        dump.append(int(hex_values[2:], 16))

    mem = nc8.MachineMemory()
    mem.store(0, dump)
    return mem
