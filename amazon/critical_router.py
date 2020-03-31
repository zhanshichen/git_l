#思路： 将边转换成 字典，每个节点为索引，里面是所有的连通边。 去掉一个点后，检查是否连通，用深度优先搜索。

def isConnected(graph):
    trav = set()
    start = None
    for k in graph:
        start = k    #索引
        break
    
    def DFS(node):
        trav.add(node)  #加的是字典的索引 即已经遍历到的点
        
        for child in graph[node]:   #与这个点连接的所有点 
            if child not in trav:   #如果连接的点未遍历  ，那么就遍历
                DFS(child)
        return
    
    DFS(start)
    if len(trav)==len(graph):
        return True
    return False
    
                
def getGraph(nodeNum, edges):
    g = {}
    for n in range(nodeNum):
        g[n] = []
    
    for edg in edges:
        g[edg[0]].append(edg[1])
        g[edg[1]].append(edg[0])
    # print(type(g))

    
    return g  
def findCriticalNodes(nodeNum, edges):

    ans = []
    for n in range(nodeNum):
        g = getGraph(nodeNum, edges)   #g 是一个字典
        del g[n]   #去掉一个点
        for node in g:    #曲调相应的边
            if n in g[node]:
                g[node].remove(n)
     
        if(not isConnected(g)): #判断连通
            ans.append(n)
        
 
    return ans

print(findCriticalNodes(7, [[0,1], [0, 2], [1, 3], [2, 3], [2, 5], [5, 6], [3,4]]))
    