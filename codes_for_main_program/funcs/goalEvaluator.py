def _is_met_recursive(goal, session_data):
    """
    Part 1: Core Evaluation. Returns only True or False.
    """
    if isinstance(goal, list) and len(goal) == 1 and isinstance(goal[0], list):
        return _is_met_recursive(goal[0], session_data)

    if isinstance(goal, dict):
        goal_names = goal.get('goalName', [])
        goal_quota = goal.get('goalQuota')

        if goal_quota == 'd' or goal_quota == 'done':
            required = 1
        else:
            try:
                required = int(goal_quota)
            except (ValueError, TypeError):
                return False

        current_total = 0
        all_vars_in_goal = []
        for name_item in goal_names:
            if isinstance(name_item, list):
                all_vars_in_goal.extend(name_item)
            else:
                all_vars_in_goal.append(name_item)
        
        for var in all_vars_in_goal:
            current_total += session_data.get(var, 0)
            
        return current_total >= required

    if isinstance(goal, list):
        if not goal:
            return False
        is_or_condition = isinstance(goal[0], list)
        sub_results = [_is_met_recursive(sub_goal, session_data) for sub_goal in goal]
        return any(sub_results) if is_or_condition else all(sub_results)
            
    return False

def _get_requirements_recursive(goal):
    """
    Part 2: Requirement Calculation. Returns a dictionary like {'c': 2}.
    """
    if isinstance(goal, list) and len(goal) == 1 and isinstance(goal[0], list):
        return _get_requirements_recursive(goal[0])

    if isinstance(goal, dict):
        reqs = {}
        goal_names = goal.get('goalName', [])
        goal_quota = goal.get('goalQuota')

        if goal_quota == 'd' or goal_quota == 'done':
            required = 1
        else:
            try:
                required = int(goal_quota)
            except (ValueError, TypeError):
                return {}

        all_vars_in_goal = []
        for name_item in goal_names:
            if isinstance(name_item, list):
                all_vars_in_goal.extend(name_item)
            else:
                all_vars_in_goal.append(name_item)

        for var in all_vars_in_goal:
            reqs[var] = required
        return reqs

    if isinstance(goal, list):
        all_reqs = {}
        for sub_goal in goal:
            sub_reqs = _get_requirements_recursive(sub_goal)
            for var, req_val in sub_reqs.items():
                all_reqs[var] = max(all_reqs.get(var, 0), req_val)
        return all_reqs
    
    return {}

def _find_combined_goal_vars(goal):
    """
    Finds sets of variables that are part of a "combined" goal.
    e.g., {'goalName': ['a', 'b']} -> returns [{'a', 'b'}]
    """
    combined_sets = []
    if isinstance(goal, dict):
        goal_names = goal.get('goalName', [])
        # A combined goal has multiple single names in its goalName list
        if len(goal_names) > 1 and all(isinstance(name, str) for name in goal_names):
            combined_sets.append(set(goal_names))
    elif isinstance(goal, list):
        for sub_goal in goal:
            combined_sets.extend(_find_combined_goal_vars(sub_goal))
    return combined_sets

def evaluate_goal(parsed_goal_structure, session_data):
    """
    Part 3: Main function to assemble the final result.
    """
    is_met = _is_met_recursive(parsed_goal_structure, session_data)
    requirements = _get_requirements_recursive(parsed_goal_structure)
    
    # Build the basic breakdown using original, unmodified session_data.
    breakdown = {}
    all_vars = set(session_data.keys()) | set(requirements.keys())
    for var in all_vars:
        breakdown[var] = {
            'required': requirements.get(var, 0),
            'current': session_data.get(var, 0)
        }
        
    # Apply special display rule for COMBINED goals (e.g., c+t=10)
    combined_goal_sets = _find_combined_goal_vars(parsed_goal_structure)
    for var_set in combined_goal_sets:
        # Calculate the total current value for this specific combined goal
        total_current = sum(session_data.get(var, 0) for var in var_set)
        # Update the breakdown for all variables in this set FOR DISPLAY ONLY
        for var in var_set:
            if var in breakdown:
                breakdown[var]['current'] = total_current
                
    return is_met, breakdown

