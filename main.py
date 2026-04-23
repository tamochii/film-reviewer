from __future__ import annotations

import importlib


TASKS = {
    "1": ("Zero-shot vs Few-shot", "task1_classification"),
    "2": ("JSON extraction", "task2_json_extract"),
    "3": ("CoT comparison", "task3_cot_compare"),
    "4": ("Roleplay chat", "task4_roleplay_chat"),
    "5": ("Prompt evaluator", "task5_prompt_evaluator"),
    "6": ("Grid search", "task6_grid_search"),
}


def main() -> None:
    print("智能影评专家系统")
    for key, (name, _) in TASKS.items():
        print(f"{key}. {name}")

    choice = input("请选择任务编号：").strip()
    if choice not in TASKS:
        print("无效选择")
        return

    module = importlib.import_module(TASKS[choice][1])
    module.main()


if __name__ == "__main__":
    main()
