from .agents import LLMAgent, NumericAgent, Crew
from utils import parser, db, analysis
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def _classification_task(payload: str) -> str:
    """Agent A — Expense Classifier (uses Gemini LLM)
    """
    categories = ["Food", "Transport", "Grocery", "Subscription", "Entertainment", "Utilities", "Travel", "Misc"]
    prompt = f"Classify the following transaction into one of these categories: {', '.join(categories)}.\nTransaction: {payload}\nReturn only the category name."
    llm = LLMAgent(model=os.getenv('GEMINI_MODEL', 'gemini'))
    resp = llm.generate(prompt, max_tokens=32)
    # Heuristic: pick first matching category if present
    for c in categories:
        if c.lower() in resp.lower():
            return c
    # If LLM returned something else, sanitize
    candidate = resp.strip().split('\n')[0]
    candidate = candidate.split('.')[0].strip()
    if candidate in categories:
        return candidate
    return 'Misc'


def _analysis_task(payload: dict) -> dict:
    """Agent B — Financial Analyst (no LLM)
    """
    if isinstance(payload, dict):
        balance = float(payload.get('balance', 0.0))
    else:
        balance = float(payload or 0.0)

    df = db.load_df()
    result = analysis.calculate_forecast(df, balance)
    return result


def _advice_task(payload: dict) -> str:
    """Agent C — Financial Advisor
    """
    from utils import db
    
    # Get category spending data
    df = db.load_df()
    category_spending = {}
    if not df.empty:
        category_spending = df.groupby('category')['amount'].sum().to_dict()
    
    llm = LLMAgent(model=os.getenv('GEMINI_MODEL', 'gemini'))
    
    # Build context with category spending
    category_text = ""
    if category_spending:
        category_text = "\nCategory-wise spending (in INR):\n"
        for cat, amount in sorted(category_spending.items(), key=lambda x: x[1], reverse=True):
            category_text += f"- {cat}: ₹{amount:.2f}\n"
    
    prompt = (
        "You are a friendly personal financial advisor for an Indian user. All amounts are in Indian Rupees (INR). "
        "Provide natural, conversational advice (4-6 sentences) based on their spending analysis. "
        "Focus on category-wise spending patterns and give specific actionable tips. "
        "If they're spending too much in any category, mention it specifically. "
        "Be encouraging but realistic about their financial habits.\n\n"
    )
    
    analysis_text = '\n'.join(f"{k}: {v}" for k, v in (payload or {}).items())
    full_prompt = prompt + "Financial Analysis:\n" + analysis_text + category_text
    
    resp = llm.generate(full_prompt, max_tokens=300)
    return resp.strip()


def get_budget_crew() -> Crew:
    crew = Crew()
    crew.register_task('transaction_classification', _classification_task)
    crew.register_task('transaction_analysis', _analysis_task)
    crew.register_task('transaction_advice', _advice_task)
    return crew
