import re
from datetime import date, datetime
from typing import Dict, List

RUPEE_REGEX = re.compile(r"(?:Rs\.?|INR|₹)\s*([0-9,]+(?:\.[0-9]{1,2})?)", re.IGNORECASE)
DEBIT_CREDIT_REGEX = re.compile(r"(?:debited|credited|by)\s*[:\s]?\s*([0-9,]+(?:\.[0-9]{1,2})?)", re.IGNORECASE)
DECIMAL_REGEX = re.compile(r"([0-9]+\.[0-9]{1,2})")
GENERIC_INT_REGEX = re.compile(r"\b([1-9][0-9]{1,6}(?:\.[0-9]{1,2})?)\b")


def _extract_vendor(text: str) -> str:
    # Try to find "to <vendor> Refno" or "to <vendor> on" patterns
    m = re.search(r"to\s+(.+?)(?:\s+Refno|\s+refno|\s+on\s|$)", text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return "Unknown"


def _categorize_by_vendor(vendor: str) -> str:
    """Simple rule-based categorization based on vendor name"""
    vendor_lower = vendor.lower()
    
    if any(word in vendor_lower for word in ['food', 'restaurant', 'cafe', 'pizza', 'burger', 'kitchen', 'plaz']):
        return 'Food'
    elif any(word in vendor_lower for word in ['google', 'microsoft', 'netflix', 'spotify', 'amazon']):
        return 'Subscription'
    elif any(word in vendor_lower for word in ['uber', 'ola', 'taxi', 'transport', 'metro']):
        return 'Transport'
    elif any(word in vendor_lower for word in ['grocery', 'mart', 'store', 'supermarket']):
        return 'Grocery'
    elif any(word in vendor_lower for word in ['electricity', 'gas', 'water', 'utility']):
        return 'Utilities'
    elif len(vendor.split()) >= 2 and all(word.istitle() for word in vendor.split()[:2]):
        return 'Personal Transfer'  # Likely person names
    else:
        return 'Misc'


def _extract_date(text: str) -> str:
    """Extract date from SMS text in format DDMmmYY (e.g., 25Oct25, 04Nov25)"""
    date_match = re.search(r'\b(\d{1,2})(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\d{2})\b', text, re.IGNORECASE)
    if date_match:
        day, month, year = date_match.groups()
        month_map = {
            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
            'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
            'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
        }
        month_num = month_map.get(month.lower(), '01')
        full_year = f"20{year}" if int(year) < 50 else f"19{year}"
        try:
            parsed_date = datetime.strptime(f"{full_year}-{month_num}-{day.zfill(2)}", "%Y-%m-%d")
            return parsed_date.date().isoformat()
        except ValueError:
            pass
    return date.today().isoformat()


def parse_bulk_sms(text: str) -> List[Dict]:
    """Parse multiple SMS messages from bulk text and return list of transactions"""
    if not text.strip():
        return []
    
    # Split by lines and filter out empty lines
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    
    transactions = []
    for line in lines:
        if 'debited' in line.lower() or 'credited' in line.lower():
            txn = parse_sms(line)
            transactions.append(txn)
    
    return transactions


def parse_sms(text: str) -> Dict:
    """Extract amount from an SMS-like text and return a transaction dict.

    Returns dict: {date, amount, vendor, text}
    Basic extraction rules:
    - Prefer explicit currency symbols (₹, Rs., INR)
    - Then look for phrases like 'debited by 19.0' or 'credited by'
    - Then prefer decimal numbers
    - Fallback to a generic integer match (avoids single-digit days)
    """
    if not isinstance(text, str):
        text = str(text or "")

    amount = 0.0

    # 1) currency symbols
    m = RUPEE_REGEX.search(text)
    if m:
        raw = m.group(1).replace(',', '')
        try:
            amount = float(raw)
        except Exception:
            amount = 0.0
    else:
        # 2) phrases like 'debited by 19.0' or 'credited by'
        m2 = DEBIT_CREDIT_REGEX.search(text)
        if m2:
            raw = m2.group(1).replace(',', '')
            try:
                amount = float(raw)
            except Exception:
                amount = 0.0
        else:
            # 3) decimal number anywhere (prefer decimals to avoid matching dates)
            m3 = DECIMAL_REGEX.search(text)
            if m3:
                try:
                    amount = float(m3.group(1))
                except Exception:
                    amount = 0.0
            else:
                # 4) fallback to generic integer-like numbers (avoid single-digit)
                m4 = GENERIC_INT_REGEX.search(text)
                if m4:
                    try:
                        amount = float(m4.group(1).replace(',', ''))
                    except Exception:
                        amount = 0.0

    vendor = _extract_vendor(text)

    txn = {
        "date": _extract_date(text),
        "amount": float(amount),
        "vendor": vendor,
        "text": text.strip(),
    }
    return txn
