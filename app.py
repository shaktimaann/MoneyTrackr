import streamlit as st
from utils import parser, db, analysis
from crewai.budget_crew import get_budget_crew
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Budget Guardian CrewAI", layout="wide")

st.title("Budget Guardian CrewAI")

crew = get_budget_crew()

col1, col2 = st.columns([2, 3])

with col1:
    st.header('Add Transaction (SMS)')
    sms = st.text_area('Paste SMS or transaction text here (supports multiple messages)', height=120)
    if st.button('Process'):
        if not sms.strip():
            st.warning('Please paste an SMS or transaction text.')
        else:
            transactions = parser.parse_bulk_sms(sms)
            if not transactions:
                st.warning('No valid transactions found in the text.')
            else:
                processed_count = 0
                for txn in transactions:
                    try:
                        classification_input = f"Vendor: {txn['vendor']} | SMS: {txn['text']}"
                        category = crew.run_task('transaction_classification', classification_input)
                        if category == 'Misc':
                            category = parser._categorize_by_vendor(txn['vendor'])
                    except Exception as e:
                        category = parser._categorize_by_vendor(txn['vendor'])
                    txn['category'] = category
                    db.insert_txn(txn)
                    processed_count += 1
                st.success(f"Processed {processed_count} transactions successfully!")
                for txn in transactions:
                    st.info(f"₹{txn['amount']} on {txn['date']} to {txn['vendor']}")

with col2:
    st.header('Recent Transactions')
    df = db.load_df()
    if df.empty:
        st.info('No transactions yet')
    else:
        st.dataframe(df.sort_values('date', ascending=False))
        if st.button('Clear All Transactions', type='secondary'):
            db.clear_all_transactions()
            st.success('All transactions cleared!')
            st.rerun()

st.header('Forecast')
balance = st.number_input('Current balance (₹)', min_value=0.0, value=1000.0, step=100.0)
if st.button('Compute Forecast'):
    df = db.load_df()
    result = analysis.calculate_forecast(df, float(balance))
    st.metric('Burn rate (daily avg, last 10 days)', f"₹{result['burn_rate']:.2f}")
    st.metric('Predicted run-out date', result['run_out_date'])
    st.metric('Safe daily spending (30-day horizon)', f"₹{result['safe_daily']:.2f}")

st.header('AI Advice')
if st.button('Get AI Advice'):
    df = db.load_df()
    analysis_result = crew.run_task('transaction_analysis', {'balance': float(balance)})
    analysis_result['transactions_count'] = int(len(df))
    
    try:
        advice = crew.run_task('transaction_advice', analysis_result)
    except Exception as e:
        st.error(f"Error details: {str(e)}")
        if 'GEMINI_API_KEY' in str(e):
            # Fallback advice based on analysis
            burn_rate = analysis_result.get('burn_rate', 0)
            safe_daily = analysis_result.get('safe_daily', 0)
            advice = f"""💡 Basic Financial Advice:
• Your daily burn rate is ₹{burn_rate:.2f}
• Safe daily spending limit: ₹{safe_daily:.2f}
• Track expenses regularly to stay within budget
• Consider reducing discretionary spending if burn rate is high
• Set up Gemini API key for personalized AI advice"""
        else:
            burn_rate = analysis_result.get('burn_rate', 0)
            safe_daily = analysis_result.get('safe_daily', 0)
            advice = f"""💡 Basic Financial Advice (API Error):
• Your daily burn rate is ₹{burn_rate:.2f}
• Safe daily spending limit: ₹{safe_daily:.2f}
• Track expenses regularly to stay within budget
• Consider reducing discretionary spending if burn rate is high
• Error: {str(e)}"""
    
    st.text_area('Advice', value=advice, height=200)
