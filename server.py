import socket as sk

# TCP = doesnt stop until info reaches

HOST = '0.0.0.0'
PORT = 1914

def log(adress, data):
    with open('./logs/messages.log', 'a') as x:
        x.write(f'({adress}, "{data}")\n')

class Play:
    def __init__(self, player, choice):
        self.player = player
        self.choice = choice

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
                print(f'{self.self[1].player} Won')
            if self.self[1].choice == 'Scicors':
                print(f'{self.self[0].player} Won')
        elif self.self[0].choice == 'Paper':
            if self.self[1].choice == 'Rock':
                print(f'{self.self[0].player} Won')
            if self.self[1].choice == 'Paper':
                print('Tie')
            if self.self[1].choice == 'Scicors':
                print(f'{self.self[1].player} Won')
        elif self.self[0].choice == 'Scicors':
            if self.self[1].choice == 'Rock':
                print(f'{self.self[1].player} Won')
            if self.self[1].choice == 'Paper':
                print(f'{self.self[0].player} Won')
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
                    log(adr, data.decode())
                    if data.decode() == '1':
                        print(f'{adr} chose Rock')
                        game.add(Play(adr, 'Rock'))
                    elif data.decode() == '2':
                        print(f'{adr} chose Paper')
                        game.add(Play(adr, 'Paper'))
                    elif data.decode() == '3':
                        print(f'{adr} chose Scicors')
                        game.add(Play(adr, 'Rock'))
                con.sendall(b'Recived messages')