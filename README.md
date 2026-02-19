# Wythoffs-Game
TCP-based two-player Wythoff’s Game implementation using Python sockets and multithreading.

This project implements the classical Wythoff’s Game using Python’s built-in socket module.
The game is designed as a client–server application, supporting two-player interaction over TCP connections.

The server handles multiple clients using multithreading and enforces game rules, turn order, and move validation.

# Features
- TCP-based client–server architecture
- Multi-threaded server implementation
- Real-time two-player gameplay
- Turn-based move validation
- Proper message formatting and protocol handling
- Error handling for invalid moves
- Game state synchronization between clients

# Game Rules
Wythoff’s Game consists of two piles of objects.
Players take turns and may:
- Remove objects from one pile only, or
- Remove the same number of objects from both piles
The player who removes the last object(s) wins.

# How to Run

### 1) Start the Server

Open a terminal and run:

```bash
python WythoffsGameServer.py <port> <pile1> <pile2>
```

Example:

```bash
python WythoffsGameServer.py 6000 7 5
```

---

### 2) Start Client 1

Open a new terminal and run:

```bash
python WythoffsGameClient.py localhost 6000
```

---

### 3) Start Client 2

Open another terminal and run:

```bash
python WythoffsGameClient.py localhost 6000
```

---

The game starts automatically once both clients are connected.

