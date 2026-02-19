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
