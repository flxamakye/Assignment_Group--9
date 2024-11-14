import datetime as dt
import requests
import pandas as pd
import os

file_object = open('C:\\Users\\Noah\\Desktop\\BALLINGS\\groupassignment.txt', 'a') 
file_object.write('Executed on ' + str(dt.datetime.now()) + '\n') 
file_object.close()


# Fetch the script from the URL and execute it
url = 'http://ballings.co/data.py'
exec(requests.get(url).content)

# Define the directory and file path where the CSV file is saved
save_directory = r'C:\\Users\\Noah\\Desktop\\BALLINGS'  # Change this to your desired path
file_name = 'sales_data.csv'
file_path = os.path.join(save_directory, file_name)

# Check if the file exists, and if it does, append the new data
if os.path.exists(file_path):
    # Read the existing file to check for duplicates (optional step)
    existing_data = pd.read_csv(file_path)
    
    # Append the new data to the existing file
    data.to_csv(file_path, mode='a', header=False, index=False)
    print(f"New data appended to {file_path}")
else:
    # If the file doesn't exist, create it and save the data
    data.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")



