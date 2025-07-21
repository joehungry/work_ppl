#ver.2.2.4
import math, datetime, stat, glob, time, win32api, msvcrt, os, pygame.mixer, subprocess
from time import sleep
from datetime import timedelta
from os import system
from time import sleep
from funcs import sendEmail, goalLanguage, goalEvaluator, goalProgress, prints


print("\033[8m")
print("\033[0m")
os.system('cls')

main_debugger = 1

#making visible files and stuff I think
#import and export data
#music data stuff
#rest timer
#main ui
#results ui
#completely background stuff
#stuff for the main program
#command screen stuff

print("loading.")

loading_count = 0

Title = "Workman"

def Loading_Screen():
            global loading_count
            os.system('cls')
            loading_count += 1
            print("loading", end = '')
            for i in range(loading_count):
                print(".", end = '')
            print(".")

system("title " + Title)

CannotClick = True

TimeToCheck = 15 * 60

TimedTime = 10 * 60

cntinuous_tim = None

tim_out = False



try:
    RED = '\033[31m'
    END = '\033[0m'

    pstpn = 1
    stdy_tym = None
    add_point = None
    div_point = 0.7
    div_givup_rst = 0.1

    count = 0
    recess = 0
    FixMain = 0
    correct = 0
    the_time = 0
    givup_rst = 0
    incorrect = 0
    new_words = 0
    totl_point = 0
    last_point = 0
    repeat_right = 0
    last_session = 0
    LastCorrect = 0
    LastIncorrect = 0
    pages_finished = 0
    last_count = 0
    there_was_error = 1
    all_minus_point = 0
    minute = 0
    past_count = 0
    cntinuous_tim = 0
    recess_time = 0
    started_time = 0
    recess_now = 0
    last_session_show = 0
    givup_rst = 0
    recess_before = 0
    pages_finished_first = 0
    volume = 0.5
    goal = None
    one_finish = 0
    right = 0
    wrong = 0
    new = 0
    pastGoal = None
    bonusPointPercentage = 0
    repeat_one_finish = 0
    repeat_wrong = 0
    repeat_new = 0
    pointString = ''
    time_list = []
    label_list = []
    time_now = []
    time_before = []
    comment_list = []
    totl_tim_point = 0



    frst_rest = 0
    point = None
    second = None
    no_error = None
    tim_point = None
    reset_time = None
    label = None
    comment = None
    last_study_tym = None
    comment_OK = False
    file_missing = False
    diary_tim = None
    ShowMain = True
    StdyMusicUsed = None
    RstMusicUsed = None
    useMusic = None
    MainMusic = True
    isMusicUsed = None
    turnEmailOn = True


    
###################################making visible files and stuff I think########################################################################################################################################

    def auto_create(var):
        if not os.path.exists(var):
            os.makedirs(var)
            file_missing = True

    def create_file_path():
        newpath = [r'Python Report', r'Python Report\Music', r'Python Report\python_hidden_file', r'Python Report\Diary', r'Python Report\StudyContent', r'Python Report\StudyPoint']
                        
        for i in newpath:
            auto_create(i)
            if newpath.index(i) > 3:
                auto_create(i + '\\' + str(now_start.year))
                auto_create(i+ '\\' + fileDirSort)
                
        subprocess.check_call(["attrib","+H","Python Report\python_hidden_file"])

    def print_list():
        create_file_path()
        list_num = len(time_list) - len(time_now)-1
        list_num_date = -1
        a_read_good = 0
        
        
        open_file(printContent)
        
        with open(printContent, 'a') as a:
            a.write('\n')
            if file_missing == True:
                    a.write("File was not found. Error was corrected")
                    
            a.write("_______________________________________")
            if not len(time_now) > 0:
                    a.write('\n')
                    a.write('\n')
            else:
                for i in range(len(time_now)):
                    list_num +=1
                    list_num_date += 1
                    a.write('\n')
                    a.write(str(int(list_num +1)))
                    a.write("回目 ")
                    a.write('「')
                    a.write(str(label_list[list_num]))
                    a.write("」　ー　")
                    a.write(str(time_list[list_num]))
                    a.write("分")
                    a.write('\n')
                    a.write(str(time_before[list_num_date]))
                    a.write(" - ")
                    a.write(str(time_now[list_num_date]))
                    if add_point == 0:
                            a.write(" *no point*")
                    a.write('\n')
                    a.write('\n')
            a.write('ended program:')
            time_right_now(time_now)
            a.write(str(time_now[(len(time_now) - 1)]))
            a.write('\n')
            a.write("---------------------------------------")
            uneditable(printContent)
                
        hidden_file()

    def end_print():
        print_list()
        now_end = (datetime.datetime.today())
        now_time_end = str(now_end.time())[:8]
        ended_time = now_time_end
        done_hour_count(cntinuous_tim - start_cntinuous_tim)
        open_file(printPoint)
        with open(printPoint, 'a') as b:
            b.write('\n')
            b.write("---------------------------------------")
            b.write('\n')
            b.write(str(done_hr))
            b.write("時間 ")
            b.write(str(done_min))
            b.write("分 ")
            b.write(str(done_sec))
            b.write("秒")
            b.write('\n')
            done_hour_count(cntinuous_tim)
            b.write("（合計：")
            b.write(str(done_hr))
            b.write("時間 ")
            b.write(str(done_min))
            b.write("分 ")
            b.write(str(done_sec))
            b.write("秒）")
            b.write('\n')
            b.write('\n')
            b.write("ポイント：")
            b.write(str(last_session_show - start_last_session))
            b.write('\n')
            b.write("（ポイントの合計：")
            b.write(str(last_session_show))
            b.write("）")
            b.write('\n')
            b.write("---------------------------------------")
            b.write('\n')
            b.write('ended : ')
            b.write(ended_time)
            uneditable(printPoint)

        hidden_file_log()

    def diary():
        if not comment == None:
            #auto_create( str(now_start.year))
            auto_create('Python Report\Diary/' + fileDirSort)
            open_file(printDiary)
            with open(printDiary, 'a') as b:
                b.write('\n')
                b.write(str(diary_tim))
                b.write("　【")
                b.write("")
                b.write(str(label_list[len(label_list)-1]))
                b.write("】")
                b.write('\n')
                b.write('--------------------------------------------------------------------------------------')
                b.write('\n')
                try:
                    b.write(str(comment))
                except ValueError:
                    for i in comment:
                        try:
                            b.write(str(i))
                        except ValueError:
                            b.write('(?)')
                b.write('\n')
                b.write('\n')
                b.write('\n')
                uneditable(printDiary)
            diary_tim == None
    
    def the_program_started():
        #used 1
        read_good = 0
        Loading_Screen()
        def creating_text_file(file, indecator, num, subst):
            read_good = 0
            create_file_path()
            
            with open(file, 'r') as a:
                Loading_Screen()
                if indecator in a.read():
                    read_good = 1
                                
                if read_good == 1:
                    for i in range(num):
                        subst.write('\n')
                        
                uneditable(file)
        
        open_file(printContent)
        l = open(printContent, 'a')
        a_read_good = creating_text_file(printContent, 'started', 2, l)
        l.write('\n')
        l.write("started program:")
        l.write(started_time)
        uneditable(printContent)
        l.close()

        open_file(printPoint)
        l = open(printPoint, 'a')
        b_read_good = creating_text_file(printPoint, 'started : ', 3, l)
        if read_good == 1:
                l.write('\n')
        l.write('__________________________________________________________________________________')
        l.write('\n')
        l.write('\n')
        l.write("started : ")
        l.write(started_time)
        uneditable(printPoint)
        l.close()

            
    def hidden_file_log():
        #used 3
        def ultimate_procastination(file, var):
            create_hidden_files(file)
                    
            try:
                proc_list_num = -1
                with open(file, 'w') as e:
                    for i in range(len(time_list)):
                        proc_list_num +=1
                        try:
                            e.write(str(var[proc_list_num]))
                        except UnicodeEncodeError:
                            e.write('Unusable character')
                        e.write('\n')
                    e.write(today)
                            
                    subprocess.check_call(["attrib","+H", file])
                    uneditable(file)
            except PermissionError:
                pass
                
            Loading_Screen()
                
        if not len(time_list) > 0:
            pass
        else:
            ultimate_procastination('Python Report\python_hidden_file\LL_log.txt', label_list)
            ultimate_procastination('Python Report\python_hidden_file\TL_log.txt', time_list)

    def uneditable(editing_file):
        os.chmod(editing_file, stat.S_IRUSR)

    def open_file(file):
        try:
            os.chmod(file, stat.S_IWUSR)

        except FileNotFoundError:
            pass

    def create_hidden_files(file):
        create_file_path()
        open_file(file)
        try:
            os.remove(file)
        except FileNotFoundError:
                pass



