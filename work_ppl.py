#ver.2.2.4

def seconds_to_hms(seconds):
    done_hr = math.floor(seconds / 3600)
    done_min = math.floor((seconds - (done_hr* 3600)) / 60)
    done_sec = int(seconds - (done_min * 60) - (done_hr * 3600))
    return done_hr, done_min, done_sec        

def return_time():
    now = (datetime.datetime.today())
    time_right_now = str(now.time())[:8]
    return time_right_now

def keypres(amount):
    print(f'+{amount}')
    sleep(0.1)

def goal_add_value(amount, goal_name):
    if goal_name == None:
        return 0
    return amount
        

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
    replacement = []
    for i in temp_replacement:
        if num.isNum(i) == False:
            replacement.append(i)
        elif i == True:
            replacement.append('on')
        elif i == False:
            replacement.append('off')
        else:
            replacement.append(str(i))

    split_string_list = string.split(temp_value)
    return_var = ''
    replacement_index = 0
    for ilen, i in enumerate(split_string_list):
        return_var += i
        if not ilen == len(split_string_list)-1:
            return_var += str(replacement[replacement_index])
            replacement_index += 1
    return return_var


def ReturnRest(rest_var, recess):
    if rest_var == 'all':
        return recess
    if rest_var == 'none':
        return 0
    if rest_var == 'auto':
        var = workSession.AutoRest(recess)
        return var
    if num.isNum(rest_var) == False:
        pass
    elif rest_var <= recess:
        return rest_var
    return None

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
        self.email_on = True

        self.diary = None
        self.comment_command_type = None
        self.comment_index = 0
        self.comment_list = []
        self.comment_time = None


        self.goal = None
        self.temp_past_goal = None
        self.add_point = None

        self.start_session = None
        self.current_points = 0

        self.REST_POINT_CONVERSION_RATE = 0.1
        self.MAX_DELETION_PERCENTAGE = 0.45

        self.rest_time_points = 0
        self.time_started_list = []
        self.time_ended_list = []

        self.DEVIDE_POINT_BY = 0.7

        self.filetype = None
        self.user_made_file_content = None

        self.name_task = None
        self.name_new = None
        self.name_correct = None
        self.name_incorrect = None

        self.pages_finished_dict = {}
        self.new_num_dict = {}
        self.correct_num_dict = {}
        self.incorrect_num_dict = {}

        self.pages_finished_session = 0
        self.new_num_session = 0
        self.correct_num_session = 0
        self.incorrect_num_session = 0



        persistent_data_file = file.content('REPORT\\logs', 'progress.txt', lock=True)
        settings_file = file.content('REPORT\\logs', 'settings.txt', lock=True)
        subprocess.check_call(["attrib","+H","REPORT\\logs"])

        persistent_data = {'continuous_time': 0, 'current_points': 0, 'new_words_full': 0, 'correct_full': 0, 'incorrect_full': 0, 'pages_finished_full': 0, 'recess_now': 0, 'past_goal': None, 'last_study_time': None, 'label_base': None, 'today': None}
        self.manage_persistent_data = data.manage(persistent_data, persistent_data_file)
        subprocess.check_call(["attrib","+H", 'REPORT\\logs\\progress.txt'])
        settings_data = {'volume': 100, 'choose_music_study': None, 'choose_music_rest': None, 'chose_music': False, 'music_on': True, 'filename': None, 'filedir': None}#, 'email_from': None, 'email_to': None, 'gmail_app_password': None}
        self.manage_settings_data = data.manage(settings_data, settings_file)
        subprocess.check_call(["attrib","+H", 'REPORT\\logs\\Settings.txt'])


        file.content(f'REPORT\\music')
        self.diary_file = file.content(f'REPORT\\diary\\{str(now_start.year)}\\{now_start.month}', f'diary for {str(today)}.txt', lock=True)
        self.point_detail_file = file.content(f'REPORT\\log of points\\{str(now_start.year)}\\{now_start.month}', f'point {str(today)}.txt', lock=True)
        self.study_content_file = file.content(f'REPORT\\log of studied content\\{str(now_start.year)}\\{now_start.month}', f'content {str(today)}.txt', lock=True)
        self.log_file = file.content('REPORT\\logs', 'log.txt', lock=True)

    def done_hour(self):
        print()
        hour, minute, second = seconds_to_hms(self.continuous_time)
        print(str(hour) + "時間：" + str(minute) + "分", str(second) + "秒")


    def show_list(self):
        list_num = -1
        if not len(self.time_list) > 0:
            print(None)
            return 0
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
        return recess

    def write_study_content_file(self):
        what_to_write = f'\n{"_" * 39}'
        #list num is looking at time list which has all the times i have logged how long i have studied for, 
        # and subtracting the length of how much i have logged my progress after i started the program
        session_nunber = len(self.time_list) - len(self.time_started_list)-1


        for time_code_start, time_code_end, name_task, name_new, name_correct, name_incorrect in zip(self.time_started_list, self.time_ended_list, self.pages_finished_dict, self.new_num_dict, self.correct_num_dict, self.incorrect_num_dict):
            session_nunber +=1

            what_to_write += f'\n{time_code_start} - {time_code_end}'
            what_to_write += f'\n{str(int(session_nunber +1))}回目 「{str(self.label_list[session_nunber])}」　ー　{str(self.time_list[session_nunber])}分'
            if name_task != None:
                what_to_write += f"\n{name_task}: {self.pages_finished_dict[name_task]}"
            if name_new != None:
                what_to_write += f"\n{name_new}: {self.new_num_dict[name_new]}"
            if name_correct != None:
                what_to_write += f"\n{name_correct}: {self.correct_num_dict[name_correct]}"
            if name_incorrect != None:
                what_to_write += f"\n{name_incorrect}: {self.incorrect_num_dict[name_incorrect]}"
            if self.add_point == 0:
                what_to_write += ' *no point*'
        what_to_write += f'\n\nended program:{str(return_time())}\n{"-"*39}'
        self.study_content_file.save(what_to_write, sameLN=True, lock=True)

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
        self.point_detail_file.save(what_to_write, sameLN=True, lock=True)

    def write_diary_file(self):
        if not self.diary == None:
            what_to_write = f'\n{str(self.comment_time)}　【{str(self.label_list[len(self.label_list)-1])}】\n'
            what_to_write += f'{"-"*86}\n'
            what_to_write += f'{self.diary}\n\n'
            self.diary_file.save(what_to_write, lock=True)
            self.comment_time == None    
            
    def write_log_files(self):   
        save_string = ''         
        if not len(self.log_file.fetch()) == 0:
            save_string += f'\n'
        if not len(self.time_list) == 0:
            save_string += f'{self.time_list[len(self.time_list)-1]}:{self.label_list[len(self.label_list)-1]}'
            self.log_file.save(save_string, sameLN=True, lock=True)
            


    def extract_data_from_file(self):
        extracted_dict = self.manage_persistent_data.extract_from_file()
        isToday = False
        if extracted_dict['today'] == None:
            isToday = True
        elif extracted_dict['today'] == today:
            isToday = True
        self.continuous_time = extract_if_True(extracted_dict['continuous_time'], isToday)
        self.manage_persistent_data.change_value({'continuous_time': self.continuous_time}) #its going to overwrite the thing in the file to the thing in the program, so when i end study brefore the first session starts, i need it to know the actual value

        self.new_words_full = extract_if_True(extracted_dict['new_words_full'], isToday)
        self.manage_persistent_data.change_value({'new_words_full': self.new_words_full})

        self.correct_full = extract_if_True(extracted_dict['correct_full'], isToday)
        self.manage_persistent_data.change_value({'correct_full': self.correct_full})

        self.incorrect_full = extract_if_True(extracted_dict['incorrect_full'], isToday)
        self.manage_persistent_data.change_value({'incorrect_full': self.incorrect_full})

        self.pages_finished_full = extract_if_True(extracted_dict['pages_finished_full'], isToday)
        self.manage_persistent_data.change_value({'pages_finished_full': self.pages_finished_full})

        self.recess = extract_if_True(extracted_dict['recess_now'], isToday)
        self.manage_persistent_data.change_value({'recess_now': self.recess})

        self.past_goal = extract_if_True(extracted_dict['past_goal'], isToday)
        self.manage_persistent_data.change_value({'past_goal': self.past_goal})

        self.label_base = extract_if_True(extracted_dict['label_base'], isToday)
        self.manage_persistent_data.change_value({'label_base': self.label_base})

        self.manage_persistent_data.change_value({'today': today})

        if self.recess == None:
            self.recess = 0
        self.past_points = extracted_dict['current_points']
        self.last_study_time = extracted_dict['last_study_time']

        extracted_dict = self.manage_settings_data.extract_from_file()
        self.volume = extracted_dict['volume']
        self.choose_music_study = extracted_dict['choose_music_study']
        self.choose_music_rest = extracted_dict['choose_music_rest']
        self.chose_music = extracted_dict['chose_music']
        self.music_on = extracted_dict['music_on']

        self.user_made_dir = extracted_dict['filedir']
        self.user_made_file = extracted_dict['filename']

        
        self.label_list = []
        self.time_list = []
        self.past_label = None
        self.delete_log_file = False
        past_log_file = []
        if isToday == False:
            past_log_file = self.log_file.fetch()
            log_file_list = []
        else:
            log_file_list = self.log_file.fetch()
        if not past_log_file == []:
            last_entry_log_file = past_log_file[len(past_log_file)-1]
            temp, self.past_label = splice.splice(last_entry_log_file, ':', 'str')
            self.delete_log_file = True
        
        #?what is the point of this???
        #self.log_file.save('', sameLN=True)
        if log_file_list == None:
            log_file_list = []
        for i in log_file_list:
            study_time, label = splice.splice(i, ':', 'str')
            self.label_list.append(label)
            self.time_list.append(float(study_time))
        
        if not log_file_list == []:
            self.past_label = self.label_list[len(self.label_list)-1]
        
        self.count_one = len(self.time_list)
        #the same thing in time list
        self.pages_finished_first = self.pages_finished_full
        self.past_correct_len = self.correct_full
        self.past_incorrect_len = self.incorrect_full
        self.continuous_time_at_start = self.continuous_time
        self.last_session_at_start = self.past_points
        self.count = self.count_one
        if self.continuous_time == 0 and self.recess <= 0:
            self.recess = self.first_recess

        if float(self.recess) > 0:
            opening_string = f'\n>> There is unused rest: {self.recess} minutes\n'
        else:
            opening_string = ''

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
        self.study_content_file.save(what_to_write, lock=True)

        point_detail_file_data = self.point_detail_file.fetch()
        what_to_write = ''
        if not point_detail_file_data == []:
            what_to_write += f'\n\n\n'
        what_to_write += f'{"_" * 82}\n\nstarted : {started_time}'
        self.point_detail_file.save(what_to_write, lock=True)
    

    def rest(self, time_of_rest):
        self.manage_persistent_data.change_value({'recess_now': 0})
        self.manage_persistent_data.write_to_file()
        rest_session = work_ppl_rest.main_rest_class()
        #? i think its past points
        rest_session.get_values(time_of_rest, self.rest_time_points, self.REST_POINT_CONVERSION_RATE, self.email_on, self.MAX_DELETION_PERCENTAGE, self.past_points, self.music_content, self.music_on)
        minus_points = rest_session.rest_func()
        if minus_points == 'crash':
            self.write_study_content_file()
            self.manage_persistent_data.change_value({'current_points': self.past_points*self.MAX_DELETION_PERCENTAGE})
            self.manage_persistent_data.write_to_file()
            exit()

        self.past_points -= minus_points
        self.manage_persistent_data.change_value({'current_points': self.past_points})
    
    def ui_screen(self, ui_type):
        goal_dict = {'one_finish': self.pages_finished_session, 'right': self.correct_num_session, 'wrong': self.incorrect_num_session, 'new': self.new_num_session} #this is here because it doesn't work if i directly put it in the variable wtf why
        match ui_type:
            case 'session_ui':#main_ui
                print(END)
                progress, progressDict = goalProgress.get_goal_progress(self.goal, goal_dict)

                print(f'{self.count}回目( {self.label}-{self.study_time}分 ) ', end='')
                if self.swich_ui == 1:
                    print('\033[33m' + '総勉強時間モード' + END)
                else:
                    print()
                if not self.goal == 0:
                    percentageStr = f'目標時間の{self.showPercentage}%が終了 ({self.bonusPointPercentage}倍ボーナス)\n{self.encouragementWord}'
                    prints.progress(int(progress))
                    print()
                    print('~~~~~~~')
                    print(percentageStr)
                    print('~~~~~~~')
                    print()
                if self.name_task != None:
                    print()
                    print('\033[32m' + self.name_task + END + 'は"4/←"', end='')
                    print(f' ({progressDict['one_finish']['current']}', end='')
                if self.goal == 0:
                    pass
                elif self.name_task != None:
                    print(f'/{progressDict['one_finish']['required']}', end='')
                if self.name_task != None:
                    print(')')

                if self.name_correct != None:
                    print()
                    print('\033[32m' + self.name_correct + END + 'は"1/END"', end='')
                    print(f' ({progressDict['right']['current']}', end='')
                if self.goal == 0:
                    pass
                elif self.name_correct != None:
                    print(f'/{progressDict['right']['required']}', end='')
                if self.name_correct != None:
                    print(')')

                if self.name_incorrect != None:
                    print()
                    print('\033[32m' + self.name_incorrect + END +'は"2/↓"', end='')
                    print(f' ({progressDict['wrong']['current']}', end='')
                if self.goal == 0:
                    pass
                elif self.name_incorrect != None:
                    print(f'/{progressDict['wrong']['required']}', end='')
                if self.name_incorrect != None:
                    print(')')

                if self.name_new != None:
                    print()
                    print('\033[32m' + self.name_new + END + 'は"3/pgDn"', end='')
                    print(f' ({progressDict['new']['current']}', end='')
                if self.goal == 0:
                    pass
                elif self.name_new != None:
                    print(f'/{progressDict['new']['required']}', end='')
                if self.name_new != None:
                    print(')')

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
                    progress, progressDict = goalProgress.get_goal_progress(self.goal, goal_dict)
                    os.system('cls')
                    print(END)
                    print(f'{self.count}回目( {self.label}-{self.study_time}分 ) ')
                    if not self.goal == 0:
                        prints.progress(int(progress))
                    print()
                    if self.name_task != None:
                        print()
                        print(f'{self.name_task}：{self.pages_finished_session}', end='')
                    if self.goal == 0:
                        pass
                    elif self.name_task != None:
                        print(f'/{progressDict['one_finish']['required']}', end='')

                    if self.name_correct != None:
                        print()
                        print(f'{self.name_correct}：{self.correct_num_session}', end='')
                    if self.goal == 0:
                        pass
                        print(f'/{progressDict['right']['required']}', end='')

                    if self.name_incorrect != None:
                        print()
                        print(f'誤答：{self.incorrect_num_session}', end='')
                    if self.goal == 0:
                        pass
                    elif self.name_incorrect != None:
                        print(f'/{progressDict['wrong']['required']}', end='')
                    
                    if self.name_new != None:
                        print()
                        print(f'新規：{self.new_num_session}', end='')
                    if self.goal == 0:
                        pass
                    elif self.name_new != None:
                        print(f'/{progressDict['new']['required']}', end='')
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
                self.done_hour()
                print()
                print()
                print("ポイントの合計：", self.current_points)
                print()
                if self.pages_finished_full > 0:
                    print("TASK：" + str(self.pages_finished_full))
                if self.new_words_full > 0:
                    print(f"NEW：" + str(self.new_words_full) + "個")
                if self.correct_full > 0:
                    print(f"RIGHT：" + str(self.correct_full) + "個")
                if self.incorrect_full > 0:
                    print(f"WRONG：" + str(self.incorrect_full) + "個")
                print() 
                print()
                self.show_list()

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
        print_var = []
        error = False
        for command in output_keys:
            match command:
                case 'error':
                    prints.err(cli_output[command])
                    error = True
                case 'label':
                    self.label = cli_output[command]
                    print_var.append(self.label)
                case 'label_base':
                    self.label_base = cli_output[command]
                    print_var.append(self.label_base)
                case 'string_to_add_label':
                    if not self.label_base == None:
                        self.label = f'{self.label_base}{cli_output[command]}'
                        print_var.append(self.label)
                    else:
                        prints.err('base label does not exist')
                        error = True
                case 'same_label':
                    if not self.past_label == None:
                        self.label = self.past_label
                        print_var.append(self.label)
                    else:
                        error = True
                        prints.err('past label does not exist')
                case 'use_label':
                    if not self.recommended_label == None:
                        self.label = self.recommended_label
                        print_var.append(self.label)
                    else:
                        prints.err('label to use does not exist')
                        error = True
                case 'time':
                    self.study_time = cli_output[command]
                    print_var.append(self.study_time)
                case 'same_time':
                    if not self.last_study_time == None:
                        self.study_time = self.last_study_time
                        print_var.append(self.study_time)
                    else:
                        error = True
                        prints.err('past session does not exist')

                case 'overwrite_diary':
                    self.diary =  cli_output[command]
                    self.comment_list.append(self.diary)
                    self.comment_index = len(self.comment_list)-1
                    print_var.append(self.diary)

                case 'diary_written_time':
                    if self.comment_time == None:
                        self.comment_time = cli_output[command]

                case 'filename':
                    self.user_made_file = cli_output[command]
                    self.manage_settings_data.change_value({'filename': cli_output[command]})
                    self.user_made_file_content = file.content(self.user_made_dir, self.user_made_file)
                    self.comment_list = self.user_made_file_content.fetch()
                    self.comment_index = len(self.comment_list)-1

                case 'dirname':
                    self.user_made_dir = cli_output[command]
                    self.manage_settings_data.change_value({'dirname': cli_output[command]})

                case 'filetype':
                    self.filetype = cli_output[command]


                case 'file_content':
                    if self.filetype == None:
                        prints.err('please specify filetype')
                        return None
                    if not self.filetype == 'diary' and self.user_made_file == None:
                        prints.err('please specify file')
                        return None
                    self.comment_command_type = cli_output[command]

                    #it saves my progress
                    if not self.comment_command_type == 'save':
                        pass
                    elif self.filetype == 'diary':
                        self.diary = '\n'.join(self.comment_list)
                    elif self.filetype == 'goal':
                        comment = [f'{ilen+1}.{i}' for ilen, i in enumerate(self.comment_list)]
                        comment_string = '\n'.join(comment)
                        self.user_made_file_content.save(comment_string, overwrite=True, lock=True)
                    elif self.filetype == 'none':
                        comment_string = '\n'.join(self.comment_list)
                        self.user_made_file_content.save(comment_string, overwrite=True, lock=True)


                case 'move_file_index':
                    if cli_output[command] == 'go_back_to_original_place':
                        self.comment_index = len(self.comment_list)-1
                    elif cli_output[command] == 'go_to_head_of_index':
                        #bc it adds one in add_to_diary
                        self.comment_index = -1
                        print()
                        return None
                    elif int(cli_output[command]) >= len(self.comment_list):
                        prints.err('index number is too large')
                        return None
                    else:
                        self.comment_index = cli_output[command]
                    print(self.comment_list[self.comment_index])

                case 'add_comment':
                    if self.comment_command_type == None:
                        prints.err("execute F' command first")
                    elif self.comment_list == None:
                        prints.err('please write diary first')
                    elif self.comment_command_type == 'write':
                        self.comment_list.insert(self.comment_index+1, cli_output[command])
                        self.comment_index += 1
                    elif self.comment_command_type == 'change':
                        self.comment_list[int(self.comment_index)] = cli_output[command]
                    
                case 'remove_file_index':
                    if self.comment_list == None:
                        prints.err('no comment yet')
                        return None
                    #elif self.comment_command_type != 'change':
                    #    pass
                    elif cli_output == None:
                        pass
                    elif len(self.comment_list) != 0:
                        self.comment_list.pop(self.comment_index)
                        print_var.append(self.diary)

                case 'sound_on':
                    self.music_on = cli_output[command]
                    print_var.append(cli_output[command])
                    self.manage_settings_data.change_value({'music_on': self.music_on})
                case 'email_on':
                    self.email_on = cli_output[command]
                    print_var.append(cli_output[command])
                case 'start_session':
                    goals = {}
                    ready_to_start = True
                    if self.study_time == None:
                        ready_to_start = False
                        prints.err('please enter study time')
                        error = True
                    if self.label == None:
                        ready_to_start = False
                        prints.err('please enter label')
                        error = True
                    if self.goal == None:
                        ready_to_start = False
                        prints.err('please enter goal')
                        error = True
                    if self.add_point == None:
                        ready_to_start = False
                        prints.err('please enter point system')
                        error = True
                    if ready_to_start == True:
                        temp, goals = goalProgress.get_goal_progress(self.goal, {})#i dont need the session data, i just need the goals, but i don't want a tuple objects
                    
                    if ready_to_start == False:
                        pass
                    elif 'one_finish' in goals and self.name_task == None:
                        prints.err('choose name for task')
                        ready_to_start = False
                    elif 'new' in goals and self.name_new == None:
                        ready_to_start = False
                        prints.err('choose name for new')
                    elif 'right' in goals and self.name_correct == None:
                        ready_to_start = False
                        prints.err('choose name for correct_full')
                    elif 'wrong' in goals and self.name_incorrect == None:
                        ready_to_start = False
                        prints.err('choose name for incorrect_full')
                    elif ready_to_start == True:
                        self.manage_settings_data.write_to_file()
                        return True
                case 'points':
                    self.add_point = cli_output[command]
                    print_var.append(self.add_point)
                case 'show_study_time':
                    self.done_hour()
                case 'show_study_list':
                    self.show_list()
                case 'show_points':
                    if self.current_points >= self.past_points:
                        print(self.current_points)
                    elif self.current_points < self.past_points:
                        print(self.past_points)
                case 'show_goals':
                    print(str(self.goal))
                case 'show_comment':
                    print(self.diary)
                case 'show_file':
                    [print(f'{ilen}.{i}') for ilen, i in enumerate(self.comment_list)]
                case 'end_study':
                    os.system('cls')
                    return False
                case 'volume':
                    self.volume = cli_output[command]
                    print_var.append(self.volume)
                    self.manage_settings_data.change_value({'volume': self.volume})
                case 'change_sound':
                    temp_choose_music = self.music_content.chage_music()
                    choose_music = 'None'
                    if not choose_music == None:
                        choose_music = temp_choose_music

                    self.music_content.import_change(cli_output[command], temp_choose_music)
                    self.manage_settings_data.change_value({cli_output[command]: choose_music})
                    print_var.append(choose_music)
                case 'use_rest':
                    if self.recess >= 0 and self.count == self.count_one:
                        self.rest_time = self.recess
                        print('rest safely pending usage')
                        return 2
                case 'goal':
                    self.goal = cli_output[command]
                    print_var.append(str(self.goal))
                case 'goal_no_goal':
                    self.goal = 0
                    print_var.append('goal is None')
                case 'goal_same_goal':
                    if self.past_goal:
                       self.goal = self.past_goal
                       print_var.append(str(self.goal))
                    else:
                        prints.err('past goal does not exist')
                case 'goal_prompt':
                    self.temp_past_goal = cli_output[command]
                        
                case 'name_correct':
                    self.name_correct = cli_output[command]
                    print_var.append(cli_output[command])
                case 'name_incorrect':
                    self.name_incorrect = cli_output[command]
                    print_var.append(cli_output[command])
                case 'name_task':
                    self.name_task = cli_output[command]
                    print_var.append(cli_output[command])
                case 'name_new':
                    self.name_new = cli_output[command]
                    print_var.append(cli_output[command])

                case 'print':
                    if error == False:
                        print(print_string_true_false(temp_value, cli_output[command], print_var))

    def initialize_session(self):
        self.count = self.count + 1
        self.minute = 0
        self.tim_point = 0
        self.pages_finished_session = 0
        self.correct_num_session = 0
        self.incorrect_num_session = 0
        self.new_num_session = 0
        self.past_correct_len = self.correct_full
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
            JustInTimeStr = 'over time'
        elif self.last_study_time < CalTim - 5:
            JustInTimeDiv = self.last_study_time/CalTim
            JustInTimeStr = 'under time'
        
        original_time_point = self.totl_tim_point * self.DEVIDE_POINT_BY
        self.pointString = f'{original_time_point} points'
        if self.goal == 0:
            totl_tim_point_divided = original_time_point * JustInTimeDiv
            if JustInTimeDiv != 1:
                self.pointString += f' multiplied by {JustInTimeDiv} because you went {JustInTimeStr}'
        elif self.progress == 100:
            totl_tim_point_divided = original_time_point * self.bonusPointPercentage
            if self.bonusPointPercentage == 1:
                self.pointString += f', nothing else because you went over time'
            else:
                self.pointString += f' multiplied by {self.bonusPointPercentage}'
        else:
            print()
            totl_tim_point_divided = original_time_point * (self.progress/100)
            self.pointString += f' multiplied by {self.progress/100} because you didn\'t complete goal' 
        
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
            self.calculate_time_and_point()

            SWTMain = win32api.GetKeyState(0x67)
            if SWTMain < 0:
                self.swich_ui = num.cap(self.swich_ui+1, 3)
                self.print_minimal_ui = True
                sleep(0.1)

            if self.swich_ui == 2:
                self.ui_screen('minimal_session_ui')
            else:
                self.print_minimal_ui = False
                self.ui_screen('session_ui')
                
            one_finish = win32api.GetKeyState(0x64)
            if self.name_task == None:
                pass
            elif one_finish < 0:
                self.pages_finished_session += goal_add_value(1, self.name_task)
                self.print_minimal_ui = True
                self.finished_content_list.append('one_finish')
                keypres(1)

            right = win32api.GetKeyState(0x61)
            if self.name_correct == None:
                pass
            elif right < 0:                            
                self.correct_num_session += goal_add_value(1, self.name_correct)
                self.print_minimal_ui = True
                self.finished_content_list.append('right')
                keypres(1)

            wrong = win32api.GetKeyState(0x62)
            if self.name_incorrect == None:
                pass
            elif wrong < 0:
                self.incorrect_num_session += goal_add_value(1, self.name_incorrect)
                self.print_minimal_ui = True
                self.finished_content_list.append('wrong')
                keypres(1)
                    
            new = win32api.GetKeyState(0x63)
            if self.name_new == None:
                pass
            elif new < 0:
                self.new_num_session += goal_add_value(1, self.name_new)
                self.print_minimal_ui = True
                self.finished_content_list.append('new')
                keypres(1)

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
                self.pages_finished_session -= 1
                self.print_minimal_ui = True
                self.last_finished_content = None
                self.finished_content_list.pop(len(self.finished_content_list)-1)

            elif self.last_finished_content == 'right':
                self.correct_num_session -= 1
                self.print_minimal_ui = True
                self.last_finished_content = None
                self.finished_content_list.pop(len(self.finished_content_list)-1)

            elif self.last_finished_content == 'wrong':
                self.incorrect_num_session -= 1
                self.print_minimal_ui = True
                self.last_finished_content = None
                self.finished_content_list.pop(len(self.finished_content_list)-1)
                
            elif self.last_finished_content == 'new':
                self.new_num_session -= 1
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
                while msvcrt.kbhit():
                    msvcrt.getch()
                os.system('cls')
                while True:
                    self.progress, temp = goalProgress.get_goal_progress(self.goal, {'one_finish': self.pages_finished_session, 'right': self.correct_num_session, 'wrong': self.incorrect_num_session, 'new': self.new_num_session})
                    if self.progress != 100 and not self.goal == 0:
                        print("タスクがまだ完了していません。\n本当に", end='')
                    print("終了しますか +/-")
                    finish = input(">> ")
                    if finish == "":
                        os.system('cls')

                    elif finish == "-" or finish == "n":
                        sleep(0.1)
                        if self.swich_ui == 2:
                            self.print_minimal_ui = True
                        break
                    elif finish == '+' or finish == "y":
                        self.calculate_time_and_point()
                        self.manage_persistent_data.change_value({'continuous_time': self.continuous_time, 'new_words_full': self.new_words_full, 'correct_full': self.correct_full, 'incorrect_full': self.incorrect_full, 'pages_finished_full': self.pages_finished_full})

                        os.system('cls')
                        return True
                    else:
                        prints.err('input error')
                    os.system('cls')

    def wrap_up_session(self):

        self.pages_finished_dict[self.name_task] = self.pages_finished_session
        self.new_num_dict[self.name_new] = self.new_num_session
        self.correct_num_dict[self.name_correct] = self.correct_num_session
        self.incorrect_num_dict[self.name_incorrect] = self.incorrect_num_session

        self.pages_finished_full += self.pages_finished_session
        self.new_words_full += self.new_num_session
        self.correct_full += self.correct_num_session
        self.incorrect_full += self.incorrect_num_session


        self.name_task = None
        self.name_new = None
        self.name_correct = None
        self.name_incorrect = None

        if not self.temp_past_goal == None:
            self.past_goal = self.temp_past_goal
        self.temp_past_goal = None

        if self.is_using_music == True:
            self.music.stop()
        self.past_incorrect_len = self.incorrect_full
        self.actual_study_time = self.the_time #why does this need to do this 
        if not self.add_point == 0:
            self.continuous_time += self.the_time
            self.manage_persistent_data.change_value({'continuous_time': self.continuous_time, 'last_study_time': self.study_time, 'past_goal': self.past_goal})
        self.time_list.append(self.the_time/60)
        self.label_list.append(self.label)
        self.time_ended_list.append(return_time())

        if self.delete_log_file == True:
            self.log_file.delete_file()
            subprocess.check_call(["attrib","+H", 'REPORT\\logs\\progress.txt'])
        self.write_log_files()
        self.write_diary_file()
        self.past_label = self.label
        self.label = None


        self.diary = None
        self.comment_command_type = None
        self.comment_index = 0
        self.comment_list = []
        self.comment_time = None

        self.last_study_time = self.study_time
        self.study_time = None
        self.add_point = None
        self.goal = None
        os.system('cls')

    def handle_rest_time(self, recess):
        self.recess = recess
        self.manage_persistent_data.change_value({'current_points': self.current_points})
        if self.recess <= 0:
            return 0
        while True:
            self.ui_screen('ending_screen_ui')
            true_rest_time = CheckAnswer("何分休みますか？")

            true_rest_time = ReturnRest(true_rest_time, self.recess)

            if not true_rest_time == None:
                self.manage_persistent_data.change_value({'recess_now': true_rest_time})
                return true_rest_time
            prints.err('input error')
            true_rest_time = None
    
    def rest_time_to_points(self, rest_time):
        if self.recess > rest_time:
            self.current_points += (self.recess - rest_time) * self.REST_POINT_CONVERSION_RATE
            self.pointString += f' and {(self.recess - rest_time) * self.REST_POINT_CONVERSION_RATE} points added for giving up {(self.recess - rest_time)} minutes of rest time'
            self.manage_persistent_data.change_value({'current_points': self.current_points})
            self.manage_persistent_data.write_to_file()


    def chceck_if_continue(self, recess):
        self.recess = recess
        self.manage_persistent_data.write_to_file()
        while True:
            self.ui_screen('ending_screen_ui')
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
        self.write_study_content_file()
        self.write_point_detail_file()
        self.manage_persistent_data.write_to_file()

        while True:
            self.ui_screen('finished_study_ui')
            ok = input("\033[8m")
            os.system('cls')

    def error_has_occured(self):
        print(self.continuous_time)
        print(self.current_points)


if __name__ == '__main__':

    import math, msvcrt, os
    from funcs import prints, num, file, data, work_ppl_rest, play_music, command_console

    import datetime, time, win32api, subprocess
    from time import sleep
    from funcs import sendEmail, goalProgress, splice

    print("\033[8m")
    print("\033[0m")
    os.system('cls')

    Title = "WORK PPL"

    os.system("title " + Title)

    RED = '\033[31m'
    END = '\033[0m'

    now_start = datetime.datetime.today()
    started_time = str(now_start.time())[:8]
    today = str(now_start)[:10]

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
        full_recess = session.adjust_value()
        recess = session.handle_rest_time(full_recess)
        session.rest_time_to_points(recess)
        os.system('cls')
        continue_session = session.chceck_if_continue(recess)
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