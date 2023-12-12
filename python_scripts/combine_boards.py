import boardlib.api.aurora as aur
import json

def combine_gym_data():
    # List of board types
    board_types = ['tension', 'kilter', 'grasshopper', 'touchstone', 'decoy']

    # Initialize an empty list to hold all gym data
    all_gyms = []

    # Iterate over each board type
    for board in board_types:
        # Fetch the gym data for the current board
        gyms_data = aur.get_gyms(board)

        # Check if 'gyms' key exists and has data
        if 'gyms' in gyms_data and gyms_data['gyms']:
            # Add the board type to each gym's data
            for gym in gyms_data['gyms']:
                gym['board'] = board
                all_gyms.append(gym)

    return all_gyms

combined_gyms = combine_gym_data()
# Write the combined gyms data to a JSON file
with open('combined_gyms.json', 'w') as file:
    json.dump(combined_gyms, file, indent=4)

print("Data successfully written to combined_gyms.json")