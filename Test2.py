import copy
k_words = []
temp = [[0,1,2,3], [1,2,3,4], [1,2,3,4], [1,2,3,4]]
#for i in range(4):
#    for j in range(4):
#        temp[i][j] = k_words[j][i]

#for i in range(4):
#    for j in range(4):
#        #print(temp[i][j], end="  ")
#        print()
#    print("\n")


import copy
l = [1, 2, 3]

l2 = copy.deepcopy(l)
l2[0] = 789

print(l)

#key = input("Enter Key:")
#if len(key) < 16:
#    key = key + "0"*(16-len(key))
#print(key)


def inv_shift_row(text):
    temp = copy.deepcopy(text)
    for row in range(1, 4, 1):
        for i in range(4):
            text[row][i] = temp[row][(i - row) % 4]
    return text

def shift_row(text):
    temp = copy.deepcopy(text)
    for row in range(1, 4, 1):
        for i in range(4):
            text[row][i] = temp[row][(i + row) % 4]
    return text


#print(temp)
#print(inv_shift_row(temp))
#print(shift_row(temp))






























