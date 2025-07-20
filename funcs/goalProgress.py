# Version 2.0 - Debugging Enabled

def get_goal_progress(parsed_goal_structure, session_data, indent=0):
    indent_str = "  " * indent
    #print(f"{indent_str}Entering get_goal_progress with: {parsed_goal_structure}")
    #print(f"{indent_str}Session Data: {session_data}")

    if isinstance(parsed_goal_structure, list):
        or_group_progresses = []
        for i, element in enumerate(parsed_goal_structure):
            #print(f"{indent_str}  Processing element {i}: {element}")
            if isinstance(element, list):
                # This element is an AND group (or a nested OR/AND structure)
                and_group_progresses = []
                for j, condition in enumerate(element):
                    #print(f"{indent_str}    Processing AND condition {j}: {condition}")
                    and_group_progresses.append(get_goal_progress(condition, session_data, indent + 2))
                
                min_progress = min(and_group_progresses) if and_group_progresses else 0.0
                ##print(f"{indent_str}  AND group progresses: {and_group_progresses}, min: {min_progress}")
                or_group_progresses.append(min_progress)
            elif isinstance(element, dict):
                # This element is a single goal condition
                single_progress = get_single_goal_progress(element, session_data, indent + 2)
                #print(f"{indent_str}  Single goal progress: {single_progress}")
                or_group_progresses.append(single_progress)
            else:
                #print(f"{indent_str}  Unexpected element type: {type(element)}")
                or_group_progresses.append(0.0)

        max_progress = max(or_group_progresses) if or_group_progresses else 0.0
        #print(f"{indent_str}OR group progresses: {or_group_progresses}, max: {max_progress}")
        #print(f"{indent_str}Exiting get_goal_progress (list) with: {max_progress}")
        return max_progress

    elif isinstance(parsed_goal_structure, dict):
        progress = get_single_goal_progress(parsed_goal_structure, session_data, indent + 1)
        #print(f"{indent_str}Exiting get_goal_progress (dict) with: {progress}")
        return progress

    #print(f"{indent_str}Exiting get_goal_progress (unexpected) with: 0.0")
    return 0.0 # Default for unexpected input

def get_single_goal_progress(goal_dict, session_data, indent=0):
    indent_str = "  " * indent
    #print(f"{indent_str}Entering get_single_goal_progress with: {goal_dict}")
    #print(f"{indent_str}Session Data: {session_data}")

    goal_names = goal_dict.get('goalName', [])
    goal_quota = goal_dict.get('goalQuota')

    if goal_quota == 'd' or goal_quota == 'done':
        goal_quota = 1
    else:
        try:
            goal_quota = int(goal_quota)
        except (ValueError, TypeError):
            #print(f"{indent_str}  Invalid goal_quota: {goal_quota}. Returning 0.0")
            return 0.0 # Cannot calculate progress if quota is invalid

    if goal_quota <= 0:
        #print(f"{indent_str}  Goal quota is <= 0. Returning 100.0")
        return 100.0 # If quota is 0 or less, it's considered 100% complete

    current_total = 0
    for name in goal_names:
        if isinstance(name, list):
            # Handles combined goals like [['right', 'wrong']]
            for sub_name in name:
                value = session_data.get(sub_name, 0)
                current_total += value
                #print(f"{indent_str}    Combined goal: {sub_name}, value: {value}, current_total: {current_total}")
        else:
            value = session_data.get(name, 0)
            current_total += value
            #print(f"{indent_str}    Single goal: {name}, value: {value}, current_total: {current_total}")

    progress = (current_total / goal_quota) * 100.0
    final_progress = min(progress, 100.0) # Cap at 100% even if exceeded
    #print(f"{indent_str}  Calculated progress: {progress}, final: {final_progress}")
    #print(f"{indent_str}Exiting get_single_goal_progress with: {final_progress}")
    return final_progress

