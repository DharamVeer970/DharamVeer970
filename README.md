<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1f6feb,50:8957e5,100:238636&height=180&section=header&text=Dharam%20Veer&fontColor=ffffff&fontSize=52&fontAlignY=34&desc=Agentic%20AI%20Engineer%20%C2%B7%20Multi-Agent%20Systems%20%C2%B7%20AI%20Automation&descAlignY=54&descSize=16&animation=fadeIn" width="100%" alt="Dharam Veer — Agentic AI Engineer" />

<a href="https://github.com/DharamVeer970">
<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=22&pause=1200&color=8957E5&center=true&vCenter=true&width=780&height=45&lines=I+build+agents+that+act%2C+not+chatbots+that+talk.;Multi-agent+orchestration+with+LangGraph+%2B+FastAPI;64-tool+voice+agent+running+on+bare+Windows+APIs;MCP+servers%2C+tool-calling+runtimes%2C+agent+memory" alt="What I build" />
</a>

<br/>

<a href="https://www.linkedin.com/in/dharam-veer-657711226/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="mailto:dharamveeer4@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email" /></a>
<img src="https://komarev.com/ghpvc/?username=DharamVeer970&style=flat-square&color=8957e5&label=profile+views" alt="Profile views" />
<a href="https://github.com/DharamVeer970?tab=followers"><img src="https://img.shields.io/github/followers/DharamVeer970?style=flat-square&color=1f6feb&labelColor=161b22&logo=github" alt="Followers" /></a>

</div>

---

## `>` Whoami

```text
$ agent.invoke("who is dharam veer?")

  planner      → decompose(query) ................... 4 subtasks
  retriever    → scan(github, projects, shipped) .... 20 repos
  synthesizer  → build_profile() .................... ok

╭──────────────────────────────────────────────────────────────╮
│  name       Dharam Veer                                      │
│  role       Agentic AI Engineer · AI Automation Builder      │
│  builds     multi-agent systems, tool-calling runtimes,      │
│             memory-backed workflows, MCP integrations        │
│  stack      Python · LangGraph · FastAPI · MCP · OpenAI      │
│  shipping   Wilco — voice agent for Windows, 64 tools        │
│  belief     an agent is only as good as its tool layer       │
╰──────────────────────────────────────────────────────────────╯

✔ 3 steps · 0 hallucinations · returning control to user
```

---

## `>` Featured work

### 🎙️ Wilco — Voice-Controlled Agent for Windows

> Speak to your machine, it acts. Whisper transcribes, an agent loop reasons, **64 tools** touch the real OS.

Not a wrapper around a chat API — a full agent runtime with two execution paths, a safety gate, and real system access.

| | |
|---|---|
| **Dual execution** | Instant regex path for common commands, full tool-calling agent loop for everything else — so trivial requests never pay LLM latency |
| **64 tools** | App control, file ops, PowerShell, web search, email, messaging, window management |
| **Provider-agnostic** | Cohere, OpenAI, Anthropic, Groq, HuggingFace, Ollama — swapped by config, not code |
| **MCP server** | Exposes its own toolset over Model Context Protocol to Claude Desktop and other clients |
| **Safety gates** | Confirmation required before destructive actions — delete, shutdown, send |
| **Context aware** | Tracks recent searches, active apps, and working directories across turns |

<a href="https://github.com/DharamVeer970/Wilco"><img src="https://img.shields.io/badge/View_Repo-Wilco-1f6feb?style=for-the-badge&logo=github&logoColor=white" alt="View Wilco" /></a>
<img src="https://img.shields.io/badge/Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/MCP-000000?style=for-the-badge&logo=modelcontextprotocol&logoColor=white" alt="MCP" />

<br/>

### Also building

