import parameters as param
import json
import os
from datetime import datetime
from nicegui import ui  


def get_week_0():
    """Get the week that the user started capturing data"""
    log_file_path = os.path.join(os.path.dirname(__file__), param.USER_DATA)
    if not os.path.exists(param.SHOOTING_DATA):
        return 0

    with open(param.USER_DATA, 'r') as file:
        logs = json.load(file)

    # Ensure data is a list
    #if not isinstance(logs, list):
    #    return 0

    # Process log data
    for k, v in logs.items():
        if k == 'start_week':
            start_week = v
        else:
            start_week = 0


    return start_week

def last_4_weeks(week_of_year):
    """Retrieve total arrows shot for the last 4 weeks."""
    log_file_path = os.path.join(os.path.dirname(__file__), param.SHOOTING_DATA)
    if not os.path.exists(param.SHOOTING_DATA):
        debug_msgs.append(f"Log file {param.SHOOTING_DATA} not found.")
        (f"Log file {param.SHOOTING_DATA} not found.")
        return [0, 0, 0, 0]  # Return zero counts if file doesn't exist

    try:
        with open(param.SHOOTING_DATA, 'r') as file:
            logs = json.load(file)

        # Ensure data is a list
        if not isinstance(logs, list):
            return [0, 0, 0, 0]

        # Prepare week data
        week_totals = {week_of_year - i: 0 for i in range(4)}

        # Process log data
        for log in logs:
            log_date = log.get("shoot_date", "")
            arrows_shot = log.get("arrows_shot", 0)

            try:
                log_week = log.get("week_number")
                #debug_msgs.append(f"Processing log: {log_date} (Week {log_week}), Arrows: {arrows_shot}")

                if log_week in week_totals:
                    week_totals[log_week] += arrows_shot
            except ValueError:
                #debug_msgs.append(f"Invalid date format: {log_date}")
                continue  # Skip invalid dates

        return [week_totals[week_of_year - i] for i in range(4)]

    except json.JSONDecodeError:
        ui.label("Error reading log file.")
        return [0, 0, 0, 0]

def get_settings_data():
    """Retrieve user settings including start date and annual target arrows."""
    if not os.path.exists(param.USER_DATA):
        return '', 0  # Default values
    start_date = ''
    target_arrows = 0
    try:
        with open(param.USER_DATA, 'r') as file:
            user_settings = json.load(file)
            if user_settings and isinstance(user_settings, dict):
                for k, v in user_settings.items():
                    if k == 'start_date':
                        start_date = v
                        break
                for k, v in user_settings.items():
                    if k == 'annual_target_arrows':
                        target_arrows = v 
                        break
                return start_date, target_arrows
    except json.JSONDecodeError:
        pass  # Default values returned if error occurs
    
    return '', 0



def get_total_shot_arrows():
    """Calculate the total number of arrows shot."""
    total_shot_arrows = 0
    if os.path.exists(param.SHOOTING_DATA):
        try:
            with open(param.SHOOTING_DATA, 'r') as file:
                user_data = json.load(file)
                total_shot_arrows = sum(log.get('arrows_shot', 0) for log in user_data)
        except json.JSONDecodeError:
            pass  # Return 0 if data is corrupted
    return total_shot_arrows

def calculate_weekly_progress(start_date, target_arrows, total_shot_arrows):
    """Calculate shooting progress per week."""
    if not start_date:
        return 999, 999, 999  # Default values if no start date

    try:
        week_0 = datetime.strptime(start_date, '%Y-%m-%d').isocalendar()[1]
        this_week = datetime.now().isocalendar()[1]
        week_of_year = max(1, this_week - week_0)  # Prevent division by zero

        weekly_target = int(target_arrows) // 52 if int(target_arrows) else 0
        arrows_per_week = total_shot_arrows // week_of_year

        return week_of_year, arrows_per_week, weekly_target
    except ValueError:
        return 0, 0, 0  # Return default values if date parsing fails
