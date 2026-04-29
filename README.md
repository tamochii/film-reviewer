<p align="right">
  English | <a href="./README.zh.md">简体中文</a>
</p>

<h1 align="center">Film Reviewer</h1>

<p align="center">
  A course project for "Artificial Intelligence Models and Algorithms" focused on prompt engineering experiments for movie reviews.
</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-blue.svg">
  <img alt="Env" src="https://img.shields.io/badge/Config-.env-222222.svg">
  <img alt="Data" src="https://img.shields.io/badge/Data-TMDB-01B4E4.svg">
  <img alt="LLM" src="https://img.shields.io/badge/LLM-DeepSeek-7A3FFF.svg">
</p>

## Overview

This repository implements the "Intelligent Movie Review Expert" assignment. It covers six prompt-engineering tasks built around one movie:

1. Zero-shot vs Few-shot sentiment classification
2. Forced JSON output parsing
3. Chain-of-Thought comparison
4. Roleplay with system prompts in a terminal chat loop
5. Prompt evaluator with another LLM call
6. Grid Search across prompt variants

The project uses:
- DeepSeek API for LLM inference
- TMDB API for movie metadata and overview
- Local fixed review samples for reproducible experiments

## Project Structure

- `main.py`: interactive entrypoint for tasks 1-6
- `prompts.py`: all prompts used in the assignment
- `task1_classification.py` to `task6_grid_search.py`: individual task scripts
- `client.py`: DeepSeek chat completion wrapper
- `tmdb.py`: TMDB lookup utilities
- `config.py`: environment loading and validation
- `report.md`: experiment report required by the assignment
- `data/`: movie metadata, reviews, and extended plot summary
- `tests/`: unit tests for config, client, helpers, and TMDB integration logic

## Environment Setup

1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Copy the example environment file

```bash
cp .env.example .env
```

4. Fill in your API keys in `.env`

```env
DEEPSEEK_API_KEY=your_deepseek_key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
TMDB_API_KEY=your_tmdb_key
TMDB_BASE_URL=https://api.themoviedb.org/3
```

## Running the Project

Run the interactive menu:

```bash
python main.py
```

You can then choose one of the six tasks.

You may also run each script individually:

```bash
python task1_classification.py
python task2_json_extract.py
python task3_cot_compare.py
python task4_roleplay_chat.py
python task5_prompt_evaluator.py
python task6_grid_search.py
```

## Testing

Run unit tests with:

```bash
pytest -q
```

## Notes

- Task 1 uses five fixed review samples to keep accuracy comparisons reproducible.
- Task 2 uses `json.loads()` and handles parsing failures safely.
- Task 3 compares plain analysis against a step-by-step CoT prompt.
- Task 4 keeps the critic persona in the `system` message.
- Task 5 evaluates prompts on clarity, completeness, and format.
- Task 6 compares prompt variants by output length, information density, and coverage.
