import socket
import threading
import sys


def read_until(s, what):
    data = s.recv(1024)
    print data

    while what not in data:
        d = s.recv(1024)
        sys.stdout.write(d)
        data += d

    return data


def send_data(s, what):
    print what
    s.send(what)

# Server Strings
ENTER_ACTION = "[*] ENTER ACTION> "
ENTER_SERVICE_ID = "[*] ENTER SERVICE ID> "
ENTER_PROGRAM_SIZE = "[*] ENTER PROGRAM SIZE> "
ENTER_PROGRAM_NAME = "[*] ENTER PROGRAM NAME> "

# Server Options
START_SERVICE = '1\n'
LIST_RUNNING_SERVICES = '2\n'
ATTACH_TO_SERVICE_TELETYPE = '3\n'
NC8_REFERENCE_MANUAL = '4\n'
CLOSE_SESSION = '5\n'


class ReaderThread(object):
    def __init__(self, s):
        self.socket = s
        self.thread = threading.Thread(target=self.run)

    def start(self):
        self.thread.start()

    def run(self):
        while True:
            data = self.socket.recv(1024)
            sys.stdout.write(data)


class ManagementInterface(object):
    def __init__(self):
        self.s = socket.socket()
        self.reader = ReaderThread(self.s)

    def connect(self):
        self.s.connect(('challenges.ringzer0team.com', 10283))
        self.reader.start()

    def list_running_services(self):
        send_data(self.s, LIST_RUNNING_SERVICES)

    def attach_to_service(self, id):
        send_data(self.s, ATTACH_TO_SERVICE_TELETYPE)
        send_data(self.s, str(id)+'\n')

    def attach(self):
        while True:
            data = raw_input()
            self.s.send(data+'\n')

    def run_program(self, name, code):
        send_data(self.s, START_SERVICE)
        send_data(self.s, name+'\n')
        send_data(self.s, str(len(code))+'\n')
        self.s.send(code+'\n')

    def send(self, data):
        self.s.send(data+'\n')
        sys.stdout.write(self.s.recv(2048))

    def close(self):
        send_data(self.s, CLOSE_SESSION)
