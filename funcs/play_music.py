import subprocess, glob
from funcs import prints

class music:
    def __init__(self, using_instance_stduy, using_instance_rest, music_is_chosen):
        self.musicList = []
        self.music_folder = './REPORT\Music/'
        self.music_is_chosen = music_is_chosen
        self.using_instance_dict = {'choose_music_study': using_instance_stduy, 'choose_music_rest': using_instance_rest}

    def select_music_with_prompt(self, var, string, var2):
        self.musicList2 = []
        loopCounting = 0
        if var == None or len(var2) == 0:
            while True:
                subprocess.run("cls", shell=True)
                print('\033[1m' + str(string) + '\033[0m')
                print()
                if loopCounting >= 1:
                    prints.err('error')
                    print()
                print('It seems that there are more than two songs in the "Music" folder')
                print()
                print(">> Which song do you want to use :")
                print()
                loopCounting += 1
                var = music.chage_music(self)
                if not var == False:
                    
                    return var
        else:
            return var


    def import_music(self):
        stdymusicThereStart = []
        rstmusicThereStart = []      

        for name in glob.glob(self.music_folder + '*.wav'):
            self.musicList.append(name)

        for name in glob.glob(self.music_folder + '*.mp3'):
            self.musicList.append(name)
                    
        if self.using_instance_dict['choose_music_study'] == None:
            pass
        elif not self.using_instance_dict['choose_music_study'] == False:
            stdymusicThereStart = glob.glob(self.using_instance_dict['choose_music_study'], recursive=True)


        if self.using_instance_dict['choose_music_rest'] == None:
            pass
        elif not self.using_instance_dict['choose_music_rest'] == False:
            rstmusicThereStart = glob.glob(self.using_instance_dict['choose_music_rest'], recursive=True)

        if not len(stdymusicThereStart) == 0 and not len(rstmusicThereStart) == 0 or len(self.musicList) == 0:
            pass

        elif len(self.musicList) == 1:
            self.using_instance_dict['choose_music_study'] = self.musicList[0][2:]
            self.using_instance_dict['choose_music_rest'] = self.musicList[0][2:]

        elif self.music_is_chosen == True:
            pass
        else:
            self.using_instance_dict['choose_music_study'] = self.select_music_with_prompt(self.using_instance_dict['choose_music_study'], "For Ending Study", stdymusicThereStart)
            self.using_instance_dict['choose_music_rest'] = self.select_music_with_prompt(self.using_instance_dict['choose_music_rest'], "For Ending Rest", rstmusicThereStart)
        return self.using_instance_dict['choose_music_study'], self.using_instance_dict['choose_music_rest']
    
    def chage_music(self):
        for i in self.musicList:
            print(str(self.musicList.index(i) + 1) + "." + i[len(self.music_folder):])
        print(str(len(self.musicList) + 1) + "." + "None")

        print()
        whichSong = input(">> ")
        try:
            whichSong = int(whichSong)
        except:
            return False
        
        if whichSong == len(self.musicList) + 1:
            return None
        
        elif whichSong > len(self.musicList) or whichSong <= 0:
            return False
                            
        else:
            return self.musicList[whichSong-1][2:]
    
    def import_change(self, instance, value):
        self.using_instance_dict[instance] = value

    def set_song(self, using_instance_key, music_on):
        does_music_exist = []
        using_instance = self.using_instance_dict[using_instance_key]
        if using_instance != False:
            try:
                does_music_exist = glob.glob(using_instance, recursive=True)
            except:
                pass

        if using_instance == False or len(does_music_exist) == 0 or music_on == False:
            use_music = False
            using_instance = False

        else:
            use_music = True
        return use_music, using_instance