import unittest
from PowerFlowCaculation import PFC, ElectricElement as ee, EType#,TreeNode as tn
import numpy as np

class PFCUnitTest(unittest.TestCase):
    '''PFC类单元测试'''
    def setUp(self):
        self.pfc = PFC()
        pfc = self.pfc
        element = ee(EType.Y,1,(0,1),101,32.003,103.45,0)
        pfc.addElement(element)
        self.assertEqual(pfc.electricElements[-1], element)
        elements = [ee.createDcEi(2,(0,2),102),ee.createDcEu(3,(0,3),103),
                    ee.createDcY(4,(0,4),104)]
        pfc.addElement(elements)
    def testaddelement(self):
        '''测试PFC.AddElement函数，添加一个元件'''
        pfc = self.pfc
        element1 =ee.createDcY(10,(2,3),10.44)
        pfc.addElement(element1)
        self.assertEqual(pfc.electricElements[-1], element1)

    def testaddelements(self):
        '''测试PFC.AddElement函数，添加一个元件'''
        pfc = self.pfc
        start = len(pfc.electricElements)
        elements = [ee.createDcEi(2,(0,2),102),ee.createDcEu(3,(0,3),103),
                    ee.createDcY(4,(0,4),104)]
        pfc.addElement(elements)
        self.assertEqual(pfc.electricElements[-1], elements[-1])
        self.assertEqual(pfc.electricElements[start:], elements)
        
    def test_Z_Caculate(self):
        try:
            pfc = PFC()
            elements = [ee.createDcEi(1,(0,-1),5),ee.createDcY(2,(0,1),1),
                ee.createDcY(3,(-1,1),1/2.0),ee.createDcY(4,(1,2),1/2.0),
                ee.createDcY(5,(2,-1),1/1.0),ee.createDcEi(6,(-1,2),1)]
            pfc.addElement(elements)
            pfc.createYIMatrix()
            pfc.caculate()
            #print(np.mat(pfc.Y)*np.mat(pfc.U))
            self.assertTrue(np.all(np.abs(pfc.Y*pfc.U - pfc.I <\
            np.mat(np.ones(pfc.I.shape))*1e-10)))
            self.assertTrue(np.all(pfc.U == np.array([-10.6,-5.6,-1.2]).reshape(3,1)))
            self.assertTrue(np.all(pfc.I == np.array([-5,0,1.0]).reshape(3,1)))
            self.assertTrue(np.all(pfc.Y == np.array([1.0,-1.0,0,-1.0,2.0,-0.5,0.0,-0.5,1.5]).reshape(3,3)))
            '''print(pfc.U)
            print(pfc.Y)
            print(pfc.I)'''
        except Exception as e:
            print(e)
    def test_Z_Caculate1(self):
        try:
            pfc = PFC()
            elements = [ee.createAcEi(1,(0,-1),complex(5)),ee.createAcY(2,(0,1),complex(1)),
                ee.createAcY(3,(-1,1),complex(1/2.0)),ee.createAcY(4,(1,2),complex(1/2.0)),
                ee.createAcY(5,(2,-1),complex(1/1.0)),ee.createAcEi(6,(-1,2),complex(1.0))]
            pfc.addElement(elements)
            pfc.createYIMatrix()
            pfc.caculate()
            self.assertTrue(np.all(np.abs(pfc.Y*pfc.U - pfc.I <\
            np.mat(np.ones(pfc.I.shape))*1e-10)))
            self.assertTrue(np.all(pfc.U==np.array([-10.6,-5.6,-1.2]).reshape(3,1)))
            self.assertTrue(np.all(pfc.I==np.array([-5,0,1.0]).reshape(3,1)))
            self.assertTrue(np.all(pfc.Y==np.array([1.0,-1.0,0,-1.0,2.0,-0.5,0.0,-0.5,1.5]).reshape(3,3)))
            '''print(pfc.U)
            print(pfc.Y)
            print(pfc.I)'''
        except Exception as e:
            print(e) 

    def test_S_Caculate(self):
        try:#测试含有功率源的解节点电压方程组
            pfc = PFC()
            elements = [ee.createDcEi(1,(0,-1),5),ee.createDcY(2,(0,1),1),
                ee.createDcY(3,(-1,1),1/2.0),ee.createDcY(4,(1,2),1/2.0),
                ee.createDcY(5,(2,-1),1/1.0),ee.createDcEi(6,(-1,2),1)]
            pfc.addElement(elements)
            pfc.createYIMatrix()
            pfc.caculate()
            #print(np.mat(pfc.Y)*np.mat(pfc.U))
            self.assertTrue(np.all(np.abs(pfc.Y*pfc.U - pfc.I <\
            np.mat(np.ones(pfc.I.shape))*1e-10)))
            self.assertTrue(np.all(pfc.U==np.array([-10.6,-5.6,-1.2]).reshape(3,1)))
            self.assertTrue(np.all(pfc.I==np.array([-5,0,1.0]).reshape(3,1)))
            self.assertTrue(np.all(pfc.Y==np.array([1.0,-1.0,0,-1.0,2.0,-0.5,0.0,-0.5,1.5]).reshape(3,3)))
            '''print(pfc.U)
            print(pfc.Y)
            print(pfc.I)'''
        except Exception as e:
            print(e)
    def test_preu_caculate(self):
        #测试解节点电压方程组的预处理程序，主要是测试是否有并联支路电压源
        try:
            pfc = PFC()
            elements = [ee.createDcY(0,(0,-1),1),ee.createDcEu(1,(0,1),2),
                ee.createDcEu(2,(-1,1),2),ee.createDcEu(3,(1,2),2),
                ee.createDcEu(4,(2,-1),2),ee.createDcY(5,(2,3),1),
                ee.createDcY(6,(3,-1),1),ee.createDcEu(7,(3,4),2),
                ee.createDcY(8,(4,-1),1),ee.createDcEu(9,(4,5),2),
                ee.createDcY(10,(5,-1),1),ee.createDcY(11,(5,6),1),
                ee.createDcY(12,(6,-1),1),ee.createDcEu(13,(6,7),1),
                ee.createDcEu(14,(-1,7),2)]
            pfc.addElement(elements)
            pfc.createYIMatrix()
            pfc.caculate()
            #self.assertTrue(False)
        except Exception as e:
           print("test_preu_caculate 引发异常："+ e.args[0])
        try:
            pfc = PFC()
            elements = [ee.createDcY(0,(0,-1),1),ee.createDcEu(1,(0,1),2),
                ee.createDcEu(2,(-1,1),2),ee.createDcEu(3,(1,2),2),
                ee.createDcEu(4,(2,-1),2),ee.createDcY(5,(2,3),1),
                ee.createDcY(6,(3,-1),1),ee.createDcEu(7,(3,4),2),
                ee.createDcY(8,(4,-1),1),ee.createDcEu(9,(4,5),2),
                ee.createDcY(10,(5,-1),1),ee.createDcY(11,(5,6),1),
                ee.createDcY(12,(6,-1),1),ee.createDcEu(13,(6,7),1),
                ee.createDcEu(14,(-1,7),2)]
            pfc.addElement(elements)
            pfc.createYIMatrix()
            pfc.caculate()
            #self.assertTrue(False)
        except Exception as e:
           print("test_preu_caculate 引发异常："+ e.args[0])
    def test_Eu_caculate(self):
        try:
            pfc = PFC()
            elements = [ee.createDcEu(1,(0,-1),-5),ee.createDcY(2,(0,1),1),
                ee.createDcY(3,(-1,1),1/2.0),ee.createDcY(4,(1,2),1/2.0),
                ee.createDcY(5,(2,-1),1/1.0),ee.createDcEu(6,(-1,2),1)]
            pfc.addElement(elements)
            pfc.createYIMatrix()
            pfc.caculate()
            #print(np.mat(pfc.Y)*np.mat(pfc.U))
            self.assertTrue(np.all(np.abs(pfc.Y*pfc.U - pfc.I <\
            np.mat(np.ones(pfc.I.shape))*1e-10)))
            self.assertTrue(np.all(pfc.U == np.array([5,2.75,1]).reshape(3,1)))
            self.assertTrue(np.all(pfc.I == np.array([2.25,0,0.125]).reshape(3,1)))
            self.assertTrue(np.all(pfc.Y == np.array([1.0,-1.0,0,-1.0,2.0,-0.5,0.0,-0.5,1.5]).reshape(3,3)))
            '''print(pfc.U)
            print(pfc.Y)
            print(pfc.I)'''
        except Exception as e:
            print(e)

    def testTree(self):
        elements = [ee.createDcY(0,(0,-1),1),ee.createDcEu(1,(0,1),2),
            ee.createDcEu(2,(1,-1),-2),ee.createDcEu(3,(1,2),2),
            ee.createDcEu(4,(2,-1),2),ee.createDcY(5,(2,3),1),
            ee.createDcY(6,(3,-1),1),ee.createDcEu(7,(3,4),2),
            ee.createDcY(8,(4,-1),1),ee.createDcEu(9,(4,5),2),
            ee.createDcY(10,(5,-1),1),ee.createDcY(11,(5,6),1),
            ee.createDcY(12,(6,-1),1),ee.createDcEu(13,(6,7),1),
            ee.createDcEu(14,(-1,7),2)]
        s = {(min(e.ids),max(e.ids)) for e in elements}
        '''
        print(s)
        if len(s) == len(elements):
            print(True)
        else:
            print(False)
            return
        '''
        eus = filter(lambda e:e.eType == EType.Eu and min(e.ids) == -1,elements)
        eus1 = filter(lambda e:e.eType == EType.Eu and min(e.ids) != -1,elements)
        '''for e in eus:
            print(e)
        print("")
        for e in eus1:
            print(e)
        print("")
        '''
        def f(e):
            if e.ids[0] > e.ids[1]:
                if e.eType == EType.Eu:
                    e.u = -e.u
                elif e.eType == EType.Ei:
                    e.i = -e.i
                e.ids= e.ids[1],e.ids[0]
            return e
        elements =  map(f,elements)
        elements = sorted(elements, key = lambda e:(max(e.ids),min(e.ids)))
        #for e in elements:
        #    print(e)

    def testTree1(self):
        elements = [ee.createAcY(0,(0,-1),complex(1)),ee.createAcEu(1,(0,1),complex(2)),
            ee.createAcEu(2,(1,-1),complex(-2)),ee.createAcEu(3,(1,2),complex(2)),
            ee.createAcEu(4,(2,-1),complex(2)),ee.createAcY(5,(2,3),complex(1)),
            ee.createAcY(6,(3,-1),complex(1)),ee.createAcEu(7,(3,4),complex(2)),
            ee.createAcY(8,(4,-1),complex(1)),ee.createAcEu(9,(4,5),complex(2)),
            ee.createAcY(10,(5,-1),complex(1)),ee.createAcY(11,(5,6),complex(1)),
            ee.createAcY(12,(6,-1),complex(1)),ee.createAcEu(13,(6,7),complex(2)),
            ee.createAcEu(14,(-1,7),complex(2))]
        def f(e):
            if e.ids[0] > e.ids[1]:
                if e.eType == EType.Eu:
                    e.u = -e.u
                elif e.eType == EType.Ei:
                    e.i = -e.i
                e.ids= e.ids[1],e.ids[0]
            return e
        elements =  map(f,elements)
        elements = sorted(elements, key = lambda e:(max(e.ids),min(e.ids)))
        '''for e in elements:
            print(e)
        '''
    def testprepeu(self):
         elements = [ee.createDcY(0,(0,-1),1),ee.createDcEu(1,(0,1),2),
            ee.createDcEu(2,(1,-1),-2),ee.createDcEu(3,(1,2),2),
            ee.createDcEu(4,(2,-1),2),ee.createDcY(5,(2,3),1),
            ee.createDcY(6,(3,-1),1),ee.createDcEu(7,(3,4),2),
            ee.createDcY(8,(4,-1),1),ee.createDcEu(9,(4,5),2),
            ee.createDcY(10,(5,-1),1),ee.createDcY(11,(5,6),1),
            ee.createDcY(12,(6,-1),1),ee.createDcEu(13,(6,7),1),
            ee.createDcEu(14,(-1,7),2)]
'''        eus = [e for e in elements if e.eType == EType.Eu]
        def findParallelEu(eus):
            eus = eus[:]
            for e in eus:
                findeus()
            def findeus(eus):
                isfindeus = list()
                def next():
'''                 
class ElectricElementUnitTest(unittest.TestCase):
    def testcreate(self):
        e1 = ee(EType.Y,1,(0,1),10,0,0,0)
        e2 = ee.createDcY(2,(0,2),2.456)
        e3 = ee.createDcEu(3,(0,3),55.5)
        e4 = ee.createDcEi(4,(0,5),304)
        e5 = ee.createAcY(5,(0,5),complex(10,10))

        '''print(e1)
        print(e2)
        print(e3)
        print(e4)
        print(e5)
        '''
if __name__ == '__main__':
    unittest.main()
