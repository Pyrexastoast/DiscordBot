print(chr(0x1F600))
emnum = 1975

with open("emojinumcodes") as fp:
    for i, line in enumerate(fp):
        if i==(emnum-1):
            print('line {0}:\t {1}'.format(i+1,line.strip()))
            hxcode = list(map(lambda x: chr(int(x, 16)), line.strip().split(',')))
            print('len(hxcode):\t', len(hxcode))
            hxcode = ''.join(hxcode)
            print('hxcode:\t', hxcode)
            print('\n')
        elif i>(emnum+2):
            break
