#个人版本，比较复杂，关键是动态规划,边界值的问题
def ispath(arr_path,rows,columns):
    num_path = [[1 for i in range(rows)] for j in range(columns) ]
    for i in range(1,rows):
        if arr_path[i][0] == 0:  #bu neng zou
            num_path[i][0] = 0
        else:
            num_path[i][0] = min(num_path[i][0], num_path[i-1][0])
                    
    for j in range(1,columns):
        if arr_path[0][j] == 0:
            num_path[0][j] = 0
        else:
            num_path[0][j] = min(num_path[0][j],num_path[0][j-1])
    
    for i in range(1,rows):
        for j in range(1,columns):
            if arr_path[i][j] == 1:
                num_path[i][j] = num_path[i][j-1] + num_path[i-1][j]
            elif arr_path[i][j] == 0:
                num_path[i][j] = 0
            else:
                return -1
    if num_path[rows-1][columns-1] > 0:
        return True
    else:
        return False
    
def maxPathScore(matrix):                            
    print(matrix)
    rows = len(matrix)
    max = 0
    # max = [len(i) if len(i)>max for i in matrix]
    for i in matrix:
        if len(i) > max:
            max = len(i)
    # print(max)
    columns = max
    arr_path = [[1 if matrix[i][j] else 0  for i in range(rows)] for j in range(columns) ]
    
    
    # matrix_del = matrix[:]
    while True:
        min = 999
        min_cor = None
        for i in range(rows):
            for j in range(columns):
                    if matrix[i][j] < min and [i,j] != [0,0] and [i,j] != [rows-1,columns-1]:   #bu jie shou liang duan de zui xiao zhi
                        min = matrix[i][j]
                        min_cor = [i,j]
        # if matrix[0][0] <= min or matrix[rows-1][columns-1] <=
        small_corner = matrix[0][0] if matrix[0][0] < matrix[rows-1][columns-1] else matrix[rows-1][columns-1]
        if small_corner <= min:
            return small_corner
        matrix[min_cor[0]][min_cor[1]] = 999
        print(min)
        arr_path[min_cor[0]][min_cor[1]] = 0
        ans = ispath(arr_path,rows,columns)
        
        if ans == False:   #no path 
            return min

a = [[1,5,3], [2,0,9],[4,5,1]]
ans = maxPathScore(a)
print("ans is ",ans)

#核心是动态规划  掌握这个算法

# 例子
# class Solution:
#     def sol(self, nums):
        
#         N = len(nums)
#         M = len(nums[0])

#         nums[0][0] = 1e9
#         nums[N - 1][M - 1] = 1e9

#         dp = [[1e9] * M for i in range(N)]

#         for j in range(1, M):
#             dp[0][j] = min(dp[0][j - 1], nums[0][j])
#         for i in range(1, N):
#             dp[i][0] = min(dp[i - 1][0], nums[i][0])

#关键是这里
#         for i in range(1, N):
#             for j in range(1, M):
#                 cur = max(dp[i - 1][j], dp[i][j - 1])
#                 dp[i][j] = min(cur, nums[i][j])
#         #print(dp)

#         print("ans: " + str(dp[N - 1][M - 1]))