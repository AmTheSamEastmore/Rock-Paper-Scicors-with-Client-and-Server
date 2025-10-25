import socket as sk

# TCP = doesnt stop until info reaches

HOST = '0.0.0.0'
PORT = 1914

def log(adress, data):
    with open('./logs/messages.log', 'a') as x:
        x.write(f'({adress}, "{data}")\n')

class Play:
    def __init__(self, player, choice, name):
        self.player = player
        self.choice = choice
        self.name = name

class Game:
    def __init__(self):
        self.self = []
    def add(self, play:Play):
        self.self.append(play)
        if len(self.self) == 2:
            self.get_winner()
            self.self = []
    def get_winner(self):
        if self.self[0].choice == 'Rock':
            if self.self[1].choice == 'Rock':
                print('Tie')
            if self.self[1].choice == 'Paper':
                print(f'{self.self[1].name} at {self.self[1].player} Won')
            if self.self[1].choice == 'Scicors':
                print(f'{self.self[1].name} at {self.self[1].player} Won')
        elif self.self[0].choice == 'Paper':
            if self.self[1].choice == 'Rock':
                print(f'{self.self[1].name} at {self.self[1].player} Won')
            if self.self[1].choice == 'Paper':
                print('Tie')
            if self.self[1].choice == 'Scicors':
                print(f'{self.self[1].name} at {self.self[1].player} Won')
        elif self.self[0].choice == 'Scicors':
            if self.self[1].choice == 'Rock':
                print(f'{self.self[1].name} at {self.self[1].player} Won')
            if self.self[1].choice == 'Paper':
                print(f'{self.self[1].name} at {self.self[1].player} Won')
            if self.self[1].choice == 'Scicors':
                print('Tie')

game = Game()

with sk.socket(sk.AF_INET, sk.SOCK_STREAM)  as s:
    s.bind((HOST, PORT))
    s.listen()
    while 1:
        con, adr = s.accept() # conetion, adrress
        with con:
            while 1:
                data = con.recv(1024)
                if not data:
                    break
                else:
                    message = eval(data.decode())
                    log(adr, message)
                    if message[1] == '1':
                        print(f'{message[0]} at {adr} chose Rock')
                        game.add(Play(adr, 'Rock', message[0]))
                    elif message[1] == '2':
                        print(f'{message[0]} at {adr} chose Paper')
                        game.add(Play(adr, 'Paper', message[0]))
                    elif message[1] == '3':
                        print(f'{message[0]} at {adr} chose Scicors')
                        game.add(Play(adr, 'Rock', message[0]))
                con.sendall(f'[{adr}, {con}]'.encode())