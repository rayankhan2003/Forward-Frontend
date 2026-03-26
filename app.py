from flask import Flask, jsonify, request, render_template
import data_mock

app = Flask(__name__)

@app.route('/')
def dashboard():
    metrics      = data_mock.get_metrics()
    trends       = data_mock.get_enrollment_trends()
    students, _  = data_mock.get_students(page=1)
    campuses     = data_mock.get_campuses()
    demographics = data_mock.get_demographics()
    return render_template('dashboard.html',
                           metrics=metrics, trends=trends,
                           students=students, campuses=campuses,
                           demographics=demographics,
                           active_page='dashboard')

@app.route('/campuses')
def campuses():
    return render_template('campuses.html',
                           campuses=data_mock.get_campuses(),
                           active_page='campuses')

@app.route('/students')
def students():
    q       = request.args.get('q', '').lower()
    grade   = request.args.get('grade', '')
    campus  = request.args.get('campus', '')
    status  = request.args.get('status', '')
    page    = request.args.get('page', 1, type=int)
    all_s, total = data_mock.get_students(page=1, per_page=1000)
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
    return render_template('students.html',
                           students=paged, total=total, page=page, pages=pages,
                           q=request.args.get('q',''), grade=grade,
                           campus=campus, status=status,
                           active_page='students')

@app.route('/faculty')
def faculty():
    return render_template('faculty.html',
                           faculty=data_mock.get_faculty(),
                           attendance=data_mock.get_attendance(),
                           active_page='faculty')

@app.route('/reports')
def reports():
    return render_template('reports.html',
                           report_metrics=data_mock.get_report_metrics(),
                           attendance_trend=data_mock.get_attendance_trend(),
                           grade_dist=data_mock.get_grade_distribution(),
                           active_page='reports')

@app.route('/settings')
def settings():
    return render_template('settings.html', active_page='settings')

@app.route('/api/students')
def api_students():
    page = request.args.get('page', 1, type=int)
    students, total = data_mock.get_students(page=page)
    return jsonify({"students": students, "total": total})

if __name__ == '__main__':
    app.run(debug=True)
