# MoneyTrackr — AI-Powered Finance Assistant for Students

**MoneyTrackr** is an intelligent personal finance assistant built using **CrewAI**, **Google Gemini**, **Streamlit**, and **SQLite**.  
It automatically extracts expenses from text/SMS, categorizes them using AI agents, forecasts future spending, and gives clear financial advice tailored for students.

MoneyTrackr removes the manual effort from budgeting and gives you a real-time understanding of where your money is going.

---

## 🚀 Features

### 🧠 AI-Powered Transaction Classification
Paste SMS or expense text → MoneyTrackr uses a dedicated **Expense Classifier Agent** (CrewAI + Gemini) to detect:
- Amount  
- Category  
- Vendor  
- Notes  

### 📊 Smart Financial Forecasting
The **Analysis Agent** calculates:
- Daily burn rate  
- Predicted run-out date  
- Safe daily spending limit  
- Category-wise patterns  

### 💬 AI-Generated Financial Advice
The **Advisor Agent** (Gemini) generates:
- Spending insights  
- Overspending warnings  
- Actionable weekly recommendations  

### 📈 Clean Streamlit Dashboard
- View all transactions  
- Category summaries  
- Forecast insights  
- Advice panel  

### 🗄️ Local Storage (SQLite)
Your data stays local — fast, secure, and portable.

---

## 🏗️ Architecture Overview

MoneyTrackr uses a **3-agent multi-agent system**:

| Agent | Role | Power |
|-------|------|--------|
| **Expense Classifier Agent** | Categorizes transactions | Gemini LLM |
| **Financial Analysis Agent** | Computes metrics & forecasts | Python logic |
| **Financial Advisor Agent** | Produces guidance & summaries | Gemini LLM |

Orchestrated using **CrewAI**, enabling step-by-step task delegation.

---

## 🛠️ Tech Stack
- Python 3.10+
- Streamlit  
- CrewAI  
- Google Gemini API  
- SQLite  
- Pandas / NumPy  

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/MoneyTrackr.git
cd MoneyTrackr
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set your Gemini API key
Create a `.env` file:

```
GEMINI_API_KEY=YOUR_KEY_HERE
```

---

## ▶️ Run the Application

```bash
python -m streamlit run app.py
```

---

## 📚 Project Structure

```
budget_guardian/
│── app.py
│── requirements.txt
│── .env.example
│── crew/
│   │── __init__.py
│   │── agents.py
│   │── tasks.py
│   │── crew_config.py
│── utils/
│   │── __init__.py
│   │── db.py
│   │── parser.py
│   │── analysis.py
```

---

## 🎯 How It Works

1. User pastes an expense/SMS  
2. Agent 1 classifies transaction  
3. Entry stored in SQLite  
4. Dashboard updates  
5. Advice generated via Agent 2 + Agent 3  

---

## 🧩 Future Enhancements
- Spending heatmap  
- Subscription detection  
- PDF report export  
- Multi-user login  
- Alerts/notifications  

---

## 🤝 Contributions
Open PRs or issues to discuss improvements.

---

## 📜 License
MIT License

