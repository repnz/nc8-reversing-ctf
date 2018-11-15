data = open('part_1_analysis\\part_1.nc8', 'rb').read()
flag = ''

for i in xrange(0x75, 0x15c, 10):
    flag += chr(0x10000-((ord(data[i])<<8)+ord(data[i+1])))

print flag  # FLAG-B@by_st3ps_w1th_NC8