import copy
<<<<<<< HEAD

def f1():
    eus = [(7,8),(2,4),(2,3),(1,3),(-1,2),(1,5)]
    def findeus(eus1):#查找是否有并联理想电压源
        for i in eus1:#查找是否有间接并联理想电压源
            eus1.pop(eus1.index(i))
=======
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
>>>>>>> 96ed8521bbe47397814e241ab0cb776d67eff51b
            l = [i[0],i[1]]
            for j in eus:
                if j not in isfind:
                    if l.count(j[0])> 0 and l.count(j[1]) > 0:return True
                    if l.count(j[0])> 0 or l.count(j[1]) > 0:
                        l +=[j[0],j[1]]
                        isfind.append(j)
                    
    return False

<<<<<<< HEAD
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
=======
print(f1(eus))

print(f2(eus))

eus = [(7,8),(2,4),(5,3),(1,4),(-1,2),(6,5)]
def findEusTree(eus):
    eus = eus[:]
    isfind = list()
    earthEus = [e for e in eus if -1 in eus]
    for e in earthEus:
        
>>>>>>> 96ed8521bbe47397814e241ab0cb776d67eff51b
