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
    def send(self, state, other):
        msg = f'You {state} against "{other}"'
        with sk.socket(sk.AF_INET, sk.SOCK_STREAM) as s:
            s.connect((self.player[0], self.player[1]))
            s.sendall(msg.encode())

class Game(list):
    def __init__(self):
        super().__init__()
    def add(self, play:Play):
        self.append(play)
        if len(self) == 2:
            self.get_winner()
            self = []
    def get_winner(self):
        if self[0].choice == 'Rock':
            if self[1].choice == 'Rock':
                print('Tie')
                self[0].send('Tied', self[1].name)
                self[1].send('Tied', self[0].name)
            if self[1].choice == 'Paper':
                print(f'{self[1].name} at {self[1].player} Won')
                self[0].send('Lost', self[1].name)
                self[1].send('Won', self[0].name)
            if self[1].choice == 'Scicors':
                print(f'{self[0].name} at {self[0].player} Won')
                self[0].send('Won', self[1].name)
                self[1].send('Won', self[0].name)
        elif self[0].choice == 'Paper':
            if self[1].choice == 'Rock':
                print(f'{self[0].name} at {self[0].player} Won')
                self[0].send('Won', self[1].name)
                self[1].send('Lost', self[0].name)
            if self[1].choice == 'Paper':
                print('Tie')
                self[0].send('Tied', self[1].name)
                self[1].send('Tied', self[0].name)
            if self[1].choice == 'Scicors':
                print(f'{self[1].name} at {self[1].player} Won')
                self[0].send('Lost', self[1].name)
                self[1].send('Won', self[0].name)
        elif self[0].choice == 'Scicors':
            if self[1].choice == 'Rock':
                print(f'{self[1].name} at {self[1].player} Won')
                self[0].send('Lost', self[1].name)
                self[1].send('Won', self[0].name)
            if self[1].choice == 'Paper':
                print(f'{self[0].name} at {self[0].player} Won')
                self[0].send('Won', self[1].name)
                self[1].send('Lost', self[0].name)
            if self[1].choice == 'Scicors':
                print('Tie')
                self[0].send('Tied', self[1].name)
                self[1].send('Tied', self[0].name)

game = Game()

with sk.socket(sk.AF_INET, sk.SOCK_STREAM)  as s:
    s.bind((HOST, PORT))
    s.listen()
    while 1:
        con, adr = s.accept() # conetion, adrress
        with con:
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
            con.sendall(f'{adr[0]}:{adr[1]}'.encode())