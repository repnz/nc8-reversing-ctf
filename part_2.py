
def xor_encrypt(mem, a, b, a_length, b_length):
    for i in xrange(a_length):
        mem[a+i] = (mem[a+i] ^ mem[b+(i % b_length)]) & 0xFF
    return a


def check_eq(mem, a, b, length):
    for i in xrange(length):
        if mem[a+i] != mem[b+i]:
            raise Exception
    return True


def add_encrypt(mem, a, b, a_length, b_length):
    for i in xrange(a_length):
        mem[i+a] = (mem[a+i] + mem[b+(i % b_length)]) & 0xFF


def decoder():
    mem = map(ord, open('part_2.nc8', 'rb').read())


def original():
    mem = map(ord, open('part_2.nc8', 'rb').read())

    flag = 'FLAG-A_B1t_M0R3_C0MPl3X_15nTnit?'

    for i in xrange(len(flag)):
        mem[0x04+i] = ord(flag[i])

    xor_encrypt(mem, a=0x100, a_length=0xf8, b=0x04, b_length=0x4)
    check_eq(mem, a=0x100, b=0xfa, length=0x04)

    add_encrypt(mem, a=0x17d, a_length=0xfd, b=0x8, b_length=4)
    xor_encrypt(mem, a=0xc, a_length=8, b=0x104, b_length=4)
    check_eq(mem, a=0xc, b=0x27a, length=8)

    add_encrypt(mem, a=0xfa, a_length=4, b=0x282, b_length=4)
    xor_encrypt(mem, a=0x100, a_length=0xf8, b=0x14, b_length=4)
    check_eq(mem, a=0x100, b=0xfa, length=4)

    xor_encrypt(mem, a=24, a_length=8, b=260, b_length=4)
    check_eq(mem, a=24, b=0x1d2, length=8)

    print mem[0x100:0x104]
    print mem[0xfa:0xfa + 4]

    #xor_encrypt(mem, a=0x100, a_length=0x4, b=0xfa, b_length=0x04)

    print mem[0x100:0x104]
    print mem[0xfa:0xfa+4]

    xor_encrypt(mem, a=0x100, a_length=0xf8, b=0x20, b_length=4)
    check_eq(mem, a=0x100, b=0xfa, length=0x04)

    print 'yay'

    0xcd, 0xa7, 0x38, 0x7f

    0xa3, 0xce, 0x4c, 0x40


dat = map(ord, open('part_2_analysis\\part_2.nc8', 'rb').read())

flag = map(ord, 'FLAG')

l1=(0xf5, 0x5e, 0x4c, 0x7a, 0xf4, 0x78, 0x20, 0x68)
l2=(0xc4, 0x2a, 0x13, 0x37)
v = ''

for i in xrange(8):
    v += chr(l1[i] ^ l2[i%4])

print v

a_fa = (0xe0, 0xfe, 0x01, 0x10)
a_282 = (0xc3, 0xd0, 0x4b, 0x30)
a_100 = (0xe0, 0xfe, 0x01, 0x10)

# a_100 + a_282 = x ^ a_fa
# (a_100 + a_282) ^ a_fa = x

a_100_p_a_282 = []

answer = []

for i in xrange(4):
    answer.append(((a_100[i] + a_282[i]) & 0xFF) ^ a_fa[i])

print ''.join(map(chr, answer))