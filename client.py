import socket as sk
from customtkinter import *
from PIL import Image

HOST = 'localhost'
PORT = 1914

def send(message:str):
    with sk.socket(sk.AF_INET, sk.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode())
        print(s.recv(1024).decode())

class App(CTk):
    def __init__(self):
        super().__init__()
        set_appearance_mode('dark')
        set_default_color_theme('green')
        self.title('Rock, Paper, Scisors')
        self.geometry('700x450')

root = App()

rockimg = Image.open('./assets/rock.png')
rock_img_large = CTkImage(dark_image=rockimg, size=(100, 100))
rock = CTkButton(root, height=100, width=100, image=rock_img_large, text='')
rock.place(x=110, y=130)

paperimg = Image.open('./assets/paper.png')
paper_img_large = CTkImage(dark_image=paperimg, size=(100, 100))
paper = CTkButton(root, height=100, width=100, image=paper_img_large, text='')
paper.place(x=280, y=130)

scisorsimg = Image.open('./assets/scisors.png')
scisors_img_large = CTkImage(dark_image=scisorsimg, size=(100, 100))
scisors = CTkButton(root, height=100, width=100, image=scisors_img_large, text='')
scisors.place(x=450, y=130)

root.mainloop()