if __name__ == '__main__':
    print("--- Test Cases for evaluate_goal (with variable breakdown) ---")

    # Test Case 1: Simple Goal (task = d)
    parsed_goal_1 = [[{'goalName': ['one_finish'], 'goalQuota': 1}]]
    session_data_1_met = {'one_finish': 1, 'right': 0, 'wrong': 0, 'new': 0, 'sv': 0}
    session_data_1_fail = {'one_finish': 0, 'right': 0, 'wrong': 0, 'new': 0, 'sv': 0}
    
    is_met, breakdown = evaluate_goal(parsed_goal_1, session_data_1_met)
    print(f"Test 1 (task = d) - Met: {is_met}, Breakdown: {breakdown}") # Expected: True, {'one_finish': {'required': 1, 'current': 1}}

    is_met, breakdown = evaluate_goal(parsed_goal_1, session_data_1_fail)
    print(f"Test 1 (task = d) - Fail: {is_met}, Breakdown: {breakdown}") # Expected: False, {'one_finish': {'required': 1, 'current': 0}}

    # Test Case 2: AND condition (c = 2 and t = 1)
    parsed_goal_2 = [[{'goalName': ['right'], 'goalQuota': '2'}, {'goalName': ['one_finish'], 'goalQuota': '1'}]]
    session_data_2_met = {'right': 2, 'one_finish': 1, 'wrong': 0, 'new': 0, 'sv': 0}
    session_data_2_fail_c = {'right': 1, 'one_finish': 1, 'wrong': 0, 'new': 0, 'sv': 0}
    
    is_met, breakdown = evaluate_goal(parsed_goal_2, session_data_2_met)
    print(f"Test 2 (c=2 and t=1) - Met: {is_met}, Breakdown: {breakdown}") # Expected: True, {'right': {'required': 2, 'current': 2}, 'one_finish': {'required': 1, 'current': 1}}

    is_met, breakdown = evaluate_goal(parsed_goal_2, session_data_2_fail_c)
    print(f"Test 2 (c=2 and t=1) - Fail (c): {is_met}, Breakdown: {breakdown}") # Expected: False, {'right': {'required': 2, 'current': 1}, 'one_finish': {'required': 1, 'current': 1}}

    # Test Case 3: OR condition (c = 2 or x = 10)
    parsed_goal_3 = [[{'goalName': ['right'], 'goalQuota': '2'}], [{'goalName': ['wrong'], 'goalQuota': '10'}]]
    session_data_3_met_c = {'right': 2, 'one_finish': 0, 'wrong': 0, 'new': 0, 'sv': 0}
    session_data_3_met_x = {'right': 0, 'one_finish': 0, 'wrong': 10, 'new': 0, 'sv': 0}
    session_data_3_fail = {'right': 1, 'one_finish': 0, 'wrong': 9, 'new': 0, 'sv': 0}
    
    is_met, breakdown = evaluate_goal(parsed_goal_3, session_data_3_met_c)
    print(f"Test 3 (c=2 or x=10) - Met (c): {is_met}, Breakdown: {breakdown}") # Expected: True, {'right': {'required': 2, 'current': 2}, 'wrong': {'required': 10, 'current': 0}}

    is_met, breakdown = evaluate_goal(parsed_goal_3, session_data_3_met_x)
    print(f"Test 3 (c=2 or x=10) - Met (x): {is_met}, Breakdown: {breakdown}") # Expected: True, {'right': {'required': 2, 'current': 0}, 'wrong': {'required': 10, 'current': 10}}

    is_met, breakdown = evaluate_goal(parsed_goal_3, session_data_3_fail)
    print(f"Test 3 (c=2 or x=10) - Fail: {is_met}, Breakdown: {breakdown}") # Expected: False, {'right': {'required': 2, 'current': 1}, 'wrong': {'required': 10, 'current': 9}}

    # Test Case 4: Combined Goal (nw and c = 10)
    parsed_goal_4 = [[{'goalName': ['new', 'right'], 'goalQuota': '10'}]]
    session_data_4_met = {'new': 5, 'right': 5, 'wrong': 0, 'one_finish': 0, 'sv': 0}
    session_data_4_fail = {'new': 3, 'right': 6, 'wrong': 0, 'one_finish': 0, 'sv': 0} # Total 9
    
    is_met, breakdown = evaluate_goal(parsed_goal_4, session_data_4_met)
    print(f"Test 4 (nw and c = 10) - Met: {is_met}, Breakdown: {breakdown}") # Expected: True, {'new': {'required': 10, 'current': 5}, 'right': {'required': 10, 'current': 5}, 'new_right_total': {'required': 10, 'current': 10}}

    is_met, breakdown = evaluate_goal(parsed_goal_4, session_data_4_fail)
    print(f"Test 4 (nw and c = 10) - Fail: {is_met}, Breakdown: {breakdown}") # Expected: False, {'new': {'required': 10, 'current': 3}, 'right': {'required': 10, 'current': 6}, 'new_right_total': {'required': 10, 'current': 9}}

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

    complex_parsed_goal = [
        [
            part_A_parsed,
            part_B_parsed
        ]
    ]

    # Session data to meet the complex goal (e.g., task=d AND new=2)
    session_data_complex_met_1 = {
        'one_finish': 1, 'right': 0, 'wrong': 0, 'new': 2, 'sv': 0
    }
    is_met, breakdown = evaluate_goal(complex_parsed_goal, session_data_complex_met_1)
    print(f"Test 5 (Complex) - Met (task=d AND new=2): {is_met}, Breakdown: {breakdown}") # Expected: True

    # Session data to meet the complex goal (e.g., (c=2 and t=1 and x=0) AND x=10)
    session_data_complex_met_2 = {
        'one_finish': 1, 'right': 2, 'wrong': 10, 'new': 0, 'sv': 0
    }
    is_met, breakdown = evaluate_goal(complex_parsed_goal, session_data_complex_met_2)
    print(f"Test 5 (Complex) - Met ((c=2 and t=1 and x=0) AND x=10): {is_met}, Breakdown: {breakdown}") # Expected: True

    # Session data to fail the complex goal (Part A fails, new=0)
    session_data_complex_fail_A = {
        'one_finish': 0, 'right': 0, 'wrong': 0, 'new': 0, 'sv': 0
    }
    is_met, breakdown = evaluate_goal(complex_parsed_goal, session_data_complex_fail_A)
    print(f"Test 5 (Complex) - Fail (Part A): {is_met}, Breakdown: {breakdown}") # Expected: False

    # Session data to fail the complex goal (Part B fails, new=1, wrong=9)
    session_data_complex_fail_B = {
        'one_finish': 1, 'right': 0, 'wrong': 9, 'new': 1, 'sv': 0
    }
    is_met, breakdown = evaluate_goal(complex_parsed_goal, session_data_complex_fail_B)
    print(f"Test 5 (Complex) - Fail (Part B): {is_met}, Breakdown: {breakdown}") # Expected: False

    print("\n--- End Test Cases ---")

    print()
    print('my_test')
    parsed_goal_4 = [{'goalName': ['one_finish', 'right'], 'goalQuota': 10}]
    session_data_4_fail = {'new': 0, 'right': 6, 'wrong': 0, 'one_finish': 1, 'sv': 0}
    is_met, breakdown = evaluate_goal(parsed_goal_4, session_data_4_fail)
    print(is_met, breakdown)

    parsed_goal_5 = [[{'goalName': ['one_finish'], 'goalQuota': 2}], [{'goalName': ['right'], 'goalQuota': 4}]]
    session_data_5_fail = {'new': 0, 'right': 2, 'wrong': 0, 'one_finish': 1, 'sv': 0}
    is_met, breakdown = evaluate_goal(parsed_goal_5, session_data_5_fail)
    print(is_met, breakdown)