import csv
import time
import os
from datetime import datetime

# Function to read the CSV file and return updates
def read_csv(file_path):
    updates = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            updates.append(
                (
                    int(row['target_index']),
                    row['flag'],
                    row['submit_success'],
                    row['timestamp'],
                )
            )
    return updates

# Function to track the latest submission status for each target
def track_targets(file_path):
    target_data = {}

    # Read the entire CSV at startup, ensuring we retain the last successful submission timestamp
    updates = read_csv(file_path)
    for target_index, flag, submit_success, timestamp in updates:
        # Initialize or update the data for each target
        if (
            target_index not in target_data
            or target_data[target_index]['flag'] != flag
        ):
            # If submission is successful, update or initialize timestamp
            if submit_success.lower() == 'true':
                target_data[target_index] = {
                    'flag': flag,
                    'submit_success': True,
                    'timestamp': timestamp,
                }
            else:
                # If unsuccessful, keep the previous timestamp (if it exists)
                target_data[target_index] = target_data.get(
                    target_index,
                    {
                        'flag': flag,
                        'submit_success': False,
                        'timestamp': None,  # No previous success, thus None
                    },
                )

    # Enter an indefinite loop to update the view dynamically
    while True:
        try:
            new_updates = read_csv(file_path)
            next_target_data = target_data.copy()

            for target_index, flag, submit_success, timestamp in new_updates:
                if (
                    target_index not in next_target_data
                    or next_target_data[target_index]['flag'] != flag
                ):
                    if submit_success.lower() == 'true':
                        next_target_data[target_index] = {
                            'flag': flag,
                            'submit_success': True,
                            'timestamp': timestamp,
                        }
                    else:
                        # If unsuccessful, retain the last successful timestamp
                        next_target_data[target_index] = {
                            'flag': flag,
                            'submit_success': False,
                            'timestamp': target_data.get(target_index, {}).get(
                                'timestamp', None
                            ),  # Keep the previous success timestamp
                        }

            if next_target_data != target_data:
                target_data = next_target_data

                # Clear the console
                os.system('cls' if os.name == 'nt' else 'clear')

                print('Latest Status:')
                print(
                    'Target Index | Flag               | Submit Success  | Last Success Timestamp'
                )
                print(
                    '--------------------------------------------------------------------------------'
                )
                for index, data in sorted(target_data.items()):
                    timestamp_display = (
                        data['timestamp'] if data['timestamp'] else ""
                    )
                    print(
                        f'{index:<12} | {data["flag"]:<15} | {str(data["submit_success"]):<15} | {timestamp_display}'
                    )

            time.sleep(2)  # Check for updates every 2 seconds

        except Exception as e:
            print(f'Error reading file: {e}')
            time.sleep(2)  # Pause for 2 seconds before retrying


if __name__ == "__main__":
    csv_file_path = 'targets.csv'  # Update this to your csv file's path
    track_targets(csv_file_path)
