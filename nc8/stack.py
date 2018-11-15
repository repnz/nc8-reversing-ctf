import hexdump


class MachineStack(object):
    def __init__(self, machine):
        self.machine = machine

    def push(self, value):
        self.machine.regs['sp'] -= 2
        current_sp = self.machine.regs['sp']
        self.machine.memory.store_word(current_sp, value)

    def pop(self):
        current_sp = self.machine.regs['sp']
        val = self.machine.memory.load_word(current_sp)
        self.machine.regs['sp'] += 2
        return val

    def dump(self, n=20):
        dump = ''

        start = self.machine.regs['sp']

        for i in xrange(start, start + 20, 2):
            if i > 0x7ffe:
                break

            dump += '{sp}: {b}\n'.format(
                sp=hex(i),
                b=hex(self.machine.memory.load_word(i))
            )

        return dump
