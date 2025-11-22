# services/ws_broadcast.py
import json

clients = set()

def register(ws):
    clients.add(ws)

def unregister(ws):
    if ws in clients:
        clients.remove(ws)

def broadcast(data):
    dead = []
    for ws in clients:
        try:
            ws.send(json.dumps(data))
        except:
            dead.append(ws)

    for d in dead:
        unregister(d)