| Project | What it does | Stack |
|---|---|---|
| **Trading Agent** `private` | Autonomous market-analysis agent — signal ingestion, LLM reasoning over indicators, decision logging | Python · LLM tool calling |
| [**Cancer Treatment ML**](https://github.com/DharamVeer970/Cancer_treatment_Project) | Classification pipeline for treatment outcome prediction — preprocessing, training, evaluation | scikit-learn · Jupyter |
| [**Stock Management System**](https://github.com/DharamVeer970/Stock_management_system) | Inventory tracking with full CRUD and persistent storage | Python · SQL |
| [**ChatGPT Clone**](https://github.com/DharamVeer970/Chatgpt-Clone) | Conversational UI with streaming responses and chat persistence | JS · OpenAI API |
| [**House Price Prediction**](https://github.com/DharamVeer970/House_Price_Prediction) | Regression modelling with feature engineering and error analysis | pandas · scikit-learn |
| [**Wine Quality Prediction**](https://github.com/DharamVeer970/Wine_Quality_Prediction) | Multi-class classification on physicochemical features | pandas · scikit-learn |

---

## `>` How I architect agents

Every system I build follows the same spine: **plan → route → act → remember → critique → repeat.**
The critic loop is the part most "AI apps" skip — and it's the reason they break in production.

<div align="center">

<img src="assets/agent-architecture.svg" width="100%" alt="Agent architecture: input passes guardrails into either a deterministic fast path or a planner; the planner routes to research, code and system agents that share a tool layer backed by memory; a critic either replans or releases the final response." />

</div>

---

## `>` Tech arsenal

<details open>
<summary><b>🤖 Agentic AI &amp; LLM</b></summary>
<br/>

![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square&logo=langgraph&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![MCP](https://img.shields.io/badge/Model_Context_Protocol-000000?style=flat-square&logo=modelcontextprotocol&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-D97757?style=flat-square&logo=anthropic&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=flat-square&logo=groq&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging_Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![Whisper](https://img.shields.io/badge/Whisper_STT-412991?style=flat-square&logo=openai&logoColor=white)

`tool calling` · `function schemas` · `RAG` · `agent memory` · `multi-agent routing` · `reflection loops` · `prompt engineering`

</details>

<details>
<summary><b>⚙️ Backend &amp; APIs</b></summary>
<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white)
![REST](https://img.shields.io/badge/REST_APIs-005571?style=flat-square&logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)

</details>

<details>
<summary><b>📊 Data &amp; Machine Learning</b></summary>
<br/>

![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat-square&logo=python&logoColor=white)

</details>

<details>
<summary><b>🎨 Frontend</b></summary>
<br/>

![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)

</details>

<details>
<summary><b>🗄️ Data Stores &amp; Tooling</b></summary>
<br/>

![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=flat-square&logo=postman&logoColor=white)
![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=flat-square&logo=visualstudiocode&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)

</details>

---

## `>` By the numbers

<div align="center">

<!-- Flagship repo: DharamVeer970/Wilco. Its name is baked into the badge URLs
     below and into the language row further down. Renaming the repo means
     updating every one of those URLs together. -->

<img src="https://img.shields.io/github/followers/DharamVeer970?style=for-the-badge&logo=github&logoColor=white&label=Followers&labelColor=161b22&color=1f6feb" alt="GitHub followers" />
<img src="https://img.shields.io/github/stars/DharamVeer970/Wilco?style=for-the-badge&logo=github&logoColor=white&label=Wilco%20stars&labelColor=161b22&color=8957e5" alt="Stars on Wilco" />
<img src="https://img.shields.io/github/last-commit/DharamVeer970/Wilco?style=for-the-badge&logo=git&logoColor=white&label=Last%20commit&labelColor=161b22&color=238636" alt="Last commit to Wilco" />

<br/><br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com?user=DharamVeer970&hide_border=true&background=0d1117&stroke=30363d&ring=8957e5&fire=1f6feb&currStreakLabel=8957e5&sideLabels=c9d1d9&dates=8b949e&currStreakNum=c9d1d9&sideNums=c9d1d9" />
  <img src="https://streak-stats.demolab.com?user=DharamVeer970&hide_border=true&ring=8957e5&fire=1f6feb&currStreakLabel=8957e5" height="165" alt="Contribution streak" />
</picture>

<br/><br/>

<sub><b>PRIMARY LANGUAGE PER PROJECT</b> — read live from the GitHub API</sub>

<br/>

<a href="https://github.com/DharamVeer970/Wilco"><img src="https://img.shields.io/github/languages/top/DharamVeer970/Wilco?style=flat-square&label=Wilco&labelColor=161b22&color=8957e5" alt="Top language in Wilco" /></a>
<a href="https://github.com/DharamVeer970/Cancer_treatment_Project"><img src="https://img.shields.io/github/languages/top/DharamVeer970/Cancer_treatment_Project?style=flat-square&label=Cancer%20ML&labelColor=161b22&color=8957e5" alt="Top language in Cancer Treatment ML" /></a>
<a href="https://github.com/DharamVeer970/Stock_management_system"><img src="https://img.shields.io/github/languages/top/DharamVeer970/Stock_management_system?style=flat-square&label=Stock%20System&labelColor=161b22&color=8957e5" alt="Top language in Stock Management System" /></a>
<a href="https://github.com/DharamVeer970/Chatgpt-Clone"><img src="https://img.shields.io/github/languages/top/DharamVeer970/Chatgpt-Clone?style=flat-square&label=ChatGPT%20Clone&labelColor=161b22&color=8957e5" alt="Top language in ChatGPT Clone" /></a>
<a href="https://github.com/DharamVeer970/House_Price_Prediction"><img src="https://img.shields.io/github/languages/top/DharamVeer970/House_Price_Prediction?style=flat-square&label=House%20Prices&labelColor=161b22&color=8957e5" alt="Top language in House Price Prediction" /></a>
<a href="https://github.com/DharamVeer970/Wine_Quality_Prediction"><img src="https://img.shields.io/github/languages/top/DharamVeer970/Wine_Quality_Prediction?style=flat-square&label=Wine%20Quality&labelColor=161b22&color=8957e5" alt="Top language in Wine Quality Prediction" /></a>

<br/><br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=DharamVeer970&theme=github-compact&bg_color=0d1117&color=c9d1d9&line=8957e5&point=1f6feb&area=true&hide_border=true" />
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=DharamVeer970&theme=github-light&line=8957e5&point=1f6feb&area=true&hide_border=true" width="100%" alt="Contribution activity graph" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=DharamVeer970&theme=github_dark" />
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=DharamVeer970&theme=github" alt="GitHub stats" width="100%" />
</picture>

</div>

---

## `>` Live agent log

> This block isn't hand-written. A scheduled agent ([`scripts/profile_agent.py`](scripts/profile_agent.py))
> wakes up daily, queries the GitHub API, and rewrites everything between the markers below —
> then commits only if something actually changed. My README maintains itself.

<!-- AGENT-LOG:START -->

### 🔦 Currently in the workshop — [`Wilco`](https://github.com/DharamVeer970/Wilco)

> Voice agent for Windows: Whisper STT, an instant regex command path, and a 39-tool agent loop that controls apps, files, settings and PowerShell.

`Python` · updated 7h ago

### 📡 Recent signals

| when | what |
|:--|:--|
| `2w ago` | branched `main` on [`Wilco`](https://github.com/DharamVeer970/Wilco) |

### 🧬 What I actually write

<sub>share of public projects by primary language</sub>

```text
Jupyter Notebook  ███████████░░░░░░░░░░░░░░░░░░░░░░░   33.3%  5 projects
HTML              █████████░░░░░░░░░░░░░░░░░░░░░░░░░   26.7%  4 projects
Python            █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   13.3%  2 projects
Java              █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   13.3%  2 projects
JavaScript        ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    6.7%  1 project
CSS               ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    6.7%  1 project
```

<div align="right">

<sub>🤖 generated by <code>profile_agent.py</code> · 20 public repos · last run 21 Aug 2026 · 03:16 UTC</sub>

</div>

<!-- AGENT-LOG:END -->

---

## `>` What's next

```yaml
now:
  - Wilco v2 — parallel tool execution + streaming voice responses
  - Multi-agent orchestrator with shared episodic memory
  - Publishing reusable MCP servers for local system control

learning:
  - Agent evaluation: how do you unit-test something non-deterministic?
  - Long-horizon memory — compaction, retrieval, forgetting
  - Cost-aware routing: cheapest model that still gets it right

open_to:
  - Agentic AI / LLM engineering roles
  - Collaborations on open-source agent tooling
```

---

## `>` Contribution graph, eaten

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/DharamVeer970/DharamVeer970/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/DharamVeer970/DharamVeer970/output/github-snake.svg" />
  <img src="https://raw.githubusercontent.com/DharamVeer970/DharamVeer970/output/github-snake.svg" alt="Contribution snake animation" />
</picture>

</div>

---

<div align="center">

## `>` Let's build something autonomous

<a href="mailto:dharamveeer4@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
<a href="https://www.linkedin.com/in/dharam-veer-657711226/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="https://github.com/DharamVeer970"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>

<br/><br/>

**⭐ Anything here useful? A star helps more than you'd think.**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:238636,50:8957e5,100:1f6feb&height=120&section=footer" width="100%" alt="" />

</div>
