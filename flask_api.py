from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sock import Sock
import json

from utils.redis_client import get_redis
from services.ws_broadcast import register, unregister, broadcast

app = Flask(__name__)
CORS(app)
sock = Sock(app)

r = get_redis()

# ========== API: 最新訊號 ==========
@app.route("/latest_signals", methods=["GET"])
def latest_signals():
    if r:
        data = r.get("latest_signal")
        if data:
            return jsonify(json.loads(data))
    return jsonify({"msg": "no data"})


# ========== API: Radar 清單 ==========
@app.route("/radar", methods=["GET"])
def radar():
    if r:
        d = r.get("radar_list")
        if d:
            return jsonify(json.loads(d))
    return jsonify([])


# ========== API: 個股資訊 ==========
@app.route("/stock/<sid>", methods=["GET"])
def stock(sid):
    if r:
        d = r.get(f"stock_{sid}")
        if d:
            return jsonify(json.loads(d))
    return jsonify({"msg": "no data"})


# ========== WebSocket（手機 App 即時訊號） ==========
@sock.route('/ws')
def ws(ws):
    register(ws)
    try:
        while True:
            msg = ws.receive()
            if not msg:
                break
    except:
        pass
    unregister(ws)


# ========== 從 notify.py 轉過來推 WebSocket ==========
@app.route("/broadcast", methods=["POST"])
def ws_broadcast_api():
    data = request.json
    broadcast(data)
    return jsonify({"status": "ok"})
