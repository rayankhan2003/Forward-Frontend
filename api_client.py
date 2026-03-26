import requests
import logging

# Configuration - ADD YOUR API KEY AND BASE URL HERE
API_KEY = "YOUR_API_KEY_HERE"
API_BASE_URL = "https://api.yourwebsite.com/v1"

# ── Odoo Dashboard API ──────────────────────────
ODOO_URL = "http://localhost:8069"
ODOO_API_KEY = "FGC-DASHBOARD-SECRET-2026"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

# ── Odoo helpers ─────────────────────────────────
def _odoo_request(path):
    """Call an Odoo dashboard endpoint and return the parsed JSON data list/dict."""
    url = f"{ODOO_URL}{path}"
    try:
        resp = requests.get(url, headers={"X-API-KEY": ODOO_API_KEY}, timeout=10)
        resp.raise_for_status()
        body = resp.json()
        return body.get("data", body)
    except requests.RequestException as e:
        logger.error(f"Odoo API error ({path}): {e}")
        return None

def get_odoo_stats():
    """Fetch total_students / total_teachers counts from Odoo."""
    data = _odoo_request("/api/v1/dashboard/stats")
    if data:
        return data
    return {"total_students": 0, "total_teachers": 0}

def get_odoo_students():
    """Fetch full student list from Odoo (name, father_name, class, roll_no)."""
    data = _odoo_request("/api/v1/dashboard/students")
    if isinstance(data, list):
        return data
    return []

def get_odoo_teachers():
    """Fetch full teacher list from Odoo (name, cnic, subjects)."""
    data = _odoo_request("/api/v1/dashboard/teachers")
    if isinstance(data, list):
        return data
    return []

def _handle_request(endpoint, params=None):
    """Internal helper to handle API requests and errors."""
    if API_KEY == "YOUR_API_KEY_HERE":
        logger.warning(f"API Key not configured. Using placeholder for endpoint: {endpoint}")
        return None
    
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, headers=_get_headers(), params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API Request failed for {endpoint}: {e}")
        return None

def get_metrics():
    """Fetches dashboard metrics."""
    data = _handle_request("metrics")
    if data:
        return data
    # Fallback/Placeholder if API fails or not configured
    return {"total_students": 0, "students_growth": 0, "total_faculty": 0, "faculty_ratio": "0:0", "yearly_growth": 0}

def get_enrollment_trends():
    """Fetches enrollment trend data."""
    data = _handle_request("trends/enrollment")
    if data:
        return data
    return {"labels": [], "datasets": []}

def get_students(page=1, per_page=4):
    """Fetches paginated student list."""
    params = {"page": page, "per_page": per_page}
    data = _handle_request("students", params=params)
    if data:
        return data.get("students", []), data.get("total", 0)
    return [], 0

def get_campuses():
    """Fetches campus information."""
    data = _handle_request("campuses")
    if data:
        return data
    return []

def get_demographics():
    """Fetches student demographics."""
    data = _handle_request("demographics")
    if data:
        return data
    return []

def get_faculty():
    """Fetches faculty members."""
    data = _handle_request("faculty")
    if data:
        return data
    return []

def get_attendance():
    """Fetches attendance data."""
    data = _handle_request("attendance")
    if data:
        return data
    return {}

def get_report_metrics():
    """Fetches report-specific metrics."""
    data = _handle_request("metrics/reports")
    if data:
        return data
    return []

def get_attendance_trend():
    """Fetches attendance trend data."""
    data = _handle_request("trends/attendance")
    if data:
        return data
    return {"labels": [], "datasets": []}

def get_grade_distribution():
    """Fetches grade distribution data."""
    data = _handle_request("distribution/grades")
    if data:
        return data
    return {"labels": [], "datasets": []}
