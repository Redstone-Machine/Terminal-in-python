from nis import cat
import subprocess
import sys
import readline
import random
import time
import re

# Definerar filer
data_file = "data.txt"
current_password_file = "current-password.txt"
password_list = "different-passwords.txt"
current_ip_file = "current-ip.txt"
server_list = "ip-list.txt"
style_file = "style.txt"

# Skapar filer om dessa inte existerar
try:
    with open(current_password_file, "r") as file:
        lines = file.readlines()
except FileNotFoundError:
    print("Skapar en nuvarande lösenords fil.")
    with open(current_password_file, "w") as file:
        file.write("")

try:
    with open(current_ip_file, "r") as file:
        lines = file.readlines()
except FileNotFoundError:
    print("Skapar en nuvarande IP fil.")
    with open(current_ip_file, "w") as file:
        file.write("")

# Sätter några globala variabler
pwd = "/"
the_ip = "192.168.0.15"
the_password = "password"
history = []

company = "insert"
start_text = "Välkommen!"
company_secrets = "hemligheter"
course_material = "Idag ska ni testa en terminal!"

# Ändrar variabler baserat på style.txt
try:
    with open(style_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        if " = " not in line:
            continue

        key, value = line.split(" = ", 1)
        value = value.replace("{company}", company).replace("\\n", "\n")

        match key:
            case "company":
                company = value
            case "start_text":
                start_text = value
            case "company_secrets":
                company_secrets = value
            case "course_material":
                course_material = value
except:
    pass

# Denna kod stänger av ctrl-c för att avsluta koden
# signal.signal(signal.SIGINT, signal.SIG_IGN)

# Alla prints använder denna för att lägga till en tomrad över och under för att göra det mer lätläst. Den gör det även möjligt att göra felmeddelanden röda
def print_style(print_input, status=None):

    if status == "error":
        print("\033[31m", end="")

    print("")
    print(print_input)
    print("")

    if status == "error":
        print("\033[0m", end="")

# Koden som körs varje gång koden startar
def start():

    subprocess.run("clear")
    change_password()
    print(start_text)

# Vanliga terminal få input funktionen
def ask_for_input():

    if pwd == "/":
        show_pwd = "/"
    else:
        show_pwd = pwd.split("/")[-1]

    prompt = f"{company}@laptop {show_pwd} % "
    cur_input = input(prompt)

    if cur_input.strip():
        readline.add_history(cur_input)

    return cur_input

# Input funktionen till tävlingen
def ask_for_input_program():

    cur_input = input("> ")
    
    return cur_input

# Hämtar senaste lösenordet och IP:n från respektive filer
def update_password():

    global the_password
    global the_ip

    with open(current_password_file, "r") as file:
        file_content = file.readlines()
        the_password = file_content[0].strip()
    
    with open(current_ip_file, "r") as file:
        file_content = file.readlines()
        the_ip = file_content[0].strip()

# Slumpar lösenordet och IP:n
def change_password():
    
    with open(password_list, "r") as file:
        file_content = file.readlines()

    random_password = random.choice(file_content).strip()

    with open(current_password_file, "w") as file:
        file.write(random_password)

    with open(server_list, "r") as file:
        file_content = file.readlines()

    random_ip = random.choice(file_content).strip()

    with open(current_ip_file, "w") as file:
        file.write(random_ip)

# Tar historik och liknande
def restore():

    readline.clear_history()
    history = []
    pwd = "/"
    start()

# Om du ger inputen av en mapp skickar den tillbaka innehållet i mappen
def get_info_from_folder(folder):

    match folder:
        case "/":
            return "file.txt     hemlig_mapp    massa_bös"
        case "hemlig_mapp":
            return f"{company}_secrets.txt"
        case "massa_bös":
            return "kursmaterial.txt    logga.png"
        case _:
            return ""

# Kollar om inputen är en existerande fil eller mapp
def check_if_valid_folder_or_file(path, folder_or_file):

    if pwd == "/":
        cur_folder = "root"
    else:
        cur_folder = pwd.split("/")[-1]

    path = path.replace(company, "company")
    match path:
        case "hemlig_mapp" | "massa_bös" | "file.txt":
            if cur_folder == "root":
                if folder_or_file == "file" and path == "file.txt":
                    return True
                elif folder_or_file == "folder" and not path == "file.txt":
                    return True 
                else:
                    return False
            else:
                return False
        case "company_secrets.txt":
            if cur_folder == "hemlig_mapp" and folder_or_file == "file":
                return True
            else:
                return False
        case "kursmaterial.txt" | "logga.png":
            if cur_folder == "massa_bös" and folder_or_file == "file":
                return True
            else:
                return False
        case _:
            return False

# Kollar om inputen är i formatet av en IP
def check_if_ip(ip: str):

    ip_split = ip.split(".")

    if len(ip_split) == 4:
        return True
    else:
        return False

# Returnerar en man text till programmet man skickar som input
def get_man(program):

    match program:
        case "pwd":
            return "Kommandot berättar vart du är i filsystemet"
        case "ls":
            return "Kommandot listar filer och mappar där du är i filsystemet."
        case "cd":
            return "Kommandot flyttar dig till en annan mapp i filsystemet.\nTill exempel \"cd hemlig_mapp\."
        case "cat":
            return "Kommandot visar innehållet i en fil.\nTill exempel \"cat file.txt\"."
        case "echo":
            return "Kommandot skriver ut det du skriver efter kommandot."
        case "clear":
            return "Kommandot rensar texten i terminalen."
        case "history":
            return "Kommandot visar en lista på alla kommandon du har skrivit i terminalen."
        case "whoami":
            return "Kommandot visar vilket användarnamn du är inloggad som."
        case "date":
            return "Kommandot visar nuvarande datum och tid."
        case "help":
            return "Kommandot ger en lista på alla kommandon som finns i den här terminalen."
        case "nmap":
            return "NMAP används för att skanna ett nätverk.\nGenom att skriva \"nmap 192.168.0.0/8\" skannar du det lokala nätverket."
        case "ping":
            return "Kommandot ping används för att kolla om en dator är online.\nTill exempel \"ping 192.168.0.11\"."
        case "curl":
            return "Kommandot curl används för se innehållet på en hemsida från en ip-adress.\nTill exempel \"curl 192.168.0.11\"."
        case _:
            return "Det finns ingen dokumentation för det kommandot."

# Skriver ut alla program som terminalen stödjer
def help():
    print_style(
        "Den här terminalen stödjer dessa kommandon:\n" +
        "pwd\n" +
        "ls\n" +
        "cd\n" +
        "cat\n" +
        "echo\n" +
        "clear\n" +
        "history\n" +
        "whoami\n" +
        "date\n" +
        "nmap\n" +
        "ping\n" +
        "curl"
    )

# Funktion för att låtsas vara ls kommandot
def ls():
    if pwd == "/":
        folder_print = get_info_from_folder("/")
    else:
        cur_folder = pwd.split("/")[-1]
        folder_print = get_info_from_folder(cur_folder)
    
    print_style(folder_print)

# Funktion för att låtsas vara cd kommandot
def cd(where_to_go):
    global pwd
    match where_to_go:
        case ".." | "../":
            if pwd != "/":
                pwd_split = pwd.split("/")
                pwd = "/".join(pwd_split[:-1])
                if pwd == "":
                    pwd = "/"

        case "/" | "":
            pwd = "/"

        case _:
            if check_if_valid_folder_or_file(where_to_go, "folder"):
                pwd = pwd + where_to_go
    return

# Funktion för att låtsas vara cat kommandot
def cat(what_to_cat):
    if check_if_valid_folder_or_file(what_to_cat, "file"):
        what_to_cat = what_to_cat.replace(company, "company")
        match what_to_cat:
            case "file.txt":
                print_style("Hej hej gymnasiemässan!")
            case "company_secrets.txt":
                print_style(company_secrets)
            case "kursmaterial.txt":
                print_style(course_material)
            case "logga.png":
                print_style("Nk?ê?î?ù?'??êHg$&L??hpB?ZBVa??BêH6?D'.	5????3??1J????pM?4 \nWO?b?RX??Tq-DŅ?P?=?]?#PS???P?$C?/qL??E???                                           ?N?H?{@06??`??f?KZX~???I?*?V?????N?.??5a?;X?!?,???o\n????Nî???Y?à?K?ߩ0?àà?+?;wﻳ?????v=>??ô0B???ô?è?ckô\nb?撳<h?g?yt8E??+???é?f???ké?J?	\n                               ?7:ôL??%?8?D?P?s?\n                                                J,0 ?Lp+d???Uf???V?î-i?àNa????Q???fU??Ϭ??ǆ???W?F???ê?O_zŵ?k?é???h#?f?=?w??$ݲ????L䛙?.?.?彽ݫO_;ù0\n                                                                    C????'Q?_??1Y??sIl@F??s?ET??zX??C?4?n'K?.????mm Qq?갱<YVR???y[{?8w?S?䤘??Xꟕ?i?$?Kd? ??o?ʕ?????F???`0\n        ?>\n          ?A?$???8??|*￹^??YW?܎t??H0????g?$?x<?|Xpəg?P?r??-q?9?iB۱D?Ӕ??]_'4??6-wZ?`????UP&D&?2#?!sFi@?>s&?԰z\ni<??m??儗$^     ?7??.hx*ù?%???ù?????Wéw?8?iۺŋ?k????dt???8s??V?????\n                                         ???A\n                                             ?????3?ypuߝk7\n	??Lb??3? !????+???>???çn6??M?\n?q??wà???$nK??fC???3??k???#?g?t????+T??ù!?ϵ-+?/?Q;??I?û??C?é????1è?s?dl-??\n??/O?N???r??z?????`0??`0\n                        ~?|?w??3???7y?????S??x?f?K\???.R?8???.S???E?{Ӽ/?D??%?ވ8'??)$???i??&?L3??<o??$?0?g{w??????YY???D&o&ȅ???<??$	!$?Γ??lR?????ka??/?t?t?0/EMwM\n     Nh-1F?j?H?? ??û?????à?U?G????wuôm?àFB?? -???	G??G???è?zp????X'çV???3â???٠_?7S???t????X??JZuN??5ů??\n                              /..?733g????>z?????v??i???Ul??~????\?YkyB?`?1*?IT???!&gf?Uqԩ?'mڜgN/H???U????<??1??b.??5b??U1?(%?(?J??5??	 q????%?fї??u0	??+ ???P\+b??G?2???s??????R?H?H Pf3??H??hn?????'wO~???n?_???9@733????6?ӻ??mv??Ө??&??D???I??a?_????s?O?y4R9?5??&*?jD#??ç??aqc䒵?5?.?f?8??Zo??Z&?T??àI \n                                                               ??P???w?mf??????*?g???è????-????????????????????????????????????????????????????????????>g?b\n          ?`??0IEND?B`?% ")
            case _:
                print_style("cat: " + what_to_cat + ": No such file")

    else:
        if check_if_valid_folder_or_file(what_to_cat, "folder"):
            print_style("cat: " + what_to_cat + ": No such file")
        else:
            print_style("cat: " + what_to_cat + ": No such file or directory")

# Funktion för att låtsas vara nmap kommandot. Den slumpar en del för att ge känslan att man gör olika nmaps.
# Den är hårdkodad till vad den kommer visa. Så den utgår från att den får samma sträng.
def nmap():
    
    print("")
    procent = 0
    seconds = 0
    while procent < 100:
        print("Stats: 0:00:0" + str(seconds) + " elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan\nConnect Scan Timing: About " + str(procent) + "." + str(random.randint(0, 99)) + "% done; (0:00:0" + str(9 - seconds) + " remaining)")
        procent = procent + random.randint(10, 20)
        seconds = seconds + 1
        time.sleep(1)
        print("\033[2A", end="")

    print("Stats: 0:00:0" + str(seconds) + " elapsed; 0 hosts completed (3 up), 1 undergoing Connect Scan\nConnect Scan Timing: About 100.00% done; (0:00:00 remaining)\n")

    print(
    "Nmap scan report for 192.168.0.11\n" +
    "Host is up (0.000068s latency).\n" +
    "Not shown: 998 closed tcp ports (conn-refused)\n" +
    "PORT     STATE SERVICE\n" +
    "22/tcp   open  ssh\n" +
    "5900/tcp open  vnc\n\n" +

    "Nmap scan report for " + the_ip + "\n"
    "Host is up (0.032s latency).\n"
    "Not shown: 999 filtered tcp ports (no-response)\n"
    "PORT     STATE  SERVICE\n"
    "\033[4m80/tcp   open   http SUPER HEMLIG\033[0m\n\n"

    "Nmap scan report for 192.168.0.48\n"
    "Host is up (0.000068s latency).\n"
    "Not shown: 998 closed tcp ports (conn-refused)\n"
    "PORT     STATE SERVICE\n"
    "23/tcp   closed telnet\n"
    "5900/tcp open  vnc\n"
    )

    print_style("\033[4mOm du ser att port 80 är öppen. Testa att skriva \"curl *den-ip-adressen*\033[0m\"")

# Ping kollar ifall ip:n finns definierad i koden. Och låtsas då komma åt mottagaren, annars försöker den och misslyckas.
# Även här lite slumpade saker, men svaret är hårdkodat.
def ping(ip):

    if not check_if_ip(ip):
        print_style("Du gav ingen IP.", "error")
        return

    i=0

    print("PING " + ip + " (" + ip + ") 56(84) bytes of data.")

    real_ip = False

    if ip == "192.168.0.11" or ip == the_ip or ip == "192.168.0.48":
        real_ip = True

    if real_ip:
        while i < 15:
            i = i + 1
            print("64 bytes from " + ip + ": icmp_seq=" + str(i) + " ttl=64 time=0.0" + str(random.randint(10, 35)) + " ms")
            time.sleep(0.4)
        print(
        "\n--- " + ip + " ping statistics ---\n" +
        "15 packets transmitted, 15 received, 0% packet loss, time 6" + str(random.randint(100, 900)) + "ms\n"
        )
    else:
        while i < 10:
            i = i + 1
            print("From " + ip + " icmp_seq=" + str(i) + " Destination Host Unreachable")
            time.sleep(0.4)

        print(
            "\n--- " + ip + " ping statistics ---\n" +
            "10 packets transmitted, 0 received, 100% packet loss, time 4" + str(random.randint(100, 900)) + "ms\n"
            )

# Den kan curla det vi definierat
def curl(ip):

    if not check_if_ip(ip):
        print_style("Du gav ingen IP.", "error")
        return

    real_ip = False

    if ip == the_ip or ip == the_ip + ":80":
        real_ip = True

    if real_ip:
        print(
            "\n<!DOCTYPE html>\n"
            "<html>\n"
            "<head>\n"
            "<title>Super hemligt!</title>\n"
            "<style>\n"
            "html { color-scheme: light dark; }\n"
            "body { width: 35em; margin: 0 auto;\n"
            "font-family: Tahoma, Verdana, Arial, sans-serif; }\n"
            "</style>\n"
            "</head>\n"
            "<body>\n"
            "<h1>Det här är den superhemliga sidan!</h1>\n"
            "\033[4m<p>Lösenordet är: " + the_password + "</p>\033[0m\n"
            "</body>\n"
            "</html>\n"
        )
    else:
        print_style("curl: (7) Failed to connect to " + ip + " port 80 after " + str(random.randint(10, 80)) + " ms: Couldn't connect to server")

# Kollar om lösenordet du gav är korrekt. Isåfall ändrar den framtida lösenord och returnar success. Annars berättar den att det var fel
def check_password(password):
    if password == the_password:
        print_style("SNYGGT! Du hittade lösenordet.")
        change_password()
        update_password()
        return 0
    else:
        print_style("Fel lösenord!", "error")
        return 1

# Frågar om information om tävlingen och sparar det i en fil
def ask_for_information():
    while True:
        print_style("Vill du vara med i tävlingen? (ja/nej)")
        user_input = ask_for_input_program().upper()


        if user_input == "JA":
            break
        elif user_input == "NEJ":
            print_style("Okej! Bra jobbat med att hitta lösenordet.")
            return
        else:
            print_style("Du gav inte svaret (ja/nej)", "error")

    while True:
        print_style("För att vara med kommer vi spara din mailadress till " + company + ":s maillista, är det okej? (ja/nej)")
        user_input = ask_for_input_program().upper()

        if user_input == "JA":
            break
        elif user_input == "NEJ":
            print_style("Okej! Då skippar vi tävlingen den här gången ;)\nBra jobbat med att hitta lösenordet!")
            return
        else:
            print_style("Du gav inte svaret (ja/nej)", "error")

    print_style("Vad heter du? Denna information kommer raderas efter tävlingen. (För att avsluta skriv 'exit')")
    user_input = ask_for_input_program()

    if user_input == "exit":
        return
    else:
        name = user_input

    print_style("Vad är ditt telefonnummer? Vi kommer kontakta dig genom detta om du vunnit. Denna information kommer raderas efter tävlingen. (För att avsluta skriv 'exit')")
    user_input = ask_for_input_program()

    if user_input == "exit":
        return
    else:
        phone = user_input.replace("¢", "")

    print_style("Vad är din mailadress? Denna mail kommer registreras till " + company + ":s maillista. (För att avsluta skriv 'exit')")
    user_input = ask_for_input_program()

    if user_input == "exit":
        return
    else:
        mail = user_input

    print_style("Det var allt! Om du vunnit kommer vi kontakta dig på ditt telefonnumer.")

    with open(data_file, "a") as file:
        file.write(name + "¢" + phone + "¢" + mail + "\n")
    
    time.sleep(4)
    restore()
    
# Koden som faktiskt körs.
start()

while True:

    update_password()

    base_command = ""
    flag1 = ""
    flag2 = ""
    
    # Input av användaren
    user_input = ask_for_input()

    parts = re.split(r'["\']', str(user_input))
    if len(parts) > 1:
        user_input_hashtag_phrase = parts[1].replace(" ", "¢")
        user_input = parts[0] + user_input_hashtag_phrase + parts[2]


    user_input_split = user_input.split(" ")

    continue_script = True

    # Parsar inputen
    if len(user_input_split) > 0 :
        base_command = user_input_split[0]
    else:  
        print_style("Ingen input gavs")
        continue_script = False
    
    if len(user_input_split) > 1:
        flag1 = user_input_split[1]


    if len(user_input_split) > 2:
        flag2 = user_input_split[2]

    if len(user_input_split) > 3:
        print_style("Det finns inte stöd för fler än två flaggor.", "error")
        continue_script = False

    if flag1 == "--man":
        man = get_man(base_command)
        print_style(man)
        continue_script = False

    # Kör själva koden
    if continue_script:

        match base_command:
            
            # I production skulle jag kommentera ut första raden, och avkommentera den undre för att göra scriptet svårare att avsluta
            case "break" | "exit" | "quit":
            # case "force_quit":
                sys.exit()
            case "restore":
                restore()
            case "pwd":
                print_style(pwd)
            case "ls":
                ls()
            case "cd":
                cd(flag1)
            case "cat":
                cat(flag1)
            case "echo":
                echo = flag1.replace("\"", "").replace("'", "")
                echo = echo.replace("¢", " ")
                print_style(echo)
            case "clear":
                subprocess.run("clear")
            case "history":
                history_print = "\n".join(history)
                print_style(history_print)
            case "whoami":
                print_style(company)
            case "date":
                print("")
                subprocess.run("date")
                print("")
            case "mkdir" | "rmdir" | "rm" | "cp" | "mv" | "touch":
                print_style("Alla typer av filändringar är avstängt i terminalen.", "error")
            case "nmap":
                if flag1 == "192.168.0.0/8":
                    nmap()
                else:
                    print_style("Ett tips, kör \"nmap 192.168.0.0/8\".")
            case "ping":
                ping(flag1)
            case "curl":
                curl(flag1)
            case "help":
                help()
            case "password":
                result = check_password(flag1)
                if result == 0:
                    ask_for_information()
            case _:
                print_style("Kommandot fungerar inte i denna terminal.", "error")

        history.append(user_input)