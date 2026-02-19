import socket
import sys
import json

player_id = None
clean_exit = False
latest_turn = None

if len(sys.argv) != 3:
    print("Usage: python WythoffsGameClient.py <server_ip> <port>")
    sys.exit(1)

SERVER_IP = sys.argv[1]
PORT = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

print("Connected to server.")

while True:
    try:
        msg = client_socket.recv(1024).decode()
        if not msg:
            break

        if player_id is None and "You are Player" in msg:
            print(msg)
            player_id = int(msg.strip()[-1])
            continue

        try:
            data = json.loads(msg)

            if data["type"] == "state":
                print(f"\nPiles: {data['piles']}")
                if data["turn"] != player_id:
                    print(f"It's Player {data['turn']}'s turn.")
                else:
                    move = input("Your turn. Enter move (pile_index count; use 2 for both): ")
                    client_socket.send(move.encode())

            elif data["type"] == "win":
                winner = data["winner"]
                if winner == player_id:
                    print("\nCongratulations! You win!")
                else:
                    print(f"\nGame over. Player {winner} is the winner.")
                clean_exit = True
                break


        except json.JSONDecodeError:
            print(msg)

            if "Illegal move" in msg or "Invalid format" in msg:
                move = input("Try again (pile_index count; use 2 for both): ")
                client_socket.send(move.encode())

    except KeyboardInterrupt:
        break

client_socket.close()

if clean_exit:
    print("Server has closed the connection.")
