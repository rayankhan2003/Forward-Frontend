from flask import Flask, jsonify, request, render_template
import api_client

app = Flask(__name__)

@app.route('/')
def dashboard():
    metrics      = api_client.get_metrics()
    trends       = api_client.get_enrollment_trends()
    campuses     = api_client.get_campuses()
    demographics = api_client.get_demographics()
    odoo_stats   = api_client.get_odoo_stats()
    odoo_students = api_client.get_odoo_students()
    return render_template('dashboard.html',
                           metrics=metrics, trends=trends,
                           campuses=campuses,
                           demographics=demographics,
                           odoo_stats=odoo_stats,
                           odoo_students=odoo_students[:10],
                           active_page='dashboard')

@app.route('/campuses')
def campuses():
    return render_template('campuses.html',
                           campuses=api_client.get_campuses(),
                           active_page='campuses')

@app.route('/students')
def students():
    q    = request.args.get('q', '').lower()
    page = request.args.get('page', 1, type=int)
    all_s = api_client.get_odoo_students()
    # filter by name or father_name
    if q:
        all_s = [s for s in all_s
                 if q in s.get('name','').lower()
                 or q in s.get('father_name','').lower()]
    total = len(all_s)
    per_page = 10
    start = (page-1)*per_page
    paged = all_s[start:start+per_page]
    pages = max(1, (total + per_page - 1) // per_page)
    return render_template('students.html',
                           students=paged, total=total,
                           page=page, pages=pages,
                           q=request.args.get('q',''),
                           active_page='students')

@app.route('/faculty')
def faculty():
    return render_template('faculty.html',
                           faculty=api_client.get_odoo_teachers(),
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
