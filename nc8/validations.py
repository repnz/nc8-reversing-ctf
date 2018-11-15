def is_word(value):
    return 0 <= value <= 0xFFFF


def is_byte(value):
    return 0 <= value < 0xFF


def validate_word(value, name):
    if not is_word(value):
        raise IndexError(name + " cannot be " + hex(value) + ", it has to be a word")


def validate_byte(value, name):
    if not is_byte(value):
        raise IndexError(name + " cannot be " + hex(value) + ", it has to be a byte")