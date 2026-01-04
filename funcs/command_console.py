import datetime
try:
    from funcs import num, splice, goalLanguage

except:
    import num, splice, goalLanguage

today = datetime.datetime.now()
today_foratted = today.strftime('%Y-%m-%d')

def check_value_preset(command, value_preset_dict):
    if command in value_preset_dict:
        return value_preset_dict[command]
    return None
    

def check_time_value(time_value):
    time_list = time_value.split(' ')
    return_list = []
    skip = 0
    for ilen, i in enumerate(time_list):
        if skip != 0:
            skip -= 1
        #bc i need three elements of a list to do the next step, i just tell the program to not bother
        elif time_list[len(time_list)-1] == i or time_list[len(time_list)-2] == i:
            return_list.append(i)
        #makes element one (1*h is one element)
        elif time_list[ilen+1] == '*':
            return_list.append(''.join([i, time_list[ilen+1], time_list[ilen+2]]))
            skip = 2
        else:
            return_list.append(i)

    return_time = 0
    for i in return_list:
        if '*' in i:
            temp_number, unit = splice.splice(i, '*', 'str')
            number = float(temp_number)
        else:
            number = float(i)
            unit = 'm'
        if num.isNum(number) == False:
            pass
        elif unit == 'm':
            return_time += number
        elif unit == 'h':
            return_time += number*60
        elif unit == 's':
            return_time += number/60
    return return_time

def splice_command(splice_sign, command_input, command_dict):
    temp_command_key = None
    command_key = None
    command_value = None
    original_command_key = None
    if splice_sign == '':
        temp_command_key = command_input

    elif splice_sign in command_input:
        temp_command_key, command_value = splice.splice(command_input, splice_sign, 'str')
    if temp_command_key == None:
        pass
    elif temp_command_key in command_dict:
        original_command_key = temp_command_key
        command_key = command_dict[temp_command_key]
    return original_command_key, command_key, command_value

def turn_on(variable_name, command_value, local_preset, preset_content, temp_value):
    returnDict = {}
    preset_value = check_value_preset(command_value, local_preset)
    if not preset_value == None:
        returnDict = preset_content[preset_value]
        returnDict['print'] = f'{variable_name} is {temp_value}'
        return returnDict


