def get_metrics():
    return {"total_students": 1240, "students_growth": 8,
            "total_faculty": 85, "faculty_ratio": "14.5:1", "yearly_growth": 12.5}

def get_enrollment_trends():
    return {
        "labels": ["Phase 1", "Phase 2", "Ring Road"],
        "datasets": [
            {"label": "2023", "data": [400, 420, 310], "backgroundColor": "#1D4ED8", "borderRadius": 4},
            {"label": "2024", "data": [450, 410, 390], "backgroundColor": "#0F172A", "borderRadius": 4}
        ]
    }

def get_students(page=1, per_page=4):
    all_students = [
        {"id": 1,  "name": "Alice Johnson",  "initials": "AJ", "school": "Phase 1 Campus", "grade": "10th", "date": "2024-01-15", "status": "ENROLLED", "gpa": "3.8", "id_num": "STU-10021", "email": "a.johnson@edu.forward.org", "phone": "+1 (555) 012-9844"},
        {"id": 2,  "name": "Bob Smith",       "initials": "BS", "school": "Phase 2 Campus", "grade": "11th", "date": "2023-11-20", "status": "ALUMNI",   "gpa": "3.5", "id_num": "STU-10022", "email": "b.smith@edu.forward.org",   "phone": "+1 (555) 012-9845"},
        {"id": 3,  "name": "Charlie Davis",   "initials": "CD", "school": "Ring Road Campus",  "grade": "12th", "date": "2024-02-10", "status": "ENROLLED", "gpa": "3.9", "id_num": "STU-10023", "email": "c.davis@edu.forward.org",   "phone": "+1 (555) 012-9846"},
        {"id": 4,  "name": "Diana Ross",      "initials": "DR", "school": "Phase 1 Campus", "grade": "9th",  "date": "2024-03-01", "status": "ENROLLED", "gpa": "3.7", "id_num": "STU-10024", "email": "d.ross@edu.forward.org",    "phone": "+1 (555) 012-9847"},
        {"id": 5,  "name": "Edward Norton",   "initials": "EN", "school": "Phase 2 Campus", "grade": "12th", "date": "2023-12-05", "status": "ALUMNI",   "gpa": "3.2", "id_num": "STU-10025", "email": "e.norton@edu.forward.org",  "phone": "+1 (555) 012-9848"},
        {"id": 6,  "name": "Fiona Grant",     "initials": "FG", "school": "Ring Road Campus",  "grade": "10th", "date": "2024-01-20", "status": "ENROLLED", "gpa": "4.0", "id_num": "STU-10026", "email": "f.grant@edu.forward.org",   "phone": "+1 (555) 012-9849"},
        {"id": 7,  "name": "George Hill",     "initials": "GH", "school": "Phase 1 Campus", "grade": "11th", "date": "2023-10-15", "status": "ENROLLED", "gpa": "3.6", "id_num": "STU-10027", "email": "g.hill@edu.forward.org",    "phone": "+1 (555) 012-9850"},
        {"id": 8,  "name": "Hannah Brooks",   "initials": "HB", "school": "Phase 2 Campus", "grade": "9th",  "date": "2024-02-28", "status": "ENROLLED", "gpa": "3.4", "id_num": "STU-10028", "email": "h.brooks@edu.forward.org",  "phone": "+1 (555) 012-9851"},
        {"id": 9,  "name": "Ivan Reyes",      "initials": "IR", "school": "Ring Road Campus",  "grade": "10th", "date": "2024-03-10", "status": "ENROLLED", "gpa": "3.3", "id_num": "STU-10029", "email": "i.reyes@edu.forward.org",   "phone": "+1 (555) 012-9852"},
        {"id": 10, "name": "Julia Torres",    "initials": "JT", "school": "Phase 1 Campus", "grade": "12th", "date": "2023-09-01", "status": "ALUMNI",   "gpa": "3.9", "id_num": "STU-10030", "email": "j.torres@edu.forward.org",  "phone": "+1 (555) 012-9853"},
        {"id": 11, "name": "Kevin Patel",     "initials": "KP", "school": "Phase 2 Campus", "grade": "9th",  "date": "2024-01-08", "status": "ENROLLED", "gpa": "3.1", "id_num": "STU-10031", "email": "k.patel@edu.forward.org",   "phone": "+1 (555) 012-9854"},
        {"id": 12, "name": "Laura Nguyen",    "initials": "LN", "school": "Ring Road Campus",  "grade": "11th", "date": "2024-02-14", "status": "ENROLLED", "gpa": "3.7", "id_num": "STU-10032", "email": "l.nguyen@edu.forward.org",  "phone": "+1 (555) 012-9855"},
    ]
    start = (page - 1) * per_page
    return all_students[start:start + per_page], len(all_students)


