import requests
import logging
from api_client import ODOO_INSTANCES, _odoo_request

logger = logging.getLogger(__name__)

# ── Financial Analytics & Executive KPIs (Boys School Focus for Phase 1) ─────────
# Fallback to mock data if live Odoo finance endpoints are unavailable.

def get_financial_kpis():
    """
    Returns Total Revenue, Monthly Revenue, Fee Recovery %, Outstanding Fees, 
    Net Profit/Loss, and Total Defaulters.
    """
    # Attempt to fetch from Boys School Odoo 13
    try:
        data = _odoo_request('boys_school', '/api/v1/finance/kpis')
        if data: return data
    except Exception as e:
        logger.warning(f"Live finance KPIs unavailable. Using mock data. Error: {e}")

    # MOCK FALLBACK
    return {
        "total_revenue": "PKR 12.4M",
        "monthly_revenue": "PKR 1.8M",
        "fee_recovery_percent": 84,
        "outstanding_fees": "PKR 2.1M",
        "net_profit_loss": "PKR 450K",
        "total_defaulters": 142
    }

def get_revenue_trends():
    """Returns monthly revenue vs collection trends for charts."""
    try:
        data = _odoo_request('boys_school', '/api/v1/finance/revenue-trends')
        if data: return data
    except Exception:
        pass

    # MOCK FALLBACK
    return {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "datasets": [
            {
                "label": "Billed Revenue",
                "data": [1.2, 1.3, 1.5, 1.4, 1.6, 1.8, 1.9, 2.0, 1.8, 1.7, 1.9, 2.1], # in Millions
                "backgroundColor": "rgba(59, 130, 246, 0.2)",
                "borderColor": "#3B82F6",
                "borderWidth": 2,
                "fill": True,
                "tension": 0.4
            },
            {
                "label": "Collected Revenue",
                "data": [1.0, 1.1, 1.3, 1.2, 1.4, 1.5, 1.6, 1.7, 1.5, 1.4, 1.6, 1.8],
                "backgroundColor": "rgba(16, 185, 129, 0.2)",
                "borderColor": "#10B981",
                "borderWidth": 2,
                "fill": True,
                "tension": 0.4
            }
        ]
    }

def get_profit_loss():
    """Returns P&L statement data: Income, Expenses, Net Profit."""
    try:
        data = _odoo_request('boys_school', '/api/v1/finance/profit-loss')
        if data: return data
    except Exception:
        pass

    # MOCK FALLBACK
    return {
        "income": [
            {"category": "Tuition Fees", "amount": 10500000},
            {"category": "Admission Fees", "amount": 1200000},
            {"category": "Transport Fees", "amount": 700000}
        ],
        "expenses": [
            {"category": "Payroll", "amount": 6500000},
            {"category": "Utilities", "amount": 800000},
            {"category": "Maintenance", "amount": 400000},
            {"category": "Marketing", "amount": 250000}
        ],
        "summary": {
            "total_income": 12400000,
            "total_expense": 7950000,
            "net_profit": 4450000,
            "margin_percent": 35.8
        }
    }

def get_defaulters():
    """Returns top outstanding fee defaulters."""
    try:
        data = _odoo_request('boys_school', '/api/v1/finance/defaulters')
        if data: return data
    except Exception:
        pass

    # MOCK FALLBACK
    return [
        {"student_id": "S-1023", "name": "Ahmad Ali", "class": "Matric", "amount_due": "PKR 45,000", "days_overdue": 65},
        {"student_id": "S-1452", "name": "Bilal Khan", "class": "F.Sc I", "amount_due": "PKR 32,500", "days_overdue": 45},
        {"student_id": "S-2104", "name": "Hamza Tariq", "class": "Grade 8", "amount_due": "PKR 28,000", "days_overdue": 30},
        {"student_id": "S-0988", "name": "Zain ul Abideen", "class": "Matric", "amount_due": "PKR 25,000", "days_overdue": 90},
        {"student_id": "S-3341", "name": "Raza Hassan", "class": "F.Sc II", "amount_due": "PKR 21,000", "days_overdue": 20}
    ]

def get_campus_financial_performance():
    """Compares financial metrics across campuses (using mock data for Girls campuses)."""
    try:
        data = _odoo_request('boys_school', '/api/v1/finance/campus-performance')
        if data: return data
    except Exception:
        pass

    # MOCK FALLBACK
    return [
        {
            "campus_key": "boys_school",
            "name": "Boys School",
            "revenue": "12.4M",
            "expense": "7.9M",
            "profit": "4.5M",
            "recovery_rate": 84,
            "status": "Excellent"
        },
        {
            "campus_key": "girls_school",
            "name": "Girls School",
            "revenue": "14.2M",
            "expense": "8.1M",
            "profit": "6.1M",
            "recovery_rate": 89,
            "status": "Excellent"
        },
        {
            "campus_key": "girls_college",
            "name": "Girls College",
            "revenue": "9.8M",
            "expense": "6.2M",
            "profit": "3.6M",
            "recovery_rate": 78,
            "status": "Attention Needed"
        }
    ]