#########################################import and export data#################################################################################################################################################

    def hdnFlFunc(placeholder, var):
        placeholder.write(str(var))
        placeholder.write('\n')
        #why = input(var)
            
    def hidden_file():
        try:
            create_hidden_files('Python Report\python_hidden_file\CT_LS.txt')
            with open('Python Report\python_hidden_file\CT_LS.txt', 'w') as e:
                hdnFlFunc(e, cntinuous_tim)
                hdnFlFunc(e, last_session_show)
                hdnFlFunc(e, new_words)
                hdnFlFunc(e, correct)
                hdnFlFunc(e, incorrect)
                hdnFlFunc(e, pages_finished)
                hdnFlFunc(e, recess_now)
                hdnFlFunc(e, last_study_tym)
                e.write(today)
                        
                subprocess.check_call(["attrib","+H", 'Python Report\python_hidden_file\CT_LS.txt'])
                uneditable('Python Report\python_hidden_file\CT_LS.txt')
                        
        except PermissionError:
            input('Unable to write to file')

    def settingsFile():
        try:
            create_hidden_files('Python Report\python_hidden_file\Settings.txt')
            with open('Python Report\python_hidden_file\Settings.txt', 'w') as e:
                hdnFlFunc(e, volume)
                hdnFlFunc(e, StdyMusicUsed)
                hdnFlFunc(e, RstMusicUsed)

                subprocess.check_call(["attrib","+H", 'Python Report\python_hidden_file\Settings.txt'])
                uneditable('Python Report\python_hidden_file\Settings.txt')
                        
        except PermissionError:
            pass

            
    def extract_data():
        #used 1
        global last_session
        global cntinuous_tim
        global new_words
        global correct
        global incorrect
        global recess_now
        global time_list
        global label_list
        global count_one
        global last_study_tym
        global pages_finished_first
        global StdyMusicUsed
        global RstMusicUsed
        global volume

        count_one = 0
        settingsReturned = []
        right_this_now = datetime.datetime.now()
        yesterday = right_this_now - timedelta(1)
        yesterday = str(yesterday)[:10]
        
        def same_start(file):
            try:
            
                with open(file, 'r') as o:
                    file_lines = (o.readlines())
                    if str(today) in file_lines[len(file_lines)-1]:
                        return file_lines
            except:
                pass

            Loading_Screen()


        def convert_file(var, list1):
            list_raw = list(var)
            for i in range(len(list_raw)):
                list1.append(list_raw[i].strip())
            del list1[len(list1)-1]

        def readFile(file, new_file):
            for i in file:
                q = i.strip()
                try:
                    q = float(q)
                    
                    if q.is_integer() == True:
                        q = int(q)
                except:
                    pass
                if q == "None":
                    q = None
                new_file.append(q)

                

        lines_returned = same_start('Python Report\python_hidden_file\CT_LS.txt')
        if not lines_returned == None:
                lines_returned_Clean = []
                
                readFile(lines_returned, lines_returned_Clean)
                cntinuous_tim = lines_returned_Clean[0]
                last_session = lines_returned_Clean[1]
                new_words = lines_returned_Clean[2]
                correct = lines_returned_Clean[3]
                incorrect = lines_returned_Clean[4]
                pages_finished = lines_returned_Clean[5]
                recess_now = lines_returned_Clean[6]
                if recess_now == None:
                        recess_now = 0
                last_study_tym = lines_returned_Clean[7]
                #don't forget to make it global
                
                yesterday = lines_returned_Clean[len(lines_returned_Clean)-1]
        else:
                try:
                                with open('Python Report\python_hidden_file\CT_LS.txt', 'r') as o:
                                        lines_returned = (o.readlines())
                except:
                        pass
                else:
                        lines_returned_Clean = []
                        readFile(lines_returned, lines_returned_Clean)
                        last_session = lines_returned_Clean[1]


        try:
                with open('Python Report\python_hidden_file\Settings.txt', 'r') as o:
                        file_settings = (o.readlines())
                        readFile(file_settings, settingsReturned)
                        volume = settingsReturned[0]
                        StdyMusicUsed = settingsReturned[1]
                        RstMusicUsed = settingsReturned[2]
        except:
                pass
                
        open_file(printContent)
        open_file(printPoint)
        open_file(printDiary)

        lines_returned = same_start('Python Report\python_hidden_file\LL_log.txt')
        if not lines_returned == None:
                convert_file(lines_returned, label_list)

        lines_returned = same_start('Python Report\python_hidden_file\TL_log.txt')
        if not lines_returned == None:
                convert_file(lines_returned, time_list)
                count_one = len(time_list)




