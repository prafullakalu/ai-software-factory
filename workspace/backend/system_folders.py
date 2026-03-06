import os

# Define the list of system folders based on the database schema
db_schema_folders = ['users', 'products', 'orders', 'logs']

# Function to create system folders

def create_system_folders(folder_list):
    for folder in folder_list:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f'Created folder: {folder}')
        else:
            print(f'Folder already exists: {folder}')