def cheat_code():
    global ReadyCommand
    global ReadyContent
    global enter_break
    global ComIsTrue
    global ShowMain
    global FixMain
    global goal
    
    B = 0
    printed = False
    enter_break = None
    ComIsTrue = True
    reccommended_label = None
    ShowMain = 0
    showGoal = None
    FixMain = 0
    ShortCutComList = ["s", "n", "u"]#same, null, use
    
    os.system('cls')


            
    print()
    print("始めます [Enter]")
    print()
    
    if not count == count_one and label == None and last_study_tym == 1000001000100:
        print(">> label'" + str(last_study_tym))
        print()
        print(">> tim.length'forever")
        print()
    
    elif not count == count_one and  label == None:
        print(">> label'" + str(label_list[(len(label_list)-1)]))
        print()
        print(">> tim.length'" + str(last_study_tym))
        print()

    elif count == count_one and recess_now > 0:
        print(">> There is unused rest:", recess_now, "min")
        print()
            
    
                    

    def ShortCutCom(): 
        if ReadyContent == "":
            pass
        
        elif '\\' == ReadyContent[0]:
            ShortCutContent = ready[(ready.find("\\")) + 1:]
            for i in range(len(ShortCutComList)):
                if ShortCutComList[i] == ShortCutContent:
                    return ShortCutContent
        else:
            return None

    def ShortCutContent(MainVar, SubVar):
        try:
            if not SubVar == None:
                    MainVar = SubVar
            print()
            print(MainVar)
            return MainVar
            

        except:
            return None
        
    def goalContent():
        global goal
        global showGoal
        global ComIsTrue
        if ReadyContent == '\\n' or ReadyContent == 'n' or ReadyContent == 'none':
            goal = 0
            ComIsTrue = True
        elif not pastGoal == None and (ReadyContent == '\\s' or ReadyContent == 's' or ReadyContent == 'same'):
            goal = pastGoal
        else:
            goal, ComIsTrue = goalLanguage.breakdownGoalInput(ReadyContent, ComIsTrue)
        if goal == []:
            goal = None
            err_msg()
        elif goal == 0:
            showGoal = None
            print('no goal')
        elif not ComIsTrue == None:
            showGoal = ReadyContent
            print(f'goal is {showGoal}')
        else:
            goal = None



                

        



    ColCommand = {'p': 3, 'P': 3, 'D': 7, 'diary': 7, 'T': 8, 'time': 8,'tim.length': 8, 'L': 9, 'label': 9, 'TL': 10, 'LT': 10, 'MainScreen': 11, 'MS': 11, 'mainScreen':11, 'UI': 11, 'L+': 12, 'sound': 14, 'S': 14, 'mail': 15, 'email': 15}

    NoCommand = {'p': 3, 'P': 3, 'error': 4, 'exit': 5, '(*default)': 6}

    Command = {'show': 0, 'end': 1, 'use': 2, 'sound': 13, 'goal': 16, 'g': 16, 'G': 16}

    content = [ShowContent, EndContent, UseContent, PointContent, fillerContent, enter, fillerContent, CommentContent, TimeContent, LabelContent, TimeLabelContent, fillerContent, LabelAddContent, SoundContent, MainSoundContent, EmailContent, goalContent]
    #          0            1           2           3             4             5      6               7               8            9             10                11         12               13            14                15            16



        if ComIsTrue == None:
            err_msg()

        print()

        if enter_break == True and tim_out == False:
            break
