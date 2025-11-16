from flask import Flask, request
import subprocess
import json
import os

app = Flask(__name__)

# 設定JSONをロード
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "bot_update_config.json")

with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

@app.post("/github-webhook")
def webhook():
    event = request.headers.get("X-GitHub-Event")
    payload = request.json

    if event != "push":
        return "ignored", 200

    repo = payload.get("repository", {}).get("full_name")
    print(f"GitHub push received: {repo}")

    # 設定 JSON を元に更新対象を探す
    for bot in CONFIG["bots"]:
        if bot["repo"] == repo:
            print(f"Updating {bot['name']} ...")
            subprocess.Popen([bot["update_script"]])
            return f"{bot['name']} update started", 200

    return "ignored (repo not match)", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
