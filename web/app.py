import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from agent.core.agent_loop import run_agent
from agent.core.context import ContextManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'agentx-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global context (per session)
context = ContextManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global context
    data = request.json
    user_input = data.get('message', '').strip()

    if not user_input:
        return jsonify({'error': 'Empty message'}), 400

    if user_input.lower() == 'clear':
        context = ContextManager()
        return jsonify({'response': '🗑️ Chat history clear ho gayi!'})

    try:
        response = run_agent(user_input, context)

# Image response check karo
if "static/generated/" in response:
    import re
    img_match = re.search(r'static/generated/\S+\.png', response)
    if img_match:
        img_path = img_match.group()
        return jsonify({
            "response": response,
            "image": "/" + img_path
        })

return jsonify({"response": response})
            except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    global context
    context = ContextManager()
    return jsonify({'status': 'reset done'})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)