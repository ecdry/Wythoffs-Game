import socket
import threading
import sys
import json

pile_0 = 5
pile_1 = 10

if len(sys.argv) < 2:
    print("Usage: python WythoffsGameServer.py <port> [pile_0_size pile_1_size]")
    sys.exit(1)

PORT = int(sys.argv[1])
if len(sys.argv) == 4:
    pile_0 = int(sys.argv[2])
    pile_1 = int(sys.argv[3])

piles = [pile_0, pile_1]
clients = []
turn = 0

def send_to_all(message_dict):
    message = json.dumps(message_dict).encode()
    for c in clients:
        c.send(message)

def is_valid_move(pile_index, count):
    if count <= 0:
        return False, "Illegal move: you cannot remove 0 or negative objects."
    if pile_index == 0:
        if piles[0] >= count:
            return True, ""
        else:
            return False, f"Illegal move: not enough objects in pile 0."
    elif pile_index == 1:
        if piles[1] >= count:
            return True, ""
        else:
            return False, f"Illegal move: not enough objects in pile 1."
    elif pile_index == 2:
        if piles[0] >= count and piles[1] >= count:
            return True, ""
        else:
            return False, f"Illegal move: both piles do not have enough objects."
    return False, "Illegal move: invalid pile index."


def apply_move(pile_index, count):
    if pile_index == 0:
        piles[0] -= count
    elif pile_index == 1:
        piles[1] -= count
    elif pile_index == 2:
        piles[0] -= count
        piles[1] -= count

def handle_client(connection, address, player_id):
    global piles, turn

    connection.send(f"Connected. You are Player {player_id}".encode())

    while len(clients) < 2:
        pass

    if player_id == 0:
        print(f"Game is starting: Piles are {piles}")
        send_to_all({
            "type": "state",
            "piles": piles,
            "turn": turn
        })

    last_announced_turn = -1

    while True:
        if turn != player_id:
            continue

        if last_announced_turn != turn:
            print(f"Waiting for Player {player_id}'s move")
            last_announced_turn = turn

        try:
            move_data = connection.recv(1024).decode().strip()
        except ConnectionResetError:
            print(f"Player {player_id} disconnected. Shutting down game.")
            try:
                send_to_all({
                    "type": "disconnect",
                    "message": f"Player {player_id} has disconnected. Game aborted."
                })
            except:
                pass
            for c in clients:
                try:
                    c.close()
                except:
                    pass
            server_socket.close()
            sys.exit(0)

        try:
            pile_index, count = map(int, move_data.split())
        except:
            connection.send("Invalid format. Use: <pile_index> <count>".encode())
            continue

        valid, error_msg = is_valid_move(pile_index, count)
        if not valid:
            print(f"Received move from Player {player_id}: \"{move_data}\". {error_msg}")
            connection.send(error_msg.encode())
            continue

        print(f"Received move from Player {player_id}: \"{move_data}\". Legal move.")
        apply_move(pile_index, count)
        print(f"Piles after move: {piles}")

        if piles == [0, 0]:
            print(f"Game Over. Player {player_id} wins!")
            send_to_all({
                "type": "win",
                "winner": player_id
            })
            break

        turn = 1 - turn
        send_to_all({
            "type": "state",
            "piles": piles,
            "turn": turn
        })

    print("Closing connections.")
    connection.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', PORT))
server_socket.listen(2)

print(f"Server is listening on port {PORT}")


try:
    for player_id in range(2):
        connection, address = server_socket.accept()
        print(f"Player {player_id} is connected.")
        clients.append(connection)
        threading.Thread(target=handle_client, args=(connection, address, player_id)).start()

    while True:
        for t in threading.enumerate():
            if t is not threading.current_thread():
                t.join(0.1)

except KeyboardInterrupt:
    for c in clients:
        try:
            c.close()
        except:
            pass
    server_socket.close()
    sys.exit(0)