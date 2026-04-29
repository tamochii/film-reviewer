from __future__ import annotations

from backend.app.clients.deepseek import chat_completion
from prompts import ROLEPLAY_SYSTEM_PROMPT


def run(payload: dict) -> dict:
    history = list(payload.get("history") or [])
    message = payload.get("message", "")
    messages = [{"role": "system", "content": ROLEPLAY_SYSTEM_PROMPT}, *history, {"role": "user", "content": message}]
    reply = chat_completion(messages, temperature=0.7)
    new_history = [*history, {"role": "user", "content": message}, {"role": "assistant", "content": reply}]
    return {"reply": reply, "history": new_history}
