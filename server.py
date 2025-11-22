import socket as sk
import ast

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
        try:
            with sk.socket(sk.AF_INET, sk.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((self.player[0], self.player[1]))
                s.sendall(msg.encode())
        except Exception as e:
            # If the client isn't listening for direct connections this will fail
            # Log the error so the server keeps running.
            print(f"Failed to send to {self.name} at {self.player}: {e}")

class Game(list):
    def __init__(self):
        super().__init__()
    def add(self, play:Play):
        self.append(play)
        if len(self) == 2:
            self.get_winner()
            # Clear the matches so a new game can start
            self.clear()
    def get_winner(self):
        # Determine winner between two Play objects and notify them.
        if len(self) < 2:
            return
        p1, p2 = self[0], self[1]
        # Normalize expected choice names
        choices_map = {
            'Rock': 'Rock',
            'Paper': 'Paper',
            'Scissors': 'Scissors',
            'Scicors': 'Scissors'  # tolerate misspelling
        }
        c1 = choices_map.get(p1.choice, p1.choice)
        c2 = choices_map.get(p2.choice, p2.choice)

        if c1 == c2:
            print('Tie')
            p1.send('Tied', p2.name)
            p2.send('Tied', p1.name)
            return

        # rock beats scissors, scissors beats paper, paper beats rock
        beats = {'Rock': 'Scissors', 'Scissors': 'Paper', 'Paper': 'Rock'}
        if beats.get(c1) == c2:
            # p1 wins
            print(f'{p1.name} at {p1.player} Won')
            p1.send('Won', p2.name)
            p2.send('Lost', p1.name)
        else:
            # p2 wins
            print(f'{p2.name} at {p2.player} Won')
            p1.send('Lost', p2.name)
            p2.send('Won', p1.name)

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
                try:
                    message = ast.literal_eval(data.decode())
                except Exception:
                    # Fall back to raw split if literal_eval fails
                    message = tuple(data.decode().split(','))
                log(adr, message)
                if message[1] == '1':
                    print(f'{message[0]} at {adr} chose Rock')
                    game.add(Play(adr, 'Rock', message[0]))
                elif message[1] == '2':
                    print(f'{message[0]} at {adr} chose Paper')
                    game.add(Play(adr, 'Paper', message[0]))
                elif message[1] == '3':
                    print(f'{message[0]} at {adr} chose Scissors')
                    game.add(Play(adr, 'Scissors', message[0]))
            con.sendall(f'{adr[0]}:{adr[1]}'.encode())