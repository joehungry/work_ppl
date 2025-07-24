# WorkPPL Session Tracker

Welcome to WorkPPL, a command-line application designed to help you focus, track your work sessions, and stay motivated using a points-based system.

This guide will walk you through setting up and running a work session, from initial configuration to tracking your goals.

## 1. Setting Up Your Session

Before starting a session, you need to configure four key settings. These settings define the parameters of your work period. You must set them up in each session.

### Command Syntax

The application uses a simple `command'value` syntax. For example, to set the session label, you would type `L'My First Session`.

---

### 1.1. Enable the Point System (Optional)

The point system is a core feature of this application. By enabling it, you earn points for the time you spend in a session. The longer you work, the more points you accumulate per hour. These points can be used as a reward or for motivation. You can also complete specific goals to earn bonus points.

If you just want to track your time without earning points, you can disable this feature.

**Commands:**

*   **Enable Points:** `p` or `p'on`
*   **Disable Points:** `p'off`, `p'no`, `p'none`, or `p'\n`

**Example:**
```
>> P
point system is on
```
*Note: Commands are generally case-insensitive (e.g., `p` or `P`), but values like `on` or `off` must be in lowercase.*

---

### 1.2. Set the Session Name

Giving your session a name helps you clarify your objective and maintain focus. It's a simple but powerful way to reduce distractions.

**Commands:**

*   **Set Name:** `L'Your Session Name` or `label'Your Session Name`
*   **Use Previous Name:** `L'\s` (uses the name from the last session in the current run; does not persist if the program is closed).

**Example:**
```
>> L'Researching Python asyncio
session name = Researching Python asyncio
```

---

### 1.3. Set the Estimated Time

Define how long you expect the session to last. This setting is crucial for the point system, as it helps calculate potential bonus points for completing goals on time. Be realistic with your estimate for the best results.

**Commands:**

*   **Set Time (in minutes):** `T'minutes` or `tim.length'minutes` (e.g., `T'25` for 25 minutes).
*   **Use Previous Time:** `T'\s`
*   **Unlimited Time:** `T'\n` (sets a very long duration, practical use is limited).

**Example:**
```
>> T'45
tim.length = 45 (minutes)
```
*Note: The input must be a number.*

---

### 1.4. Define the Session Goal

Setting a goal allows you to earn significant bonus points. Completing a goal within the estimated time can earn you up to **4x** the standard points. Even just finishing the goal (regardless of time) can double your points.

**Command:** `goal <goal_definition>`

**Goal Presets:**

You can set goals from the following presets:

*   `new` or `nw`: Learning something new.
*   `correct` or `c`: Answering a question correctly.
*   `incorrect` or `x`: Answering a question incorrectly.
*   `solve` or `sv`: Solving a problem (regardless of correctness).
*   `task` or `t`: Completing a single task.

**Setting Goal Targets:**

Assign a number to your goal using `=`. 

*   **Example:** To solve 8 problems: `goal solve = 8`

You can also use `done` or `d` as a shorthand for `1`.

*   **Example:** To complete one task: `goal task = done` (or `goal task = d`, or simply `goal task`). These are all equivalent to `goal task = 1`.

**Combining Goals:**

You can create complex goals using `and` and `or`.

*   **`and`:** Use `and` to link goals that must all be achieved.
    *   **Example:** `goal task = d and new = 2` (Complete 1 task AND learn 2 new things).
*   **`or`:** Use `or` to specify alternative goals.
    *   **Example:** `goal c = 2 or x = 10` (Get 2 correct answers OR 10 incorrect answers).
*   **Combined Logic:** Use parentheses `()` to group expressions for clarity and correct order of operations, especially in complex cases.
    *   **Example:** `(task = d and new = 2) or x = 10`

**Special Goal Commands:**

*   `goal none` or `goal n` or `goal \n`: Do not set a goal for the session.
*   `goal same` or `goal s` or `goal \s`: Use the same goal as the previous session (data is lost when the program closes).

## 2. Running the Session

Once you've configured your session, you can start it by typing `start`.

### During the Session

While the session is active, you can update your goal progress using your keyboard's numpad. The application will display a progress bar indicating how close you are to completing your goal.

**Keybindings for Goal Tracking:**

*   **Numpad 4:** Mark a task as complete.
*   **Numpad 1:** Mark an answer as correct.
*   **Numpad 2:** Mark an answer as incorrect.
*   **Numpad 3:** Mark something as newly learned.
*   **Numpad `.` (period):** Undo the last action.

**Changing the UI:**

Press **Numpad 7** to cycle through different UI modes during your session:

1.  **Default View:** The standard interface with a detailed goal progress breakdown, encouragement messages, and bonus multipliers.
2.  **Total Study Time View:** A variation of the default view that displays your total study time for the day, rather than just the current session time.
3.  **Minimal View:** A distraction-free UI that shows only a simple progress bar and a summary of your goal counts. The cursor and input are hidden to help you focus.

### Ending the Session

To end the session, press **Numpad 0**. The application will then calculate your points and save the session data.

## 3. Post-Session

After each session, the application displays a summary screen with your results.

### Post-Session Summary

The summary screen includes:

*   **Total study time for the day.**
*   **Total points earned.**
*   **A breakdown of your performance, including:**
    *   Number of new things learned.
    *   Number of correct and incorrect answers.
    *   Number of tasks completed.
*   **A list of all sessions from the day.**

## 4. The Rest System

