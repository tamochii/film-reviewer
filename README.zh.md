<p align="right">
  <a href="./README.md">English</a> | 简体中文
</p>

<h1 align="center">Film Reviewer</h1>

<p align="center">
  《人工智能模型与算法》课程作业项目，围绕电影评论场景完成六类提示词工程实验。
</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-blue.svg">
  <img alt="Env" src="https://img.shields.io/badge/Config-.env-222222.svg">
  <img alt="Data" src="https://img.shields.io/badge/Data-TMDB-01B4E4.svg">
  <img alt="LLM" src="https://img.shields.io/badge/LLM-DeepSeek-7A3FFF.svg">
</p>

## 项目概览

本仓库实现了“智能影评专家”作业，并新增 FastAPI + React 实验工作台，可在浏览器中运行围绕同一部电影的 6 个提示词工程任务：

1. Zero-shot 与 Few-shot 情感分类对比
2. 强制 JSON 输出与解析
3. Chain-of-Thought（CoT）分析对比
4. 使用 system prompt 的角色扮演终端对话
5. 调用另一个 LLM 进行提示词打分
6. 针对提示词变体的 Grid Search 比较

项目使用：
- DeepSeek API：负责大模型推理
- TMDB API：负责电影元信息和剧情简介获取
- 本地固定影评样本：保证实验可复现

## 项目结构

- `backend/app/`：FastAPI 应用、任务服务、API 路由、客户端、配置与 SQLite 历史记录
- `frontend/`：React/Vite/TypeScript 的 Editor Workbench 前端界面
- `main.py`：原有任务 1 到任务 6 的交互式入口
- `prompts.py`：集中管理全部提示词
- `task1_classification.py` 到 `task6_grid_search.py`：六个任务的独立脚本
- `client.py`：DeepSeek 聊天接口封装
- `tmdb.py`：TMDB 查询工具
- `config.py`：环境变量读取与校验
- `report.md`：实验报告
- `data/`：电影信息、影评样本、扩展剧情简介与本地 `runs.sqlite3` 运行历史
- `tests/`：原有单元测试
- `backend/tests/`：后端服务、持久化与 API 测试

## 环境准备

1. 创建虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 复制环境变量模板

```bash
cp .env.example .env
```

4. 在 `.env` 中填写 API 配置

```env
DEEPSEEK_API_KEY=your_deepseek_key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
TMDB_API_KEY=your_tmdb_key
TMDB_BASE_URL=https://api.themoviedb.org/3
```

## 运行方式

启动 FastAPI 后端：

```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

另开终端启动 React 工作台：

```bash
cd frontend
npm install
npm run dev
```

打开 `http://localhost:5173`，即可在 Web UI 中运行 6 个任务。运行历史会保存到 `data/runs.sqlite3`。

仍然可以运行原有交互式菜单：

```bash
python main.py
```

启动后可以选择 1 到 6 中的任意任务。

也可以分别运行单个任务脚本：

```bash
python task1_classification.py
python task2_json_extract.py
python task3_cot_compare.py
python task4_roleplay_chat.py
python task5_prompt_evaluator.py
python task6_grid_search.py
```

## 测试

执行单元测试：

```bash
pytest -q
```

构建前端：

```bash
cd frontend
npm run build
```

## 补充说明

- Task 1 使用 5 条固定影评样本，便于稳定对比 Zero-shot 与 Few-shot 的分类准确率。
- Task 2 在解析失败时返回错误信息和原始输出，避免程序崩溃。
- Task 3 通过相同剧情简介对比普通提示和逐步思考提示的分析深度差异。
- Task 4 将“刻薄但专业的电影评论家”写入 `system` 角色消息中，增强多轮对话的一致性。
- Task 5 从 clarity、completeness、format 三个维度对提示词进行评估。
- Task 6 同时比较输出长度、信息密度和内容覆盖度，而不是只看字数。
