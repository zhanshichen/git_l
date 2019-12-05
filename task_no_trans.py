from bs4 import BeautifulSoup as bs
soup = bs(open("/home/zhanshichen/Desktop/code/wn-cmn-lmf.xml"),"xml")
pa_child = {}
parent = {}
#Synset
tag = soup.LexicalEntry

#vector 中有的词汇
vector = []
with open("/home/zhanshichen/nball4tree/w2v.vector","r") as f:
    lines = f.readlines()
    for line in lines:
        vec = line.split(" ")
        vector.append(vec[0])

# print(vector)
word_name = []  #记录下wordnet中出现的所有名字（纯名字）

#生成在/nabll4tree/nabll4tree 下 别忘了
with open("child.txt","w") as f:
    while not tag.name == "Synset":
        tag_sense = tag.Sense
        tag_id = tag_sense['synset']
        tag_name_o = tag.Lemma['writtenForm']  
        part = tag.Lemma['partOfSpeech']  #partofspeech
        i = 1
        number = str(i)
        
        tag_name = tag_name_o.replace("+","")

        #如果这个名字出现在vector中 才生成字典，否则根本不生成 
        if tag_name in vector:
            word_name.append(tag_name)
            
            pa_child[tag_id] = {}
            
            tag_total_name = tag_name + '.' + part + '.' + number
            pa_child[tag_id][tag_total_name] = []

            
            #如果一个单词有多个意思的话
            while tag_sense.next_sibling.next_sibling:
                i = i + 1
                number = str(i)
                tag_sense = tag_sense.next_sibling.next_sibling
                tag_id = tag_sense['synset']
                pa_child[tag_id] = {}
                tag_total_name = tag_name + '.' + part + '.' + number
                pa_child[tag_id][tag_total_name] = []
        
        #跳入下一个tag
        tag = tag.next_sibling.next_sibling
    
    #处理节点关系  只关注hypo 子节点信息
    while tag:
        current_id = tag['id']
        
        tag_syn = tag.SynsetRelations.SynsetRelation
        only_parent = 0
        if current_id in pa_child.keys():  #对于不在pa_child 中的id（也就是说没有对应汉字的id）不考虑           
        #含有多个子节点的情况
            #无论有没有父节点 都生成 
            parent[current_id] = []
            for x in pa_child[current_id]:
                parent[current_id].append(x)

            while tag_syn:     
                if tag_syn['relType'] == 'hypo':   #子节点
                    child_id = tag_syn['targets']
                    for x in pa_child[current_id]:  #得到当前节点的名字
                        pa_child[current_id][x].append(child_id)
                elif tag_syn['relType'] == 'hype':  #父节点
                    if only_parent == 0:   #确定只有一个父节点
                        parent_id = tag_syn['targets']  
                        if parent_id in pa_child.keys():    #父节点的id真实存在（就是说有汉字对应）
                            parent[current_id].append(parent_id)
                            only_parent = 1

                tag_syn = tag_syn.next_sibling.next_sibling
            
        tag = tag.next_sibling.next_sibling
    
    
    #检查是否为树，去掉图的情况
    #深度优先遍历
    for id in parent:
        if len(parent[id]) == 1:  #每棵树的根节点
            parent_path = []
            parent_path.append(id)   #存的是id，记住了！
            for x in pa_child[id]:  #得到名字
                name = x
            node_id = id
           
            queue=[]
            queue.append(node_id)    #queue 中存的是id
            while queue:
                v = queue.pop()    #访问节点v
                parent_path.append(v) 
                for x in pa_child[v]:
                    name = x
                for children_id in reversed(pa_child[v][name]):   #先入右字数再入左字数
                    if children_id in pa_child.keys():
                        if children_id in parent_path:
                            pa_child[v][name].remove(children_id)
                            print("deleted 1 \n")
                        else:
                            queue.append(children_id)


    f.write("*root* ")
    #构造root节点
    for id in parent:
        if len(parent[id]) == 1:  #当前id没有父节点
            f.write(parent[id][0]+' ')   #写入
            parent[id].append("*root*")  #把root节点当做父节点
    f.write('\n')    

    #写入文件 child.txt
    for pa_id in pa_child:
        for pa_name in pa_child[pa_id]:
            f.write(pa_name + ' ')
            for children_id in pa_child[pa_id][pa_name]:  
                if children_id in pa_child.keys():
                    for children_name in pa_child[children_id]:
                        f.write(children_name)
                        f.write(" ")
        f.write("\n")
    
#重新生成vector文件 与wordnet相匹配
with open("/home/zhanshichen/nball4tree/w2v.vector","r") as f:
    with open("/home/zhanshichen/nball4tree/w2v_new.txt","w") as f_w:    
        lines = f.readlines()
        for line in lines:
            vec = line.strip().split(" ")
            if vec[0] in word_name:
                for each_vector in vec:
                    f_w.write(each_vector + " ")
            f_w.write("\n")


longest_dimension = 0
with open("catcode.txt","w") as f:
    for id in parent:  #每个单词 
        f.write(parent[id][0]+' ') #先写入单词名字  
        node_id = id
        position = []  #位置
        
        while not parent[node_id][1] == "*root*":  #当前节点还有父节点
            parent_id =  parent[node_id][1]
            number = 0
            for x in pa_child[parent_id]:
                for child_id in pa_child[parent_id][x]:
                    number = number + 1
                    if child_id == node_id:
                        position.append(str(number) + " ")
                        break
            node_id = parent_id  #当前节点等于父节点 向上查找
            if len(position) == 8:  #最深的树
                print("root node8:" + parent[node_id][0])

            
        position.append("1")
        dimension = len(position)
        if dimension > longest_dimension:
            longest_dimension = dimension

        level = 0 
        for po_number in position[::-1]:
            f.write(po_number + ' ')
            level = level + 1
        while level <= 17:
            f.write("0" + " ")
            level = level + 1
        f.write("\n")

print ("longest dimension is "+ str(longest_dimension) + "\n")
#longest dimension is 12

