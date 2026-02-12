import socket
import threading
from rich.prompt import Prompt
from crypto import Crypto
from ui import console, msg, sys, error, info

crypto = None
sock = None

def receive():
    while True:
        try:
            len_b = sock.recv(4)
            if not len_b: break
            ln = int.from_bytes(len_b, 'big')
            token = sock.recv(ln)
            text = crypto.decrypt(token)

            if "Online:" in text:
                console.print(f"[cyan bold]{text}[/]")
            elif "joined" in text or "left" in text:
                sys(text)
            else:
                msg("User", text)
        except:
            error("Disconnected")
            break

def run_client(host, port, key):
    global crypto, sock

    crypto = Crypto(key.encode())

    try:
        sock = socket.socket()
        sock.connect((host, port))
        info("Connected to Helia")
    except Exception as e:
        error(f"Connection failed: {e}")
        return

    threading.Thread(target=receive, daemon=True).start()

    info("Type messages (exit to quit)")

    while True:
        try:
            text = Prompt.ask("")
            if text.lower() in ("exit", "quit"):
                sock.sendall(crypto.encrypt("exit"))
                break
            if text.strip():
                sock.sendall(crypto.encrypt(text))
        except KeyboardInterrupt:
            break

    info("Disconnecting...")
    sock.close()
