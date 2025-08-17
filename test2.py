dicttesst = {1: {'test': 'var', "good": "lord"}, 2: {"no": "bitches", "fo": "real"}, None: 0}

test_list = [3, 4]

for i, i2 in zip(dicttesst, test_list):
    [print(f'{ikey}: {ivalue}') for ikey, ivalue in dicttesst[i].items() if not ikey == None]
    print(i2)