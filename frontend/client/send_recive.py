import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
from rich import console; print = console.Console().print
import os

os.system("cls" if os.name == "nt" else "clear")
# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

print("Welcome to the chatroom!", style="bold red")
print("Enter a username : ", end="", style="bold green")
name = input()
# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...", style="bold yellow")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.", style="bold green")

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        s.send(name.encode())
        try:
            message = message.split("]")[1]
        except:
            pass
        print(message.startswith(f"{name}"))
        if message.startswith(f"{name}"):
            print("\033[F\033[K", end="")
            print(message, style="bold blue")
            # move the cursor length of the name + 3 to the right
            print("\033[{}C".format(len(name) + 3), end="")
            

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    # input message we want to send to the server
    print(f"\n[bold green]{name} > ", end="")
    to_send = input()
    # a way to exit the program
    if to_send.lower() == 'q':
        break
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # finally, send the message
    s.send(to_send.encode())

# close the socket
s.close()