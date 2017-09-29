import numpy as np
from enum import Enum,unique
import math as mh
import copy
class PFC(object):
    '''潮流计算类PFC'''
    # electricElementsCount = 0
    def __init__(self, numOfIterations=100, voltageOfIterator=1):
        '''初始化函数'''
        self.numOfIterations = numOfIterations
        self.voltageOfIterator = voltageOfIterator
        self.electricElements = list()
    def addElement(self, elements):
        '''添加一个元件，可以是一个元件或者元件列表，注意元件参考节点编号为-1，其它均大于-1
        elements={"eType":'Y', "id":0, "ids":(0,1), "Y":1, "U":1, "I"=1}或者
        elements=[{"eType":'Y', "id":1, "ids":(0,1), "Y":1, "U":1, "I"=1},
                  {"eType":'I', "id":2, "ids":(0,1), "Y":1, "U":1, "I"=1}]
        '''
        if isinstance(elements, list):
            self.electricElements += elements
        else:
            self.electricElements.append(elements)
    def createYIMatrix(self):
        '''构造潮流计算线性方程组的Y，I矩阵，并核实节点电压方程组节点编号以0为起点的连续编号
           返回值(self.Y,self.I)
        '''
        elments = self.electricElements
        if len(elments) <=0:raise IndexError("没有电气元件，无法进行潮流计算！")

        ids = [j for i in elments for j in i.ids]
        ids = list(set(ids))
        if max(ids)+2>len(ids) or min(ids)  < -1:
            raise Exception('电气元件节点号有误，请核实')
        self.__initYUI(len(ids)-1,type(elments[0].y))

        for e in elments:
            id1,id2 = e.ids
            if e.eType == EType.Y:
                if id1 >= 0: self.Y[id1,id1] += e.y
                if id2 >= 0: self.Y[id2,id2] += e.y
                if id1 >= 0 and id2 >= 0:
                    self.Y[id1,id2] -= e.y
                    self.Y[id2,id1] -= e.y
            elif e.eType == EType.Ei:   
                if id1 >= 0:self.I[id1,0] -= e.i
                if id2 >= 0:self.I[id2,0] += e.i
            elif e.eType == EType.Eu:
                if id1 >=0: self.U[id1,0] += e.u
                if id2 >=0: self.U[id2,0] -= e.u
        return (self.Y,self.I)
    def __initYUI(self, elmentCout,type):
        N = elmentCout
        self.Y = np.mat(np.zeros((N,N),dtype=type))
        self.U = np.mat(np.zeros((N,1),dtype=type))
        self.I = np.mat(np.zeros((N,1),dtype=type))
    def caculate(self):
        '''
        求解电路节点电压方程组，求解时，需要进行迭代计算，直到满足迭代精度或者达到迭代次数才结束。
        返回值(self.U,self.Y,self.I)
        '''
        num = 0;isFirst = True
        
        eus = [e for e in self.electricElements if e.eType == EType.Eu]#理想电压源列表
        
        def prepEu():#预处理有理想电源的节点电压方程组参数
            def findeus(eus):#查找是否有并联理想电压源
                eus1 = copy.copy(eus)
                for i in eus1:
                    eus1.pop(eus1.index(i))
                    l = [i.ids[0],i.ids[1]]
                    while(True):
                        has = False
                        for j in eus1:
                            if j.ids[0] in l and j.ids[1] in l: return True
                            if j.ids[0] in l or j.ids[1] in l:
                                l +=[j.ids[0],j.ids[1]]
                                eus1.pop(eus1.index(j))
                                has = True
                                break
                        if not has :break
                return False
            if findeus(eus): raise Exception("有并联的理想电压源")

            eus.sort(key=lambda x:(max(x.ids),min(x.ids) == -1,min(x.ids)))
            unodes = dict()#保存节点理想电压源及节点电压
            
            def funodes(node):#查找与给定理想电压源相连的理想电压源列表
                for n in eus:
                    if node in n.ids and\
                    not ((n.ids[0] if n.ids[0] == node else n.ids[1])in unodes.keys()):
                        nd = {n.ids[1],n.u} if n.ids[0] == node else {n.ids[0],-e.u}
                        unodes.items.append(nd)
                        funodes(nd)
            for e in eus:#查找并保存与以参考节点为节点理想电压源及其相连的理想电压源的的节点列表
                if min(e.ids) == -1:#查找以参考节点为节点的理想电压源的理想电压源列表
                    node = max(e.ids)
                    unodes[node] = e.u
                    funodes(node)
            unodes1 = list()#保存不以参考节点为节点的理想电压及其相邻节点
            for e in eus:#查找并保存剩余理想电压源节点及节点电压
                if not e.ids[0] in unodes.keys() and not e.ids[1] in unodes.keys():
                    unodes[e.ids[1]] =e.u
                    funodes(e.ids[1])

        prepEu()#预处理

        '''解节点电压方程组'''
        while self.__iteration(isFirst) and num <= self.numOfIterations:
            if len(eus) <= 0:self.U = np.linalg.solve(self.Y,self.I)#无理想电压源
            else:
                if isFirst:
                    for e in eus:
                        if e.ids[0] == -1 or e.ids[1] == -1:
                            pass
                        elif True:
                            pass
            num += 1
            isFirst = False
        return (self.U,self.Y,self.I)
    def __iteration(self,isFirst):
        isIter = False#是否需要继续迭代，FALSE表示迭代结束，TRUE表示继续迭代
        if isFirst:return True
        for e in self.electricElements:
            if e.eType == EType.S:
                '''元件为功率源，判断功率源前后电压是否恒定，如果是，结束迭代，否则更新功率源电流i=s/u'''
                oldu,e.u = e.u,self.getElementU(e)
                if(abs(oldu - e.u) > self.voltageOfIterator):
                    newi = (e.s/e.u).conj
                    di = newi - e.i
                    e.i = newi
                    if e.ids[0] != -1:self.I[e.ids[0],0] -= di
                    if e.ids[1] != -1:self.I[e.ids[1],0] += di
                    isIter = True#进行下一次迭代计算
        return isIter
    def getElementU(self,element):
        ids = element.ids
        if ids[0] ==-1:element.u = -self.U[ids[1],0]
        elif ids[1]:element.u = self.U[ids[0],0]
        else:element.u = self.U[ids[0],0] - self.U[ids[1],0]
        return element.u

