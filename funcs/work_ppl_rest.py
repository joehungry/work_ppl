from funcs import prints, sendEmail
from time import sleep
import time, math, os, win32api, msvcrt

END = '\033[0m'

class rest_elements:
    def __init__(self, POSTPONE_PENALTY, MAX_DELETION_PERCENTAGE, REST_TIME, last_session_show, REST_TIME_POINTS, REST_POINT_CONVERSION_RATE):
        self.REST_TIME = REST_TIME
        self.POSTPONE_PENALTY = POSTPONE_PENALTY
        self.MAX_DELETION_PERCENTAGE = MAX_DELETION_PERCENTAGE
        self.REST_TIME_POINTS = REST_TIME_POINTS
        self.REST_POINT_CONVERSION_RATE = REST_POINT_CONVERSION_RATE
        self.rest_start_time = time.time()
        self.rest_reset_time = time.time()
        self.last_session_show = last_session_show

        sleep(0.1)

    def calculate_time(self):
        self.the_rest_time = time.time() - self.rest_start_time
        self.rest_time_left = self.REST_TIME * 60 - self.the_rest_time + 1
        self.rest_minute = math.floor(self.rest_time_left/60)
        self.rest_second = math.floor(self.rest_time_left) - self.rest_minute * 60

    def calculate_penalty_exit(self):
        if not self.the_rest_time >= self.REST_TIME * 60:
            pass

        elif self.the_rest_time >= (self.REST_TIME + self.POSTPONE_PENALTY) * 60 and (self.last_session_show * self.MAX_DELETION_PERCENTAGE) - self.minus_point > 0:
            pass

        elif self.the_rest_time >= (self.REST_TIME + self.POSTPONE_PENALTY) * 60 and (self.last_session_show * self.MAX_DELETION_PERCENTAGE) - self.minus_point <= 0:
            return True

    def rest_ui(self, rest_ui, color_for_rest_ui):
        match rest_ui:
            case 'minimal_rest_ui':
                print()
                print('\033[0m' + "ポイント：", (self.last_session_show + self.REST_TIME_POINTS * self.REST_POINT_CONVERSION_RATE))
                print()
                print()
                print('休みが終わったら"' + color_for_rest_ui + 'end' + END + '"キー')

            case 'rest_ui':
                print()
                print('\033[0m' + "ポイント：", (self.last_session_show + self.REST_TIME_POINTS * self.REST_POINT_CONVERSION_RATE))
                print()
                print()
                print('休みが終わったら"' + color_for_rest_ui + 'end' + END + '"キー')
                print()
                if self.rest_time_left >= 0:
                    print(self.rest_minute, "分", self.rest_second, "秒")

                elif self.rest_time_left > self.the_rest_time:
                    print(self.rest_minute, "分", self.rest_second, "秒")
                else:
                    print("0 分 0 秒")
                print()
                recess_sec, recess_min = math.modf(self.REST_TIME) #REST_TIME is a local variable in rest
                print()
                print(f'最大休憩時間は {int(recess_min)}分 {int(recess_sec * 60)}秒')

                print()

    
    def calculate_penalty(self):
        self.minus_point = ((time.time() - self.rest_reset_time) - ((self.REST_TIME + self.POSTPONE_PENALTY) * 60)) * (self.last_session_show / 60)

        return self.the_rest_time, self.minus_point



