from flask import Flask, jsonify, request, render_template
import api_client

app = Flask(__name__)

@app.route('/')
def dashboard():
    campus = request.args.get('campus', '').strip()

    metrics      = api_client.get_metrics()
    campuses     = api_client.get_campuses()
    demographics = api_client.get_demographics()

    # Get stats from all 3 schools for the chart
    all_stats = api_client.get_all_odoo_stats()
    
    # Prepare chart data (X-axis: School name, Y-axis: Students)
    trends = {
        "labels": [api_client.ODOO_INSTANCES[k]["name"] for k in all_stats],
        "datasets": [{
            "label": "Total Students",
            "data": [all_stats[k].get("total_students", 0) for k in all_stats],
            "backgroundColor": ["#3B82F6", "#EC4899", "#8B5CF6"],
            "borderRadius": 6
        }]
    }

    # Filter by campus if selected, otherwise show combined stats
    if campus and campus in api_client.ODOO_INSTANCES:
        single_stats = api_client.get_odoo_stats(campus)
        combined_stats = {
            'total_students': single_stats.get('total_students', 0),
            'total_teachers': single_stats.get('total_teachers', 0),
            'per_campus': {campus: single_stats},
        }
        odoo_students = api_client.get_all_odoo_students(campus_filter=campus)
    else:
        combined_stats = api_client.get_combined_odoo_stats()
        odoo_students  = api_client.get_all_odoo_students()
        campus = ''

    return render_template('dashboard.html',
                           metrics=metrics, trends=trends,
                           campuses=campuses,
                           demographics=demographics,
                           combined_stats=combined_stats,
                           odoo_instances=api_client.ODOO_INSTANCES,
                           odoo_students=odoo_students[:10],
                           active_page='dashboard',
                           campus=campus)

@app.route('/campuses')
def campuses():
    return render_template('campuses.html',
                           combined_stats=api_client.get_combined_odoo_stats(),
                           odoo_instances=api_client.ODOO_INSTANCES,
                           active_page='campuses')

@app.route('/students')
def students():
    q      = request.args.get('q', '').lower()
    page   = request.args.get('page', 1, type=int)
    campus = request.args.get('campus', '').strip()

    # Fetch from one campus or all
    if campus and campus in api_client.ODOO_INSTANCES:
        all_s = api_client.get_all_odoo_students(campus_filter=campus)
    else:
        all_s = api_client.get_all_odoo_students()
        campus = ''  # reset invalid values

    # search filter
    if q:
        all_s = [s for s in all_s
                 if q in s.get('name','').lower()
                 or q in s.get('father_name','').lower()]

    total    = len(all_s)
    per_page = 10
    start    = (page - 1) * per_page
    paged    = all_s[start:start + per_page]
    pages    = max(1, (total + per_page - 1) // per_page)

    return render_template('students.html',
                           students=paged, total=total,
                           page=page, pages=pages,
                           q=request.args.get('q', ''),
                           campus=campus,
                           odoo_instances=api_client.ODOO_INSTANCES,
                           active_page='students')

@app.route('/faculty')
def faculty():
    campus = request.args.get('campus', '').strip()
    subject = request.args.get('subject', '').strip()

    # Fetch teachers based on campus filter
    teachers = api_client.get_all_odoo_teachers(campus_filter=campus)
    
    # Extract all unique subjects for the filter dropdown
    all_subjects = set()
    for t in teachers:
        subjs = t.get('subjects', [])
        if isinstance(subjs, list):
            for s in subjs:
                all_subjects.add(s)
    
    all_subjects = sorted(list(all_subjects))

    # Apply subject filter if selected
    if subject:
        teachers = [t for t in teachers if subject in t.get('subjects', [])]

    return render_template('faculty.html',
                           faculty=teachers,
                           campus=campus,
                           selected_subject=subject,
                           all_subjects=all_subjects,
                           odoo_instances=api_client.ODOO_INSTANCES,
                           active_page='faculty')

@app.route('/reports')
def reports():
    return render_template('reports.html',
                           report_metrics=api_client.get_report_metrics(),
                           attendance_trend=api_client.get_attendance_trend(),
                           grade_dist=api_client.get_grade_distribution(),
                           active_page='reports')

@app.route('/settings')
def settings():
    return render_template('settings.html', active_page='settings')

@app.route('/api/students')
def api_students():
    page = request.args.get('page', 1, type=int)
    students, total = api_client.get_students(page=page)
    return jsonify({"students": students, "total": total})

if __name__ == '__main__':
    app.run(debug=True)
    app.run(debug=True)