class command_executor:
    def __init__(self, temp_value):
        self.value_preset_dict = {'s': 'same_content', 'n': 'no_content', 'u':'use_content'}
        self.temp_value = temp_value

    def set_label(self, command_key, command_value):#make it print \nL'{label}\n
        value_preset_content = {'same_content': {'same_label': None}, 'no_content': {}, 'use_content': {'use_label': None}}
        preset_value = None
        return_dict = {}
        if '\\' in command_value:#command_value[1:] is bc of L'\s "\" part. i dont need this part
            preset_value = check_value_preset(command_value[1:], self.value_preset_dict)
        if not preset_value == None:
            return_dict = value_preset_content[preset_value]
        if preset_value == None:
            return_dict['label'] = command_value
        if not return_dict == {}:
            return_dict['print'] = f'{self.temp_value}'
            return return_dict

    def set_time(self, command_key, command_value):
        value_preset_content = {'same_content': {'same_time': None}, 'no_content': {}, 'use_content': {}}
        preset_value = None
        if '\\' in command_value:
            preset_value = check_value_preset(command_value[1:], self.value_preset_dict)
        if '*' in command_value:
            command_value = check_time_value(command_value)
        if not preset_value == None:
            return value_preset_content[preset_value]
        elif num.isNum(command_value) == False:
            pass
        elif not float(command_value) == 0:
            return {'time': float(command_value)}
        return {'error': 'time must be number'}

    def set_time_label(self, command_key, command_value):
        value_preset_content = {'same_content': {'same_label': None, 'same_time': None}, 'no_content': {}, 'use_content': {}}
        preset_value = None
        return_dict = {}
        if '\\' in command_value:
            preset_value = check_value_preset(command_value[1:], self.value_preset_dict)
        if not preset_value == None:
            return_dict = value_preset_content[preset_value]
        if preset_value == None and num.isNum(command_value) == True:
            return_dict['label'] = command_value
            return_dict['time'] = float(command_value)
        if not return_dict == {}:
            return_dict['print'] = f'{self.temp_value} {self.temp_value}分'
            return return_dict
        return {'error': 'time must be number'}
        
    def change_file_command_type(self, command_key, command_value):
        return_dict = {}
        diary_type = {'write': 'write', 'w': 'write', 'change': 'change', 'c': 'change', 'save': 'save', 'sv': 'save'} 
        index_moving = {'back': 'go_back_to_original_place', 'r': 'go_back_to_original_place',
                         'return': 'go_back_to_original_place', 'top': 'go_to_head_of_index', 't': 'go_to_head_of_index', }
        type_preset_value = check_value_preset(command_value, diary_type)
        index_preset_vale = check_value_preset(command_value, index_moving)
        if not type_preset_value == None:
            return_dict['file_content'] = type_preset_value
        elif not index_preset_vale == None:
            return_dict['move_file_index'] = index_preset_vale
        elif num.isInt(command_value):
            return_dict['move_file_index'] = int(command_value)
        if not return_dict == {}:
            return return_dict
    
    def add_comment(self, command_key, command_value):
        return {'add_comment': command_value}
    
    def remove_file_index(self, command_key, command_value):
        return {'remove_file_index': None}
    
    def overwrite_diary(self, command_key, command_value):
        today = datetime.datetime.now()
        today_foratted = today.strftime('%Y-%m-%d %H:%M:%S')
        return {'overwrite_diary': command_value, 'diary_written_time': today_foratted}
        
    def turn_sound_on(self, command_key, command_value):#make it print sound is on
        local_preset = {'on': 'sound_on', 'off': 'sound_off'}
        preset_content = {'sound_on': {'sound_on': True}, 'sound_off': {'sound_on': False}}
        return turn_on('sound', command_value, local_preset, preset_content, self.temp_value)
    
    def turn_email_on(self, command_key, command_value):
        local_preset = {'on': 'email_on', 'off': 'email_off'}
        preset_content = {'email_on': {'email_on': True}, 'email_off': {'email_on': False}}
        return turn_on('email', command_value, local_preset, preset_content, self.temp_value)
    
    def start_session(self, command_key, command_value):
        return {'start_session': None}
    
    def add_to_past_label(self, command_key, command_value):
        return {'string_to_add_label': command_value, 'print': f'{self.temp_value}'}
    
    def set_label_base(self, command_key, command_value):
        return {'label_base': command_value, 'print': f'{self.temp_value}'}
    
    def set_points(self, command_key, command_value):
        local_preset = {None: 'points_on', 'on': 'points_on', 'off': 'points_off', 'no': 'points_off'}
        preset_content = {'points_on': {'points': 1}, 'points_off': {'points': 0}}
        return turn_on('point system', command_value, local_preset, preset_content, self.temp_value)
    
    def show_value(self, command_key, command_value):
        local_preset = {'study time': 'study_time', 'time': 'study_time',
                         'study list': 'study_list', 'list': 'study_list',
                         'point': 'points', 'points': 'points',
                         'goal': 'goals', 'goals': 'goals', 'diary': 'comment', 
                         'comment': 'comment', 'file': 'file', 'f': 'file'}
        if command_value in local_preset:
            return {f'show_{local_preset[command_value]}': None}
    
    def end_something(self, command_key, command_value):
        local_preset = {'study': 'study'}
        if command_value in local_preset:
            return {f'end_{local_preset[command_value]}': None}
        
    def change_sound_volume(self, command_key, command_value):
        if num.isNum(command_value) == False:
            return {'error': 'volume must be a number'}
        volume = float(command_value)
        if volume >= 0 and volume < 101:
            return {'volume': int(command_value), 'print': f'volume = {self.temp_value}'}
        return {'error': 'volume must be within 0 and 100'}
    
    def change_settings(self, command_key, command_value):
        local_preset_sound = {'sound rest': 'choose_music_rest', 'sound study': 'choose_music_study'}
        if command_value in local_preset_sound:
            return {f'change_sound': local_preset_sound[command_value]}
        
    def use_content(self, command_key, command_value):
        local_preset = {'unused rest': 'rest', 'rest': 'rest', 'reccomended label': 'label', 'label': 'label'}
        comment_preset = {'rest': 'this would not print because rest returns be4 this comes', 
                          'label': f'{self.temp_value}'}
        if command_value in local_preset:
            return {f'use_{local_preset[command_value]}': None, 'print': comment_preset[local_preset[command_value]]}

    def set_goal(self, command_key, command_value):
        return_dict = {}
        goal = None
        local_preset = {'\\n': 'no_goal', 'none': 'no_goal', 'n': 'no_goal',
                        '\\s': 'same_goal', 's': 'same_goal', 'same': 'same_goal'}
        if command_value in local_preset:
            return_dict = {f'goal_{local_preset[command_value]}': None}
            goal = True
        else:
            goal = goalLanguage.breakdownGoalInput(command_value)
            return_dict = {'goal': goal, 'goal_prompt': command_value}
        if goal == None or goal == []:
            pass
        else:
            return_dict['print'] = f'{self.temp_value}'
            return return_dict
        
    def set_filetype(self, command_key, command_value):
        local_preset = {'goal': 'goal', 'g': 'goal', 'd': 'diary', 'diary': 'diary', 'none': 'none', 'free': 'none', 'n': 'none'}
        if command_value in local_preset:
            return {'filetype': local_preset[command_value]}
        
    def choose_file(self, command_key, command_value):
        if '.' in command_value:
            return {'filename': command_value}
    
    def choose_dir(self, command_key, command_value):
        return {'filedir': command_value}
    
    def change_goal_name(self, command_key, command_value):
        return_value_dict = {}
        local_preset = {'C': 'correct', 'X': 'incorrect', 'TK': 'task', 'TSK': 'task', 'NW': 'new'}
        value_preset_content = {'same_content': {'same_content': "same_"}, 'no_content': {}, 'use_content': {}}
        goal_to_change = ""
        if '\\' in command_value:#command_value[1:] is bc of L'\s "\" part. i dont need this part
            preset_value_dict = check_value_preset(command_value[1:], self.value_preset_dict)
            goal_to_change = 'same_' #so that it adds same_ when making the same thing i know its conveluted
            command_value = None
        goal_to_change += local_preset[command_key]
        return {"name_goal": f'{goal_to_change}:{command_value}', "print": f'{local_preset[command_key]} is {self.temp_value}'}

