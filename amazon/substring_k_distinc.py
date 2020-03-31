#复杂版   关键是有很多情况， 元素只能一个一个进，一个一个出，每有一个出队都要检查一下。
def substring(string, size):
    if not string or size == 0: 
        return []
    count = 0
    queue = []
    ans = set()
    for i in range(len(string)):
       
        if count < size:
            if string[i] not in queue:
                queue.append(string[i])
                # print("loop1")
                count += 1
            else:  # 重复元素
                while queue:
                    if string[i] in queue:
                        # print("loop2")
                        queue.pop(0)
                        count -= 1
                    else:
                        # print("loop3")
                        queue.append(string[i])
                        count += 1
                        break
                if not queue:
                    # print("loop4")
                    queue.append(string[i])
                    count += 1
                
        else: #changdu=3
            b = ""
            for x in range(size):
                b = b + queue[x]
            ans.add(b)
            # print("ans now is ",ans)
            queue.pop(0)
            count -= 1
            # print(queue)
            # print("string i is:",string[i])
            if string[i] not in queue:
                queue.append(string[i])
                # print(queue)
                count += 1
            else:  # 重复元素
                while queue:
                    if string[i] in queue:
                        queue.pop(0)
                        # print("in loop,",queue)
                        count -= 1
                    else:
                        queue.append(string[i])
                        count += 1
                        break
                if not queue:
                    queue.append(string[i])
                    count += 1
    # print(queue)
    if len(queue) == size:
        b = ""
        for x in range(size):
            b = b + queue[x]
        ans.add(b)
    return list(ans)





s = "awaglknagawunagwkwagl"
k = 4
ans = substring(s,k)
print("ans is ",ans)

#大老版：
#直接用操作下标，不u需要新建一个队列
# def substringk(s, k):
#     if not s or k == 0:
#         return []
    
#     letter, res = {}, set()
#     start = 0
#     for i in range(len(s)):
#         if s[i] in letter and letter[s[i]] >= start:
#             start = letter[s[i]]+1
#         letter[s[i]] = i
#         if i-start+1 == k:
#             res.add(s[start:i+1])
#             start += 1
#     return list(res)
