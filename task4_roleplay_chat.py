from __future__ import annotations

from client import chat_completion
from prompts import ROLEPLAY_SYSTEM_PROMPT


def main() -> None:
    messages = [{"role": "system", "content": ROLEPLAY_SYSTEM_PROMPT}]
    print("输入 quit 退出。")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"quit", "exit"}:
            break

        messages.append({"role": "user", "content": user_input})
        reply = chat_completion(messages, temperature=0.7)
        messages.append({"role": "assistant", "content": reply})
        print(f"Critic: {reply}")


if __name__ == "__main__":
    main()
