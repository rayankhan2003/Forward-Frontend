import requests
import logging

# Configuration - ADD YOUR API KEY AND BASE URL HERE
API_KEY = "YOUR_API_KEY_HERE"
API_BASE_URL = "https://api.yourwebsite.com/v1"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

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
