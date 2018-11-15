import os
import nc8
import sys
import argparse
from pprint import pprint


def main():
    nc8_run_tool({
        'debug': debug,
        'run': run,
        'disassemble': disassemble,
        'assemble': assemble,
        'run_remote': run_remote_tool
    })


def nc8_run_tool(commands):
    parser = argparse.ArgumentParser(
        description='NC8 Tool Interface',
        usage='''nc8_cli.py <command> [<args>]

assemble       Assemble code of NC8
disassemble    Disassemble NC8 machine code 
run            Run an NC8 Code in an emulator
debug          Debug NC8 Code 
'''
    )

    parser.add_argument('command', help='Subcommand to run')
    args = parser.parse_args(sys.argv[1:2])

    if args.command not in commands:
        print 'Unrecognized command'
        parser.print_help()
        exit(1)

    commands[args.command]()


def run():
    parser = argparse.ArgumentParser(
        description='Run NC8 machine code')

    parser.add_argument('binfile')

    args = parser.parse_args(sys.argv[2:])

    with open(args.binfile, 'rb') as f:
        code = f.read()

    machine = nc8.Machine(map(ord, code))
    machine.run()


def get_file_name(file_path):
    base = os.path.basename(file_path)
    return os.path.splitext(base)[0]


def assemble():
    parser = argparse.ArgumentParser(
        description='Assemble NC8 Source Files')

    parser.add_argument('sourcefile')
    parser.add_argument('--outfile')
    parser.add_argument('--action')
    parser.add_argument('--offset')
    parser.add_argument('--inject_file')
    parser.add_argument('--program_name')

    args = parser.parse_args(sys.argv[2:])

    with open(args.sourcefile, 'r') as source_file:
        source = source_file.read()

    offset = 0

    if args.offset:
        offset = int(args.offset, 16)

    s, machine_code, names, macros = nc8.assemble(source.split('\n'), offset)
    pprint(macros)
    print '\n'.join([(hex(value) + ': ' + key) for key, value in sorted(names.items(), key=lambda (kv): kv[1])])

    if args.inject_file:
        original_code = map(ord, open(args.inject_file, 'rb').read())

        back_offset = len(original_code)-offset

        if back_offset < len(machine_code):
            original_code += [0] * (len(machine_code)-back_offset)

        for index, new_value in enumerate(machine_code):
            original_code[index+offset] = new_value

        machine_code = original_code

    if args.outfile:
        with open(args.outfile, 'wb') as f:
            f.write(''.join(map(chr, machine_code)))

    if args.action == 'debug':
        dbg = nc8.Debugger(machine_code)
        dbg.run()

    elif args.action == 'run':
        machine = nc8.Machine(machine_code)
        machine.run()

    elif args.action == 'run_remote':

        run_remote(
            code=''.join(map(chr, machine_code)),
            program_name=args.program_name if args.program_name else get_file_name(args.sourcefile)
        )


def disassemble():
    parser = argparse.ArgumentParser(
        description='Disassemble NC8 machine code')

    parser.add_argument('binfile')
    parser.add_argument('--outfile')

    args = parser.parse_args(sys.argv[2:])

    with open(args.binfile, 'rb') as f:
        code = f.read()

    source_lines = nc8.disassemble(map(ord, code))
    source = '\n'.join(source_lines)

    if args.outfile:
        with open(args.outfile, 'wb') as outfile:
            outfile.write(source)
    else:
        print source


def debug():
    parser = argparse.ArgumentParser(
        description='Debug NC8 machine code')

    parser.add_argument('binfile')

    args = parser.parse_args(sys.argv[2:])

    with open(args.binfile, 'rb') as f:
        code = map(ord, f.read())

    dbg = nc8.Debugger(code)
    dbg.run()


def run_remote(code, program_name):
    iface = nc8.ManagementInterface()
    iface.connect()
    iface.run_program(program_name, code)
    iface.attach_to_service(4)

    try:
        iface.attach()
    except:
        while True:
            try:
                os._exit(0)
            except:
                pass


def run_remote_tool():
    parser = argparse.ArgumentParser(
        description='Run Remote Programs')

    parser.add_argument('binfile')
    parser.add_argument('--program_name')
    args = parser.parse_args(sys.argv[2:])

    program_name = 'CHALLENGE3'

    if args.program_name:
        program_name = args.program_name

    run_remote(open(args.binfile, 'rb').read(), program_name)


if __name__ == "__main__":
    main()
