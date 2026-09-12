from funcs import prints, sendEmail
from time import sleep
import time, math, subprocess, win32api, msvcrt
from playsound3 import playsound

END = '\033[0m'
MAX_DELETION_PERCENTAGE = 0.45
POSTPONE_PENALTY = 1

class rest_elements:
    def __init__(self, REST_TIME, last_session_show):
        self.REST_TIME = REST_TIME
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

        elif self.the_rest_time >= (self.REST_TIME + POSTPONE_PENALTY) * 60 and (self.last_session_show * MAX_DELETION_PERCENTAGE) - self.minus_point > 0:
            pass

        elif self.the_rest_time >= (self.REST_TIME + POSTPONE_PENALTY) * 60 and (self.last_session_show * MAX_DELETION_PERCENTAGE) - self.minus_point <= 0:
            return True

    def rest_ui(self, rest_ui, color_for_rest_ui):
        print()
        print('\033[0m' + "ポイント：", self.last_session_show)
        print()
        print()
        print('休みが終わったら"' + color_for_rest_ui + '0/Ins' + END + '"キー')
        print()
        if rest_ui == 'rest_ui':
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
        self.minus_point = ((time.time() - self.rest_reset_time) - ((self.REST_TIME + POSTPONE_PENALTY) * 60)) * (self.last_session_show / 60)

        return self.the_rest_time, self.minus_point



class main_rest_class:
    def __init__(self):
        self.playing_music = None

    def get_values(self, REST_TIME, email_on, last_session_show, music_class, music_on):
        self.use_music, self.music_path = music_class.set_song('choose_music_rest', music_on)
        self.REST_TIME = REST_TIME
        self.EMAIL_ON = email_on
        self.last_session_show = last_session_show

    def rest_func(self):
        broken = 0
        clear_screen = 0
        minimal_screen = 0
        email_sent = False
        rest_finished = 0

        email_label = '【WORKPPL】REST HAS ENDED NOTIFICATION'
        email_body = f'休憩の{self.REST_TIME}分が終了しました\n勉強を再開してください'

        study_ended_email = sendEmail.EmailSender(email_label, email_body)
        rest_content = rest_elements(self.REST_TIME, self.last_session_show)

        while True:
            rest_content.calculate_time()
            if minimal_screen == 0:
                rest_content.rest_ui('rest_ui', '\033[1m')
            elif clear_screen == 0:
                subprocess.run("cls", shell=True)
                rest_content.rest_ui('minimal_rest_ui', '\033[1m')
                clear_screen= 1
            is_exit = rest_content.calculate_penalty_exit()
            if is_exit == True:
                return 'crash'
            the_rest_time, minus_point = rest_content.calculate_penalty()

            if not the_rest_time >= self.REST_TIME * 60:
                pass
            elif the_rest_time >= (self.REST_TIME + POSTPONE_PENALTY) * 60 and (self.last_session_show * MAX_DELETION_PERCENTAGE) - minus_point > 0:
                print(minus_point, 'ポイント引かれます')
            elif the_rest_time >= (self.REST_TIME + POSTPONE_PENALTY) * 60 and (self.last_session_show * MAX_DELETION_PERCENTAGE) - minus_point <= 0:
                pass
            elif self.EMAIL_ON == True and email_sent == False:
                email_sent = True
                try:
                    study_ended_email.sendEmail()
                except:
                    pass
            elif rest_finished == 1 and minimal_screen == 1:
                pass
            elif self.use_music == True and minimal_screen == 1:
                rest_finished = 1
                subprocess.run("cls", shell=True)
                rest_content.rest_ui('minimal_rest_ui', '\033[1m')
                print(0, 'ポイント引かれます')
                self.playing_music = playsound(self.music_path, block=False)
                self.use_music = False
            elif minimal_screen == 1:
                rest_finished = 1
                subprocess.run("cls", shell=True)
                rest_content.rest_ui('minimal_rest_ui', '\033[1m')
                print(0, 'ポイント引かれます')
            elif self.use_music == True:
                print(f'{(self.last_session_show * MAX_DELETION_PERCENTAGE) - minus_point}')
                print(0, 'ポイント引かれます')
                self.playing_music = playsound(self.music_path, block=False)
                self.use_music = False
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
                subprocess.run("cls", shell=True)
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
                        subprocess.run("cls", shell=True)
                        prints.err('input error')
            if minimal_screen == 0:
                subprocess.run("cls", shell=True)

            if broken ==1:
                subprocess.run("cls", shell=True)
                if self.playing_music != None:
                    self.playing_music.stop()

                        
                if minus_point > 0:
                    return minus_point
                return 0
