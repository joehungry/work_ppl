from funcs import file, prints, splice, num, data
import os, datetime, subprocess

today = datetime.datetime.now()

pointsFile = file.content('REPORT/python_hidden_file', 'CT_LS.txt', lock=True)
persistent_data = {'continuous_time': 0, 'current_points': 0, 'new_words': 0, 'correct': 0, 'incorrect': 0, 'pages_finished': 0, 'recess_now': 0, 'last_study_time':0, 'today': None}
manage_persistent_data = data.manage(persistent_data, pointsFile)
subprocess.check_call(["attrib","+H", 'REPORT\python_hidden_file\CT_LS.txt'])
extracted_value = manage_persistent_data.extract_from_file()
originalPointNumber = float(extracted_value['current_points'])


whatToDo = {'can impliment new feature': 'CODING', 'don\'t have to do anything toddy': 'NOTHING_DAY'}
pointsDict = {'CODING': 100,  'NOTHING_DAY': 500}

def subtractPonts(totalPoints, pointsToSubtract):
    if totalPoints >= pointsToSubtract:
        totalPoints -= pointsToSubtract
        return totalPoints
    else:
        input('YOU DONT HAVE ENOUGH POINTS')
        return None
    
def secondsInMinute(MinuteAndSeconds):
    minute, second = splice.splice(MinuteAndSeconds, ':', 'str')
    if num.isNum(minute) == True and num.isNum(second) == True:
        return int(minute) + (int(second)/60)
    else:
        return False
    

while True:
    chooseSetting = None
    tempPointNumber = None
    os.system('cls')
    print('WELCOME USE POINTS TO HAVE FUN')
    print('YOU HAVE', originalPointNumber, 'POINTS')
    print()
    for lenI, i in enumerate(whatToDo):
        if not pointsDict[whatToDo[i]] == 0:
            usablePoints = originalPointNumber/pointsDict[whatToDo[i]]
        else:
            usablePoints = 0
        print(f'{lenI+1}. {i} ({pointsDict[whatToDo[i]]} points) -- can use {usablePoints}')
    print()
    try:
        chooseSetting = whatToDo[list(whatToDo)[int(input(">> "))-1]]
    except ValueError:
        chooseSetting = None
    else:
        usedPoints = pointsDict[chooseSetting]
        if not chooseSetting == 'FUCK_YOU' or chooseSetting == 'BADBAD':
            nameOfContent = prints.ask('WHAT ARE YOU GOING TO USE IT FOR?')
            timeOfContent = False
            while True:
                tempTimeOfContent = prints.ask('HOW LONG IS IT?')
                if ":" in tempTimeOfContent:
                    timeOfContent = secondsInMinute(tempTimeOfContent)
                elif num.isNum(tempTimeOfContent) == False:
                    timeOfContent = False
                else:
                    timeOfContent = tempTimeOfContent
                if not timeOfContent == False:
                    break
            pointsTimesTime = float(timeOfContent) * usedPoints
        else:
            pointsTimesTime = usedPoints
            nameOfContent = chooseSetting
        tempPointNumber = subtractPonts(originalPointNumber, pointsTimesTime)
    if not tempPointNumber == None:
        os.system('cls')
        print(f'YOU ARE ABOUT TO USE {pointsTimesTime} POINTS FOR {nameOfContent}')
        finalCheck = prints.ask('ARE YOU SURE? (y/n) or write "bug!" if there was a bug')
        while True:
            os.system('cls')
            if finalCheck.lower() == 'y':
                pointNumber = tempPointNumber
                input('thanks')
                break
            elif finalCheck.lower() == 'bug!':
                pointsTimesTime = pointsTimesTime/3
                input("I'm so sorry")
                pointNumber = subtractPonts(originalPointNumber, pointsTimesTime)
                pointsTimesTime = f'{pointsTimesTime} <= bug devided'
                break
            else:
                pass

        manage_persistent_data.change_value({'current_points': str(pointNumber)})
        manage_persistent_data.write_to_file()
    

        month = str(today.month)
        date = str(today.day)

        endingDash = '----------'

        onpeningString = f'{endingDash}\n\n'

        yearFile = file.content(f'REPORT/usedPoints/{str(today.year)}', f'Points used in {today.strftime('%m %Y')}.txt')
        savedContent = yearFile.fetch()
        dashLen = '-----'
        if len(month) == 2:
            dashLen += '-'
        if len(date) == 2:
            dashLen += '-'
        contentString = f'{month}月{date}日分のポイント消費{dashLen}'

        savingContentString = ''
        if savedContent == []:
            savingContentString += f'{contentString}\n'
        else:
            savedContent.pop(len(savedContent)-1)

        for i in savedContent:
            if contentString == i:
                savingContentString = ''
                break
            else:
                savingContentString = onpeningString + contentString + '\n'

        savingContentString += f'{today.strftime('%H:%M')} {nameOfContent}――{pointsTimesTime}pt\n{endingDash}'

        allFileContent = ''
        for i in savedContent:
            allFileContent += f'{i}\n'
        allFileContent += savingContentString

        yearFile.delete('*file*')
        yearFile.save(f'{allFileContent}', '*lock*')    