class cli:
    def __init__(self, temp_value):
        self.colon_split_command_dict = {'L': 'set_label', 'L+':'add_to_past_label', 'T': 'set_time', 'D': 'overwrite_diary', 'F': 'change_file_command_type', 
                                         'F+': 'add_comment', 'F-': 'remove_file_index',
                                         'S': 'turn_sound_on', 'TL': 'set_time_label', 'LT': 'set_time_label', 
                                         'p': 'set_points', 'P': 'set_points', 'Lb': 'set_label_base', 
                                         'C': 'change_goal_name', 'X': 'change_goal_name', 'TK': 'change_goal_name',  'TSK': 'change_goal_name', 
                                         'NW': 'change_goal_name'}
        self.no_split_command_dict = {'p': 'set_points', 'P': 'set_points', 'start': 'start_session', '': 'start_session', 
                                         'F-': 'remove_file_index'}
        self.space_split_command_dict = {'sound': 'turn_sound_on', 'email': 'turn_email_on', 'mail': 'turn_email_on',
                                         'show': 'show_value', 'end': 'end_something', 'volume': 'change_sound_volume',
                                         'change': 'change_settings', 'use': 'use_content', 'goal': 'set_goal', 'g': 'set_goal', 
                                         'filetype': 'set_filetype', 'open': 'choose_file', 'dir': 'choose_dir'}
        execute = command_executor(temp_value)
        self.command_content_dict = {'set_label': execute.set_label, 'set_time': execute.set_time, 'change_file_command_type': execute.change_file_command_type, 
                                     'turn_sound_on': execute.turn_sound_on, 'turn_email_on': execute.turn_email_on, 
                                     'start_session': execute.start_session, 'add_to_past_label': execute.add_to_past_label,
                                     'set_time_label': execute.set_time_label, 'set_points': execute.set_points, 'show_value': execute.show_value,
                                     'end_something': execute.end_something, 'change_sound_volume': execute.change_sound_volume,
                                     'change_settings': execute.change_settings, 'use_content': execute.use_content, 'set_goal': execute.set_goal,
                                     'add_comment': execute.add_comment, 'remove_file_index': execute.remove_file_index, 'overwrite_diary': execute.overwrite_diary,
                                     'choose_file': execute.choose_file, 'choose_dir': execute.choose_dir, 'set_filetype': execute.set_filetype, 
                                     'set_label_base': execute.set_label_base, 'change_goal_name': execute.change_goal_name}
        self.command_key = None
        self.command_value = None


    def get_command(self, command_input):
        temp_original_key, temp_command_key, temp_command_value = splice_command('\'', command_input, self.colon_split_command_dict)
        if not temp_command_key == None:
            self.command_key = temp_command_key
            self.command_value = temp_command_value
            self.original_key = temp_original_key
        temp_original_key, temp_command_key, temp_command_value = splice_command(' ', command_input, self.space_split_command_dict)
        if not temp_command_key == None:
            self.command_key = temp_command_key
            self.command_value = temp_command_value
            self.original_key = temp_original_key
        temp_original_key, temp_command_key, temp_command_value = splice_command('', command_input, self.no_split_command_dict)
        if not temp_command_key == None:
            self.command_key = temp_command_key
            self.original_key = temp_original_key
        
    def execute_command(self):
        #print(self.command_key, self.command_value)
        #input()
        if not self.command_key == None:
            return self.command_content_dict[self.command_key](self.original_key, self.command_value)


if __name__ == '__main__':
    cli_test = cli('$')
    cli_test.get_command('NW\'ページ数')
    print(cli_test.execute_command())
