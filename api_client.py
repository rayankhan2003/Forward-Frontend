import requests
import logging

# Configuration - ADD YOUR API KEY AND BASE URL HERE
API_KEY = "YOUR_API_KEY_HERE"
API_BASE_URL = "https://api.yourwebsite.com/v1"

# ── Odoo Dashboard API – Three Instances ─────────
# For testing, all three point to the same server.
# In production, change each URL to the real Odoo server for that campus.
ODOO_INSTANCES = {
    "boys_school": {
        "name": "Boys School",
        "url": "http://localhost:8069",
        "api_key": "FGC-DASHBOARD-SECRET-2026",
    },
    "girls_school": {
        "name": "Girls School",
        "url": "http://localhost:8069",
        "api_key": "FGC-DASHBOARD-SECRET-2026",
    },
    "girls_college": {
        "name": "Girls College",
        "url": "http://localhost:8069",
        "api_key": "FGC-DASHBOARD-SECRET-2026",
    },
}

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

# ── Odoo helpers ─────────────────────────────────
def _odoo_request(instance_key, path):
    """Call an Odoo dashboard endpoint for a specific campus instance."""
    inst = ODOO_INSTANCES.get(instance_key)
    if not inst:
        logger.error(f"Unknown Odoo instance: {instance_key}")
        return None
    url = f"{inst['url']}{path}"
    try:
        resp = requests.get(url, headers={"X-API-KEY": inst["api_key"]}, timeout=10)
        resp.raise_for_status()
        body = resp.json()
        return body.get("data", body)
    except requests.RequestException as e:
        logger.error(f"Odoo API error ({instance_key} – {path}): {e}")
        return None


# ── Per-instance fetchers ────────────────────────
def get_odoo_stats(instance_key):
    """Fetch total_students / total_teachers counts from one Odoo campus."""
    data = _odoo_request(instance_key, "/api/v1/dashboard/stats")
    if data:
        return data
    return {"total_students": 0, "total_teachers": 0}

def get_odoo_students(instance_key):
    """Fetch student list from one Odoo campus (name, father_name, class, roll_no)."""
    data = _odoo_request(instance_key, "/api/v1/dashboard/students")
    if isinstance(data, list):
        return data
    return []

def get_odoo_teachers(instance_key):
    """Fetch teacher list from one Odoo campus (name, cnic, subjects)."""
    data = _odoo_request(instance_key, "/api/v1/dashboard/teachers")
    if isinstance(data, list):
        return data
    return []


# ── Aggregated fetchers (all 3 campuses) ─────────
def get_all_odoo_stats():
    """Return {instance_key: stats_dict} for every configured campus."""
    result = {}
    for key in ODOO_INSTANCES:
        result[key] = get_odoo_stats(key)
    return result

def get_combined_odoo_stats():
    """Return a single dict with combined totals across all campuses."""
    all_stats = get_all_odoo_stats()
    total_students = sum(s.get("total_students", 0) for s in all_stats.values())
    total_teachers = sum(s.get("total_teachers", 0) for s in all_stats.values())
    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "per_campus": all_stats,
    }

def get_all_odoo_students(campus_filter=None):
    """
    Fetch students from all campuses (or one if campus_filter is set).
    Each student dict gets a 'campus' and 'campus_name' field injected.
    """
    keys = [campus_filter] if campus_filter and campus_filter in ODOO_INSTANCES else list(ODOO_INSTANCES.keys())
    combined = []
    for key in keys:
        students = get_odoo_students(key)
        for s in students:
            s["campus"] = key
            s["campus_name"] = ODOO_INSTANCES[key]["name"]
        combined.extend(students)
    return combined

def get_all_odoo_teachers(campus_filter=None):
    """
    Fetch teachers from all campuses (or one if campus_filter is set).
    Each teacher dict gets a 'campus' and 'campus_name' field injected.
    """
    keys = [campus_filter] if campus_filter and campus_filter in ODOO_INSTANCES else list(ODOO_INSTANCES.keys())
    combined = []
    for key in keys:
        teachers = get_odoo_teachers(key)
        for t in teachers:
            t["campus"] = key
            t["campus_name"] = ODOO_INSTANCES[key]["name"]
        combined.extend(teachers)
    return combined


# ── Generic API helpers (unchanged) ──────────────
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
    data = _handle_request("metrics")
    if data:
        return data
    return {"total_students": 0, "students_growth": 0, "total_faculty": 0, "faculty_ratio": "0:0", "yearly_growth": 0}

def get_enrollment_trends():
    data = _handle_request("trends/enrollment")
    if data:
        return data
    return {"labels": [], "datasets": []}

def get_students(page=1, per_page=4):
    params = {"page": page, "per_page": per_page}
    data = _handle_request("students", params=params)
    if data:
        return data.get("students", []), data.get("total", 0)
    return [], 0

def get_campuses():
    data = _handle_request("campuses")
    if data:
        return data
    return []

def get_demographics():
    data = _handle_request("demographics")
    if data:
        return data
    return []

def get_faculty():
    data = _handle_request("faculty")
    if data:
        return data
    return []

def get_attendance():
    data = _handle_request("attendance")
    if data:
        return data
    return {}

def get_report_metrics():
    data = _handle_request("metrics/reports")
    if data:
        return data
    return []

def get_attendance_trend():
    data = _handle_request("trends/attendance")
    if data:
        return data
    return {"labels": [], "datasets": []}

def get_grade_distribution():
    data = _handle_request("distribution/grades")
    if data:
        return data
    return {"labels": [], "datasets": []}
