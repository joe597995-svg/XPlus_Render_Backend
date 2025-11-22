from flask import Flask, request, jsonify
import json

from utils.redis_client import get_redis
from services.fcm_sender import send_push
import requests

app = Flask(__name__)
r = get_redis()


# ========== 你 Windows 送訊號到這裡 ==========
@app.route("/signal", methods=["POST"])
def receive_signal():
    data = request.json

    # 存到 Redis
    if r:
        r.set("latest_signal", json.dumps(data))

    # 轉推播
    send_push(
        topic="all",
        title=f"{data['stock_id']} - {data['signal']}",
        body=f"價 {data['price']} | 量比 {data.get('vol_ratio','-')}"
    )

    # 廣播 WebSocket（讓手機 App 實時跳畫面）
    try:
        requests.post(
            "http://localhost:5000/broadcast",
            json=data
        )
    except:
        pass

    return jsonify({"status": "ok"})