#######################################music data stuff##########################################################################################################################################################



    musicList = []
    
    music_folder = './Python Report\Music/'
    
    def MusicImport():
            global RstMusicUsed
            global StdyMusicUsed
            global musicList
            stdymusicThereStart = []
            rstmusicThereStart = []

            def ChooseMusicUI(var, string, var2):
                loopCounting = 0
                if var == None or len(var2) == 0:
                        while True:
                                os.system('cls')
                                print('\033[1m' + str(string) + '\033[0m')
                                print()
                                if loopCounting >= 1:
                                    err_msg()
                                    print()
                                print('It seems that there are more than two songs in the "Music" folder')
                                print()
                                print(">> Which song do you want to use :")
                                print()
                                loopCounting += 1
                                var = ChooseMusic()
                                if not var == False:
                                    return var

                else:
                    return var
                
            musicThereStart = []

            for name in glob.glob(music_folder + '*.wav'):
                    musicList.append(name)

            for name in glob.glob(music_folder + '*.mp3'):
                        musicList.append(name)
                        
                        
            if StdyMusicUsed == None:
                pass
            elif not StdyMusicUsed == False:
                stdymusicThereStart = glob.glob(StdyMusicUsed, recursive=True)


            if RstMusicUsed == None:
                pass
            elif not RstMusicUsed == False:
                rstmusicThereStart = glob.glob(RstMusicUsed, recursive=True)

            if not len(stdymusicThereStart) == 0 and not len(rstmusicThereStart) == 0 or len(musicList) == 0:
                    pass

            elif len(musicList) == 1:
                    StdyMusicUsed = musicList[0][2:]
                    RstMusicUsed = musicList[0][2:]

            else:
                StdyMusicUsed = ChooseMusicUI(StdyMusicUsed, "For Ending Study", stdymusicThereStart)
                RstMusicUsed = ChooseMusicUI(RstMusicUsed, "For Ending Rest", rstmusicThereStart)

                    
    def ChooseMusic():
        
        for i in musicList:
                print(str(musicList.index(i) + 1) + "." + i[len(music_folder):])
        print(str(len(musicList) + 1) + "." + "None")

        print()
        whichSong = input(">> ")
        try:
            
            whichSong = int(whichSong)

        except:
            return False
        
        if whichSong == len(musicList) + 1:
                return None
        
        elif whichSong > len(musicList) or whichSong <= 0:
                return False
                            
        else:
                return musicList[whichSong-1][2:]
            

    def song_start(var):
            global isMusicUsed
            global useMusic
            global music
            global vol

            musicThere = ""
            
            if not var == False:
                    try:
                            musicThere = glob.glob(var, recursive=True)
                    except:
                            pass

            if var == False or len(musicThere) == 0 or MainMusic == False:
                    isMusicUsed = False
                    useMusic = 0

            else:
                    useMusic = 1
                    isMusicUsed = True
                    pygame.init()
                    pygame.mixer.init()
                    music = pygame.mixer.Sound(var)
                    music.set_volume(volume)
                    vol = music.get_volume()

            

########################################rest timer###############################################################################################################################################################


                    
    def ShowCal_rest_time(time, which):
            WtchIsIt = which
            recess_sec, recess_min = math.modf(time)
            recess_sec = recess_sec * 60
            recess_sec = int(recess_sec)
            recess_min = int(recess_min)
            
            if WtchIsIt == "show":
                print()
                print("最大休憩時間は", recess_min, "分", recess_sec, "秒")

            elif WtchIsIt == "cal":
                return recess_min, recess_sec


    #休み等のタイマー
    def rest(rst_tym):
            global the_rest_time
            global givup_rst
            global last_session_show
            global recess
            global useMusic

            broken = 0
            start_count = False
            sleep(0.1)
            var_amount()
            rest_start_time = time.time()
            rest_reset_time = time.time()

            restMinNow, restSecNow = ShowCal_rest_time(rst_tym, "cal")
            
            def rest_strt_scrn(color):
                    print()
                    print('\033[0m' + "ポイント：", (last_session_show + givup_rst * div_givup_rst))
                    print()
                    print()
                    print('休みが終わったら"' + color + 'end' + END + '"キー')
                    print()
                    if rest_time_left >= 0:
                            print(rest_minute, "分", rest_second, "秒")

                    elif rest_time_left > the_rest_time:
                        print(rest_minute, "分", rest_second, "秒")
                    else:
                            print("0 分 0 秒")
                    print()
                    ShowCal_rest_time(rst_tym, "show")
                    print()

                    
            def K3():
                    global last_session_show
                    global time_now
                    global time_before
                    global useMusic
                    
                    if not the_rest_time >= rst_tym * 60:
                            pass

                    elif the_rest_time >= (rst_tym + pstpn) * 60 and (last_session_show * maxDeletionPercentage) - minus_point > 0:
                            pass

                    elif the_rest_time >= (rst_tym + pstpn) * 60 and (last_session_show * maxDeletionPercentage) - minus_point <= 0:
                            time_right_now(time_before)
                            print_list()
                            time_now = []
                            last_session_show = last_session_show * maxDeletionPercentage
                            hidden_file()
                            exit()

            def noScreenK3(color):
                    print()
                    print('\033[0m' + "ポイント：", (last_session_show + givup_rst * div_givup_rst))
                    print()
                    print()
                    print('休みが終わったら"' + color + 'end' + END + '"キー')



            song_start(RstMusicUsed)
            noScreen = 0
            doneREST = 0
            clearedScreen = 0
            emailSent = False
            emailLabel = '【WORKPPL】REST HAS ENDED NOTIFICATION'
            emailBody = f'休憩の{rst_tym}分が終了しました\n勉強を再開してください'

            studyEndedEmail = sendEmail.EmailSender(emailLabel, emailBody)

            while True:
                    the_rest_time = time.time()-rest_start_time
                    rest_time_left = rst_tym * 60 - the_rest_time + 1
                    
                    rest_minute = math.floor(rest_time_left/60)
                    rest_second = math.floor(rest_time_left) - rest_minute * 60
                    if noScreen == 0:
                            rest_strt_scrn("\033[1m")
                    elif clearedScreen == 0:
                            os.system('cls')
                            noScreenK3("\033[1m")
                            clearedScreen= 1
                    maxDeletionPercentage = 0.45
                    minus_point = ((time.time()-rest_reset_time) - ((rst_tym + pstpn) * 60)) * (last_session_show / 60)
                    K3()

                    if not the_rest_time >= rst_tym * 60:
                            pass

                    elif the_rest_time >= (rst_tym + pstpn) * 60 and (last_session_show * maxDeletionPercentage) - minus_point > 0:
                            print(minus_point, 'ポイント引かれます')

                    elif the_rest_time >= (rst_tym + pstpn) * 60 and (last_session_show * maxDeletionPercentage) - minus_point <= 0:
                            pass
                    
                    elif turnEmailOn == True and emailSent == False:
                        emailSent = True
                        studyEndedEmail.sendEmail()
                    
                    elif doneREST == 1 and noScreen == 1:
                            pass

                    elif useMusic == 1 and noScreen == 1:
                            doneREST = 1
                            os.system('cls')
                            noScreenK3("\033[1m")
                            print(0, 'ポイント引かれます')
                            music.play()
                            useMusic = 0
                    elif noScreen == 1:
                            doneREST = 1
                            os.system('cls')
                            noScreenK3("\033[1m")
                            print(0, 'ポイント引かれます')
                    elif useMusic == 1:
                            print(f'{(last_session_show * maxDeletionPercentage) - minus_point=}')
                            print(0, 'ポイント引かれます')
                            music.play()
                            useMusic = 0
                    else:
                            print(0, 'ポイント引かれます')



                    sleep(0.02)
                    noScreenEnter = win32api.GetKeyState(0x2E)
                    if noScreenEnter < 0:
                            clearedScreen = 0
                            noScreen = 1
                    stop = win32api.GetKeyState(0x23)
                    if stop < 0:
                            print("\033[8m")
                            os.system('cls')
                            clear_input_buffer()
                            while True:
                                    if noScreen == 0:
                                            rest_strt_scrn(END)
                                    else:
                                            noScreenK3(END)
                                    rest_done = input("[Enter / - (key) 押す]")
                                    sleep(0.14)

                                    if rest_done == '' or rest_done == 'y' or rest_done == "+":
                                            the_rest_time = time.time()-rest_start_time
                                            sleep(0.15)
                                            K3()
                                            broken = 1
                                            break

                                    elif rest_done == "-" or rest_done == "n":
                                            clearedScreen = 0
                                            noScreen = 0
                                            sleep(0.1)
                                            break

                                    elif rest_done == "'" or rest_done == "%" or rest_done == "/" or rest_done == "&":
                                            K3()
                                            if minus_point > last_session_show:
                                                    minus_point = last_session_show

                                            elif minus_point > 0.4:
                                                    minus_point += minus_point
                                                    
                                            cheat_code()
                                            
                                    else:
                                            exception_error()

                    if broken ==1:
                            os.system('cls')
                            if isMusicUsed == True:
                                    music.stop()
                                    
                            if minus_point > 0:
                                    return minus_point
                            return None
                    if noScreen == 0:
                            os.system('cls')


                    
