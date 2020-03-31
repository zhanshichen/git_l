import re
quotes = [
"Elmo is the hottest of the season! Elmo will be on every kid's wishlist!",
"The new Elmo dolls are super high quality",
"Expect the Elsa dolls to be very popular this year, Elsa!",
"Elsa and Elmo are the toys I'll be buying for my kids, Elsa is good",
"For parents of older kids, look into buying them a drone",
"Warcraft is slowly rising in popularity ahead of the holiday season"
]
toys = ["elmo", "elsa", "legos", "drone", "tablet", "warcraft"]
N=3

toys_freq = { toy:[0,0] for toy in toys }
for quote in quotes:
    quote_toy = {toy:False for toy in toys}
    for word in quote.lower().split():
        
        word = re.sub('[^a-z]','',word)  #将没用的符号全去掉
        if word in toys_freq:
            toys_freq[word][0] += 1

            if quote_toy[word] is False:
                quote_toy[word] = True
                toys_freq[word][1] += 1
    
print(toys_freq.items())

result = [ w[0] for w in sorted(toys_freq.items(), key= lambda x : (x[1][0],x[1][1],x[0]) , reverse=True) [:N]   ]  #好强的代码能力   
# 这里(x[1][0],x[1][1],x[0])   表示排序的优先级，根据第一个排序，第一个如相同根据第二个在，，，
print(result)