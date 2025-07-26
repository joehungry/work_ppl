try:
    from funcs import splice, num
except:
    import splice, num
pastGoal = None
#======

def removeUnneededSpace(originalString):
    if originalString == '':
        pass
    elif originalString[len(originalString)-1] == ' ' and originalString[0] == ' ':
        return originalString[1:len(originalString)-1]
    elif originalString[len(originalString)-1] == ' ':
        return originalString[:len(originalString)-1]
    elif originalString[0] == ' ':
        return originalString[1:]
    else:
        return originalString

def breakdownParentheses(oringinalString):
    resultString = ''
    for i in oringinalString:
        if i == '(':
            #this is += so that if the input is nested like (task = d or (c = 2 and x=0)), it would still understand it or something
            resultString = ''
        elif i == ')':
            return resultString
        else:
            resultString += i


def breakdownGoalSingleInput(goalInput):
    goalCommand = {"new": 'new', 'nw': 'new', "correct": 'right', "c": 'right', "C": 'right', "incorrect": 'wrong', "x": 'wrong', "X": 'wrong', "solve": ['right, wrong'], "sv": ['right', 'wrong'], "SV": ['right', 'wrong'], "task": 'one_finish', "t": 'one_finish', "T": 'one_finish'}

    tempGoalName = None
    tempGoalQuota = None
    goalNameList = []
    goalQuota = None
    tempGoalNameList = []
    if ',' in goalInput:
        tempGoalNameList = splice.toList(goalInput, ',', 'str')
        goalName, tempGoalQuota = splice.splice(tempGoalNameList[len(tempGoalNameList)-1], '=', 'str')
        tempGoalNameList.pop(len(tempGoalNameList)-1) #bc the last element in goalInput is always the has the quota
        tempGoalNameList.append(goalName)#i know i can just fucking separate the last element but im just laz
    elif not '=' in goalInput:
        tempGoalNameList.append(goalInput)
        tempGoalQuota = 1
    else:
        goalNameRaw, goalQuotaRaw = splice.splice(goalInput, '=', 'str')
        tempGoalName = removeUnneededSpace(goalNameRaw)
        tempGoalQuota = removeUnneededSpace(goalQuotaRaw)
        tempGoalNameList.append(tempGoalName)
        goalNameList = []
    for i in tempGoalNameList:
        if not i in goalCommand:
            goalNameList = []
            break
        else:
            goalNameList.append(goalCommand[i])
        if tempGoalQuota == 'd' or tempGoalQuota == 'done':
            goalQuota = 1
        elif num.isNum(tempGoalQuota):
            goalQuota = int(tempGoalQuota)
    return goalNameList, goalQuota


def mergeConnectedElements(originalString):
    tokens = []
    tokenMergeList = []
    for ilen, i in enumerate(originalString):
        if i == '=':
            tokenMergeList.append(f'f{ilen-1}')
        elif i[0] == '=':
            tokenMergeList.append(f'l{ilen-1}')
        elif i[len(i)-1] == '=' and not ilen == len(originalString)-1:#so that it doesnt bug and say 'noooo its out of range waaaaa' in the next for loop
            tokenMergeList.append(f'r{ilen}')


    #connects elements if '=' in there so, "a", "=", "b" would become "a=b"
    skip = 0
    tokens = []
    positionList = [int(i[1:]) for i in tokenMergeList]
    for ilen, i in enumerate(originalString):
        mergeType = None
        if not ilen in positionList:
            pass
        else:
            mergeType = tokenMergeList[positionList.index(ilen)][0]

        if mergeType == None and not skip == 0:
            skip -= 1
        elif mergeType == None:
            tokens.append(i)

        if mergeType == 'f':
            mergedParts = ''.join(originalString[ilen:ilen+3])
            tokens.append(mergedParts)
            skip = 2
        elif mergeType == 'l':
            mergedParts = ''.join(originalString[ilen:ilen+2])
            tokens.append(mergedParts)
            skip = 1
        elif mergeType == 'r':
            mergedParts = ''.join(originalString[ilen:ilen+2])
            tokens.append(mergedParts)
            skip = 1
    
    completedTokens = []
    saveIndex = None
    for ilen, i in enumerate(tokens):
        if i == '(':
            saveIndex = ilen+1 #bc i dont need to save '(', i just need the variable names
        elif ')=' in i and saveIndex != None:#bc if )=1 is there that means that the variables are treated in the same place
            tempVar = ''
            for num in range(saveIndex, ilen):#ts messy af i know, but its just cecking if 
                completedTokens.pop(len(completedTokens)-1)#this just pops the last index in completedTokens bc you dont need the last 'num' amount of indexes, bc i join it here
                if not tokens[num] == 'and' and not tokens[num] == 'or':
                    tempVar += tokens[num]
                    if not num == ilen-1:
                        tempVar += ','
            garbage, goalNumber = splice.splice(i, '=', 'str')
            tempVar += f'={goalNumber}'
            completedTokens.append(tempVar)
        else:
            completedTokens.append(i)

    return completedTokens

