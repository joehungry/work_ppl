from funcs import compare
test = '((nw and (c=10 or x=5)) or (nw=2 and c=10) and t=100)'

start_index = []
end_index = []
builder = []
nested_list = [0]
test_list = list(test)
while True:
    for ilen, i in enumerate(test_list):
        pass_element = False
        for istart, iend in zip(start_index, end_index):
            if compare.isSandwitchNum(ilen, istart, iend) == True:
                pass_element = True
                break
        if pass_element == True:
            pass
        elif i == '(':
            temp_start_index = ilen
            builder = []
        elif i == ')':
            built_string = ''.join(builder)
            #what if i join it and then put that joined element into the list
            end_index.append(ilen)
            start_index.append(temp_start_index)
            #nested_list[-1].append(built_string)
            print(built_string)
            break
        else:
            builder.append(i)
    #print(builder)
    #break

for i in range(10):
    if i == 9:
        i = 0
    print(i)