"""
def __prepEu(self,eus):#预处理有理想电源的节点电压方程组参数
        if __findParallelEu(eus): raise PFCErr(PFCErrCode.HasParallelEu,'电路中含有并联理想电压源或者环接理想电压源')
        
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
        def geteus(eus):
            while(True):
                for e in eus:#查找并保存与以参考节点为节点理想电压源及其相连的理想电压源的的节点列表
                    if min(e.ids) == -1:#查找以参考节点为节点的理想电压源的理想电压源列表
                        node = max(e.ids)
                        unodes[-1] = {node:e.u}
                        eus.pop(eus.index(e))
                        funodes(node)
        unodes1 = list()#保存不以参考节点为节点的理想电压及其相邻节点
        for e in eus:#查找并保存剩余理想电压源节点及节点电压
            if not e.ids[0] in unodes.keys() and not e.ids[1] in unodes.keys():
                unodes[e.ids[1]] =e.u
                funodes(e.ids[1])
        def funodes(node):#查找与给定理想电压源相连的理想电压源列表
            for n in eus:
                if node in n.ids and\
                not ((n.ids[0] if n.ids[0] == node else n.ids[1])in unodes.keys()):
                    nd = {n.ids[1],n.u} if n.ids[0] == node else {n.ids[0],-e.u}
                    unodes.items.append(nd)
                    funodes(nd)
         

       

    def __findEarthEu(eus):
        #查找接地理想电压源及与之相连的理想电压源
        eus = eus[:]
        earthEus = [e for e in eus if -1 in e.ids]#直接接地的理想电压源列表
        isfind = earthEus[:]#已经查找过点元件列表

    def __findChildsU(eus,eu,nodeId,nodeU,nodesU):
        #在eus列表中查找与eu理想电源相连的其它理想电压源列表
        childs = [e for e in eus if e != eu and nodeId in e.ids]
    #    nodesU += {(c.ids[0] if c.ids[0] != nodeId) :(nodeU + (c.U if c.ids[0] == nodeId else -c.U),c)
    #        for c in childs}
        eus = [e for e in eus if e not in childs]
        for  i in childs:
            __findChildsU(eus)
"""
           