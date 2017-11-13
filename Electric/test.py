import copy
eus = [(7,8),(2,4),(5,3),(1,4),(1,2),(6,5)]
def f1(eus):
    eus1 = eus[:]
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

def f2(eus):
    eus = eus[:]
    isfind = list()
    for i in eus:
        if i not in isfind:
            isfind.append(i)
            l = [i[0],i[1]]
            for j in eus:
                if j not in isfind:
                    if l.count(j[0])> 0 and l.count(j[1]) > 0:return True
                    if l.count(j[0])> 0 or l.count(j[1]) > 0:
                        l +=[j[0],j[1]]
                        isfind.append(j)
                    
    return False

#print(f1(eus))

#print(f2(eus))

eus = [(7,8),(2,4),(5,3),(1,4),(-1,2),(6,5)]
def findEusTree(eus,e,e1):
    e.extend(eus[0:3])
    e1 = eus[0:3]
e ,e1 =[],[]
findEusTree(eus,e,e1)
print(eus)
print(e)
print(e1)