data_file = "data.txt"

with open(data_file, "r") as file:
    lines = file.readlines()

for line in lines:
    mail = line.strip().split("2")[2]
    print(mail)