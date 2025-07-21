#ver.2.2.4
import math, datetime, time, win32api, msvcrt, os, pygame.mixer, subprocess
from time import sleep
from os import system
from time import sleep
from funcs import sendEmail, goalEvaluator, goalProgress, prints, num, file, data, prints, work_ppl_rest, play_music, command_console

print("\033[8m")
print("\033[0m")
os.system('cls')

Title = "WORK PPL"

system("title " + Title)

RED = '\033[31m'
END = '\033[0m'

now_start = datetime.datetime.today()
started_time = str(now_start.time())[:8]
today = str(now_start)[:10]


def clear_input_buffer():
    while msvcrt.kbhit():
        msvcrt.getch()

def seconds_to_hms(seconds):
    done_hr = math.floor(seconds / 3600)
    done_min = math.floor((seconds - (done_hr* 3600)) / 60)
    done_sec = int(seconds - (done_min * 60) - (done_hr * 3600))
    return done_hr, done_min, done_sec        

def return_time():
    now = (datetime.datetime.today())
    time_right_now = str(now.time())[:8]
    return time_right_now        

def keypres(amount, what):
    variable = what + 1
    print(f'+{amount}')
    sleep(0.1)
    return variable
        

#質問をし答えをVariableに記録します
def CheckAnswer(question):
    print()
    print(question)
    print()
    answer = input(">> ")
    if answer == '':
        os.system('cls')
        no_error = False
        print()
        prints.err("何か入力してください")
    else:
        try:
            answer = float(answer)
            return answer
    
        except:
            prints.err('数字を入力してください')
            return answer

def print_string_true_false(temp_value, string, temp_replacement):
    if num.isNum(temp_replacement) == False:
        replacement = temp_replacement
    elif temp_replacement == True:
        replacement = 'on'
    elif temp_replacement == False:
        replacement = 'off'
    else:
        replacement = str(temp_replacement)
    split_string_list = string.split(temp_value)
    return_var = ''
    for ilen, i in enumerate(split_string_list):
        return_var += i
        if not ilen == len(split_string_list)-1:
            return_var += str(replacement)
    return return_var


def ReturnRest(rest_var, recess):
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
        if rest_var == 'all':
            return recess
        elif 'none':
            return 0
        if rest_var == "auto":
            var = workSession.AutoRest(recess)
            return var
        elif not rest_var == None:
            return rest_var



def extract_if_True(extract_value, boolian):
    if boolian == True:
        return extract_value
    return 0

