import copy
import numpy as np
import pandas as pd
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

def f3():
    eus = [(7,8),(2,4),(5,3),(1,4),(-1,2),(6,-5)]
    def findEusTree(eus,e,e1):
        e.extend(eus[0:3])
        e1 = eus[0:3]
    e ,e1 =[],[]
    findEusTree(eus,e,e1)
    print(eus)
    print(e)
    print(e1)
    print([True if 1 in e else False for e in eus ])
    print(all([True if 1 in e else False for e in eus ]))
    print(any([True if 1 in e else False for e in eus ]))
    t = list()
    [t.extend(list(e)) for e in eus]
    print(t)
    print(set(t))

def f4():
    eus=[(-1,1),(-1,2),(-1,3),(-1,4)]
    t = list()
    [t.extend(list(e)) for e in eus]
    print(set(t))
    print(all([True if -1 in e else False for e in eus ]))
    print(len(set(t))== len(eus)+1)
    print(set(eus[0]) & set(eus[1]))
    print([e for e in eus if 100 in e])
    a = [e for e in range(10)]
    print(a)
    for e in a:
        if e == 5: e = 30
    print(a)
    for i in range(len(a)):
        if i == 7: a[i] = 30
    print(a)
def f5():
    a=np.arange(0,20).reshape(4,5)
    print(a)
    b = np.arange(1,5).reshape(4,1)
    print(b)
    print(a[:,(0,2)])
    print(b[2])
    print(a[:,2]*b[2])
    c = [1,4,2,-1,10,49]
    c.sort()
    print(c)
    print(eus.sort(key=lambda x:x[1],reverse=True))
    print(eus)

def f6():
    eus=[(-2,2),(-1,1),(-1,3)]
    print(len(set(eus[0]) & set(eus[1])))

    eus = [(7,8),(2,4),(5,3),(1,4),(1,2),(6,5)]
    g = list()
    for e in eus:
        g1 = list()
        g1.append(e)
        for s in eus:
            if len(set(s) & set(e))==1: g1.append(s)
        g.append(g1)
    for g1 in g:
        print(g1)

