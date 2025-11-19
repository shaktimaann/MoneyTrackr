# Budget Guardian CrewAI 🤖💰

A multi-agent AI system for personal budget management that processes SMS transactions and provides intelligent financial advice using Google Gemini AI.

## 🚀 Features

- **SMS Transaction Processing**: Parse bulk SMS messages from banks/UPI apps
- **AI-Powered Categorization**: Automatically classify expenses (Food, Transport, Subscription, etc.)
- **Financial Forecasting**: Calculate burn rate, predict run-out dates, suggest safe spending limits
- **Personalized AI Advice**: Get natural language financial recommendations based on spending patterns
- **Category Analysis**: Track spending by category with detailed insights
- **Real-time Dashboard**: Interactive Streamlit interface

## 🏗️ Architecture

### Multi-Agent System
- **Agent A (Expense Classifier)**: Uses Gemini LLM to categorize transactions
- **Agent B (Financial Analyst)**: Performs numeric analysis and forecasting
- **Agent C (Financial Advisor)**: Generates personalized advice using AI

### Tech Stack
- **Frontend**: Streamlit
- **Database**: SQLite + SQLAlchemy
- **AI**: Google Gemini API (gemini-2.0-flash)
- **Data Processing**: Pandas, Regex
- **Environment**: Python 3.8+

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/budget-guardian-crewai.git
cd budget-guardian-crewai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///budget.db
```

4. **Run the application**
```bash
streamlit run app.py
```

## 🔑 Getting Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## 💡 Usage

### 1. Process SMS Transactions
Paste your bank/UPI SMS messages:
```
Dear UPI user A/C X8707 debited by 19.0 on date 25Oct25 trf to Google India Ser Refno 529850309750
Dear UPI user A/C X8707 debited by 35.0 on date 04Nov25 trf to AVENUE FOOD PLAZ Refno 567447771840
```

### 2. View Financial Forecast
- Daily burn rate calculation
- Predicted money run-out date
- Safe daily spending recommendations

### 3. Get AI Advice
Receive personalized financial advice based on:
- Spending patterns by category
- Financial health metrics
- Actionable recommendations

## 📁 Project Structure

```
budget-guardian-crewai/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── utils/
│   ├── parser.py         # SMS parsing and date extraction
│   ├── db.py            # Database operations
│   └── analysis.py      # Financial calculations
└── crewai/
    ├── agents.py        # AI agent framework
    └── budget_crew.py   # Agent task definitions
```

## 🤖 Agent Workflow

1. **SMS Input** → **Parser** extracts amount, vendor, date
2. **Agent A** → Classifies transaction category using AI
3. **Database** → Stores structured transaction data
4. **Agent B** → Analyzes spending patterns and forecasts
5. **Agent C** → Generates personalized financial advice

## 🔧 Configuration

### Supported Categories
- Food & Dining
- Transport
- Grocery
- Subscription
- Entertainment
- Utilities
- Travel
- Personal Transfer
- Miscellaneous

### SMS Format Support
- UPI transaction messages
- Bank debit/credit notifications
- Multiple SMS processing in bulk
- Date formats: DDMmmYY (e.g., 25Oct25)

## 🛡️ Privacy & Security

- All data stored locally in SQLite database
- No transaction data sent to external services (except Gemini for categorization)
- API keys stored in environment variables
- No sensitive financial information logged

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for natural language processing
- Streamlit for the amazing web framework
- CrewAI concept for multi-agent architecture

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ for better financial management**