class workSession:
    def __init__(self):
        self.first_recess = 10
        self.label = None
        self.recommended_label = None

        self.study_time = None

        self.music_on = True
        self.email_on = True

        self.comment = None

        self.goal = None
        self.add_point = None

        self.start_session = None
        self.current_points = 0
        self.past_goal = None

        self.REST_POINT_CONVERSION_RATE = 0.1
        self.MAX_DELETION_PERCENTAGE = 0.45

        self.rest_time_points = 0
        self.time_started_list = []
        self.time_ended_list = []

        self.DEVIDE_POINT_BY = 0.7

        persistent_data_file = file.content('REPORT\python_hidden_file', 'CT_LS.txt')
        settings_file = file.content('REPORT\python_hidden_file', 'settings.txt')
        subprocess.check_call(["attrib","+H","REPORT\python_hidden_file"])

        persistent_data = {'continuous_time': 0, 'current_points': 0, 'new_words': 0, 'correct': 0, 'incorrect': 0, 'pages_finished': 0, 'recess_now': 0, 'last_study_time':0, 'today': None}
        self.manage_persistent_data = data.manage(persistent_data, persistent_data_file)
        subprocess.check_call(["attrib","+H", 'REPORT\python_hidden_file\CT_LS.txt'])

        settings_data = {'volume': 100, 'choose_music_study': None, 'choose_music_rest': None, 'chose_music': False}
        self.manage_settings_data = data.manage(settings_data, settings_file)
        subprocess.check_call(["attrib","+H", 'REPORT\python_hidden_file\Settings.txt'])


        file.content(f'REPORT\music')
        self.diary_file = file.content(f'REPORT\diary\{str(now_start.year)}\{now_start.month}', f'diary for {str(today)}.txt')
        self.point_detail_file = file.content(f'REPORT\log of points\{str(now_start.year)}\{now_start.month}', f'point {str(today)}.txt')
        self.study_content_file = file.content(f'REPORT\log of studied content\{str(now_start.year)}\{now_start.month}', f'point {str(today)}.txt')
        self.study_content_log_file = file.content('REPORT\python_hidden_file', 'LL_log.txt')
        self.study_time_log_file = file.content('REPORT\python_hidden_file', 'TL_log.txt')

    def done_hour(self):
        print()
        hour, minute, second = seconds_to_hms(self.continuous_time)
        print(str(hour) + "時間：" + str(minute) + "分", str(second) + "秒")


    def show_list(self):     
        list_num = -1
        if not len(self.time_list) > 0:
            print(None)
        else:
            print('_' * 47)
            for i in range(len(self.time_list)):
                list_num +=1
                print()
                print(str(list_num +1) + "回目(" + str(self.label_list[list_num]) + "):" + str(self.time_list[list_num]) + "分", end = '')
                print()
            print('_' * 47)

    def AutoRest(self, recess):
        #どうやらrecess_timeは休憩時間を計算しているわけでなくて、前セッションの勉強時間を計算しているようです。だから、この式は、勉強時間(actual_study_time)を1500秒(25分)だと仮定したときに、最低5分の休憩を取ることができるように設定されているみたい？
        if (self.actual_study_time / 60) * 0.2 < recess:
            return (self.actual_study_time / 60) * 0.2
        else:
            return recess

    def write_study_content_file(self):
        what_to_write = f'\n{"_" * 39}'
        #list num is looking at time list which has all the times i have logged how long i have studied for, 
        # and subtracting the length of how much i have logged my progress after i started the program
        session_nunber = len(self.time_list) - len(self.time_started_list)-1

        for time_code_start, time_code_end in zip(self.time_started_list, self.time_ended_list):
            session_nunber +=1
            what_to_write += f'\n{str(int(session_nunber +1))}回目 「{str(self.label_list[session_nunber])}」　ー　{str(self.time_list[session_nunber])}分'
            what_to_write += f'\n{time_code_start} - {time_code_end}'
            if self.add_point == 0:
                what_to_write += ' *no point*'
        what_to_write += f'\n\nended program:{str(return_time())}\n{"-"*39}'
        self.study_content_file.save(what_to_write, '*lock*')

    def write_point_detail_file(self):
        hour, minute, second = seconds_to_hms(self.continuous_time - self.continuous_time_at_start)
        total_hour, total_minute, total_second = seconds_to_hms(self.continuous_time)
        what_to_write = f'\n{"-"*39}'
        what_to_write += f'\n{str(hour)}時間 {str(minute)}分 {str(second)}秒'
        what_to_write += f'\n（合計：{str(total_hour)}時間 {str(total_minute)}分 {str(total_second)}秒）'
        what_to_write += f'\n\nポイント：{str(float(self.current_points) - float(self.last_session_at_start))}'
        what_to_write += f'\n（ポイントの合計：{str(self.current_points)}）'
        what_to_write += f'\n{"-"*39}'
        what_to_write += f'\nended : {str(return_time())}'
        self.point_detail_file.save(what_to_write, '*lock*')

    def write_diary_file(self):
        if not self.comment == None:
            what_to_write = f'\n{str(self.comment_time)}　【{str(self.label_list[len(self.label_list)-1])}】\n{"-"*86}\n'
            self.diary_file.save(what_to_write)
            what_to_write = ''
            try:
                self.diary_file.save(self.comment)
            except ValueError:
                for i in self.comment:
                    try:
                        what_to_write += str(i)
                    except ValueError:
                        what_to_write += '(?)'
                self.diary_file.save(what_to_write, '*lock*')
                what_to_write = ''
            what_to_write += '\n\n\n'
            self.diary_file.save(what_to_write, '*lock*')
            self.comment_time == None    
            
    def write_log_files(self):            
        if not len(self.time_list) == 0:
            self.study_time_log_file.delete_file()
            what_to_write = ''
            for i in self.time_list:
                what_to_write += f'{i}\n'
            self.study_time_log_file.save(what_to_write, '*lock*')


            self.study_content_log_file.delete_file()
            for i in self.label_list:
                what_to_write += f'{i}\n'
            try:
                self.study_content_log_file.save(what_to_write, '*lock*')
            except UnicodeEncodeError:
                for i in self.label_list:
                    self.study_content_log_file.save(i, '*lock*')


    def extract_data_from_file(self):
        extracted_dict = self.manage_persistent_data.extract_from_file()
        isToday = False
        if extracted_dict['today'] == today:
            isToday = True
        self.continuous_time = extract_if_True(extracted_dict['continuous_time'], isToday)
        self.new_words = extract_if_True(extracted_dict['new_words'], isToday)
        self.correct = extract_if_True(extracted_dict['correct'], isToday)
        self.incorrect = extract_if_True(extracted_dict['incorrect'], isToday)
        self.pages_finished = extract_if_True(extracted_dict['pages_finished'], isToday)
        self.recess = extract_if_True(extracted_dict['recess_now'], isToday)
        self.last_study_time = extract_if_True(extracted_dict['last_study_time'], isToday)
        if self.recess == None:
            self.recess = 0
        self.past_points = extracted_dict['current_points']
        extracted_dict = self.manage_settings_data.extract_from_file()
        self.volume = extracted_dict['volume']
        self.choose_music_study = extracted_dict['choose_music_study']
        self.choose_music_rest = extracted_dict['choose_music_rest']
        self.chose_music = extracted_dict['chose_music']
        
        label_list_temp = self.study_content_log_file.fetch()
        if isToday == True:
            self.label_list = label_list_temp
        else:
            self.label_list = []
        #i want the last label to be extracted no matter what
        time_list_temp = self.study_time_log_file.fetch()
        if isToday == True:
            self.time_list = time_list_temp
        else:
            self.time_list = []
        self.count_one = len(self.time_list)
        #the same thing in time list
        self.pages_finished_first = self.pages_finished
        self.past_correct_len = self.correct
        self.past_incorrect_len = self.incorrect
        self.continuous_time_at_start = self.continuous_time
        self.last_session_at_start = self.past_points
        self.count = self.count_one
        if self.continuous_time == 0 and self.recess <= 0:
            self.recess = self.first_recess

        if float(self.recess) > 0:
            opening_string = f'\n>> There is unused rest: {self.recess}\n'
        else:
            opening_string = ''

        self.manage_persistent_data.change_value({'today': today})
        return self.recess, opening_string
    
    def import_settings(self):
        self.music_content = play_music.music(self.volume, self.choose_music_study, self.choose_music_rest, self.chose_music)
        self.choose_music_study, self.choose_music_rest = self.music_content.import_music()
        self.manage_settings_data.change_value({'choose_music_study': self.choose_music_study, 
                                                 'choose_music_rest': self.choose_music_rest, 
                                                 'chose_music': True})
        self.manage_settings_data.write_to_file()


    def writing_start_of_file(self):
        study_content_file_data = self.study_content_file.fetch()
        what_to_write = ''
        if not study_content_file_data == []:
            what_to_write += f'\n\n'
        what_to_write += '\n'
        what_to_write += f'started program:{started_time}'
        self.study_content_file.save(what_to_write)

        point_detail_file_data = self.point_detail_file.fetch()
        what_to_write = ''
        if not point_detail_file_data == []:
            what_to_write += f'\n\n\n'
        what_to_write += f'{"_" * 82}\n\nstarted : {started_time}'
        self.point_detail_file.save(what_to_write)
    

    def rest(self, time_of_rest):
        rest_session = work_ppl_rest.main_rest_class()
        #? i think its past points
        rest_session.get_values(time_of_rest, self.rest_time_points, self.REST_POINT_CONVERSION_RATE, self.email_on, self.MAX_DELETION_PERCENTAGE, self.past_points, self.music_content, self.music_on)
        minus_points = rest_session.rest_func()
        if minus_points == True:
            self.manage_persistent_data.change_value({'current_points': 0})
            self.write_study_content_file()
            exit()

        self.past_points -= minus_points
        self.manage_persistent_data.change_value({'current_points': self.past_points})
    
    def ui_screen(self, ui_type):
        goal_dict = {'one_finish': self.repeat_one_finish, 'right': self.repeat_right, 'wrong': self.repeat_wrong, 'new': self.repeat_new} #this is here because it doesn't work if i directly put it in the variable wtf why
        match ui_type:
            case 'session_ui':#main_ui
                print(END)
                temp, progressDict = goalEvaluator.evaluate_goal(self.goal, goal_dict)

                print(f'{self.count}回目( {self.label}-{self.study_time}分 ) ', end='')
                if self.swich_ui == 1:
                    print('\033[33m' + '総勉強時間モード' + END)
                else:
                    print()
                percentageStr = f'目標時間の{self.showPercentage}%が終了 ({self.bonusPointPercentage}倍ボーナス)\n{self.encouragementWord}'
                prints.progress(int(goalProgress.get_goal_progress(self.goal, goal_dict)))
                print()
                if not self.goal == 0:
                    print('~~~~~~~')
                    print(percentageStr)
                    print('~~~~~~~')
                    print()
                print()
                print('\033[32m' + '一章' + END + '終わったら"4/←"', end='')
                if not self.goal == 0:
                    print(f' ({progressDict['one_finish']['current']}/{progressDict['one_finish']['required']})')
                else:
                    print(f' ({progressDict['one_finish']['current']})')

                print()
                print('\033[32m' + '正答' + END + 'は"1/END"', end='')
                if not self.goal == 0:
                    print(f' ({progressDict['right']['current']}/{progressDict['right']['required']})')
                else:
                    print(f' ({progressDict['right']['current']})')

                print()
                print('\033[32m' + '不正答' + END +'は"2/↓"', end='')
                if not self.goal == 0:
                    print(f' ({progressDict['wrong']['current']}/{progressDict['right']['required']})')
                else:
                    print(f' ({progressDict['wrong']['current']})')
                print()
                print('\033[32m' + '新規' + END + 'は"3/pgDn"', end='')
                if not self.goal == 0:
                    print(f' ({progressDict['new']['current']}/{progressDict['right']['required']})')
                else:
                    print(f' ({progressDict['new']['current']})')
                print()
                print()
                print('勉強が終わったら "' + '\033[1m' + '0/Ins' + END + '"キー')
                print()
                print()
                print(f'{self.minute} min {self.second} sec')
                print()
                if not self.add_point == 0:
                    print(f'{((self.new_point + self.tim_point) * self.DEVIDE_POINT_BY * 100)} points')
                else:
                    print(f'{0} points')

            case 'minimal_session_ui':
                if self.print_minimal_ui == True:
                    temp, progressDict = goalEvaluator.evaluate_goal(self.goal, goal_dict)
                    
                    os.system('cls')
                    print(END)
                    print(f'{self.count}回目( {self.label}-{self.study_time}分 ) ')
                    prints.progress(int(goalProgress.get_goal_progress(self.goal, goal_dict)))
                    print()
                    print()
                    print(f'{self.pages_finished - self.pages_finished_first}/{progressDict['one_finish']['required']}章終わり')
                    print()
                    print(f'正答：{self.correct - self.past_correct_len}/{progressDict['right']['required']}個')
                    print()
                    print(f'不正答：{self.incorrect - self.past_incorrect_len}/{progressDict['wrong']['required']}個')
                    print()
                    print(f'新規：{self.repeat_new}/{progressDict['new']['required']}個')
                    #if minute < study_time: #Ln257
                    #    pass
                        
                    print("\033[8m")
                    self.print_minimal_ui = False

            case 'ending_screen_ui':
                print()
                print(self.count,"回目")
                print()
                if self.current_points >= float(self.past_points):
                    print("今回のポイント：", self.current_points - float(self.past_points))
                else:
                    print("今回のポイント： 0")
                print(f'({self.pointString})')
                print()
                print("前回までのポイント：", self.past_points)
                print()
                if self.recess == None or self.recess == 0:
                    print("合計：", self.current_points, "points")
                else:
                    print("合計", self.current_points + ((self.recess - self.recess) * self.REST_POINT_CONVERSION_RATE), "points")        
                print()

                show_recess = float(self.recess)
                if show_recess > 0 and self.recess == None:
                    print('休み:', show_recess, "min")
                elif self.recess >= 0:
                    print('休み:', self.recess, "min")
                elif self.recess <= 0:
                    print('休み:', 0, "min")
                else:
                    print('休み: ' + RED + 'error' + END + ' min')   
                print()

            case 'finished_study_ui':
                todayRaw = datetime.datetime.today()
                todayShow = todayRaw.strftime('%Y年%#m月%#d')

                print("\033[0m" + f'{todayShow}日の最終スコアは：')
                workSession.done_hour(self)
                print()
                print()
                print("ポイントの合計：", self.current_points)
                print()
            
                if self.correct > 0 or self.new_words > 0:
                    print()
                    print("新しく覚えた単語：" + str(self.new_words) + "個")
                    print("正答した問題：" + str(self.correct) + "個")
                    print("不正答の問題：" + str(self.incorrect) + "個")
                    print()
                    print()
                    
                if self.pages_finished > 0:
                    print("終わった章：" + str(self.pages_finished) + "章")
                    print() 
                print()
                workSession.show_list(self)

    def cli_screen(self):
        temp_value = '$'
        cli = command_console.cli(temp_value)
        command_input = input('>> ')
        cli.get_command(command_input)
        cli_output = cli.execute_command()
        #print(cli_output)
        if cli_output == None:
            output_keys = ['None']
            prints.err('invalid command')

        else:
            output_keys = list(cli_output.keys())
        self.start_session = False
        print_var = None
        for command in output_keys:
            match command:
                case 'error':
                    prints.err(cli_output[command])
                case 'label':
                    self.label = cli_output[command]
                    print_var = self.label
                case 'same_label':
                    if self.label_list:
                        self.label = self.label_list[len(self.label_list)-1]
                        print_var = self.label
                    else:
                        prints.err('past label does not exist')
                case 'use_label':
                    if not self.recommended_label == None:
                        self.label = self.recommended_label
                        print_var = self.label
                    else:
                        prints.err('label to use does not exist')
                case 'time':
                    self.study_time = cli_output[command]
                    print_var = self.label
                case 'same_time':
                    if not self.last_study_time == None:
                        self.study_time = self.last_study_time
                        print_var = self.label
                    else:
                        prints.err('past session does not exist')
                case 'diary_written_time':
                    self.comment_time = cli_output[command]
                    print_var = self.label
                case 'diary_content':
                    self.comment = cli_output[command]
                    print_var = self.label
                case 'sound_on':
                    self.music_on = cli_output[command]
                    print_var = cli_output[command]
                case 'email_on':
                    self.email_on = cli_output[command]
                    print_var = cli_output[command]
                case 'start_session':
                    ready_to_start = True
                    if self.study_time == None:
                        ready_to_start = False
                        prints.err('please enter study time')
                    if self.label == None:
                        ready_to_start = False
                        prints.err('please enter label')
                    if self.goal == None:
                        ready_to_start = False
                        prints.err('please enter goal')
                    if self.add_point == None:
                        ready_to_start = False
                        prints.err('please enter point system')
                    if ready_to_start == True:
                        self.manage_settings_data.write_to_file()
                        return True
                case 'string_to_add_label':
                    if self.label_list:
                        self.label = f'{self.label_list[len(self.label_list)-1]}{cli_output[command]}'
                        print_var = self.label
                    else:
                        prints.err('past label does not exist')
                case 'points':
                    self.add_point = cli_output[command]
                    print_var = cli_output[command]
                case 'show_study_time':
                    workSession.done_hour(self)
                case 'show_study_list':
                    workSession.show_list(self)
                case 'show_points':
                    print(self.current_points)
                case 'end_study':
                    return False
                case 'volume':
                    self.volume = cli_output[command]
                    print_var = self.volume
                    self.manage_settings_data.change_value({'volume': self.volume})
                case 'change_sound':
                    temp_choose_music = self.music_content.chage_music()
                    choose_music = 'None'
                    if not choose_music == None:
                        choose_music = temp_choose_music

                    self.music_content.import_change(cli_output[command], temp_choose_music)
                    self.manage_settings_data.change_value({cli_output[command]: choose_music})
                    print_var = choose_music
                case 'use_rest':
                    if self.recess >= 0 and self.count == self.count_one:
                        self.rest_time = self.recess
                        print('rest safely pending usage')
                        return 2
                case 'goal':
                    self.goal = cli_output[command]
                    print_var = str(self.goal)
                case 'goal_no_goal':
                    self.goal = 0
                    print_var = 'None'
                case 'goal_same_goal':
                    if not self.past_goal == None:
                       self.goal = self.past_goal
                    else:
                        prints.err('past goal does not exist')
                case 'print':
                    print(print_string_true_false(temp_value, cli_output[command], print_var))

    def initialize_session(self):
        self.count = self.count + 1
        self.minute = 0
        self.tim_point = 0
        self.repeat_one_finish = 0
        self.repeat_right = 0
        self.repeat_wrong = 0
        self.repeat_new = 0
        self.past_correct_len = self.correct
        self.session_time_finished = False
        self.the_time = 0
        self.swich_ui = 0
        self.reset_time = time.time()
        self.cntnuos_rst = time.time()
        self.last_count = math.floor(((self.continuous_time + self.the_time) / 60) / 25) + 1
        self.until_next_count = 1500 - (self.continuous_time - 1500 *(math.floor(self.continuous_time / 1500)))
        self.past_count = self.until_next_count
        self.time_started_list.append(return_time())
        self.actual_study_time = 0
        self.new_point = 0
        self.print_minimal_ui = True
        self.email_sent = False
        self.finished_content_list = []
        self.last_finished_content = None
        
        self.use_music, self.is_using_music, self.music = self.music_content.set_song('choose_music_study', self.music_on)

        EMAIL_LABEL = '【WORKPPL】STUDY TIME HAS ENDED NOTIFICATION'
        EMAIL_BODY = f'{self.label}の{self.study_time}分が終了しました\n勉強を終了してください'
        self.studyEndedEmail = sendEmail.EmailSender(EMAIL_LABEL, EMAIL_BODY)

    def calculate_time_and_point(self):
        self.the_time = round(time.time()-self.reset_time)
        if self.swich_ui == 1:
            self.showTime = self.the_time + self.continuous_time
        else:
            self.showTime = self.the_time

        
        self.second = self.showTime - self.minute * 60
        self.minute = math.floor(self.showTime/60)
        #Changes were made so that even if unforseen elements cause the program to not calculate the amount, rebooting(?) the program will achive the same result as calculating it real-time
        if self.the_time > self.past_count:
            self.the_countdown_time = self.the_time
            
            #I'm no sure but i think tim_point resets when getting to a milestone(i think) thats why there is this new_point thing, which probably keeps track on how much i got each milestone or something IDK
            while self.the_countdown_time > self.until_next_count:
                self.the_countdown_time -= self.until_next_count

                self.new_point += (self.until_next_count * self.add_point / 1500) * ((math.ceil(self.past_count/1500) - 1) +  self.last_count)
                self.until_next_count = 1500
                self.past_count += 1500                
        self.tim_point = (((time.time()- (self.reset_time + (self.past_count - self.until_next_count))) * self.add_point / 1500) * ((math.ceil(self.past_count/1500) - 1) +  self.last_count))
        #(reset_time + (past_count - until_next_count)) is a variable which essentially resets the timer whenever the point added increases
        #((math.ceil(past_count/1500) - 1) +  last_count) is the past "count" variable, but calculated using math, rather than increassing the amount every time the point addded will increase
        
        
        self.totl_tim_point = self.new_point + self.tim_point

        self.timePercentage = self.the_time/(self.study_time*60)
        self.showPercentage = int(self.timePercentage * 100)
        if self.timePercentage < .5:
            self.bonusPointPercentage = 1.4
            self.encouragementWord = 'まだまだ頑張れー(ง •̀_•́)ง'
        elif self.timePercentage >= .5 and self.timePercentage < .8:
            self.bonusPointPercentage = 3.2
            self.encouragementWord = 'その調子‼(； ･`ω･´)'
        elif self.timePercentage >= .8 and self.timePercentage < 1.3:
            self.bonusPointPercentage = 4.8
            self.encouragementWord = 'よくがんばったネ(๑˃̵ᴗ˂̵)و'
        elif self.timePercentage >= 1.3:
            self.bonusPointPercentage = 1
            self.encouragementWord = 'もう終わったよ( ´･ω･`) '

    def adjust_value(self): # this calculates the points and time you are able to study iguess
        CalTim = self.the_time / 60
        JustInTimeDiv = 1

        if self.last_study_time == None: #this if/elif statement is calcutlating how much you diviated from the intended study time to fincd out how much to devide from the recess time
            pass
        
        elif self.last_study_time > CalTim + 5:
            JustInTimeDiv = CalTim/self.last_study_time
            
        elif self.last_study_time < CalTim - 5:
            JustInTimeDiv = self.last_study_time/CalTim

        goalCompletedPercentage = goalProgress.get_goal_progress(self.goal, {'one_finish': self.repeat_one_finish, 'right': self.repeat_right, 'wrong': self.repeat_wrong, 'new': self.repeat_new})
        
        totl_tim_point = self.totl_tim_point * self.DEVIDE_POINT_BY
        self.pointString = f'{totl_tim_point} points'
        if self.goal == None:
            totl_tim_point_divided = totl_tim_point * JustInTimeDiv
            if JustInTimeDiv != 1:
                self.pointString += f' multiplied by {JustInTimeDiv} because you went over or under time'
        elif int(goalCompletedPercentage) == 100:
            totl_tim_point_divided = totl_tim_point * self.bonusPointPercentage
            if self.bonusPointPercentage == 1:
                self.pointString += f', nothing else because you went over time'
            else:
                self.pointString += f' multiplied by {self.bonusPointPercentage}'
        else:
            totl_tim_point_divided = totl_tim_point * (goalCompletedPercentage/100)
            self.pointString += f' multiplied by {goalCompletedPercentage/100} because you didn\'t complete goal' 
        
        self.current_points =  totl_tim_point_divided + float(self.past_points)
        self.manage_persistent_data.change_value({'current_points': self.current_points})
        oldRest = 5 * (((self.current_points ** 0.5) +1)/2) + (((self.actual_study_time - 1500) /60 * 2 / 10) * abs((self.current_points ** 0.5)-1))
        newRest = 5 * (((self.current_points ** 0.5) +1)/2) + (((self.actual_study_time - 1500) /60 * 2 / 10) * abs(((((self.continuous_time/1500)*((self.continuous_time/1500)))/2) ** 0.5)-1))
        if oldRest > newRest:
            return newRest
        else:
            return oldRest
        #recess の計算式について：めちゃ分かりづらいので、ここで解説します。
        #「5」という最初の数字は、ポモドーロメソッドでの一番基本の休憩時間だから。
        # つまりこれが基本で、次からがおまけということ
        #まずは現在のポイントの平方根(current_points ** 0.5)を求めています。
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


    def session(self):
        while True:
            workSession.calculate_time_and_point(self)

            SWTMain = win32api.GetKeyState(0x67)
            if SWTMain < 0:
                self.swich_ui = num.cap(self.swich_ui+1, 3)
                self.print_minimal_ui = True
                sleep(0.04)

            if self.swich_ui == 2:
                workSession.ui_screen(self, 'minimal_session_ui')
            else:
                self.print_minimal_ui = False
                workSession.ui_screen(self, 'session_ui')
                
            one_finish = win32api.GetKeyState(0x64)
            if one_finish < 0:
                self.pages_finished = keypres(1, self.pages_finished)
                self.print_minimal_ui = True
                self.repeat_one_finish += 1
                self.finished_content_list.append('one_finish')

            right = win32api.GetKeyState(0x61)
            if right < 0:                            
                self.correct = keypres(1, self.correct)
                self.repeat_right += 1
                self.print_minimal_ui = True
                self.finished_content_list.append('right')

            wrong = win32api.GetKeyState(0x62)
            if wrong < 0:
                self.incorrect = keypres(1, self.incorrect)
                self.repeat_wrong += 1
                self.print_minimal_ui = True
                self.finished_content_list.append('wrong')
                    
            new = win32api.GetKeyState(0x63)
            if new < 0:
                self.new_words = keypres(1, self.new_words)
                self.repeat_new += 1
                self.print_minimal_ui = True
                self.finished_content_list.append('new')

            undo = win32api.GetKeyState(0x6E)
            if undo >= 0:
                pass
            elif not len(self.finished_content_list) == 0:
                self.last_finished_content = self.finished_content_list[len(self.finished_content_list)-1]
                print(f'-1 {self.last_finished_content}')
                sleep(0.1)
            if self.last_finished_content == None:
                pass
            elif self.last_finished_content == 'one_finish':
                self.repeat_one_finish -= 1
                self.pages_finished -= 1
                self.print_minimal_ui = True
                self.last_finished_content = None
                self.finished_content_list.pop(len(self.finished_content_list)-1)

            elif self.last_finished_content == 'right':
                self.correct -= 1
                self.repeat_right -= 1
                self.print_minimal_ui = True
                self.last_finished_content = None
                self.finished_content_list.pop(len(self.finished_content_list)-1)
            elif self.last_finished_content == 'wrong':
                self.incorrect -= 1
                self.repeat_wrong -= 1
                self.print_minimal_ui = True
                self.last_finished_content = None
                self.finished_content_list.pop(len(self.finished_content_list)-1)
            elif self.last_finished_content == 'new':
                self.new_words -= 1
                self.repeat_new -= 1
                self.print_minimal_ui = True
                self.last_finished_content = None
                self.finished_content_list.pop(len(self.finished_content_list)-1)


            #if not self.last_finished_content == None:

            if self.the_time / 60  < self.study_time: #Ln257
                pass
            elif self.email_on == True and self.email_sent == False:
                self.email_sent = True
                try:
                    self.studyEndedEmail.sendEmail()
                except:
                    pass
                self.print_minimal_ui = True

            elif self.session_time_finished == False:
                if self.use_music == 1:
                    self.music.play()
                    self.use_music = 0
                print(END)
                print(str(self.study_time) + "分が経ちました" + "\033[8m")
                self.session_time_finished = True
            sleep(0.02)
            if not self.swich_ui == 2:
                os.system('cls')

            fin = win32api.GetKeyState(0x60)
            if fin < 0:
                print("\033[8m")
                os.system('cls')
                clear_input_buffer()
                while True:
                    completed_goal, temp = goalEvaluator.evaluate_goal(self.goal, {'one_finish': self.repeat_one_finish, 'right': self.repeat_right, 'wrong': self.repeat_wrong, 'new': self.repeat_new})
                    if completed_goal == False and not self.goal == 0:
                        print("\033[0m" + "タスクがまだ完了していません。\n本当に", end='')
                    print("\033[0m" + "終了しますか +/-")
                    finish = input(">> ")
                    if finish == "":
                        os.system('cls')

                    elif finish == "-" or finish == "n":
                        sleep(0.1)
                        if self.swich_ui == 2:
                            self.print_minimal_ui = True
                        break
                    elif finish == '+' or finish == "y":
                        workSession.calculate_time_and_point(self)
                        os.system('cls')
                        return True
                    else:
                        prints.err('input error')

    def wrap_up_session(self):
        if self.is_using_music == True:
            self.music.stop()
        self.past_incorrect_len = self.incorrect
        self.actual_study_time = self.the_time
        if not self.add_point == 0:
            self.continuous_time += self.the_time
        self.time_list.append(self.the_time/60)
        self.label_list.append(self.label)
        self.time_ended_list.append(return_time())
        self.write_log_files()
        self.write_diary_file()
        self.label = None
        self.comment = None
        self.last_study_time = self.study_time
        self.study_time = None
        self.add_point = None
        self.past_goal = self.goal
        self.goal = None
        self.manage_persistent_data.change_value({'continuous_time': self.continuous_time, 'new_words': self.new_words, 'correct': self.correct, 'incorrect': self.incorrect, 'pages_finished': self.pages_finished, 'last_study_time': self.last_study_time})
        os.system('cls')

    def handle_rest_time(self, recess):
        self.recess = recess
        self.manage_persistent_data.change_value({'current_points': self.current_points})
        if recess <= 0:
            return 0
        while True:
            workSession.ui_screen(self, 'ending_screen_ui')
            rest_time_points = CheckAnswer("何分休みますか？")

            rest_time_points = ReturnRest(rest_time_points, recess)

            if not rest_time_points == None:
                self.manage_persistent_data.change_value({'recess_now': rest_time_points})
                return rest_time_points
            else:
                prints.err('input error')
                rest_time_points = 0 #ending_screenでのcrashを防ぐため。error.rest_time_points has no number to it
    
    def rest_time_to_points(self, rest_time):
        if rest_time > 0:
            self.current_points += (self.recess - self.rest_time) * self.REST_POINT_CONVERSION_RATE
            self.manage_persistent_data.change_value({'current_points': self.current_points})


    def chceck_if_continue(self):
        while True:
            self.manage_persistent_data.write_to_file()
            workSession.ui_screen(self, 'ending_screen_ui')
            print()
            print("続けますか？")
            end = input("[Enter / - (key)押す]")
            if end == "-" or end == "n":
                return False
            elif end == "" or end == "+" or end == "y":
                self.past_points = self.current_points
                return True

    def finish_program(self):
        self.write_diary_file()                
        self.write_log_files()
        self.write_study_content_file()
        self.write_point_detail_file()

        while True:
            workSession.ui_screen(self, 'finished_study_ui')
            ok = input("\033[8m")
            os.system('cls')

    def error_has_occured(self):
        print(self.continuous_time)
        print(self.current_points)




        
           
##########################################上は全部関数等です######################################################################################################################################
if __name__ == '__main__':
    session = workSession()
    first_rest, opening_string = session.extract_data_from_file()
    session.import_settings()
    os.system('cls')
    session.writing_start_of_file()
    print('始めます [Enter]')
    print(opening_string, end='')
    start_first_rest = False
    while True:
        print()
        start_session = session.cli_screen()
        if start_session == True:
            break
        elif start_session == False:
            session.finish_program()
        if start_session == 2:
            start_first_rest = True

    if start_first_rest == True:
        session.rest(first_rest)
        session.rest_time_to_points(first_rest)

    os.system('cls')
    while True:
        session.initialize_session()
        sleep(0.45)
        session.session()

        session.wrap_up_session()
        recess = session.adjust_value()
        session.handle_rest_time(recess)
        os.system('cls')
        continue_session = session.chceck_if_continue()
        
        os.system('cls')
        if continue_session == False:
            session.finish_program()
        os.system('cls')
        print('始めます [Enter]')
        while True:
            print()
            start_session = session.cli_screen()
            if start_session == True:
                break
            elif start_session == False:
                session.finish_program()
        if recess > 0:
            sleep(0.3)
            session.rest(recess)
            session.rest_time_to_points(recess)