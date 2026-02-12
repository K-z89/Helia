import socket
import threading
from crypto import Crypto
from ui import sys, msg, info, error

clients = []
crypto = None
room_pw = ""

def broadcast(text, sender=None, skip=None, system=False):
    content = f"Helia: {text}" if system else f"{sender}: {text}"
    enc = crypto.encrypt(content)
    payload = len(enc).to_bytes(4, 'big') + enc

    for c_sock, _ in clients[:]:
        if c_sock is skip:
            continue
        try:
            c_sock.sendall(payload)
        except:
            clients.remove((c_sock, _))

def run_server(port, password, crypto_inst):
    global crypto, room_pw
    crypto = crypto_inst
    room_pw = password

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(200)

    info(f"Helia listening on port {port}")
    info(f"Password: {password}")

    while True:
        client, addr = s.accept()
        info(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

def handle_client(sock):
    nick = None
    try:
        sock.sendall(crypto.encrypt("Nickname: "))
        len_b = sock.recv(4)
        ln = int.from_bytes(len_b, 'big')
        token = sock.recv(ln)
        nick = crypto.decrypt(token).strip()

        sock.sendall(crypto.encrypt("Password: "))
        len_b = sock.recv(4)
        ln = int.from_bytes(len_b, 'big')
        token = sock.recv(ln)
        if crypto.decrypt(token).strip() != room_pw:
            sock.sendall(crypto.encrypt("Wrong password"))
            return

        clients.append((sock, nick))
        broadcast(f"→ {nick} joined", system=True)

        sock.sendall(crypto.encrypt("Helia welcomes you to the light 💜"))

        while True:
            len_b = sock.recv(4)
            if not len_b: break
            ln = int.from_bytes(len_b, 'big')
            token = sock.recv(ln)
            text = crypto.decrypt(token)

            if text == "exit": break

            if text.startswith("/"):
                if text == "/online":
                    nicks = ", ".join(n for _, n in clients)
                    sock.sendall(crypto.encrypt(f"Online: {nicks}"))
                continue

            broadcast(text, sender=nick, skip=sock)

    finally:
        if nick:
            clients[:] = [c for c in clients if c[1] != nick]
            broadcast(f"← {nick} left", system=True)
        sock.close()