#########################################main ui################################################################################################################################################################

                    

    def main_screen():
        global bonusPointPercentage
        
        print(END)
        fuckingdict = {'one_finish': repeat_one_finish, 'right': repeat_right, 'wrong': repeat_wrong, 'new': repeat_new} #this is here because it doesn't work if i directly put it in the variable wtf why
        temp, progressDict = goalEvaluator.evaluate_goal(goal, fuckingdict)
        print(f'{count}回目( {label}-{stdy_tym}分 )')
        timePercentage = the_time/(stdy_tym*60)
        showPercentage = int(timePercentage * 100)
        if timePercentage < .5:
            bonusPointPercentage = 1.4
            encouragementWord = 'まだまだ頑張れー(ง •̀_•́)ง'
        elif timePercentage >= .5 and timePercentage < .8:
            bonusPointPercentage = 3.2
            encouragementWord = 'その調子‼(； ･`ω･´)'
        elif timePercentage >= .8 and timePercentage < 1.3:
            bonusPointPercentage = 4.8
            encouragementWord = 'よくがんばったネ(๑˃̵ᴗ˂̵)و'
        elif timePercentage >= 1.3:
            bonusPointPercentage = 1
            encouragementWord = 'もう終わったよ( ´･ω･`) '

        percentageStr = f'目標時間の{showPercentage}%が終了 ({bonusPointPercentage}倍ボーナス)\n{encouragementWord}'
        prints.progress(int(goalProgress.get_goal_progress(goal, {'one_finish': repeat_one_finish, 'right': repeat_right, 'wrong': repeat_wrong, 'new': repeat_new})))
        print()
        if not goal == 0:
            print('~~~~~~~')
            print(percentageStr)
            print('~~~~~~~')
            print()
        print()
        print('一章終わったら"0"', end='')
        if not goal == 0:
            print(f' ({progressDict['one_finish']['current']}/{progressDict['one_finish']['required']})')
        print()
        print('\033[34m' + '正答' + END + 'は"4"', end='')
        if not goal == 0:
            print(f' ({progressDict['right']['current']}/{progressDict['right']['required']})')
        print()
        print('\033[34m' + '不正答' + END +'は"5"')
        if not goal == 0:
            print(f' ({progressDict['wrong']['current']}/{progressDict['right']['required']})')
        print()
        print('\033[34m' + '新規' + END + 'は"6"')
        if not goal == 0:
            print(f' ({progressDict['new']['current']}/{progressDict['right']['required']})')
        print()
        print()
        print('勉強が終わったら "' + '\033[1m' + 'END' + END + '"キー')
        print()
        print()
        print(f'{minute} min {second} sec')
        print()
        if not add_point == 0:
            print(f'{((new_point + tim_point) * div_point * 100)} points')
        else:
            print(f'{int(point)} points')
            



    def no_main_screen():
        global MINpassedPrint
        global printNoMain
        if printNoMain == True:
            temp, progressDict = goalEvaluator.evaluate_goal(goal, {'one_finish': repeat_one_finish, 'right': repeat_right, 'wrong': repeat_wrong, 'new': repeat_new})
            
            os.system('cls')
            print(END)
            print(f'{count}回目( {label} )')
            prints.progress(int(goalProgress.get_goal_progress(goal, {'one_finish': repeat_one_finish, 'right': repeat_right, 'wrong': repeat_wrong, 'new': repeat_new})))
            print()
            print()
            print(f'{pages_finished - pages_finished_first}/{progressDict['one_finish']['required']}章終わり')
            print()
            print(f'正答：{correct - LastCorrect}/{progressDict['right']['required']}個')
            print()
            print(f'不正答：{incorrect - LastIncorrect}/{progressDict['wrong']['required']}個')
            print()
            print(f'新規：{repeat_new}/{progressDict['new']['required']}個')
            if minute < stdy_tym: #Ln257
                pass
                
            print("\033[8m")
            printNoMain = False
            MINpassedPrint = False

            

#########################################results ui#############################################################################################################################################################

            

    def done_hour():
        print()
        done_hour_count(cntinuous_tim)
        print(str(done_hr) + "時間：" + str(done_min) + "分", str(done_sec) + "秒")

    #終了時のスクリーン
    def end_scrn():
        global last_session_show
        global last_session
        global totl_point
        global givup_rst
        global recess
        global the_time
    
        print()
        print(count,"回目")
        print()
        if last_session_show >= float(last_session):
            print("今回のポイント：", last_session_show - float(last_session))
        else:
            print("今回のポイント： 0")
        print(f'({pointString})')

        print()
        print("前回までのポイント：", last_session)
        print()
        if recess_now == None or recess_now == 0:
            print("合計：", last_session_show, "points")
                
        else:
            print("合計", last_session_show + ((recess_before - recess_now) * div_givup_rst), "points")
                
        print()

        recess = float(recess)

        if recess > 0 and recess_now == None:
            print('休み:', recess, "min")

        elif recess <= 0:
            
            print('休み:', 0, "min")
            recess = 0

        elif recess_now >= 0:
            print('休み:', recess_now, "min")

        else:
            print('休み: ' + RED + 'error' + END + ' min')
                
        print()
            

    def done_study():
        global last_session
        global CannotClick
        
        CannotClick == True
        os.system('cls')
        diary()
        if recess >= 0:
                last_session += recess * div_givup_rst
                
        var_amount()
        settingsFile()
        end_print()
        os.system('cls')
        
        todayRaw = datetime.datetime.today()
        todayShow = todayRaw.strftime('%Y年%#m月%#d')

        while True:
            print("\033[0m" + f'{todayShow}日の最終スコアは：')
            done_hour()
            print()
            print()
            print("ポイントの合計：", last_session_show)
            print()
        
            if correct > 0 or new_words > 0:
                print()
                print("新しく覚えた単語：" + str(int(new_words)) + "個")
                print("正答した問題：" + str(int(correct)) + "個")
                print("不正答の問題：" + str(int(incorrect)) + "個")
                print()
                print()
                
            if pages_finished > 0:
                print("終わった章：" + str(int(pages_finished)) + "章")
                print()
                    
            print()
            
            show_list()
            ok = input("\033[8m")
            os.system('cls')

                    

