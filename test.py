from funcs import file

test = file.content('', 'test.txt')
test.save('😭', encoding='shift-jis')