class main_rest_class:
    def __init__(self):
        pass
    def get_values(self, REST_TIME, REST_TIME_POINTS, REST_POINT_CONVERSION_RATE, email_on, MAX_DELETION_PERCENTAGE, last_session_show, music_class, music_on):
        self.use_music, self.IS_USING_MUSIC, self.MUSIC = music_class.set_song('choose_music_rest', music_on)
        self.POSTPONE_PENALTY = 1
        self.MAX_DELETION_PERCENTAGE = MAX_DELETION_PERCENTAGE
        self.REST_TIME = REST_TIME
        self.EMAIL_ON = email_on
        self.REST_TIME_POINTS = REST_TIME_POINTS
        self.REST_POINT_CONVERSION_RATE = REST_POINT_CONVERSION_RATE
        self.last_session_show = last_session_show


        
    def rest_func(self):
        broken = 0
        clear_screen = 0
        minimal_screen = 0
        email_sent = False
        self.POSTPONE_PENALTY = 1
        rest_finished = 0
        #MAX_DELETION_PERCENTAGE = 0.45

        email_label = '【WORKPPL】REST HAS ENDED NOTIFICATION'
        email_body = f'休憩の{self.REST_TIME}分が終了しました\n勉強を再開してください'

        study_ended_email = sendEmail.EmailSender(email_label, email_body)
        rest_content = rest_elements(self.POSTPONE_PENALTY, self.MAX_DELETION_PERCENTAGE, self.REST_TIME, self.last_session_show, self.REST_TIME_POINTS, self.REST_POINT_CONVERSION_RATE)

        while True:
            rest_content.calculate_time()
            if minimal_screen == 0:
                rest_content.rest_ui('rest_ui', '\033[1m')
            elif clear_screen == 0:
                os.system('cls')
                rest_content.rest_ui('minimal_rest_ui', '\033[1m')
                clear_screen= 1
            is_exit = rest_content.calculate_penalty_exit()
            if is_exit == True:
                return 'crash'
            the_rest_time, minus_point = rest_content.calculate_penalty()

            if not the_rest_time >= self.REST_TIME * 60:
                pass
            elif the_rest_time >= (self.REST_TIME + self.POSTPONE_PENALTY) * 60 and (self.last_session_show * self.MAX_DELETION_PERCENTAGE) - minus_point > 0:
                print(minus_point, 'ポイント引かれます')
            elif the_rest_time >= (self.REST_TIME + self.POSTPONE_PENALTY) * 60 and (self.last_session_show * self.MAX_DELETION_PERCENTAGE) - minus_point <= 0:
                pass
            elif self.EMAIL_ON == True and email_sent == False:
                email_sent = True
                try:
                    study_ended_email.sendEmail()
                except:
                    pass
            elif rest_finished == 1 and minimal_screen == 1:
                pass
            elif self.use_music == 1 and minimal_screen == 1:
                rest_finished = 1
                os.system('cls')
                rest_content.rest_ui('minimal_rest_ui', '\033[1m')
                print(0, 'ポイント引かれます')
                self.MUSIC.play()
                self.use_music = 0
            elif minimal_screen == 1:
                rest_finished = 1
                os.system('cls')
                rest_content.rest_ui('minimal_rest_ui', '\033[1m')
                print(0, 'ポイント引かれます')
            elif self.use_music == 1:
                print(f'{(self.last_session_show * self.MAX_DELETION_PERCENTAGE) - minus_point}')
                print(0, 'ポイント引かれます')
                self.MUSIC.play()
                self.use_music = 0
            else:
                print(0, 'ポイント引かれます')

            sleep(0.02)

            noScreenEnter = win32api.GetKeyState(0x2E)
            if noScreenEnter < 0:
                clear_screen = 0
                minimal_screen = 1
            stop = win32api.GetKeyState(0x60)
            if stop < 0:
                print("\033[8m")
                os.system('cls')
                while msvcrt.kbhit():
                    msvcrt.getch()
                while True:
                    if minimal_screen == 0:
                        rest_content.rest_ui('rest_ui', END)
                    else:
                        rest_content.rest_ui('minimal_rest_ui', END)
                    rest_done = input("[Enter / - (key) 押す]")
                    sleep(0.14)
                    if rest_done == '' or rest_done == 'y' or rest_done == "+":
                        rest_content.calculate_time()
                        is_exit = rest_content.calculate_penalty_exit()
                        if is_exit == True:
                            return 'crash'
                        the_rest_time, minus_point = rest_content.calculate_penalty()
                        sleep(0.15)
                        broken = 1
                        break

                    elif rest_done == "-" or rest_done == "n":
                        clear_screen = 0
                        minimal_screen = 0
                        sleep(0.1)
                        break
                    else:
                        prints.err('input error')
            if minimal_screen == 0:
                os.system('cls')

            if broken ==1:
                os.system('cls')
                if self.IS_USING_MUSIC == True:
                    self.MUSIC.stop()
                        
                if minus_point > 0:
                    return minus_point
                return 0