#########################################completely background stuff############################################################################################################################################

    def clear_input_buffer():
        while msvcrt.kbhit():
            msvcrt.getch()

    def done_hour_count(which_CNT):
            global done_hr
            global done_min
            global done_sec
            
            done_hr = math.floor(which_CNT / 3600)
            done_min = math.floor((which_CNT - (done_hr* 3600)) / 60)
            done_sec = int(which_CNT - (done_min * 60) - (done_hr * 3600))
                    
    def cal_pnt():
            global second
            global the_time
            global minute
            global totl_point
            global point
            global tim_point
            global stdy_tym
            global add_point
            global cntinuous_tim
            global last_count
            global past_count
            global until_next_count
            global new_point
            global totl_tim_point
            

            the_time = round(time.time()-reset_time)
            
            second = the_time - minute * 60
            minute = math.floor(the_time/60)
            #Changes were made so that even if unforseen elements cause the program to not calculate the amount, rebooting(?) the program will achive the same result as calculating it real-time
            if the_time > past_count:
                    the_countdown_time = the_time
                    
                    #I'm no sure but i think tim_point resets when getting to a milestone(i think) thats why there is this new_point thing, which probably keeps track on how much i got each milestone or something IDK
                    while the_countdown_time > until_next_count:
                            the_countdown_time -= until_next_count

                            new_point += (until_next_count * add_point / 1500) * ((math.ceil(past_count/1500) - 1) +  last_count)
                            until_next_count = 1500
                            past_count += 1500

                    else:
                            pass
                    
            tim_point = (((time.time()- (reset_time + (past_count - until_next_count))) * add_point / 1500) * ((math.ceil(past_count/1500) - 1) +  last_count))
            #(reset_time + (past_count - until_next_count)) is a variable which essentially resets the timer whenever the point added increases
            #((math.ceil(past_count/1500) - 1) +  last_count) is the past "count" variable, but calculated using math, rather than increassing the amount every time the point addded will increase
            
            
            totl_tim_point = new_point + tim_point

    def var_amount(): # this calculates the points and time you are able to study iguess
            global recess
            global totl_point
            global last_session_show
            global repeat_new
            global bonusPointPercentage
            global pointString
            global totl_tim_point

            CalTim = the_time / 60
            JustInTimeDiv = 1

            if last_study_tym == None: #this if/elif statement is calcutlating how much you diviated from the intended study time to fincd out how much to devide from the recess time
                pass
            
            elif last_study_tym > CalTim + 5:
                JustInTimeDiv = CalTim/last_study_tym
                
            elif last_study_tym < CalTim - 5:
                JustInTimeDiv = last_study_tym/CalTim

            goalCompletedPercentage = goalProgress.get_goal_progress(goal, {'one_finish': repeat_one_finish, 'right': repeat_right, 'wrong': repeat_wrong, 'new': repeat_new})
            
            totl_tim_point_divided = totl_tim_point * div_point
            pointString = f'{totl_tim_point_divided} points earned from time'

            if goal == 0:
                totl_point = totl_tim_point_divided * JustInTimeDiv
                if JustInTimeDiv != 1:
                    pointString += f' multiplied by {JustInTimeDiv} because you went over or under time'
            elif int(goalCompletedPercentage) == 100:
                totl_point = totl_tim_point_divided * bonusPointPercentage
                if bonusPointPercentage == 1:
                    pointString += f', nothing else because you went over time'
                else:
                    pointString += f' multiplied by {bonusPointPercentage}'
            else:
                totl_point = totl_tim_point_divided * (goalCompletedPercentage/100)
                pointString += f' multiplied by {goalCompletedPercentage/100} because you didn\'t complete goal' 
            
            last_session_show =  totl_point + float(last_session)
            oldRest = 5 * (((last_session_show ** 0.5) +1)/2) + (((recess_time - 1500) /60 * 2 / 10) * abs((last_session_show ** 0.5)-1))
            newRest = 5 * (((last_session_show ** 0.5) +1)/2) + (((recess_time - 1500) /60 * 2 / 10) * abs(((((cntinuous_tim/1500)*((cntinuous_tim/1500)))/2) ** 0.5)-1))
            if oldRest > newRest:
                    recess = newRest
            else:
                    recess = oldRest
            #recess の計算式について：めちゃ分かりづらいので、ここで解説します。
            #「5」という最初の数字は、ポモドーロメソッドでの一番基本の休憩時間だから。
            # つまりこれが基本で、次からがおまけということ
            #まずは現在のポイントの平方根(last_session_show ** 0.5)を求めています。
            # これはなんか増加を緩やかにするため？ってGPTさんが言ってた。
            # で、それに1を足したものを2で割ります（なぜかは知らない）。
            #次に勉強時間の調整でする。
            # 勉強時間（recess_time)を1500（25分）で割った数（ポモドーロメソッドの一番基本の勉強時間だから）を
            # 分数に直して（/60）いい分からん調整をします（ * 2 / 10）
            #こっからは二手に分かれます。一つはoldRest, もう一つはnewRest。
            # なぜ二つあるかというと、休憩時間へのポイントシステムの依存を少なくしたかったけど、
            # 結局勉強時間が少ないと、休憩時間減るから渋々残してる感じ。
            #まずはoldRest。これは、現在のポイントに今回の勉強時間を掛けることで、
            # 連続でこんなに勉強してたんだね、なら長く勉強してた分もっと休憩ほしいよねヨシヨシってこと。
            # 絶対値（abs）なのはなんでだろ。なんかとにかくマイナスの値になるって思ってたし実際なったんじゃないかな。
            # だけどポイントを一日経ってもリセットしないように機能変更した結果、
            # 機能が意味のないものに変わったので、newRestを作成
            #newRestは、その日連続の勉強時間した時間をポイントに変える式にするとこんな感じになるはず......
            # と思ってこのよう分からん式になりました！！　多分正しくないけど、正しく動作する限りは使い続けます。
            

#########################################stuff for the main program#############################################################################################################################################



    def time_right_now(variable):
            now = (datetime.datetime.today())
            now_time = str(now.time())[:8]
            variable.append(now_time)

    
    def err_msg():
            print(RED + "error" + END)
            

#error()では見つからなかったErrorがあった場合に文章をprintします
    def exception_error():
            os.system('cls')
            print()
            print(RED + "入力エラーがあります" + END)

    def keypres(amount, what):
            global point

            variable = what + 1
                
            point = point + amount
            print(f'+{amount}')
            sleep(0.1)
            return variable
            

    #質問をし答えをVariableに記録します
    def CheckAnswer(question):
            global no_error
            print()
            print(question)
            print()
            answer = input(">> ")
            if answer == '':
                    os.system('cls')
                    no_error = False
                    print()
                    print(RED + "何か入力してください" + END)
            else:
                    try:
                            answer = float(answer)
                            no_error = True
                            return answer
                
                    except:
                            no_error = False
                            return answer


    def ReturnRest(rest_var, recess):

        def AutoRest():
            #どうやらrecess_timeは休憩時間を計算しているわけでなくて、前セッションの勉強時間を計算しているようです。だから、この式は、勉強時間(recess_time)を1500秒(25分)だと仮定したときに、最低5分の休憩を取ることができるように設定されているみたい？
            if (recess_time / 60) * 0.2 < recess:
                return (recess_time / 60) * 0.2
                    

            else:
                return recess
                    
        RestCom = {'all': recess, 'none': 0, 'auto': "auto"}
                
        try:
            if "givup'" in rest_var:
                return (recess - float(rest_var[(rest_var.find("'"))+1:]))
        except:
            pass

        try:
            rest_var = float(rest_var)
            if not rest_var > recess:
                return rest_var
            

        except:
            rest_var = CompCommand(RestCom, rest_var)
                                    
            if rest_var == "auto":
                var = AutoRest()
                return var
            
            elif not rest_var == None:
                return rest_var

            

