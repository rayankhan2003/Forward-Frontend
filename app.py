from flask import Flask, jsonify, request, render_template
import api_client

app = Flask(__name__)

@app.route('/')
def dashboard():
    metrics      = api_client.get_metrics()
    trends       = api_client.get_enrollment_trends()
    students, _  = api_client.get_students(page=1)
    campuses     = api_client.get_campuses()
    demographics = api_client.get_demographics()
    return render_template('dashboard.html',
                           metrics=metrics, trends=trends,
                           students=students, campuses=campuses,
                           demographics=demographics,
                           active_page='dashboard')

@app.route('/campuses')
def campuses():
    return render_template('campuses.html',
                           campuses=api_client.get_campuses(),
                           active_page='campuses')

@app.route('/students')
def students():
    q       = request.args.get('q', '').lower()
    grade   = request.args.get('grade', '')
    campus  = request.args.get('campus', '')
    status  = request.args.get('status', '')
    page    = request.args.get('page', 1, type=int)
    all_s, total = api_client.get_students(page=1, per_page=1000)
    # filter
    if q:
        all_s = [s for s in all_s if q in s['name'].lower() or q in s['school'].lower()]
    if grade:
        all_s = [s for s in all_s if s['grade'] == grade]
    if campus:
        all_s = [s for s in all_s if campus.lower() in s['school'].lower()]
    if status:
        all_s = [s for s in all_s if s['status'].lower() == status.lower()]
    total = len(all_s)
    per_page = 4
    start = (page-1)*per_page
    paged = all_s[start:start+per_page]
    pages = max(1, (total + per_page - 1) // per_page)
    
    # Calculate simple stats for the summary cards
    avg_gpa = sum(float(s['gpa']) for s in all_s) / total if total > 0 else 0.0
    attendance_rate = 0.0 # Placeholder as it's not in student model
    warnings_count = 0 # Placeholder
    
    return render_template('students.html',
                           students=paged, total=total, page=page, pages=pages,
                           avg_gpa="{:.2f}".format(avg_gpa),
                           attendance_rate="{:.1f}".format(attendance_rate),
                           warnings_count=warnings_count,
                           q=request.args.get('q',''), grade=grade,
                           campus=campus, status=status,
                           active_page='students')

@app.route('/faculty')
def faculty():
    return render_template('faculty.html',
                           faculty=api_client.get_faculty(),
                           attendance=api_client.get_attendance(),
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