def get_campuses():
    return [
        {"name": "Phase 1 Campus", "type": "REGIONAL HUB",    "district": "Urban District Center",  "founded": "Est. 2001", "performance_num": 88, "students": 450, "img": "/static/img/phase 1 college.jpg"},
        {"name": "Phase 2 Campus", "type": "HERITAGE CENTER",  "district": "Heritage District",       "founded": "Est. 1998", "performance_num": 74, "students": 410, "img": "/static/img/phase 2 school.jpg"},
        {"name": "Ring Road Campus",  "type": "INNOVATION WING",  "district": "Riverside Expansion",     "founded": "Est. 2015", "performance_num": 64, "students": 380, "img": "/static/img/ring road.jpg"},
    ]

def get_demographics():
    return [
        {"label": "Secondary", "pct": 58, "color": "#0F172A"},
        {"label": "Primary",   "pct": 42, "color": "#93C5FD"},
    ]

def get_faculty():
    return [
        {"name": "Dr. Sarah Jenkins",  "initials": "SJ", "role": "Principal",        "dept": "Administration", "classes": 0,  "tenure": "12 yrs", "email": "s.jenkins@edu.forward.org",  "campus": "Phase 1 Campus", "present": True},
        {"name": "Prof. Mark Turner",   "initials": "MT", "role": "Senior Lecturer",  "dept": "Mathematics",    "classes": 4,  "tenure": "8 yrs",  "email": "m.turner@edu.forward.org",   "campus": "Phase 1 Campus", "present": True},
        {"name": "Ms. Linda Chen",      "initials": "LC", "role": "Lecturer",         "dept": "Science",        "classes": 5,  "tenure": "5 yrs",  "email": "l.chen@edu.forward.org",     "campus": "Phase 2 Campus", "present": True},
        {"name": "Mr. James Owens",     "initials": "JO", "role": "Head of Dept.",    "dept": "English",        "classes": 3,  "tenure": "10 yrs", "email": "j.owens@edu.forward.org",    "campus": "Phase 2 Campus", "present": False},
        {"name": "Dr. Amara Diallo",    "initials": "AD", "role": "Senior Lecturer",  "dept": "History",        "classes": 6,  "tenure": "7 yrs",  "email": "a.diallo@edu.forward.org",   "campus": "Ring Road Campus",  "present": True},
        {"name": "Ms. Kim Nakamura",    "initials": "KN", "role": "Lecturer",         "dept": "Computer Sci.",  "classes": 4,  "tenure": "3 yrs",  "email": "k.nakamura@edu.forward.org", "campus": "Ring Road Campus",  "present": True},
    ]

def get_attendance():
    return {"MON": 92, "TUE": 95, "WED": 97, "THU": 93, "FRI": 88}

def get_report_metrics():
    return [
        {"label": "AVERAGE GPA",        "value": "3.64",  "badge": "+4.2%",    "badge_type": "positive"},
        {"label": "ATTENDANCE",          "value": "94.2%", "badge": "-0.8%",    "badge_type": "negative"},
        {"label": "TUITION COLLECTION",  "value": "88.5%", "badge": "On Track", "badge_type": "neutral"},
        {"label": "TOTAL STUDENTS",      "value": "12,482","badge": "",         "badge_type": ""},
    ]

def get_attendance_trend():
    return {
        "labels": ["Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar","Apr","May"],
        "datasets": [
            {"label": "Current Year",  "data": [88,91,94,93,90,92,95,94,93,92], "borderColor": "#1D4ED8", "backgroundColor": "rgba(29,78,216,0.1)", "fill": True, "tension": 0.4},
            {"label": "Previous Year", "data": [85,88,90,89,87,90,92,91,90,89], "borderColor": "#CBD5E1", "backgroundColor": "rgba(203,213,225,0.1)", "fill": True, "tension": 0.4},
        ]
    }

def get_grade_distribution():
    return {
        "labels": ["A", "B", "C", "D", "F"],
        "datasets": [{
            "label": "Students",
            "data": [380, 520, 290, 80, 30],
            "backgroundColor": ["#0F172A","#1D4ED8","#60A5FA","#93C5FD","#DBEAFE"],
            "borderRadius": 4
        }]
    }
