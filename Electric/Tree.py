
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