#########################################command screen stuff###################################################################################################################################################


    def CompCommand(command_typ, comp_var):
        CommandList = list(command_typ.keys())
    
        for i in range(len(command_typ)):
                if CommandList[i] == comp_var:
                    return command_typ[comp_var]


    def show_list():
                        
                                
        list_num = -1
        if not len(time_list) > 0:
                print(None)
                print()

        else:
            def longestLength(a):
                max1 = len(str(a)[0])
                temp = a[0]
            
                # for loop to traverse the list
                for i in a:
                    if(len(str(i)) > max1):
                        max1 = len(str(i))
                        temp = i
                return temp
            
                            
            def LengthOfTheDotThing(writing):
                global length_thing
                print(writing + writing + writing + writing + writing + writing + writing + writing + writing + writing + writing + writing + writing, end = '')
                for i in range(len(str(length_of_count))):
                        print(writing, end = '')
                        
                for i in range(len(str(length_of_str))):
                        print(writing + writing, end = '')

                for i in range(len(str(length_of_str_2))):
                        print(writing, end = '')


            length_of_str = longestLength(label_list)
            length_of_str_2 = longestLength(time_list)

            length_of_count = time_list.index(length_of_str_2)
            

            LengthOfTheDotThing("_")
            print("_")

            for i in range(len(time_list)):
                list_num +=1
                print()
                print(str(list_num +1) + "回目(" + str(label_list[list_num]) + "):" + str(time_list[list_num]) + "分", end = '')
                print()

            LengthOfTheDotThing("_")
            print("_")

    def err_chk(varCont):
        global ready
        global no_error
        if varCont == "":
                err_msg()
                return None
        
                
        try:
                varCont = float(varCont)
                no_error = True
                return varCont
                                
        except:
                no_error = False
                return varCont
    


    def cheat_code():
        global ReadyCommand
        global ReadyContent
        global enter_break
        global ComIsTrue
        global CannotClick
        global ShowMain
        global FixMain
        global goal
        
        B = 0
        printed = False
        enter_break = None
        ComIsTrue = True
        reccommended_label = None
        ShowMain = True
        showGoal = None
        FixMain = 0
        ShortCutComList = ["s", "n", "u"]#same, null, use
        
        os.system('cls')


        def stndard_err_scrn():
            global B
            if B == 0 or no_error == False:
                    print(RED + "error" + END)
            else:
                    return B

        def enter():
            global enter_break
            enter_break = True
                
            def Missing_Component(string):
                global enter_break
                print(RED + "Please " + string + END)
                enter_break = False
                                            
            if stdy_tym == None:
                Missing_Component("Specify Time Length")

            if label == None:
                Missing_Component("Add Label to Session")

            if add_point == None:
                Missing_Component("Specify Point System")
            if goal == None:
                Missing_Component("Specify Goal")

                        

        def OnOffSCRN(answer, ModelAnswerFalse, string):
                        if answer == ModelAnswerFalse:
                            OffOnString = "off"
                        else:
                            OffOnString = "on"
                            
                        print(string + OffOnString)

                
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
                
        def ShowContent():
                def ShowPointContent():
                        NewLinePrint(last_session_show)

                def ShowRstTymContent():
                        if count == count_one:
                            ShowCal_rest_time(frst_rest, "show")

                        else:
                            ShowCal_rest_time(recess_now, "show")

                def showGoalContent():
                    print(showGoal)
                
                ShowCommand = {"study time": 0, "list": 1, "study list": 1, "point": 2, "points": 2, "rest time": 3, 'goal': 4}
                ShowContentList = [done_hour, show_list, ShowPointContent, ShowRstTymContent, showGoalContent]

                ExecuteContent(ShowCommand, ShowContentList)

        def EndContent():
                EndCommand = {"study": 0}
                EndContentList = [done_study]
                #if not count == count_one:
                ExecuteContent(EndCommand, EndContentList)
                #else:
                #    err_msg()

        def UseLabelContent():
                global label
                if not reccommended_label == None:
                        label = reccommended_label
                        NewLinePrint(label)

                else:
                        err_msg()

        def NewLinePrint(message):
                        print()
                        print(message)

        def UseContent():
                
                def UseRestContent():
                        global frst_rest
                        global recess_now
                        
                        if recess_now >= 0 and count == count_one:
                            frst_rest = recess_now
                            recess_now = 0
                            hidden_file()
                            NewLinePrint("unused rest is safely pending usage")

                        else:
                            err_msg()

                UseCommand = {'unused rest': 0, 'rest': 0, 'reccomended label': 1, 'label': 1}
                UseContentList = [UseRestContent, UseLabelContent]

                ExecuteContent(UseCommand, UseContentList)


        def SoundContent():
                global ComIsTrue
                global ReadyContent
                global ReadyCommand
                def soundVolmeContent():
                    global volume
                    global ComIsTrue
                    
                    FindContent(ReadyContent, ": ",1)
                    volume = ReadyContent
                    volume = err_chk(volume)
                    if no_error == True:
                        volume = int(volume) / 100
                        ComIsTrue = volume
                    else:
                        err_msg()

                def SoundContentChoose():
                    global StdyMusicUsed
                    global RstMusicUsed
                    global ComIsTrue
                    
                    def SoundContentChooseContent():
                        var = ChooseMusic()
                        if var == False:
                            err_msg()
                            
                        else:
                            return var
                            
                    SondContentChooseDict = {"study": 0, "rest": 1}
                    ComIsTrue = CompCommand(SondContentChooseDict, ReadyContent)
                    if ComIsTrue == None:
                        pass
                    
                    elif ComIsTrue == 0:
                        StdyMusicUsed = SoundContentChooseContent()
                        
                    elif ComIsTrue == 1:
                        RstMusicUsed = SoundContentChooseContent()
                        
                    
                soundCommand = {'change': 0, 'volume': 1}
                soundContentList = [SoundContentChoose, soundVolmeContent]


                FindContent(ReadyContent, ":",1)
                ReadyContent = ReadyContent.strip()
                ReadyCommand = ReadyCommand.strip()
                
                ComIsTrue = CompCommand(soundCommand, ReadyCommand)
                ExecuteCom(ComIsTrue, soundContentList)

                
                        
        def PointContent():
                global ComIsTrue
                global add_point
                        
                PointCommand = {'on': 1, 'off': 0, 'no': 0, 'none': 0}
            
                if ReadyCommand == None:
                        add_point = 1
                        OnOffSCRN(add_point, 0, "point system is ")
                
                else:
                        ComIsTrue = CompCommand(PointCommand, ReadyContent)
                        if not ComIsTrue == None:
                                add_point = ComIsTrue
                                OnOffSCRN(add_point, 0, "point system is ")

        def MainSType():
                global ShowMain
                global ComIsTrue
                global FixMain
                        
                PointCommand = {'on': True, 'off': False, 'no': False, 'none': False, 'fix': 'fixed_' + str(ShowMain), 'unfix': ShowMain}
                ComIsTrue = CompCommand(PointCommand, ReadyContent)
                FindContent(str(ComIsTrue), "_", 1)
                if ComIsTrue == None:
                    pass
                
                elif ReadyCommand == 'fixed':
                    FixMain = 1
                    ShowMain = bool(ReadyContent == "True")
                    
                else:
                    FixMain = 0
                    ShowMain = ComIsTrue

                OnOffSCRN(ShowMain, False, "Main Screen is ")

        def MainSoundContent():
                global ComIsTrue
                global add_point
                global MainMusic
                        
                mSoundCommand = {'on': True, 'off': False}
                ComIsTrue = CompCommand(mSoundCommand, ReadyContent)
                if not MainMusic == None:
                        MainMusic = ComIsTrue
                        OnOffSCRN(MainMusic, False, "Sound is ")

        def ErrorContent():
                global there_was_error
                    
                there_was_error = 1
                print("there_was_error = 1")

        def DefaultContent():
                global frst_rest
                global stdy_tym
                global label
                global there_was_error
                global add_point
                global pstpn

                if there_was_error == 1:
                        stdy_tym = 25
                        label = 'test'
                        there_was_error = 1
                        add_point = 0
                        pstpn = 0.1
                        frst_rest = 0.1
                        print(f'{stdy_tym = } {label = } {there_was_error = } {add_point = } {pstpn = } {frst_rest = }')

                else:
                        err_msg()

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

                    
        def CommentContent():
                global diary_tim
                global comment
                
                diary_tim = (datetime.datetime.today())
                diary_tim = str(diary_tim.time())[:8]
                
                comment = ReadyContent

        def TimeContent():
                global B
                global stdy_tym
                
                ShortCut = ShortCutCom()
                    
                if ShortCut == ShortCutComList[0]:
                        stdy_tym = ShortCutContent(stdy_tym, last_study_tym)

                elif ShortCut == ShortCutComList[1]:
                        stdy_tym = 1000001000100
                        print("timer disabled")

                else:
                        B = err_chk(ReadyContent)
                        stdy_tym =  stndard_err_scrn()

        def LabelContent():
            global label
            
            ShortCut = ShortCutCom()
            if ShortCut == ShortCutComList[0]:
                    try:
                            label_list[(len(label_list)-1)]
                    except:
                            print()
                            print(None)
                    else:
                            label = ShortCutContent(label, label_list[(len(label_list)-1)])

            elif ShortCut == ShortCutComList[2]:
                    UseLabelContent()

            else:
                    B = err_chk(ReadyContent)
                    if not ReadyContent == "":
                        label = B
                        print()
                        print(label)

        def TimeLabelContent():
            global stdy_tym
            global label
            
            stdy_tym = ShortCutContent(stdy_tym, last_study_tym)
            if stdy_tym == None:
                    pass
            else:
                    label = ShortCutContent(label, label_list[(len(label_list)-1)])

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

        def LabelAddContent():
            global label
            try:
                    label_list[(len(label_list)-1)]
            except:
                    print('print("err_scrn")')
            else:
                B = err_chk(ReadyContent)
                label = label_list[(len(label_list)-1)] + B
                print()
                print(label)

        def EmailContent():
            global turnEmailOn
            global ComIsTrue

            emailCommand = {'on': True, 'off': False}
            ComIsTrue = CompCommand(emailCommand, ReadyContent)
            if not ComIsTrue == None:
                turnEmailOn = ComIsTrue
                OnOffSCRN(turnEmailOn, False, "Email system is ")
                    

            



        ColCommand = {'p': 3, 'P': 3, 'D': 7, 'diary': 7, 'T': 8, 'time': 8,'tim.length': 8, 'L': 9, 'label': 9, 'TL': 10, 'LT': 10, 'MainScreen': 11, 'MS': 11, 'mainScreen':11, 'UI': 11, 'L+': 12, 'sound': 14, 'S': 14, 'mail': 15, 'email': 15}

        NoCommand = {'p': 3, 'P': 3, 'error': 4, 'exit': 5, '(*default)': 6}

        Command = {'show': 0, 'end': 1, 'use': 2, 'sound': 13, 'goal': 16, 'g': 16, 'G': 16}

        content = [ShowContent, EndContent, UseContent, PointContent, ErrorContent, enter, DefaultContent, CommentContent, TimeContent, LabelContent, TimeLabelContent, MainSType, LabelAddContent, SoundContent, MainSoundContent, EmailContent, goalContent]
        #          0            1           2           3             4             5      6               7               8            9             10                11         12               13            14                15            16

        def FindContent(var ,finder, subt):
                global ReadyCommand
                global ReadyContent
                                        
                ReadyCommand = var[:(var.find(finder)) + (subt - 1)]
                ReadyContent = var[(var.find(finder)) + (subt):]
                

        def ExecuteCom(CommandTyp, ContentTyp):
                if not ComIsTrue == None:
                        ContentTyp[ComIsTrue]()

        def ExecuteContent(command, content):
                global ComIsTrue
                ComIsTrue = CompCommand(command, ReadyContent)
                ExecuteCom(ComIsTrue, content)


        while True:
                ReadyCommand = None
                ReadyContent = None
                ready = input(">> ")
                

                if ready == "":
                        enter()

                elif "'" in ready:
                        FindContent(ready, "'",1)
                        ComIsTrue = CompCommand(ColCommand, ReadyCommand)
                        ExecuteCom(ComIsTrue, content)
                        

                elif " " in ready:
                        FindContent(ready, " ",1)
                        ComIsTrue = CompCommand(Command, ReadyCommand)
                        ExecuteCom(ComIsTrue, content)

                else:
                        ReadyCommand = None
                        ReadyContent = ready
                        ComIsTrue = CompCommand(NoCommand, ReadyContent)
                        ExecuteCom(ComIsTrue, content)


                if ComIsTrue == None:
                        err_msg()

                print()

                if enter_break == True and tim_out == False:
                        CannotClick = True
                        break



