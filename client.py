import socket as sk
from customtkinter import *
from PIL import Image
from threading import Thread as Thr

HOST = 'localhost'
PORT = 1914

def send(message:str):
    with sk.socket(sk.AF_INET, sk.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode())
        port = eval(s.recv(1024).decode())
        host = eval(s.recv(1024).decode())
    with sk.socket(sk.AF_INET, sk.SOCK_STREAM)  as s:
        s.bind((host, port))
        s.listen()
        while 1:
            con, adr = s.accept() # conetion, adrress
            with con:
                while 1:
                    data = con.recv(1024)
                    print(data)
                    if not data:
                        break
                    else:
                        pass

class App(CTk):
    def __init__(self):
        super().__init__()
        set_appearance_mode('dark')
        set_default_color_theme('green')
        self.title('Rock, Paper, Scisors')
        self.geometry('700x450')
    def press(self, option):
        sender = Thr(target=self.do, args=(option), daemon=True)
        sender.start()
    def do(self, option):
        self.nick = nick_input.get()
        if self.nick != '':
            alert.config(text=send(f'{[self.nick, option]}'))
            self.after(10000, lambda: alert.config(text=''))

root = App()

title = CTkLabel(root, text='Pick a Nickname and an Option', font=CTkFont('Arial', 22, 'bold'))
title.place(x=0, y=0)

nick_input = CTkEntry(root)
nick_input.place(x=0, y=35)

rockimg = Image.open('./assets/rock.png')
rock_img_large = CTkImage(dark_image=rockimg, size=(100, 100))
rock = CTkButton(root, height=100, width=100, image=rock_img_large, text='', command=lambda: root.press('1'))
rock.place(x=110, y=130)

paperimg = Image.open('./assets/paper.png')
paper_img_large = CTkImage(dark_image=paperimg, size=(100, 100))
paper = CTkButton(root, height=100, width=100, image=paper_img_large, text='', command=lambda: root.press('2'))
paper.place(x=280, y=130)

scisorsimg = Image.open('./assets/scisors.png')
scisors_img_large = CTkImage(dark_image=scisorsimg, size=(100, 100))
scisors = CTkButton(root, height=100, width=100, image=scisors_img_large, text='', command=lambda: root.press('3'))
scisors.place(x=450, y=130)

alert = CTkLabel(root, text='', font=CTkFont('Arial', 22, 'bold'))
alert.place(x=90, y=330)

root.mainloop()