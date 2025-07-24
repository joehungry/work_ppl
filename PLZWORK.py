from funcs import file, splice, prints, data
import os, datetime, subprocess

perfectTimeToSleep = 1
twelveHourClock = None
if perfectTimeToSleep >= 12:
    twelveHourClock = f'{perfectTimeToSleep - 12} PM'
else:
    twelveHourClock = f'{perfectTimeToSleep} AM'

chooseTasks = {f'Went to sleep before {twelveHourClock}': 'sleepOnTime', 'wrote story': 'MeWriter', 'read a book': 'bookWorm', 'looked for job': 'jobHunter', 'Literally Finished Everything I need to do': 'everythingDone'}#これと下のやつ変更で自動的にタスク追加できるのでよろしくです
taskPoints = {'sleepOnTime': 35, 'MeWriter': 43, 'bookWorm': 25, 'jobHunter': 50, 'everythingDone': 245}

today = datetime.datetime.now()
todayFormatted = today.strftime('%Y/%m/%d')

yesterday = today - datetime.timedelta(days=1)
yesterdayFormatted = yesterday.strftime('%Y/%m/%d')

pointsFile = file.content('REPORT/python_hidden_file', 'CT_LS.txt')
persistent_data = {'continuous_time': 0, 'current_points': 0, 'new_words': 0, 'correct': 0, 'incorrect': 0, 'pages_finished': 0, 'recess_now': 0, 'last_study_time':0, 'today': None}
manage_persistent_data = data.manage(persistent_data, pointsFile)
subprocess.check_call(["attrib","+H", 'REPORT\python_hidden_file\CT_LS.txt'])
extracted_value = manage_persistent_data.extract_from_file()
originalPointNumber = float(extracted_value['current_points'])


taskStreakFile = file.content('REPORT/python_hidden_file', 'taskStreak.txt', lock=True)
taskStreakContent = taskStreakFile.fetch()

taskStreakDict = {}
taskDateDict = {}

if not taskStreakContent == []:
    for i in taskStreakContent:
        taskKey, streakValue = splice.splice(i, ':', 'str')
        if not taskKey == False:
            taskStreakDict[taskKey[:len(taskKey)-len(todayFormatted)]] = int(streakValue)
            taskDateDict[taskKey[:len(taskKey)-len(todayFormatted)]] = taskKey[len(taskKey)-len(todayFormatted):]

#これはなんか、上でファイルをロードするじゃん。
# で、そのロードしたファイルにchooseTasks内のタスクが入っていないとき、補填するやつ。
# たとえば、MeWriterのデータがセーブファイルに入ってないときに、勝手に値を１にしてくれるやつ。
#そもそもなんでこれがいるかっていうと、セーブデータは特定のデータをセーブしたときにしか反映されないのよ。
# たとえば、bookWormっていうデータをセーブしましたってときに、bookWormの値が+1上がるのですが、
# その瞬間にセーブされるのはbookwormの値だけなんです。
# だから、何にもノータッチで初めてセーブしますっていうときには、必ずないものを補填する必要があるんです。
taskFinishedList = []
for i in taskStreakDict:
    if taskDateDict[i] == todayFormatted:
        taskFinishedList.append(i)
    elif not taskDateDict[i] == yesterdayFormatted:
        taskStreakDict[i] = 1

for i in chooseTasks.values():
    if i not in taskStreakDict:
        taskStreakDict[i] = 1


def saveDictToFile(dictionary, fileVar):
    saveVar = ''
    for i in dictionary:
        saveVar += f'{i}:{dictionary[i]}\n'
    fileVar.save(saveVar)

while True:
    chooseSetting = None
    tempPointNumber = None
    os.system('cls')
    print('WELCOME USE POINTS TO HAVE FUN')
    print('YOU HAVE', originalPointNumber, 'POINTS')
    print()
    for lenI, i in enumerate(chooseTasks):
        print(f'{lenI+1}. {i} ({int(taskPoints[chooseTasks[i]]) + (int(taskStreakDict[chooseTasks[i]]) * 5)} points)')
    print()
    try:
        chooseSetting = chooseTasks[list(chooseTasks)[int(input(">> "))-1]]
    except ValueError:
        chooseSetting = None
    except IndexError:
        chooseSetting = None
    else:
        newPointNumber = taskPoints[chooseSetting] + (int(taskStreakDict[chooseSetting]) * 5)
        if not chooseSetting in taskFinishedList:
            originalPointNumber += newPointNumber
            taskFinishedList.append(chooseSetting)
            taskStreakSaveDict = {}
            taskStreakDict[chooseSetting] = int(taskStreakDict[chooseSetting]+1)
            for i in taskStreakDict:
                taskStreakSaveDict[f'{i}{todayFormatted}'] = str(int(taskStreakDict[i]))
            input('thx')
        else:
            prints.err('YOU ALREADY DID THIS TASK TODAY')
            prints.err('NO POINTS FOR YOU')
            taskStreakSaveDict = {}
            for i in taskStreakDict:
                taskStreakSaveDict[f'{i}{todayFormatted}'] = int(taskStreakDict[i])
            input()
        manage_persistent_data.change_value({'current_points': str(originalPointNumber)})
        manage_persistent_data.write_to_file()

        
        
        taskStreakFile.delete('*file*')
        saveDictToFile(taskStreakSaveDict, taskStreakFile)