##########################################上は全部関数等です######################################################################################################################################

    Loading_Screen()
    now_start = (datetime.datetime.today())
    started_time = str(now_start.time())[:8]
    today = str(now_start)[:10]
    fileDirSort = str(now_start.year) + '/' + str(now_start.month)


    printContent = 'Python Report\StudyContent/' + fileDirSort + '\Content ' + str(today) + ' .txt'
    printPoint = 'Python Report\StudyPoint/' + fileDirSort + '\point ' + str(today) + ' .txt'
    printDiary = 'Python Report\Diary/' + fileDirSort + '\Diary for ' + str(today) + ' .txt'
    
    try:
            the_program_started()
    except:
            pass
    Loading_Screen()
    
    hidden_file_log()
    Loading_Screen()
    
    extract_data()
    pages_finished = pages_finished_first
    LastCorrect = correct
    LastIncorrect = incorrect
    
    Loading_Screen()
    
    start_cntinuous_tim = cntinuous_tim
    start_last_session = last_session
    count = count_one
    
    var_amount()
    Loading_Screen()
            
    if main_debugger == 0:
            there_was_error = 0


    hidden_file()
    Loading_Screen()
    
    MusicImport()
    
    settingsFile()
    
    Loading_Screen()

    
    CannotClick = count

    if cntinuous_tim == 0 and recess_now <= 0:
            recess_now = 10
    
    cheat_code()

    if not frst_rest == 0:
            hidden_file()
            all_minus_point = rest(frst_rest)
            if not all_minus_point == None:
                last_session -= all_minus_point
                all_minus_point = 0
                var_amount()

    #checks if i have unused rest that i haven't used, and changes it into points. Bro, the += was a = and "if recess_now > 0:" was "if recess_now >= 0:"! that means that i have been studying with the risk of literally deleting all my progress. WTF?? this is such a major bugk, i can't believe i haven't noticed it before
    if recess_now > 0:
            last_session += recess_now * (div_givup_rst / (5/4))
            recess_now = 0


    os.system('cls')
    
    while True:
            count = count + 1
            point = 0
            rightAmount = 20
            minute = 0
            tim_point = 0
            broken = 0
            givup_rst = 0
            repeat_one_finish = 0
            repeat_right = 0
            repeat_wrong = 0
            repeat_new =0
            new_point = 0
            LastCorrect = correct
            MINpassedPrint = False
            reset_time = time.time()
            cntnuos_rst = time.time()
            last_count = math.floor(((cntinuous_tim + the_time) / 60) / 25) + 1
            until_next_count = 1500 - (cntinuous_tim - 1500 *(math.floor(cntinuous_tim / 1500)))
            past_count = until_next_count
            time_right_now(time_before)
            sleep(0.45)
            printNoMain = True
            emailSent = False
            
            song_start(StdyMusicUsed)

            emailLabel = '【WORKPPL】STUDY TIME HAS ENDED NOTIFICATION'
            emailBody = f'{label}の{stdy_tym}分が終了しました\n勉強を終了してください'

            studyEndedEmail = sendEmail.EmailSender(emailLabel, emailBody)
            
                    
        
            while True:
                    cal_pnt()

                    SWTMain = win32api.GetKeyState(0x24)
                    if FixMain == 1:
                        pass
                    
                    elif SWTMain < 0 and ShowMain == False:
                            ShowMain = True
                            sleep(0.04)

                    elif SWTMain < 0 and ShowMain == True:
                            printNoMain = True
                            ShowMain = False
                            sleep(0.04)

                    if ShowMain == True:
                        main_screen()
                        MINpassedPrint = False
                        
                    else:
                        
                        no_main_screen()

                    one_finish = win32api.GetKeyState(0x60)
                    if one_finish < 0:
                            pages_finished = keypres(1, pages_finished)
                            printNoMain = True
                            repeat_one_finish += 1

                    right = win32api.GetKeyState(0x64)
                    if right < 0:                            
                            correct = keypres(1, correct)
                            repeat_right += 1
                            printNoMain = True

                    wrong = win32api.GetKeyState(0x65)
                    if wrong < 0:
                        incorrect = keypres(1, incorrect)
                        repeat_wrong += 1
                        printNoMain = True
                            
                    new = win32api.GetKeyState(0x66)
                    if new < 0:
                            new_words = keypres(1, new_words)
                            repeat_new += 1
                            printNoMain = True

                    fixChange = win32api.GetKeyState(0x2D)
                    if fixChange < 0 and FixMain == 0:
                            FixMain = 1
                            os.system('cls')
                            sleep(0.181)
                            printNoMain = True
                            
                    elif fixChange < 0:
                            FixMain = 0
                            os.system('cls')
                            sleep(0.0263)
                            printNoMain = True
                    
                    if the_time / 60  < stdy_tym: #Ln257
                            pass
                    
                    elif turnEmailOn == True and emailSent == False:
                        emailSent = True
                        studyEndedEmail.sendEmail()
                        printNoMain = True

                    elif MINpassedPrint == False:
                            if useMusic == 1:
                                music.play()
                                useMusic = 0
                            print(END)
                            print(str(stdy_tym) + "分が経ちました" + "\033[8m")
                            MINpassedPrint = True

                    sleep(0.02)

                    if ShowMain == True:
                        os.system('cls')

                                
                    fin = win32api.GetKeyState(0x23)
                    if fin < 0:
                            broken = 0
                            print("\033[8m")
                            os.system('cls')
                            clear_input_buffer()
                            if isMusicUsed == True:
                                pygame.mixer.music.set_volume(volume/2)
                            while True:
                                    finishedGoal, temp = goalEvaluator.evaluate_goal(goal, {'one_finish': repeat_one_finish, 'right': repeat_right, 'wrong': repeat_wrong, 'new': repeat_new})
                                    if finishedGoal == False and not goal == 0:
                                        print("\033[0m" + "タスクがまだ完了していません。\n本当に", end='')
                                    
                                    print("\033[0m" + "終了しますか +/-")
                                    
                                    finish = input(">> ")

                                    if finish == "":
                                        os.system('cls')


                                    elif finish == "-" or finish == "n":
                                        sleep(0.1)
                                        if ShowMain == False:
                                            printNoMain = True
                                        if isMusicUsed == True:
                                                pygame.mixer.music.set_volume(volume)
                                        break

                                    elif finish == '+' or finish == "y":
                                        broken = 1
                                        cal_pnt()
                                        os.system('cls')
                                        break

                                    else:
                                        exception_error()

                    if broken == 1:
                        if isMusicUsed == True:
                            music.stop()
                        loading_count = -1
                        Loading_Screen()
                        LastIncorrect = incorrect
                        recess_time += the_time
                        if not add_point == 0:
                            cntinuous_tim += the_time
                        time_list.append(the_time/60)
                        label_list.append(label)
                        time_right_now(time_now)
                        hidden_file_log()
                        diary()
                        label = None
                        comment = None
                        recess_now = None
                        last_study_tym = stdy_tym
                        stdy_tym = None
                        add_point = None
                        pastGoal = goal
                        os.system('cls')
                        break
                    
            CannotClick = count
            
            while True:
                var_amount()
                recess_before = recess
                if recess <= 0:
                        recess_now = recess
                        break

                end_scrn()
                givup_rst = CheckAnswer("何分休みますか？")

                givup_rst = ReturnRest(givup_rst, recess)

                if not givup_rst == None:
                    recess_now = givup_rst
                    break
                else:
                    exception_error()
                    givup_rst = 0 #end_scrnでのcrashを防ぐため。error.givup_rst has no number to it

            os.system('cls')
            
            while True:
                    if recess_now > 0:
                        last_session += (recess_before - recess_now) * div_givup_rst
                    end_scrn()
                    print()
                    print("続けますか？")
                    end = input("[Enter / - (key)押す]")
                    
                    if end == "-" or end == "n":
                            done_study()
                    
                    elif end == "" or end == "+" or end == "y":
                            goal = None
                            cheat_code()
                            if recess_now > 0:
                                    sleep(0.3)
                                    tempRecessTim = recess_now
                                    recess_now = 0 # this is because i can quit anytime and i don't want to have the fucking recess time with it i know nobody understands what im saying
                                    all_minus_point = rest(tempRecessTim)
                                    recess_time = 0
                                    if not all_minus_point == None:
                                            last_session -= all_minus_point
                                            all_minus_point = 0
                                            var_amount()

                            last_session = last_session_show
                            last_point = totl_point
                            totl_point = 0
                            hidden_file()
                            os.system("cls")
                                    
                            break
                    

                    else:
                            exception_error()


except Exception as e:
        while True:
                #thisisnew = 'a'
                os.system('cls')
                print()
                print(e)
                #print(int(thisisnew))
                print("↑エラー発生")
                print()
                try:
                        print("last_session_show:", last_session_show)
                except:
                        print('ポイントシステムが原因です。調査してください')
                else:
                        print("last_session_showをコピペして引き続き利用してください")
                input()