if __name__ == '__main__':
    print("--- Test Cases for get_goal_progress (Version 2.0) ---")
    import prints
    # Test Case 1: Simple Goal (task = d)
    parsed_goal_1 = [[{'goalName': ['one_finish'], 'goalQuota': 1}]]
    session_data_1_0 = {'one_finish': 2, 'right': 0, 'wrong': 0, 'new': 0, 'sv': 0}
    session_data_1_50 = {'one_finish': 0.5, 'right': 0, 'wrong': 0, 'new': 0, 'sv': 0}
    session_data_1_100 = {'one_finish': 1, 'right': 0, 'wrong': 0, 'new': 0, 'sv': 0}
    print(get_goal_progress(parsed_goal_1, session_data_1_0))
    print(f"Test 1 (task = d) - 0%: {get_goal_progress(parsed_goal_1, session_data_1_0):.2f}%") # Expected: 0.00%
    print(f"Test 1 (task = d) - 50%: {get_goal_progress(parsed_goal_1, session_data_1_50):.2f}%") # Expected: 50.00%
    print(f"Test 1 (task = d) - 100%: {get_goal_progress(parsed_goal_1, session_data_1_100):.2f}%") # Expected: 100.00%
    prints.progress(get_goal_progress(parsed_goal_1, session_data_1_0))

    # Test Case 2: AND condition (c = 2 and t = 1)
    parsed_goal_2 = [[{'goalName': ['right'], 'goalQuota': '2'}, {'goalName': ['one_finish'], 'goalQuota': '1'}]]
    session_data_2_0 = {'right': 0, 'one_finish': 0, 'wrong': 0, 'new': 0, 'sv': 0}
    session_data_2_partial = {'right': 1, 'one_finish': 0.5, 'wrong': 0, 'new': 0, 'sv': 0} # 50% of right, 50% of one_finish -> min is 50%
    session_data_2_met = {'right': 2, 'one_finish': 1, 'wrong': 0, 'new': 0, 'sv': 0}
    print(f"Test 2 (c=2 and t=1) - 0%: {get_goal_progress(parsed_goal_2, session_data_2_0):.2f}%") # Expected: 0.00%
    print(f"Test 2 (c=2 and t=1) - Partial: {get_goal_progress(parsed_goal_2, session_data_2_partial):.2f}%") # Expected: 50.00%
    print(f"Test 2 (c=2 and t=1) - 100%: {get_goal_progress(parsed_goal_2, session_data_2_met):.2f}%") # Expected: 100.00%

    # Test Case 3: OR condition (c = 2 or x = 10)
    parsed_goal_3 = [[{'goalName': ['right'], 'goalQuota': '2'}], [{'goalName': ['wrong'], 'goalQuota': '10'}]]
    session_data_3_0 = {'right': 0, 'one_finish': 0, 'wrong': 0, 'new': 0, 'sv': 0}
    session_data_3_right_50 = {'right': 1, 'one_finish': 0, 'wrong': 0, 'new': 0, 'sv': 0} # Right is 50%, Wrong is 0% -> max is 50%
    session_data_3_wrong_70 = {'right': 0, 'one_finish': 0, 'wrong': 7, 'new': 0, 'sv': 0} # Right is 0%, Wrong is 70% -> max is 70%
    session_data_3_right_100 = {'right': 2, 'one_finish': 0, 'wrong': 0, 'new': 0, 'sv': 0}
    print(f"Test 3 (c=2 or x=10) - 0%: {get_goal_progress(parsed_goal_3, session_data_3_0):.2f}%") # Expected: 0.00%
    print(f"Test 3 (c=2 or x=10) - Right 50%: {get_goal_progress(parsed_goal_3, session_data_3_right_50):.2f}%") # Expected: 50.00%
    print(f"Test 3 (c=2 or x=10) - Wrong 70%: {get_goal_progress(parsed_goal_3, session_data_3_wrong_70):.2f}%") # Expected: 70.00%
    print(f"Test 3 (c=2 or x=10) - Right 100%: {get_goal_progress(parsed_goal_3, session_data_3_right_100):.2f}%") # Expected: 100.00%

    # Test Case 4: Combined Goal (nw and c = 10)
    parsed_goal_4 = [[{'goalName': ['new', 'right'], 'goalQuota': '10'}]]
    session_data_4_0 = {'new': 0, 'right': 0, 'wrong': 0, 'one_finish': 0, 'sv': 0}
    session_data_4_partial = {'new': 3, 'right': 4, 'wrong': 0, 'one_finish': 0, 'sv': 0} # Total 7/10 = 70%
    session_data_4_100 = {'new': 5, 'right': 5, 'wrong': 0, 'one_finish': 0, 'sv': 0}
    print(f"Test 4 (nw and c = 10) - 0%: {get_goal_progress(parsed_goal_4, session_data_4_0):.2f}%") # Expected: 0.00%
    print(f"Test 4 (nw and c = 10) - Partial: {get_goal_progress(parsed_goal_4, session_data_4_partial):.2f}%") # Expected: 70.00%
    print(f"Test 4 (nw and c = 10) - 100%: {get_goal_progress(parsed_goal_4, session_data_4_100):.2f}%") # Expected: 100.00%

    # Test Case 5: Complex Nested Goal (from your example)
    # (task = d or (c = 2 and task = 1 and x=0 or sv=5 or nw=1)) and (new = 2 or x = 10)

    part_A_parsed = [
        [{'goalName': ['one_finish'], 'goalQuota': 1}],
        [{'goalName': ['right'], 'goalQuota': 2}, {'goalName': ['one_finish'], 'goalQuota': 1}, {'goalName': ['wrong'], 'goalQuota': 0}],
        [{'goalName': [['right', 'wrong']], 'goalQuota': 5}],
        [{'goalName': ['new'], 'goalQuota': 1}]
    ]

    part_B_parsed = [
        [{'goalName': ['new'], 'goalQuota': 2}],
        [{'goalName': ['wrong'], 'goalQuota': 10}]
    ]

    # The full complex goal is Part A AND Part B
    # This is represented as a single OR group containing a single AND group,
    # where that AND group contains part_A_parsed and part_B_parsed.
    complex_parsed_goal = [
        [
            part_A_parsed,
            part_B_parsed
        ]
    ]
    print(f"\nComplex Parsed Goal Structure: {complex_parsed_goal}")

    # Session data to meet the complex goal (e.g., task=d AND new=2)
    session_data_complex_met_1 = {
        'one_finish': 1, 'right': 0, 'wrong': 0, 'new': 2, 'sv': 0
    }
    print(f"Test 5 (Complex) - Met (task=d AND new=2): {get_goal_progress(complex_parsed_goal, session_data_complex_met_1):.2f}%") # Expected: 100.00%

    # Session data to meet the complex goal (e.g., (c=2 and t=1 and x=0) AND x=10)
    session_data_complex_met_2 = {
        'one_finish': 1, 'right': 2, 'wrong': 10, 'new': 0, 'sv': 0
    }
    print(f"Test 5 (Complex) - Met ((c=2 and t=1 and x=0) AND x=10): {get_goal_progress(complex_parsed_goal, session_data_complex_met_2):.2f}%") # Expected: 100.00%

    # Session data to fail the complex goal (Part A fails, new=0)
    session_data_complex_fail_A = {
        'one_finish': 0, 'right': 0, 'wrong': 0, 'new': 0, 'sv': 0
    }
    print(f"Test 5 (Complex) - Fail (Part A): {get_goal_progress(complex_parsed_goal, session_data_complex_fail_A):.2f}%") # Expected: 0.00% (or very low)

    # Session data to fail the complex goal (Part B fails, new=1, wrong=9)
    session_data_complex_fail_B = {
        'one_finish': 1, 'right': 0, 'wrong': 9, 'new': 1, 'sv': 0
    }
    print(f"Test 5 (Complex) - Fail (Part B): {get_goal_progress(complex_parsed_goal, session_data_complex_fail_B):.2f}%") # Expected: <100% (Part A met, Part B partial)

    print("\n--- End Test Cases ---")