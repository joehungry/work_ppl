import os
import json
import time
from datetime import datetime

class DataManager:
    """Handles saving and loading application data."""
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        self.points_file = os.path.join(self.data_folder, "points.json")
        self.log_file = os.path.join(self.data_folder, "session_log.txt")
        self._setup()

    def _setup(self):
        """Create the data folder if it doesn't exist."""
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

    def load_data(self):
        """Loads the user's total points."""
        if os.path.exists(self.points_file):
            with open(self.points_file, 'r') as f:
                data = json.load(f)
                return data.get("total_points", 0)
        return 0

    def save_data(self, points):
        """Saves the user's total points."""
        with open(self.points_file, 'w') as f:
            json.dump({"total_points": points}, f, indent=4)

    def log_session(self, session_details):
        """Logs the details of a completed session to the log file."""
        with open(self.log_file, 'a') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {session_details}\n")

class Session:
    """Base class for a work session."""
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.earned_points = 0

    def start(self):
        """Starts the session timer."""
        self.start_time = time.time()
        print("Session started.")

    def end(self):
        """Ends the session timer."""
        self.end_time = time.time()
        print("Session ended.")

    def get_duration_minutes(self):
        """Calculates the duration of the session in minutes."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time) / 60
        return 0

class FocusSession(Session):
    """A task-based session with a specific goal and target time."""
    def __init__(self, goal_description, unit_goal, target_minutes):
        super().__init__()
        self.goal_description = goal_description
        self.unit_goal = unit_goal
        self.target_minutes = target_minutes

    def calculate_points(self, actual_minutes):
        """Calculates points based on the Challenge Tier System."""
        # 1. Base Points (Reward for perseverance)
        base_points = self.unit_goal * 10  # Example: 10 points per unit

        # 2. Bonus Points (Reward for focus and planning)
        time_usage_ratio = actual_minutes / self.target_minutes
        bonus_points = 0
        tier = "Completion (Over Time)"

        if time_usage_ratio <= 0.5:
            tier = "Bronze Tier (Good Focus / Sandbagged)"
            bonus_points = 10
        elif time_usage_ratio <= 0.8:
            tier = "Silver Tier (Excellent Focus)"
            bonus_points = 50
        elif time_usage_ratio <= 1.0:
            tier = "Gold Tier (Perfect Focus)"
            bonus_points = 100
        
        self.earned_points = base_points + bonus_points
        
        summary = (
            f"Focus Session: '{self.goal_description}'\n"
            f"  - Goal: {self.unit_goal} units\n"
            f"  - Target Time: {self.target_minutes:.1f} min, Actual Time: {actual_minutes:.1f} min\n"
            f"  - Tier: {tier}\n"
            f"  - Points: {base_points} (Base) + {bonus_points} (Bonus) = {self.earned_points}"
        )
        return summary

class FlowSession(Session):
    """A time-based session for exploratory or creative work."""
    POINT_RATE_PER_MINUTE = 3

    def __init__(self, duration_minutes):
        super().__init__()
        self.duration_minutes = duration_minutes

    def calculate_points(self):
        """Calculates points based on the duration of the session."""
        actual_minutes = self.get_duration_minutes()
        self.earned_points = actual_minutes * self.POINT_RATE_PER_MINUTE
        
        summary = (
            f"Flow Session:\n"
            f"  - Target Duration: {self.duration_minutes:.1f} min, Actual Duration: {actual_minutes:.1f} min\n"
            f"  - Points: {self.earned_points:.1f}"
        )
        return summary

class WorkmanApp:
    """The main application class."""
    def __init__(self):
        self.data_manager = DataManager()
        self.current_points = self.data_manager.load_data()

    def run(self):
        """The main loop for the application."""
        print("Welcome to Workman v3!")
        while True:
            self.show_main_menu()
            choice = input(">> ")
            if choice == '1':
                self.start_focus_session()
            elif choice == '2':
                self.start_flow_session()
            elif choice == 'q':
                print("Saving and quitting. Goodbye!")
                self.data_manager.save_data(self.current_points)
                break
            else:
                print("Invalid choice. Please try again.")

    def show_main_menu(self):
        """Displays the main menu."""
        print("\n--- Main Menu ---")
        print(f"You have {self.current_points:.1f} points.")
        print("1. Start a Focus Session (Task-based)")
        print("2. Start a Flow Session (Time-based)")
        print("q. Quit")
        print("-----------------")

    def start_focus_session(self):
        """Handles the logic for starting and running a Focus Session."""
        try:
            goal = input("What is your specific goal? (e.g., Solve math problems) >> ")
            units = int(input(f"How many '{goal}' do you plan to complete? >> "))
            target_time = float(input("What is your target time in minutes? >> "))
        except ValueError:
            print("Invalid input. Please enter numbers for units and target time.")
            return

        session = FocusSession(goal, units, target_time)
        session.start()
        
        input("Press Enter when you have completed your goal...")
        
        session.end()
        
        duration = session.get_duration_minutes()
        summary = session.calculate_points(duration)
        
        self.current_points += session.earned_points
        self.data_manager.log_session(summary)
        
        print("\n--- Session Summary ---")
        print(summary)
        print("-----------------------")
        self.data_manager.save_data(self.current_points)


    def start_flow_session(self):
        """Handles the logic for starting and running a Flow Session."""
        try:
            duration = float(input("How long do you want to work for (in minutes)? >> "))
        except ValueError:
            print("Invalid input. Please enter a number for the duration.")
            return

        session = FlowSession(duration)
        session.start()
        
        print(f"Timer set for {duration} minutes. Press Ctrl+C to end early.")
        try:
            # Simulate the timer
            time.sleep(duration * 60)
        except KeyboardInterrupt:
            print("\nTimer interrupted early.")

        session.end()
        summary = session.calculate_points()
        
        self.current_points += session.earned_points
        self.data_manager.log_session(summary)

        print("\n--- Session Summary ---")
        print(summary)
        print("-----------------------")
        self.data_manager.save_data(self.current_points)


if __name__ == "__main__":
    app = WorkmanApp()
    app.run()
