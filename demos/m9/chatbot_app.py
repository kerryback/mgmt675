"""
Step 4 Demo: FastAPI chatbot that uses OpenRouter.

Usage:
    Set your OpenRouter API key as an environment variable:
        export OPENROUTER_API_KEY=sk-or-...

    Then run:
        uvicorn chatbot_app:app --reload

    Open http://localhost:8000 in your browser.
"""

import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODEL = "nvidia/nemotron-3-super-120b-a12b:free"
SYSTEM_PROMPT = "Talk like a pirate. Every response must be in pirate dialect."


class ChatRequest(BaseModel):
    messages: list[dict]


@app.post("/chat")
def chat(req: ChatRequest):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + req.messages
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return {"reply": response.choices[0].message.content}


@app.get("/", response_class=HTMLResponse)
def index():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Chat</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, sans-serif; background: #f0f2f5; display: flex;
         justify-content: center; padding: 2rem; }
  .chat-container { width: 100%; max-width: 700px; }
  h1 { text-align: center; margin-bottom: 1rem; color: #1e293b; }
  #messages { background: #fff; border-radius: 12px; padding: 1.5rem; height: 60vh;
              overflow-y: auto; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
  .msg { margin-bottom: 1rem; line-height: 1.5; }
  .msg.user { text-align: right; }
  .msg span { display: inline-block; padding: 0.6rem 1rem; border-radius: 16px;
              max-width: 80%; text-align: left; white-space: pre-wrap; }
  .msg.user span { background: #2563eb; color: #fff; }
  .msg.assistant span { background: #e2e8f0; color: #1e293b; }
  .input-row { display: flex; gap: 0.5rem; margin-top: 0.75rem; }
  #input { flex: 1; padding: 0.75rem 1rem; border-radius: 24px; border: 1px solid #cbd5e1;
           font-size: 1rem; outline: none; }
  #input:focus { border-color: #2563eb; }
  button { padding: 0.75rem 1.5rem; border-radius: 24px; border: none;
           background: #2563eb; color: #fff; font-size: 1rem; cursor: pointer; }
  button:disabled { opacity: 0.5; cursor: default; }
</style>
</head>
<body>
<div class="chat-container">
  <h1>Kerry Back's Chatbot</h1>
  <p style="text-align:center; color:#64748b; margin-top:-0.5rem; margin-bottom:1rem; font-size:0.95rem;">Powered by Nemotron 3</p>
  <div id="messages"></div>
  <div class="input-row">
    <input id="input" placeholder="Type a message..." autocomplete="off" />
    <button id="send" onclick="send()">Send</button>
  </div>
</div>
<script>
const messagesDiv = document.getElementById("messages");
const input = document.getElementById("input");
const btn = document.getElementById("send");
let history = [];

input.addEventListener("keydown", e => { if (e.key === "Enter" && !btn.disabled) send(); });

function addMsg(role, text) {
  const div = document.createElement("div");
  div.className = "msg " + role;
  div.innerHTML = "<span>" + text.replace(/</g, "&lt;") + "</span>";
  messagesDiv.appendChild(div);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function send() {
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  addMsg("user", text);
  history.push({role: "user", content: text});
  btn.disabled = true;
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({messages: history})
    });
    const data = await res.json();
    history.push({role: "assistant", content: data.reply});
    addMsg("assistant", data.reply);
  } catch (e) {
    addMsg("assistant", "Error: " + e.message);
  }
  btn.disabled = false;
  input.focus();
}
</script>
</body>
</html>"""
