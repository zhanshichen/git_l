#this file constructs child and catcode file using index in english-version wordnet,
# translate corresponding english words in to Chinese words,using the same relationships(hypernym and hyponym).
# Because the vocabularies of pre-trained word embeddings and Chinese wordnet are different, 
# it is important to delete part of words in each vocabulary, making them identical. 
from bs4 import BeautifulSoup as bs
from nltk.corpus import wordnet as wn
soup = bs(open("/home/zhanshichen/Desktop/code/wn-cmn-lmf.xml"),"xml")
pa_child = {}
parent = {}
#Synset
tag = soup.LexicalEntry

#all Chinese words which appearing in w2v.vector(file of pre-trained word embeddings)
vector = []
with open("/home/zhanshichen/nball4tree/w2v.vector","r") as f:
    lines = f.readlines()     
    for line in lines:
        vec = line.split(" ")
        vector.append(vec[0])

# print(vector)
word_name = []  
#记录下wordnet中出现的所有名字（纯名字）  用来对vector文件进行裁剪


with open("/home/zhanshichen/child_trans.txt","w") as f:
    while not tag.name == "Synset":
        tag_sense = tag.Sense
        tag_id = tag_sense['synset']
        tag_name_o = tag.Lemma['writtenForm']  
        part = tag.Lemma['partOfSpeech']  
        i = 1
        number = str(i)
        
        #remove "+" from tag_name
        tag_name = tag_name_o.replace("+","")     
        
        #如果这个名字出现在vector中 才生成字典，否则根本不生成
        #只取一万个单词

        if (tag_name in vector) and (len(pa_child) < 10000):
        # if tag_name in vector :
            word_name.append(tag_name)
            pa_child[tag_id] = {}
            

            tag_total_name = tag_name + '.' + part + '.' + number
            pa_child[tag_id][tag_total_name] = []

            
            #如果一个单词有多个意思的话
            #if one word has more than one meanings
            while tag_sense.next_sibling.next_sibling:
                i = i + 1
                number = str(i)
                tag_sense = tag_sense.next_sibling.next_sibling
                tag_id = tag_sense['synset']
                pa_child[tag_id] = {}
                tag_total_name = tag_name + '.' + part + '.' + number
                pa_child[tag_id][tag_total_name] = []
        
        tag = tag.next_sibling.next_sibling
    

    #用转换英文单词的方式构造pa_child 和 parent
    #create pa_child and parent list (searching index in english-version wordnet and translating into corresponding Chinese words)
    for id in pa_child:  #每个存在中文的单词的id 寻找父节点与子节点
        b = id.split('-')
        english_id =  b[2] + b[3]
        #15028818n 格式

        #生成parent字典
        parent[id] = []
        for name in pa_child[id]:  #名字压进去
            parent[id].append(name)
            
        try:
            english_name = wn.of2ss(english_id)  #english_name 格式 ： Synset('isoagglutinin.n.01')
        except:
            continue  #这个节点的两个list均为空  发生某个中文id没有对应英文id的情况，但是中文id有对应的单词
        else:

            #先构造pa_child 字典
            children_names = english_name.hyponyms()
            if children_names:  #有子节点
                for child_name in children_names:
                    child_id = str(child_name.offset()).zfill(8) + '-' + child_name.pos()
                    chinese_child_id = 'cmn-10-' + child_id
                    if chinese_child_id in pa_child.keys():
                        for name in pa_child[id]:
                            pa_child[id][name].append(chinese_child_id)

            parent_names = english_name.hypernyms()  #上位词
            if parent_names:  #有父节点
                label = 0
                for parent_name in parent_names:


                    only_parent_name = parent_name  #只取第一个父节点作为父节点 
                    only_parent_id = str(only_parent_name.offset()).zfill(8) + '-' + only_parent_name.pos()
                    chinese_parent_id = 'cmn-10-' + only_parent_id
                    if (chinese_parent_id in pa_child.keys()) and (label == 0):  #父节点id有中文汉字对应
                        parent[id].append(chinese_parent_id)
                        label = 1
                    elif (chinese_parent_id in pa_child.keys()) and (label == 1) : 
                         #已经为当前节点分配了一个父节点，但是又出现一个新的父节点，需要把这个关系在父节点中去掉
                        for delete_parent_name in pa_child[chinese_parent_id]:
                            if id in pa_child[chinese_parent_id][delete_parent_name]:
                                pa_child[chinese_parent_id][delete_parent_name].remove(id)
                                print("after delete from ",delete_parent_name," ",id)
                                print("then",pa_child[chinese_parent_id][delete_parent_name])
                                # print("delete relation 1 \n")   
                                 
    
    
    #检查是否为树，去掉图的情况
    #check if each child-tree is a tree(not graph),in other words, its parent-node has been included in its children nodes 
    #深度优先遍历
    #depth-first traversal
    for id in parent:
        if len(parent[id]) == 1:  #每棵树的根节点
            parent_path = []
            # parent_path.append(id)   #存的是id，记住了！
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
    # half_wordname = []    #存删除过后所有的名字 , 一定量.n.1 的形式
    # count = 1
    #create root node
    for id in parent:
        if len(parent[id]) == 1 :#当前id没有父节点
                f.write(parent[id][0]+' ')   #写入
                # half_wordname.append(parent[id][0])
                parent[id].append("*root*")  #把root节点当做父节点
                # count = count + 1
    f.write('\n')    

    #写入文件 child.txt
    for pa_id in pa_child:
        for pa_name in pa_child[pa_id]:
            # if pa_name in half_wordname:    
            f.write(pa_name + ' ')
            for children_id in pa_child[pa_id][pa_name]:  
                if children_id in pa_child.keys():
                    for children_name in pa_child[children_id]:
                        # if children_name in half_wordname:   # 只有
                        f.write(children_name)
                        f.write(" ")
        f.write("\n")

