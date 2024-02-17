import csv
from datetime import datetime

def reformat_data():
    
    # Read the CSV file
    with open('raw_data.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)

    # Code to reformat the data goes here
    for row in data[1:]:  # Skip the header row
        # Combine the date and time
        date_str = row[0]
        start_time_str = row[2]
        end_time_str = row[3]


        if 'PM' in start_time_str:  # Check if the time string is PM
            if ':' in start_time_str: # Checks if the time string contains a colon like 12:45PM, 5:30PM
                start_dt = datetime.strptime(f"{date_str} {start_time_str}", "%m/%d %H:%M%p")
                start_dt = start_dt.replace(hour=(start_dt.hour +  12)%24) # Convert into 24 hour format because of PM
                if start_dt.hour == 0: # Check if hour is zero because of conversion and turn it back to 12 
                    start_dt = start_dt.replace(hour=(12))
            else: # Do the same for time with no colon like 12PM, 5PM 
                start_dt = datetime.strptime(f"{date_str} {start_time_str}", "%m/%d %H%p")
                start_dt = start_dt.replace(hour=(start_dt.hour +  12)%24)
                if start_dt.hour == 0:
                    start_dt = start_dt.replace(hour=(12))
        elif 'AM' in start_time_str:  # Check if the time string is AM
            if ':' in start_time_str:  # Checks if the time string contains a colon like 12:45AM, 5:30AM
                start_dt = datetime.strptime(f"{date_str} {start_time_str}", "%m/%d %H:%M%p")
                if start_dt.hour == 12: # Check if start hour is 12 and make sure to add 1 to the day because of formatting
                    start_dt = start_dt.replace(hour=(0))
                    start_dt = start_dt.replace(day=(start_dt.day+1))
            else: # Do the same for time with no colon like 12PM, 5PM 
                start_dt = datetime.strptime(f"{date_str} {start_time_str}", "%m/%d %H%p")
                if start_dt.hour == 12:
                    start_dt = start_dt.replace(hour=(0))
                    start_dt = start_dt.replace(day=(start_dt.day+1))
            
        if 'PM' in end_time_str:
            if ':' in end_time_str:
                end_dt = datetime.strptime(f"{date_str} {end_time_str}", "%m/%d %H:%M%p")
                end_dt = end_dt.replace(hour=(end_dt.hour +  12)%24)
                if end_dt.hour == 0:
                    end_dt = end_dt.replace(hour=(12))
            else:
                end_dt = datetime.strptime(f"{date_str} {end_time_str}", "%m/%d %H%p")
                end_dt = end_dt.replace(hour=(end_dt.hour +  12)%24)
                if end_dt.hour == 0:
                    end_dt = end_dt.replace(hour=(12))
        elif 'AM' in end_time_str:
            if ':' in end_time_str:
                end_dt = datetime.strptime(f"{date_str} {end_time_str}", "%m/%d %H:%M%p")
                if end_dt.hour == 12:
                    end_dt = end_dt.replace(hour=(0))
                    end_dt = end_dt.replace(day=(end_dt.day+1))
            else:
                end_dt = datetime.strptime(f"{date_str} {end_time_str}", "%m/%d %H%p")
                if end_dt.hour == 12:
                    end_dt = end_dt.replace(hour=(0))
                    end_dt = end_dt.replace(day=(end_dt.day+1))

        # Format the datetime object into an ISO   8601 string
        row[2] = start_dt.replace(year=2024).isoformat() # Replace with the desired year
        row[3] = end_dt.replace(year=2024).isoformat()  # Replace with the desired year

    with open('raw_data.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header row without the 'date' column
        writer.writerow(['job_name', 'start_time', 'end_time'])
        # Write the rest of the rows without the 'date' column
        for row in data[1:]:
            writer.writerow(row[1:])  # Skip the first column ('date')

    print("Data reformatted and saved to raw_data.csv")
    if True:
        pass