def breakdownAndOr(tokens):
    # This function processes a flat list of tokens and groups them by 'and'
    and_groups = []
    current_group = []
    for token in tokens:
        if token == 'and':
            and_groups.append(current_group)
            current_group = []
        else:
            current_group.append(token)
    and_groups.append(current_group)

    parsed_groups = []
    for group in and_groups:
        if not group: continue
        # If a group is a list, it's a nested structure from parentheses
        if isinstance(group[0], list):
            parsed_groups.append(group[0])
        else:
            # It's a simple command like 'c=2'
            goalName, goalQuota = breakdownGoalSingleInput(" ".join(group))
            if goalName:
                parsed_groups.append({'goalName': goalName, 'goalQuota': goalQuota})

    return parsed_groups


def breakdownGoalInput(originalString, ComIsTrue):
    ComIsTrue = ComIsTrue
    stirng = originalString.replace('(', ' ( ').replace(')', ' ) ')
    tokensRaw = splice.toList(stirng, ' ', 'str')
    tokensRaw = [i for i in tokensRaw if not i == '']
    tokens = mergeConnectedElements(tokensRaw)
    # This list will act as a stack to handle nested structures
    stack = [[]]
    for token in tokens:
        if token == '(':
            # Start a new level of nesting
            stack.append([])
        elif token == ')':
            # End of a nesting level
            if len(stack) < 2:
                ComIsTrue = None
                break
            # Pop the completed group, parse it, and append it to the parent level
            finished_group = stack.pop()
            # Process the 'or' logic within the group
            or_groups = []
            current_or_group = []
            for item in finished_group:
                if item == 'or':
                    or_groups.append(breakdownAndOr(current_or_group))
                    current_or_group = []
                else:
                    current_or_group.append(item)
            or_groups.append(breakdownAndOr(current_or_group))
            
            # Simplify if it's not a real 'or' group
            if len(or_groups) == 1:
                stack[-1].append(or_groups[0])
            else:
                stack[-1].append(or_groups)

        else:
            # Add the token to the current nesting level
            stack[-1].append(token)

    if len(stack) != 1:
        ComIsTrue = None

    # Final processing of the top-level string
    final_tokens = stack[0]
    or_groups = []
    current_or_group = []
    for item in final_tokens:
        if item == 'or':
            or_groups.append(breakdownAndOr(current_or_group))
            current_or_group = []
        else:
            current_or_group.append(item)
    or_groups.append(breakdownAndOr(current_or_group))

    # Final simplification
    if len(or_groups) == 1:
        return or_groups[0], ComIsTrue
    else:
        return or_groups, ComIsTrue






if __name__ == '__main__':
    print(breakdownGoalInput('new = 2 or t=2', 'ABCDE'))
