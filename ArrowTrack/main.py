from nicegui import ui
import json
import os
from datetime import datetime
import queries as q
import parameters as param
import plotly.graph_objects as go
import queries as q

def save_settings_data(user_name_input, target_arrows, start_date, first_name_input):
    """ Save data captured from the setting page to a JSON file """
    user_name = user_name_input.value.lower().strip().replace('.', '_').replace('@', '_')
    if not user_name:
        ui.notify('Username is required!', type='negative')
        return

    start_week = datetime.strptime(start_date, '%Y-%m-%d').isocalendar()[1]
    user_data = {
        "username": user_name,
        "first_name": first_name_input.value.strip(),
        "annual_target_arrows": target_arrows.value.strip(),
        "start_date": start_date.value.strip(),
        "start_week": start_week
    }

    filename = f"{user_name}.json"
    with open(filename, 'w') as file:
        json.dump(user_data, file, indent=4)

    print(f"Saved user data to {filename}")

    # Clear text boxes
    user_name_input.set_value('')
    target_arrows.set_value('')
    start_date.set_value('')
    first_name_input.set_value('')
    
    ui.notify('Details saved')

def save_session_data(shoot_date, arrows_shot, score, notes):
    """ Save the data captured in session tab to a file, appending if it exists """
    username = 'antdyboll_gmail_com'  # ToDo - get from auth
    filename = f"{username}_log.json"
    formatted_date = datetime.strptime(shoot_date, '%Y-%m-%d')
    
    # Create a dictionary for the new session
    new_shoot_data = {
        'shoot_date': datetime.strftime(formatted_date, '%Y-%m-%d'),
        'week_number': formatted_date.isocalendar()[1] if shoot_date else None,
        'arrows_shot': int(arrows_shot.value),
        'perf_score': int(score.value),
        'notes': notes.value
    }
    
    # Check if the file exists and read existing data
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]  # Convert to list if necessary
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Append new data and write back to the file
    existing_data.append(new_shoot_data)
    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4)

    #Clear text boxes
    arrows_shot.set_value('')
    score.set_value('')
    notes.set_value('')
    print("Saved shooting log data")
    ui.notify("Shoot details saved")

with ui.tabs().classes('w-full') as tabs:
    settings = ui.tab('Settings')
    dashboard = ui.tab('Dashboard')
    logging = ui.tab('Log Session')

with ui.tab_panels(tabs, value=settings).classes('w-full'):
    with ui.tab_panel(settings):
        with ui.card():
            with ui.card_section():
                user_name_input = ui.input(label='Username', placeholder='email address')
                first_name_input = ui.input(label='First Name')
                target_arrows = ui.input(label='Annual Target Arrows')
                start_date = ui.input(label='Start Date', placeholder='2025-03-31')
                ui.button(
                    text='Save', 
                    on_click=lambda: save_settings_data(
                        user_name_input, 
                        target_arrows, 
                        start_date, 
                        first_name_input
                    )
                )
    with ui.tab_panel(dashboard):
        # Main execution
        user_start_date, user_target_arrows = q.get_settings_data()
        total_shot_arrows = q.get_total_shot_arrows()
        week_of_year, arrows_per_week, user_weekly_target = q.calculate_weekly_progress(
            user_start_date, user_target_arrows, total_shot_arrows
        )
        # Calculated Data
        catchup_arrows = (int(user_target_arrows) - int(total_shot_arrows))//(52 - week_of_year)
        target_to_date = week_of_year * (int(user_target_arrows)//52)
        arrows_behind = target_to_date - (int(total_shot_arrows))
        if int(total_shot_arrows) > target_to_date:
            msg = 'You are ahead by '
            arrows_behind *= -1
        else:
            msg = 'You are behind by '

        # Show Progress against annual target on slider
        ui.label('Total arrows shot against annual target')
        ui.linear_progress(value=int(total_shot_arrows) / int(user_target_arrows)).classes('w-full')
        slider_tot_arr = ui.slider(min=0, max=user_target_arrows, value=total_shot_arrows)
        slider_tot_arr.enabled = False
        ui.label(f'You have shot {total_shot_arrows} out of a target of {user_target_arrows} arrows')
        ui.separator()

        # Show YTD Progress
        ui.label(f'How you are tracking against weekly arrow targets. You should have shot {target_to_date} by now')
        slider_ytd_arr = ui.slider(min=0, max=target_to_date, value=total_shot_arrows)
        slider_ytd_arr.enabled = False
        ui.label(f'Target arrows per week is {user_weekly_target}, you need to shoot {catchup_arrows} per week to catch up')
        ui.separator()

        # See how you are doing over the last 4 weeks


        # Get total for last 4 weeks
        last_4 = q.last_4_weeks(datetime.today().isocalendar()[1])
        ui.label('Last 4 weeks arrow counts', )
        fig = go.Figure(go.Scatter(x=["Three weeks ago", "Two weeks ago", "Last week", 'This Week'], y=[last_4[3], last_4[2],last_4[1],last_4[0]]))
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        ui.plotly(fig).classes('w-full h-40')
        ui.label(f'You have shot for {week_of_year} weeks with an average of {arrows_per_week} arrows per week.')

    with ui.tab_panel(logging):
        ui.label('Put the session logger in here')
        with ui.card_section():
            """ date
                week#
                arrows
                score
                notes"""
            shoot_date = ui.date()
            shoot_date.set_value(datetime.now().date())  # Date picker instead of input
            arrows_shot = ui.input(label='Arrows Shot')
            score = ui.input(label='Performance Score')
            notes = ui.input(label='Notes')
            ui.button(
                text="save",
                on_click=lambda: [
                    save_session_data(
                        #'2025-01-01',
                        shoot_date.value if shoot_date.value else datetime.now().date(),
                        arrows_shot,
                        score,
                        notes
                )
                ])

ui.run()
