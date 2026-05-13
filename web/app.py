import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import re
from flask import Flask, render_template, request, jsonify
from agent.core.agent_loop import run_agent
from agent.core.context import ContextManager

app = Flask(__name__)
context = ContextManager()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global context
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"response": "Kuch bolo!"})

    try:
        response = run_agent(user_input, context)

        # Image response check karo
        img_match = re.search(r'static/generated/\S+\.png', response)
        if img_match:
            img_path = img_match.group()
            return jsonify({
                "response": response,
                "image": "/" + img_path
            })

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"response": f"❌ Error: {str(e)}"})

@app.route("/reset", methods=["POST"])
def reset():
    global context
    context = ContextManager()
    return jsonify({"status": "reset done"})

@app.route("/clear", methods=["POST"])
def clear():
    global context
    context = ContextManager()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)