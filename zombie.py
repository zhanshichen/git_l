
def humanDays(matrix):                            
    rows = len(matrix)
    colomns = len(matrix[0])
    print(matrix)
    print(rows)
    print(colomns)
    time = 0
    human = []
    tmp = 0
    if not rows or not colomns:
        return 0
    for i in matrix:
        if 1 in i:
            tmp = 1
    # print(tmp)        
    if tmp == 0:
        return -1;  #no zombie
    human = [ [i,j] for i in range(rows) for j in range(colomns) if matrix[i][j] == 0 ]
  
    # print(human[])
    directions = [ [1,0], [-1,0], [0,1], [0,-1] ]
    # human_today = []
    human_today = human.copy()
    while True:
       
        for survived in human:

            for d in directions:
                
                # print(human)
                ni, nj = survived[0] + d[0], survived[1] + d[1]
                if (0<= ni < rows) and (0<= nj < colomns) :   
                    # print(ni)
                    # print(nj)
                    if [ni,nj] not in human:
                        # print(survived)
                        # print(human)
                        human_today.remove(survived)
                        # print(human)
                        break
        # print(a)
        # print(human_today)
        # print(human)
        # a += 1
        if human == human_today:  #no killing
            # print("here")
            # return time
            break
        else: 
            # print("2222")
            time += 1
            human = human_today[:]
    return time   
a = [[1,0]]
day = humanDays(a)

print("day is : ", day)

