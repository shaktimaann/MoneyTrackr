import os
from typing import Dict, List
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date, Text
from sqlalchemy.sql import select
from sqlalchemy.exc import OperationalError
import pandas as pd
from datetime import datetime

DB_URL = os.getenv('DATABASE_URL', 'sqlite:///budget.db')

engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith('sqlite') else {})
metadata = MetaData()

transactions = Table(
    'transactions', metadata,
    Column('id', Integer, primary_key=True),
    Column('date', String, nullable=False),
    Column('amount', Float, nullable=False),
    Column('vendor', String, default='Unknown'),
    Column('category', String, default='Misc'),
    Column('text', Text, default=''),
)

def init_db():
    """Create DB and table if not exists."""
    metadata.create_all(engine)

def insert_txn(txn: Dict):
    """Insert a transaction dict with keys: date (iso str), amount (float), vendor, category, text."""
    init_db()
    ins = transactions.insert().values(
        date=txn.get('date'),
        amount=txn.get('amount', 0.0),
        vendor=txn.get('vendor', 'Unknown'),
        category=txn.get('category', 'Misc'),
        text=txn.get('text', ''),
    )
    with engine.begin() as conn:
        conn.execute(ins)

def load_df() -> pd.DataFrame:
    """Load transactions table into a pandas DataFrame and parse date column."""
    init_db()
    try:
        with engine.connect() as conn:
            sel = select(transactions)
            res = conn.execute(sel)
            # SQLAlchemy Row objects expose a mapping protocol; use _mapping for dict conversion
            rows = [dict(r._mapping) for r in res]
    except OperationalError:
        rows = []

    if not rows:
        df = pd.DataFrame(columns=['id', 'date', 'amount', 'vendor', 'category', 'text'])
    else:
        df = pd.DataFrame(rows)

    if 'date' in df.columns:
        # try parse to datetime
        try:
            df['date'] = pd.to_datetime(df['date']).dt.date
        except Exception:
            pass

    return df

def clear_all_transactions():
    """Delete all transactions from the database."""
    init_db()
    with engine.begin() as conn:
        conn.execute(transactions.delete())
