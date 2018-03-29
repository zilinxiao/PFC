# -*- coding: utf-8 -*-
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
        """函数功能：潮流计算，求解节点电压方程组
        求解电路节点电压方程组，求解时，需要进行迭代计算，
        直到满足迭代精度或者达到迭代次数才结束。
        包含两种电路类型，一种是不含理想电压源的常规电路；
        一种是包含理想电压源电路，这种需进行预处理。
        返回值：
        ------
        (self.U,self.Y,self.I)
        """
        num = 0;isFirst = True
        #理想电压源处理
        eus = [e for e in self.electricElements if e.eType == EType.Eu]#理想电压源列表
        
        """解节点电压方程组"""
        #保存原电路Y，I,U矩阵
        Y = self.Y[:,:]
        I = self.I[:,:]
        U = self.U[:,:]
        #包含理想电压源的电路的理想电压节点编号ids1及非理想电压源节点编号列表ids2
        ids1=[]
        ids2=[]
        while self.__iteration(isFirst) and num <= self.numOfIterations:
            if isFirst and len(eus) >0: #对包含电压源的电路进行预处理
                baseId,nodeUList =  self.__prepEu(eus)
                if baseId != -1:#对包含不是以-1为公共节点的电压源进行预处理
                    self.__changeBaseId(baseId)
                ids1,ids2 = self.__createEuYI(nodeUList)#处理包含理想电压源的节点电压方程组
                for n in nodeUList:#理想电压源节点的电压直接计算完毕
                    U[n[0]] = n[1]
            self.U = np.linalg.solve(self.Y,self.I)
            num += 1
            isFirst = False
        """求解节点电压方程组后，再把理想电压源结果填写到Y，U，I中"""
        if len(eus) >0:
            for id in ids2:
                U[id] = self.U[ids2.index(id)]
            self.U = U
            self.I = Y*U
            self.Y = Y
        return self.U,self.Y,self.I
    def __prepEu(self,eus):
        """
        函数功能：
        理想电压源的预处理程序，分为几种情况进行处理
        1、所有理想电压的一个节点均为参考节点-1，另一个节点均不一样，另一个节点电压为所
        在理想电压源电压，返回一个所有理想电压源对应节点的电压列表；
        2、所有理想电压源的一个节点未同一个节点n,另一个节点均不一样，则设节点n的电压为Un，
        另一个节点电压为Un+所在理想电压源电压，返回一个所有理想电压源对应节点的电压列表
        3、其它情况则以后实现，返回未实现异常。
        参数表：
        -----
        eus:理想电压源列表
        返回值:baseId,[(n1,u1),(n2,u2)...]
        ------
        baseId:理想电压源的公共节点
        [(n1,u1),(n2,u2)...]：理想电压源节点电压列表
        """
        if len(eus) == 1:           #只有一个理想电压源
            if -1 in eus[0].ids:
                return -1,[(eus[0].ids[1],eus[0].u) if eus[0].ids[0] == -1 else (eus[0].ids[0],-eus[0].u)]
            else:
                return eus[0].ids[0],[(eus[0].ids[1],eus[0].u)]
        #有两个以上的理想电压源
        #所有理想电压源均有一个共同的节点
        baseId = set(eus[0].ids) & set(eus[1].ids)
        if(len(baseId) == 1):
            bid = baseId.pop()
            if all([True if bid in e.ids else False for e in eus]):
                #第一种情况处理
                if -1 == bid:
                    return -1, [(e.ids[1],e.u) if e.ids[0] == -1 else (e.ids[0],-e.u) for e in eus]
                #第二种情况处理
                else:
                    n = eus[0].ids & eus[1].ids
                    return n, [(e.ids[1],e.u) if e.ids[0] == n else (e.ids[0],-e.u) for e in eus]
        raise NotImplementedError("""潮流计算程序实现了包含一个理想电压源的电路，
            以及多个理想电压源电路中所有理想电压源均只有一个公共节点，其它情况未实现""")
    def __changeBaseId(self,baseId):
        """函数功能
        处理包含公共节点不是-1的电压源预处理函数
        把电路各元件中的节点号为-1,baseId相互交换
        参数表：
        ------
        baseId:电压源的公共节点
        无返回值。
        """
        #找出节点号为-1的电路元件，并替把节点号-1替换为baseId
        baseIdelemets = [e for e in self.electricElements if -1 in e.ids]
        for i in range(len(baseIdelemets)):
            ids = baseIdelemets[i].ids
            if baseId not in  baseIdelemets[i].ids:
                baseIdelemets[i].ids = (baseId,ids[1]) if ids[0] == -1 else (ids[0],baseId)
            else:baseIdelemets.ids = (ids[1],ids[0])
        #找出节点号为baseId的电路元件，并替把节点号baseId替换为-1
        baseIdelemets = [e for e in self.electricElements if baseId in e.ids]
        for i in range(len(baseIdelemets)):
            ids = baseIdelemets[i].ids
            if -1 not in  baseIdelemets[i].ids:
                baseIdelemets[i].ids = (-1,ids[1]) if ids[0] == baseId else (ids[0],-1)
        self.createYIMatrix()
    def __createEuYI(self,nodeUList):
        """
        函数功能：处理包含理想电压源的线性方程组矩阵Y，I
        导纳矩阵Y中把理想电压源节点编号所在行，列去除，
        电流矩阵I中减去理想电压源节点电压*对应列的导纳
        eg.  YU=I,
        _                _ __   __       
        |Y11 Y12 Y13...Y1n||U1| |I1|      _            _ __  _       _
        |Y21 Y22 Y23...Y2n||U2| |I2|     |Y22 Y23...Y2n||U2| |I2-Y21U1|
        |...              |... =...  --->|...          |... =|...     |
        |Yn1 Yn2 Yn3...Ynn||Un| |In|     |Yn2 Yn3...Ynn||Un| |In-Yn1U1|
        _                _  __   __      _             _ __  _       _
        参数表：
        ------
        nodeUList:理想电压源节点电压列表[(nid1,u1),(nid2,u2)...]
        返回值：ids1,ids2,Y,I
        ------
        ids1: 理想电压源节点编号列表[id11,id12...]
        ids2: 剩下节点编号列表[id21,id22....]
        """
        nl = sorted(nodeUList, key=lambda x:x[0])
        for n in nl:
            self.I -= self.Y[:,n[0]]*n[1]
        ids1 = [n[0] for n in nl]
        ids2 = [n for n in np.arange(len(self.I)) if n not in ids1]
        self.Y = self.Y[:,ids2][ids2,:]
        self.I = self.I[ids2]
        return ids1,ids2

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
        return 'ElectricElement(电气元件类)\"eType:{0}, id:{1}, ids:({2},{3}), r:{4}A, u:{5}V, i:{6}Ω,s:{7}w"'\
    .format(self.eType,self.id,self.ids[0],self.ids[1],self.y,self.u,self.i,self.s)
    
@unique
class EType(Enum):
    Y = 0
    Eu = 1
    Ei = 2
    S = 3

class TreeNode(object):
    '''树节点类，每个节点可以有≥0个子节点'''
    def __init__(self,data,child = None):
        '''data:节点数据'''
        self.data = data
        self.childs = child
    def addChild(self,*data):
        self.childs = list()
        for d in data:
            self.childs.append(TreeNode(d))

class PFCErr(Exception):
    def __init__(self,errCode,msg):
        self.args = (errCode,msg)
        self.errCode = errCode
        self.msg = msg
@unique
class PFCErrCode(Enum):
    HasParallelEu = 0