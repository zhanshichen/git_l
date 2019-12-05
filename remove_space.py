#this file is used for removing space bwtween lines
with open("/home/zhanshichen/w2v_new_trans.txt","r") as f_r:
    with open("/home/zhanshichen/w2v_2.txt","w") as f_w:
        for line in f_r.readlines():                                  
            data=line.strip()
            if len(data)!=0:
                f_w.write(data)
                f_w.write('\n')