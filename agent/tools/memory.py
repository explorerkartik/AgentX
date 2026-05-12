import json
import os

MEMORY_FILE = "agent_memory.json"

def load_memory() -> dict:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"facts": [], "preferences": []}

def save_memory(data: dict):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def remember(fact: str) -> str:
    memory = load_memory()
    memory["facts"].append(fact)
    save_memory(memory)
    return f"✅ Yaad kar liya: {fact}"

def recall(query: str = "") -> str:
    memory = load_memory()
    facts = memory.get("facts", [])
    if not facts:
        return "🧠 Abhi kuch yaad nahi hai."
    
    if query:
        relevant = [f for f in facts if query.lower() in f.lower()]
        if relevant:
            return "🧠 Related memories:\n" + "\n".join(f"- {f}" for f in relevant)
        return f"🧠 '{query}' ke baare mein kuch yaad nahi."
    
    return "🧠 Mujhe ye sab yaad hai:\n" + "\n".join(f"- {f}" for f in facts)

def forget(fact: str) -> str:
    memory = load_memory()
    before = len(memory["facts"])
    memory["facts"] = [f for f in memory["facts"] if fact.lower() not in f.lower()]
    save_memory(memory)
    removed = before - len(memory["facts"])
    return f"🗑️ {removed} memory remove ki."


REMEMBER_TOOL = {
    "type": "function",
    "function": {
        "name": "remember",
        "description": "Save important information to memory for future reference. Use when user says 'remember that', 'note this', or shares personal info like name, preferences.",
        "parameters": {
            "type": "object",
            "properties": {
                "fact": {"type": "string", "description": "The fact or information to remember"}
            },
            "required": ["fact"]
        }
    }
}

RECALL_TOOL = {
    "type": "function",
    "function": {
        "name": "recall",
        "description": "Retrieve stored memories. Use when user asks 'do you remember', 'what do you know about me', or needs past context.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "What to search in memory (optional)", "default": ""}
            }
        }
    }
}

FORGET_TOOL = {
    "type": "function",
    "function": {
        "name": "forget",
        "description": "Remove something from memory.",
        "parameters": {
            "type": "object",
            "properties": {
                "fact": {"type": "string", "description": "The fact to forget/remove"}
            },
            "required": ["fact"]
        }
    }
}