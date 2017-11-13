import copy

def f1():
    eus = [(7,8),(2,4),(2,3),(1,3),(-1,2),(1,5)]
    def findeus(eus1):#查找是否有并联理想电压源
        for i in eus1:#查找是否有间接并联理想电压源
            eus1.pop(eus1.index(i))
            l = [i[0],i[1]]
            while(True):
                has = False
                for j in eus1:
                    if l.count(j[0])> 0 and l.count(j[1]) > 0:return True
                    if l.count(j[0])> 0 or l.count(j[1]) > 0:
                        l +=[j[0],j[1]]
                        eus1.pop(eus1.index(j))
                        has = True
                        break
                if not has :break
        return False

    print(findeus(eus))
    eus.sort(key=lambda x:(max(x),min(x)))
    for i in eus:
        print(i)
        
a=[5,1,2,5,5,4,5,4,5,5,5]
while(True):
    remove = False
    for i in a:
        if i == 5:
            a.pop(a.index(i))
            remove = True
            break
    if not remove: break
reduce
print(a)