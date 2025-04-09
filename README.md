# 🔗 Blockchain App with Proof of Work

This is a simple blockchain implementation built with Django and Python. It simulates how a blockchain works by allowing users to create, mine, and view blocks — including a Proof of Work mechanism.

---

## 🧠 Why I Built This

I created this project to **understand and demonstrate the core principles of blockchain technology**, such as:

- ✅ Block creation
- 🔐 Hashing and cryptographic linking of blocks
- ⛏️ Proof of Work algorithm
- ⛓️ How data immutability is achieved in a blockchain

It also helped me practice my Django and Python skills by building a web-based UI to interact with the blockchain.

---

## 💻 Technologies Used

- Python 🐍
- Django 🌐
- HTML/CSS + Bootstrap
- SHA-256 hashing (via `hashlib`)

---

## ⚙️ Key Features

- 📦 **Create new blocks** with custom data  
- ⛏️ **Mine blocks** using Proof of Work (configurable difficulty)
- 🔗 Each block includes:
  - ID
  - Timestamp
  - Data
  - Hash
  - Previous Hash
- 📈 Live Bitcoin price display (optional)
- 🔍 Detailed view of each block

---

## 🔧 How to Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/00riddle00/PTUA15/tree/main/Greta_J
   cd blockchain-django

2. Set up virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # on Windows use venv\Scripts\activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Run the development server:
    ```bash
    python manage.py runserver
   
5. Open your browser:
    ```bash
    http://127.0.0.1:8000/
