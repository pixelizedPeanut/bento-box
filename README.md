# 🍱 bento-box

A sandbox application built with **FastAPI** and **Vue.js**. 

Portioned into distinct compartments—just like a bento box.

---

## 🥢 Box Contents

The project is split into two directories:

*   📁 **`rice/`** — FastAPI Asynchronous Backend
*   📁 **`sushi/`** — Vue.js Frontend

---

## 🚀 Getting Started

Follow these steps to run each application locally.

### 1. Backend (`rice`)
Open a terminal tab and run:

```bash
cd rice
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
