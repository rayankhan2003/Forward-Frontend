import os
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
        "url": "http://127.0.0.1:8072",
        "db": "forward_boys",
        "api_key": "FGC-DASHBOARD-SECRET-2026",},
    "girls_school": {
        "name": "Girls School",
        "url": "http://182.180.50.23:8071",
        "api_key": "FGC-DASHBOARD-SECRET-2026",
    },
    "girls_college": {
        "name": "Girls College",
        "url": "http://182.180.50.23:8071",
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
    db_param = f"?db={inst['db']}" if inst.get('db') else ""
    url = f"{inst['url']}{path}{db_param}"
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
    # Fallback: representative academic KPIs
    return [
        {"label": "AVERAGE ATTENDANCE RATE", "value": "87.4%", "badge": "+2.1%", "badge_type": "positive"},
        {"label": "OVERALL PASS RATE",       "value": "91.2%", "badge": "+3.5%", "badge_type": "positive"},
        {"label": "ENROLLED STUDENTS",       "value": "1,248", "badge": None,     "badge_type": ""},
        {"label": "DROPOUT RATE",            "value": "3.8%",  "badge": "-0.5%", "badge_type": "negative"},
    ]

def get_attendance_trend():
    data = _handle_request("trends/attendance")
    if data:
        return data
    # Fallback: 9-month attendance data per campus
    return {
        "labels": ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May"],
        "datasets": [
            {
                "label": "Boys School",
                "data": [85, 87, 88, 82, 86, 89, 91, 90, 88],
                "borderColor": "#3B82F6",
                "backgroundColor": "rgba(59,130,246,0.08)",
                "fill": True,
                "tension": 0.4,
                "pointRadius": 4,
                "pointBackgroundColor": "#3B82F6"
            },
            {
                "label": "Girls School",
                "data": [88, 90, 89, 84, 87, 91, 93, 92, 91],
                "borderColor": "#EC4899",
                "backgroundColor": "rgba(236,72,153,0.08)",
                "fill": True,
                "tension": 0.4,
                "pointRadius": 4,
                "pointBackgroundColor": "#EC4899"
            },
            {
                "label": "Girls College",
                "data": [82, 85, 86, 80, 84, 87, 89, 88, 87],
                "borderColor": "#8B5CF6",
                "backgroundColor": "rgba(139,92,246,0.08)",
                "fill": True,
                "tension": 0.4,
                "pointRadius": 4,
                "pointBackgroundColor": "#8B5CF6"
            }
        ]
    }

def get_grade_distribution():
    data = _handle_request("distribution/grades")
    if data:
        return data
    # Fallback: realistic grade spread across all students
    return {
        "labels": ["A+", "A", "B", "C", "D", "F"],
        "datasets": [{
            "label": "Students",
            "data": [120, 285, 340, 280, 150, 73],
            "backgroundColor": ["#22c55e", "#3B82F6", "#8B5CF6", "#F59E0B", "#F97316", "#EF4444"],
            "borderRadius": 6
        }]
    }


# ── Real Report Data (computed from Odoo) ────────
def get_real_report_metrics():
    """Compute report KPI cards from actual Odoo data."""
    combined = get_combined_odoo_stats()
    total_s = combined['total_students']
    total_t = combined['total_teachers']

    all_students = get_all_odoo_students()
    classes = set(str(s.get('class', '')).strip() for s in all_students if s.get('class'))

    ratio = round(total_s / total_t, 1) if total_t else 0

    return [
        {"label": "TOTAL ENROLLED STUDENTS", "value": f"{total_s:,}", "badge": None, "badge_type": ""},
        {"label": "TOTAL FACULTY MEMBERS",   "value": str(total_t),   "badge": None, "badge_type": ""},
        {"label": "STUDENT-TEACHER RATIO",   "value": f"{ratio}:1",   "badge": None, "badge_type": ""},
        {"label": "ACTIVE CLASSES",          "value": str(len(classes)), "badge": None, "badge_type": ""},
    ]


def get_class_distribution():
    """Count students grouped by program level + year from actual Odoo data.
    e.g. 'F.Sc I [Daffodil]-2025-2026' → 'F.Sc I — 2025-2026'
    """
    import re
    all_students = get_all_odoo_students()
    group_counts = {}
    for s in all_students:
        c = s.get('class', '')
        if not c:
            continue
        # Extract program level (before '[') and year (after ']-')
        match = re.match(r'^(.*?)\s*\[.*?\]-?(.*)$', c)
        if match:
            program = match.group(1).strip()
            year = match.group(2).strip()
            group_key = f"{program} — {year}" if year else program
        else:
            group_key = c
        group_counts[group_key] = group_counts.get(group_key, 0) + 1

    sorted_groups = sorted(group_counts.items())
    colors = ['#3B82F6', '#EC4899', '#8B5CF6', '#F59E0B', '#10B981',
              '#EF4444', '#6366F1', '#14B8A6', '#F97316', '#22c55e']

    return {
        "labels": [g[0] for g in sorted_groups],
        "datasets": [{
            "label": "Students",
            "data": [g[1] for g in sorted_groups],
            "backgroundColor": [colors[i % len(colors)] for i in range(len(sorted_groups))],
            "borderRadius": 6
        }]
    }


def get_subject_distribution():
    """Count teachers per subject from actual Odoo data."""
    all_teachers = get_all_odoo_teachers()
    subj_counts = {}
    for t in all_teachers:
        for s in t.get('subjects', []):
            subj_counts[s] = subj_counts.get(s, 0) + 1

    sorted_subjects = sorted(subj_counts.items(), key=lambda x: x[1], reverse=True)
    colors = ['#3B82F6', '#22c55e', '#8B5CF6', '#F59E0B', '#EC4899',
              '#EF4444', '#14B8A6', '#F97316', '#6366F1', '#10B981']

    return {
        "labels": [s[0] for s in sorted_subjects],
        "datasets": [{
            "label": "Teachers",
            "data": [s[1] for s in sorted_subjects],
            "backgroundColor": [colors[i % len(colors)] for i in range(len(sorted_subjects))],
            "borderRadius": 6
        }]
    }

