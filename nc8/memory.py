import validations
import hexdump


class MachineMemory(object):
    def __init__(self):
        self.__memory = [0] * 0x8000

    def load_word(self, key):
        return (self[key] << 8) + self[key+1]

    def load_all(self):
        return list(self.__memory)

    def store_word(self, key, value):
        self[key] = (value >> 8) & 0xFF
        self[key+1] = value & 0xFF

    def load(self, key, length):
        return [self.__memory[i] for i in xrange(key, key+length)]

    def store(self, start, value):
        for index, val in enumerate(value):
            self[start+index] = value[index]

    def __setitem__(self, key, value):
        validations.validate_word(key, "Address")
        validations.validate_word(value, "Memory Value")
        self.__memory[key] = value

    def __getitem__(self, item):
        validations.validate_word(item, "Address")
        return self.__memory[item]

    def dump(self):
        return hexdump.hexdump(''.join(map(chr, self.__memory)), result='return')