After completing a study session, you are rewarded with rest time. This system is designed to help you take effective breaks and stay productive.

### Earning Rest Time

Your available rest time is calculated dynamically based on your performance. The better you do in your study sessions, the more rest time you earn. You can check your available rest time at any point using the `show rest time` command.

### Taking a Break

To start a break, use the `use rest` command. You can choose to use all of your available rest time, or just a portion of it.

**Using Auto Rest:**

For a more structured break, you can use the `auto` command (`use rest 'auto'`). This will calculate a recommended break time based on the length of your last study session, roughly equivalent to 20% of the study time (similar to the Pomodoro Technique). This allows you to take a short, effective break without using all of your earned rest time.

### During Your Break

A timer will display the remaining rest time. When the timer runs out, you will be notified by a sound (if configured) and an email (if configured).

### Exceeding Your Rest Time

If you exceed your allotted rest time, a point-deduction system will be activated. The longer you over-extend your break, the more points you will lose. If you lose more than 45% of your total points, the program will automatically exit.

## 5. Commands

Here is a list of all available commands:

| Command | Description |
| --- | --- |
| `p` or `p'on` | Enable the point system. |
| `p'off` | Disable the point system. |
| `L'<name>` | Set the session name. |
| `L'\s` | Use the previous session name. |
| `T'<minutes>` | Set the session duration in minutes. |
| `T'\s` | Use the previous session duration. |
| `T'\n` | Set an unlimited session duration. |
| `goal <def>` | Set a goal for the session. |
| `goal none` | Do not set a goal. |
| `goal same` | Use the previous session's goal. |
| `start` | Start the session. |
| `end` | End the session. |
| `show list` | Display a list of all sessions from the day. |
| `show point` | Display your current total points. |
| `show rest time` | Display your available rest time. |
| `use rest` | Use your accumulated rest time. |
| `sound change` | Change the notification sound. |
| `sound volume` | Change the notification volume. |
| `email on` | Enable email notifications. |
| `email off` | Disable email notifications. |

## 5. File System

The application creates a `Python Report` directory to store your data.

*   **`Python Report/Diary`**: Contains daily logs of your sessions.
*   **`Python Report/StudyContent`**: Stores the content of your study sessions.
*   **`Python Report/StudyPoint`**: Tracks the points you've earned.
*   **`Python Report/usedPoints`**: Logs the points you've spent.
*   **`Python Report/python_hidden_file`**: Contains internal application data, such as settings and logs.

## 6. Advanced Features

The application includes several advanced features for a more customized and robust experience.

### Email Notifications

The application can send you an email when your study or rest period has ended. This is useful for keeping you on track even if you aren't looking at the terminal. This feature is configured in `funcs/sendEmail.py` and can be toggled with the `email on`/`off` commands. You will need to provide your own email credentials in the script to use this feature.

### Sound Notifications

You can use custom sounds to signal the end of study and rest periods.

1.  **Add Music:** Place `.mp3` or `.wav` files into the `Python Report/Music/` directory.
2.  **Select Sounds:** The first time you run the application with music files, it will prompt you to select which sound to use for study sessions and which for rest periods.
3.  **Control:** You can change the selected sounds and adjust the volume using the `sound change` and `sound volume` commands.

### Dynamic Rest Time Calculation

Your available rest time is not a fixed value. It is dynamically calculated based on several factors, including:

*   **Total points accumulated:** More points can lead to more rest.
*   **Session duration:** Longer, focused sessions are rewarded.
*   **Consistency:** The system rewards continuous effort over time.

This encourages a sustainable work pace rather than short bursts of effort.

### Data Persistence

The application saves your progress and settings in hidden files within the `Python Report/python_hidden_file/` directory. This ensures that your total points, session history, and settings (like chosen music and volume) are carried over even if you close and reopen the program.

## 7. The Diary: A Technical Deep Dive

The diary entry system is one of the most complex features in this application. It was not designed as a simple text input, but as a **stateful, line-oriented editor** that operates via the command-line interface. This design provides granular control over the entry but requires a specific workflow.

### Core Concepts

*   **Modal System:** You cannot simply start typing your diary entry. You must first enter a specific mode. The command `D'write` puts you in "write mode," allowing you to insert new lines, while `D'change` puts you in "change mode," allowing you to overwrite existing lines. The application rejects text input if you are not in one of these modes.

*   **Line-Oriented Editing:** A diary entry is not stored as a single block of text. Instead, it is managed as a list of individual strings (`self.diary_list`). Every line is a separate piece of data that must be added or modified with a specific command.

*   **Manual Cursor Control:** The system uses an internal variable, `self.comment_index`, to act as a cursor, keeping track of the current line. You must use commands to move this index to the desired line before you can edit or delete it.


### Example Workflow

To write a simple two-line diary entry, you would need to:

1.  Enter write mode: `>> D'write`
2.  Add the first line: `>> D+'Line 1`
3.  Add the second line: `>> D+'Line 2`

To then change "Line 1" to "First line," the process would be:

1.  Switch to change mode: `>> D'change`
2.  Move the index to the first line: `>> D'0`
3.  Overwrite the line: `>> D+'First line`
4.  To remove the second line: `>> D-'`

btw, you can also use `D't` to go before the first line, and `D'r` to go to the final element

This highly structured approach is reminiscent of classic command-line editors like `ed` or `vi`. While it provides powerful and precise control, it is important to understand its complexity when using the diary feature.
