class TreeNode:
    def __init__(self, value):
        self.val = value
        self.children = []

class Solution:
    def MaxaverageSubtree(self,root):
        if not root or not root.children:     #树不存在或者只有一个结点
            return None
        self.res = [ float(0), 0 ]
        self.dfs(root)

    def dfs(self,root):    #返回当前结点的合与节点数量
        if not root.children:
            return [root.val, 1]
        
        tmp_sum = root.val
        tmp_num = 1
        for child in root.children:
            child_sum, child_num = self.dfs(child)
            tmp_num += child_num
            tmp_sum += child_sum
        
        if tmp_sum / tmp_num > self.res[0]:
            self.res = [ tmp_sum/tmp_num, root.val  ]
        
        return [tmp_sum,tmp_num]

#深度优先遍历   