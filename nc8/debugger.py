import nc8
import traceback


class Debugger(object):
    def __init__(self, code):
        self.machine = nc8.Machine(code)
        self.breakpoints = {}
        self.dump_points = []
        self.skippers = {}
        self.commands = {
            'exit': exit,
            'break': self.set_breakpoint,
            'del': self.delete_breakpoint,
            'continue': self.continue_running,
            'stack': self.stack,
            'state': self.state,
            'next': self.run_next,
            'list': self.list,
            'dump_point': self.dump_point,
            'dump': self.dump,
            'disas': self.disas,
            'jump': self.jump,
            'skipper': self.skipper
        }

    def skipper(self, address, to_address):

        address = int(address, 16)

        if to_address.startswith('+') or to_address.startswith('-'):
            to_address = int(to_address, 16)+address
        else:
            to_address = int(to_address, 16)

        self.skippers[address] = to_address

    def jump(self, n):
        if n.startswith('+') or n.startswith('-'):
            n = int(n, 16)
            self.machine.regs['pc'] += n
        else:
            n = int(n, 16)
            self.machine.regs['pc'] = n

    def run(self):
        while True:
            cmd = raw_input('>> ')
            cmd = cmd.split(' ')

            try:
                self.commands[cmd[0]](*cmd[1:])
            except:
                traceback.print_exc()

    def set_breakpoint(self, address, count='1'):
        self.breakpoints[int(address, 16)] = int(count)-1

    def delete_breakpoint(self, address):
        if address == '*':
            self.breakpoints = {}
        else:
            address = int(address, 16)
            del self.breakpoints[address]

    def handle_pc_hooks(self, pc):
        if pc in self.breakpoints:
            if self.breakpoints[pc] == 0:
                print 'hit breakpoint at ', hex(pc)
                return True
            self.breakpoints[pc] -= 1

        if pc in self.dump_points:
            print 'hit dump point at', hex(pc)
            print self.machine.dump_regs()

        if pc in self.skippers:
            self.machine.regs['pc'] = self.skippers[pc]

        return False

    def continue_running(self):
        while not self.machine.exited:

            if self.handle_pc_hooks(self.machine.regs['pc']):
                break

            try:
                opcode = self.machine.decode_current()
            except nc8.OpcodeError as e:
                traceback.print_exc()
                return

            self.machine.regs['pc'] += 1
            opcode.run(self.machine)
        else:
            print '[nc8] Program Exited.'

    def disas(self, address='0', n='50', out_filename=None):
        address = int(address, 16)
        n = int(n)

        if (address+n) >= 0x8000:
            n = 0x8000-(address+n)

        output = ''

        for i in xrange(address, address+n):
            output += nc8.opcode_to_str(i, self.machine.memory[i], self.machine.instruction_set)+'\n'

        if out_filename is not None:
            with open(out_filename, 'wb') as f:
                f.write(output)
        else:
            print output

    def dump(self, dst_filename=None):
        dump = self.machine.dump()
        print dump

        if dst_filename is not None:
            with open(dst_filename, 'wb') as dump_file:
                dump_file.write(dump)

        print 'Process dumped.'

    def dump_point(self, address):
        self.dump_points.append(int(address, 16))

    def stack(self):
        print self.machine.stack.dump()

    def state(self):
        for reg_name in nc8.regs:
            print reg_name.upper(), hex(self.machine.regs[reg_name])

    def run_next(self):
        if self.machine.exited:
            print 'Program has exited!'
            return

        opcode = self.machine.decode_current()
        self.machine.regs['pc'] += 1
        opcode.run(self.machine)
        self.list('4')

    def list(self, length='10'):
        n = int(length)

        for ip in xrange(self.machine.regs['pc'], self.machine.regs['pc'] + n):
            nc8.display_opcode(ip, self.machine.memory[ip], self.machine.instruction_set)