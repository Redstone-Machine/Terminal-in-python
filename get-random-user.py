import random 

data_file = "data.txt"

with open(data_file, "r") as file:
    file_content = file.readlines()

random_user = random.choice(file_content).strip().split("¢")

print("Namn: " + random_user[0] + "\nTelefonnummer: " + random_user[1] + "\nMail: " + random_user[2])