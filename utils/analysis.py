import pandas as pd
import numpy as np
from datetime import date, timedelta
from typing import Dict

def calculate_forecast(df: pd.DataFrame, balance: float) -> Dict:
    """Calculate burn rate (avg last 10 days), run-out date, and safe daily spending.

    Returns dict {burn_rate, run_out_date (iso or 'N/A'), safe_daily}
    """
    today = date.today()

    if df is None or df.empty:
        burn_rate = 0.0
    else:
        df_copy = df.copy()
        # Ensure date column is datetime.date
        if 'date' in df_copy.columns:
            df_copy['date'] = pd.to_datetime(df_copy['date']).dt.date
        else:
            df_copy['date'] = today

        # Consider only expenses as positive amounts
        # Aggregate spend per day for last 10 days
        start = today - timedelta(days=9)
        mask = df_copy['date'] >= start
        last_period = df_copy.loc[mask]

        if last_period.empty:
            burn_rate = 0.0
        else:
            daily = last_period.groupby('date')['amount'].sum()
            # If fewer than 10 days present, include zeros for missing days
            all_days = [start + timedelta(days=i) for i in range(10)]
            daily_full = pd.Series([daily.get(d, 0.0) for d in all_days], index=all_days)
            burn_rate = float(daily_full.mean())

    safe_daily = float(balance / 30.0) if balance is not None else 0.0

    if burn_rate <= 0:
        run_out = 'N/A'
    else:
        days_left = balance / burn_rate if burn_rate > 0 else float('inf')
        try:
            run_out_date = today + timedelta(days=int(np.floor(days_left)))
            run_out = run_out_date.isoformat()
        except Exception:
            run_out = 'N/A'

    return {
        'burn_rate': float(burn_rate),
        'run_out_date': run_out,
        'safe_daily': float(safe_daily),
    }
