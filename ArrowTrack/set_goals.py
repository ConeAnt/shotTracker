import json
import os

# Get Archers Name
# just working with ant.json for now
# Get annual target
def get_target_arrows():
    filename = 'ant_goals.json'
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                file_data = json.load(file)
                for key, value in file_data.items():
                    if key == 'ANNUAL_TARGET':
                        return value
        except:
            print("Didn't work...")
    else:
        print(f"file {filename} not found...?")

print(f"Target Arrows: {get_target_arrows()}")
