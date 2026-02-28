import json
def save_to_file(data,filename):
    try:
        with open(filename, 'w') as file: #Writes
            json.dump(data, file, indent=4)
    except Exception as e:
        print("Error occurred while writing to file:", e)

