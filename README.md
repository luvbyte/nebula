---

🌌 Nebula

A modern, self-hosted automation platform built with FastAPI, Vue, TailwindCSS, and DaisyUI.

Nebula provides a unified interface for creating, managing, and executing bots — from lightweight shell-based bots to fully programmable asynchronous modules.


![Screenshot](docs/images/ss.jpg)

---

✨ Features

Feature	Description

🧠 Bot Framework	Supports two bot types: SBot (Simple Bot) and MBot (Module Bot)
🚀 Fast Backend	Built on FastAPI with async execution for scalable automation
🎨 Beautiful UI	Frontend powered by Vue + TailwindCSS + DaisyUI
📦 Self-Hosted	Fully local control — no external cloud dependency
🔧 Extensible	Create your own modules, scripts, or execution flows

---

🤖 Bot Types

🟦 SBot — Simple Bot

Lightweight bots designed for quick execution of simple shell commands.
Best for:

System tasks

Quick scripts

One-liner automations

---

🟪 MBot — Module Bot

Programmable bots with full async Python support.
Best for:

Complex automation logic

API automation or integrations

State machines and workflows

Data collection or AI-assisted tasks


MBots can define lifecycle hooks and run as persistent modules.

---

🔧 Installation

Requirements

Python 3.10+

Node.js 18+

Git


Backend Setup

git clone https://github.com/luvbyte/nebula
cd nebula/nebula

make

Frontend Setup

cd nebula/nebula-web
pnpm install
pnpm dev

visit

http://localhost:5173

---

📈 Roadmap

[ ] Bot marketplace system

---

🤝 Contributions

Pull requests and ideas are welcome! Help shape Nebula’s automation ecosystem.

---

📜 License

MIT License — Free to use, modify, and self-host.

---