# #重新生成parent数组,使得其只保留剩余的word
# for id in parent:
#     if parent[id][0] not in half_wordname:
#         parent.pop(id)

# #对parent的父亲节点也相应的删除
# for id in parent:
#     parent_id = parent[id][1]
#     if parent_id 

# half_wordname_2 = []  # 只有删除后的名字,用来对vector裁剪
# for wordname in half_wordname:
#     names = wordname.split(".")
#     half_wordname_2.append(names[0])
# print(half_wordname_2)

#重新生成vector文件 与wordnet相匹配
#recreate file of pre-trained word embeddings, in order to match the vocabulary in wordnet 
with open("/home/zhanshichen/nball4tree/w2v.vector","r") as f:
    with open("/home/zhanshichen/w2v_new_trans.txt","w") as f_w:    
        lines = f.readlines()
        for line in lines:
            vec = line.strip().split(" ")
            if vec[0] in word_name:
                for each_vector in vec:
                    f_w.write(each_vector + " ")
            f_w.write("\n")
            

#create catcode.txt
longest_dimension = 0
with open("/home/zhanshichen/catcode_trans.txt","w") as f:
    for id in parent:  #每个单词 
        # if parent[id][0] in half_wordname:  
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
            if len(position) == 5:  #deepest tree
                print("root node5:" + parent[node_id][0])

            
        position.append("1")
        dimension = len(position)
        if dimension > longest_dimension:
            longest_dimension = dimension

        level = 0 
        for po_number in position[::-1]:
            f.write(po_number + ' ')
            level = level + 1
        while level < 9:
            f.write("0" + " ")
            level = level + 1
        f.write("\n")

print ("longest dimension is "+ str(longest_dimension) + "\n")
# # 

# root node8:物质.n.2
# root node8:物体.n.1
# root node8:物体.n.1
# root node8:物质.n.2
# root node8:物体.n.1
# root node8:物体.n.1
# root node8:物体.n.1
# root node8:一定量.n.1
# root node8:一定量.n.1
# root node8:行动.v.4
# root node8:物体.n.1
# root node8:行动.v.4
# root node8:一定量.n.1
# root node8:物体.n.1
# root node8:物体.n.1
# longest dimension is 9


# after delete from  半导体.n.1   cmn-10-14654541-n
# then []
# after delete from  黏胶.n.1   cmn-10-14703566-n
# then []
# after delete from  高烧.n.1   cmn-10-14365619-n
# then []
# after delete from  保藏.n.1   cmn-10-13548531-n
# then ['cmn-10-13538314-n']
# root node5:移动.v.4
# root node5:转让.n.1
# root node5:地位.n.2
# root node5:有机体.n.1
# longest dimension is 6