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
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"response": "Kuch bolo!"})
    
    response = run_agent(user_input, context)
    return jsonify({"response": response})

@app.route("/clear", methods=["POST"])
def clear():
    global context
    context = ContextManager()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)