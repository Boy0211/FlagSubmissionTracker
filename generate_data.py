import csv
import time
import random
from datetime import datetime

# Initial data setup
def generate_initial_data(csv_file):
    fieldnames = ['target_index', 'flag', 'submit_success', 'timestamp']
    
    # Some initial dummy data with current timestamps
    initial_data = [
        {'target_index': 1, 'flag': 'OS{init_flag_1}', 'submit_success': 'True', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        {'target_index': 2, 'flag': 'OS{init_flag_2}', 'submit_success': 'False', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        {'target_index': 3, 'flag': 'OS{init_flag_3}', 'submit_success': 'True', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        {'target_index': 4, 'flag': 'OS{init_flag_4}', 'submit_success': 'True', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ]

    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in initial_data:
            writer.writerow(row)

def generate_random_update(target_id):
    # Generate a random flag, success status, and timestamp
    flag = f"OS{{auto_flag_{random.randint(1000, 9999)}}}"
    submit_success = random.choice(['True', 'False'])
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {'target_index': target_id, 'flag': flag, 'submit_success': submit_success, 'timestamp': timestamp}

# Generate updates periodically
def update_csv_periodically(csv_file):
    fieldnames = ['target_index', 'flag', 'submit_success', 'timestamp']
    
    while True:
        for target_id in range(1, 9):
            # Generate random update
            new_entry = generate_random_update(target_id)
            
            # Write the update to the CSV file
            with open(csv_file, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(new_entry)

            print(f"Written to target {target_id}: {new_entry}")
        
        print("\nNext update in 1 minute...\n")
        time.sleep(60)  # Wait for 60 seconds before the next update

if __name__ == "__main__":
    csv_file_path = 'targets.csv'  # Path to the CSV file

    # Generate initial data if the file doesn't exist
    try:
        with open(csv_file_path, 'r') as _:
            pass
    except FileNotFoundError:
        generate_initial_data(csv_file_path)
    
    # Start updating the CSV file every minute
    update_csv_periodically(csv_file_path)
