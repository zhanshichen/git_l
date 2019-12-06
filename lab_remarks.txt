remove_space.py is used for removing space bwtween lines for original pre-trained word embeddings.
task_no_trans.py is the file using Chinese wordnet(wn-cmn-lmf.xml)
task_trans.py is the file using index in english-version wordnet, which means it translate corresponding english words in to Chinese words and use the same relationships(hypernym and hyponym). #we choose this method.
catcode_trans.txt is the file of the parent location code of a word-sense in the tree structure.
child_trans is the file of parent-children relations among word-senses.
w2v_2.txt is the file of pre-trained word embeddings.
wn-cmn-lmf.xml is Chinese wordnet.
