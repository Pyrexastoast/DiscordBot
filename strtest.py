tst = 'When can people watch a movie?, Mon, Tue, Wed, Thr, Fri, Sat, Sun'
tst = list(map(lambda s: s.strip(" "), tst.split(",")))

for a in range(len(tst)):
    print("{0} \t{1}".format(a, tst[a]))

print(tst[-1])
p = {}
p=p.fromkeys(tst[1:], 0)
p['Question']=tst[0]
#for a in poll.keys()
#    print("Key: {0}, \tValue: {1}".format(a, poll[a])