class ElectricElement(object):
    '''电气元件类，主要有eType，id,ids,u,i,r等属性,eType:电气元件类型(Y,Eu,Ei),
    id(int):元件编号,ids(int,int):元件两端节点号,参考节点编号为-1,y(float):电阻(S),u(float):电压(V),i(float):电流(A)
    比如{"eType":'R', "id":0, "ids":(0,1), "r":1, "u":1, "i"=1}
    '''
    def __init__(self, eType,id,ids,y,u,i,s):
        if not isinstance(id,int) or not isinstance(ids,tuple) or not len(ids) == 2\
           or ids[0] == ids[1] or ids[0] < -1 or ids[1] < -1:
            raise TypeError('电气元件参数有误，id(int),ids(int,int)有误')
        '''eType:电气元件类型(R,Eu,Ei)'''
        self.eType = eType
        '''id(int):元件编号'''
        self.id = id
        '''ids(int,int):元件两端节点号，电流正方向从第一个节点流向第二个节点'''
        self.ids = ids
        '''y(float/complex):导纳(S)'''
        self.y = y
        '''u(float/complex):电压(V),当ids(0,1),元件为电压源，1节点电压高于0节点时,u>0'''
        self.u = u
        '''i(float/complex):电流(A),当ids(0,1),电流从0->1时,i>0'''
        self.i = i
        '''s(float/comlpex):功率(w)'''
        self.s = s
    @staticmethod
    def createDcY(id,ids,y):
        return ElectricElement(EType.Y,id,ids,y,0.0,0.0,0.0)
    @staticmethod 
    def createDcEu(id,ids,u):
        return ElectricElement(EType.Eu,id,ids,0.0,u,0.0,0.0)
    @staticmethod 
    def createDcEi(id,ids,i):
        return ElectricElement(EType.Ei,id,ids,0.0,0.0,i,0.0)
    
    @staticmethod
    def createAcY(id,ids,y):
        return ElectricElement(EType.Y,id,ids,y,complex(0.0,0.0),complex(0.0,0.0),complex(0.0,0.0))
    @staticmethod 
    def createAcEu(id,ids,u):
        return ElectricElement(EType.Eu,id,ids,complex(0.0,0.0),u,complex(0.0,0.0),complex(0.0,0.0))
    @staticmethod 
    def createAcEi(id,ids,i):
        return ElectricElement(EType.Ei,id,ids,complex(0.0,0.0),complex(0.0,0.0),i,complex(0.0,0.0))
    
    def __str__(self):
        return "ElectricElement(电气元件类)\"eType:{0}, id:{1}, ids:({2},{3}), r:{4}A, u:{5}V, i:{6}Ω,\
                  s:{7}w\"".format(self.eType,self.id,self.ids[0],self.ids[1],self.y,self.u,self.i,self.s)
    
@unique
class EType(Enum):
    Y = 0
    Eu = 1
    Ei = 2
    S = 3
