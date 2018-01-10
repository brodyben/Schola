from flask import Flask, render_template, request, redirect, session
from flaskext.mysql import MySQL
import jinja2
import os

app = Flask(__name__)
app.secret_key = 'secret'

# MySQL configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'schola'
app.config['MYSQL_DATABASE_HOST'] = '104.154.205.224'
mysql.init_app(app)
connection = mysql.connect()

def session_login(username):
	session['username'] = username
	session['tutor'] = get_tutor_id(username)
	session['teacher'] = get_teacher_id(username)
	session.permanent = True

def session_logout():
	session.pop('username', None)
	session.pop('tutor', None)
	session.pop('teacher', None)

def logged_in():
	if session.get('username') is None:
		return None
	user = {
		'username': session.get('username'),
		'tutor': session.get('tutor'),
		'teacher': session.get('teacher'),
	}
	return user

def get_tutor_id(username):
	cursor = connection.cursor()
	tutor_query = """
		SELECT t.id
		FROM user u 
		JOIN tutor t ON t.login = u.username 
		WHERE u.username = '{}';
	""".format(username)
	cursor.execute(tutor_query)
	is_tutor = cursor.fetchone()
	if is_tutor:
		return is_tutor[0]

def get_teacher_id(username):
	cursor = connection.cursor()
	teacher_query = """
		SELECT t.id
		FROM user u 
		JOIN teacher t ON t.login = u.username 
		WHERE u.username = '{}';
	""".format(username)
	cursor.execute(teacher_query)
	is_teacher = cursor.fetchone()
	if is_teacher:
		return is_teacher[0]

@app.route('/')
def index():
	return render_template('index.html', login=logged_in())

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		if not(username):
			return render_template('login.html', error='No username found.')
		if not(password):
			return render_template('login.html', error='No password found.')
		cursor = connection.cursor()
		login_query = """
			SELECT username
			FROM user 
			WHERE username = '{}' AND password = '{}';
		""".format(username, password)
		cursor.execute(login_query)
		login = cursor.fetchall()
		if login:
			print
			session_login(username)
			return redirect('/')
		else:
			return render_template('login.html', login=logged_in(), error='Invalid login.')
	else:
		return render_template('login.html')

@app.route('/logout')
def logout():
	session_logout()
	return redirect('/')

def get_course(course_id):
	cursor = connection.cursor()
	course_query = """
		SELECT c.id, c.name, c.term, c.year, c.location, c.weekday, c.start_time, c.end_time, t.name, t.login
		FROM course c
		JOIN teacher t ON c.teacher_id = t.id
	"""
	if course_id:
		course_query += "\nWHERE c.id = {}".format(course_id)
	course_query += ";"
	cursor.execute(course_query)
	return cursor.fetchall()

def parse_course(course):
	print str(course)
	parsed_course = {
		'course_id': course[0],
		'name': course[1],
		'term': course[2],
		'year': course[3],
		'location': course[4],
		'weekday': course[5].replace(",", ", "),
		'start_time': str(course[6])[:5],
		'end_time': str(course[7])[:5],
		'teacher': course[8],
		'teacher_email': course[9] + "@schola.com"
	}
	return parsed_course

@app.route('/courses')
def courses_handler():
	courses = []
	for course in get_course(None):
		courses.append(parse_course(course))
	return render_template('courses.html', login=logged_in(), courses=courses)

@app.route('/courses/<course_id>')
def course_handler(course_id):
	course = get_course(course_id)
	if course:
		course = parse_course(course[0])
		office_hours = get_office_hours(course['course_id'], None)
		parsed_office_hours = []
		for office_hour in office_hours:
			parsed_office_hours.append(parse_office_hours(office_hour))
		return render_template('course.html', login=logged_in(), course=course, office_hours=parsed_office_hours)
	else:
		return redirect('/404')

def get_office_hours(course_id, tutor_id):
	cursor = connection.cursor()
	office_hours_query = """
		SELECT t.id, t.name, t.login, o.weekday, o.id, o.start_time, o.end_time, o.location, c.id, c.name
		FROM tutor t
		JOIN office_hours o ON o.tutor_id = t.id
		JOIN course c ON c.id = o.course_id
	"""
	if course_id:
		office_hours_query += "\nWHERE c.id = {}".format(course_id)
	if tutor_id:
		office_hours_query += "\nWHERE t.id = {}".format(tutor_id)
	office_hours_query += ";"
	cursor.execute(office_hours_query)
	return cursor.fetchall()

def parse_office_hours(office_hours):
	tutor_email = None
	if office_hours[2]:
		tutor_email = office_hours[2] + "@schola.com"
	parsed_office_hours = {
		'tutor_id': office_hours[0],
		'tutor': office_hours[1],
		'tutor_username': office_hours[2],
		'tutor_email': tutor_email,
		'weekday': office_hours[3],
		'office_hours_id': office_hours[4],
		'start_time': str(office_hours[5])[:5],
		'end_time': str(office_hours[6])[:5],
		'location': office_hours[7],
		'course_id': office_hours[8],
		'course': office_hours[9],
	}
	return parsed_office_hours

@app.route('/tutors/<tutor_id>/office-hours',  methods=['GET', 'POST'])
def office_hours_handler(tutor_id):
	if request.method == 'POST' and logged_in()['tutor'] and logged_in()['tutor'] == int(tutor_id):
		cursor = connection.cursor()
		office_hours = {}
		for field in ('location', 'weekday', 'start', 'end', 'course'):
			office_hours[field] = request.form.get(field)
		new_office_hours_query = """
			CALL add_office_hours('{}', '{}', '{}', '{}', {}, {})
		""".format(office_hours['location'], office_hours['weekday'], office_hours['start'],  office_hours['end'], tutor_id, office_hours['course'])
		cursor.execute(new_office_hours_query)
		return redirect('/tutors/' + tutor_id + '/office-hours')
	else:
		cursor = connection.cursor()
		tutor_exists_query = """
			SELECT t.name, t.login
			FROM tutor t
			WHERE t.id = '{}';
		""".format(tutor_id)
		cursor.execute(tutor_exists_query)
		tutor_exists = cursor.fetchall()
		if tutor_exists:
			tutor_name = tutor_exists[0][0]
			tutor_email = tutor_exists[0][1] + "@schola.com"
			office_hours = get_office_hours(None, tutor_id)
			parsed_office_hours = []
			for office_hour in office_hours:
				parsed_office_hours.append(parse_office_hours(office_hour))
			return render_template('office-hours.html', login=logged_in(), tutor=tutor_name, tutor_email=tutor_email, office_hours=parsed_office_hours)
		else:
			return redirect('/404')

@app.route('/tutors/<tutor_id>/office-hours/new')
def new_office_hours_handler(tutor_id):
	if logged_in()['tutor'] and logged_in()['tutor'] == int(tutor_id):
		cursor = connection.cursor()
		course_query = """
			SELECT name, id
			FROM course
		"""
		cursor.execute(course_query)
		courses = []
		for (name, course_id) in cursor:
			course = {
				'name': name,
				'course_id': course_id
			}
			courses.append(course)
		return render_template('new-office-hours.html', login=logged_in(), courses=courses)
	else:
		return redirect('/tutors/' + tutor_id + '/office-hours')

@app.route('/tutors/<tutor_id>/office-hours/<office_hours_id>/delete', methods=["POST"])
def delete_office_hours_handler(tutor_id, office_hours_id):
	cursor = connection.cursor()
	tutor_query = """
		SELECT t.id
		FROM tutor t
		WHERE t.id = '{}';
	""".format(tutor_id)
	cursor.execute(tutor_query)
	tutor_exists = cursor.fetchall()
	if tutor_exists:
		if logged_in()['tutor'] and logged_in()['tutor'] == int(tutor_id):
			delete_office_hours_query = """
				CALL delete_office_hours({})
			""".format(office_hours_id)
			cursor.execute(delete_office_hours_query)
	return redirect('/tutors/' + tutor_id + '/office-hours')

@app.route('/tutors/<tutor_id>/office-hours/<office_hours_id>/update')
def update_office_hours_handler_form(tutor_id, office_hours_id):
	cursor = connection.cursor()
	course_query = """
		SELECT name, id
		FROM course
	"""
	cursor.execute(course_query)
	courses = []
	for (name, course_id) in cursor:
		course = {
			'name': name,
			'course_id': course_id
		}
		courses.append(course)
	return render_template('update-office-hours.html', login=logged_in(), courses=courses, office_hours_id=office_hours_id)

@app.route('/tutors/<tutor_id>/office-hours/<office_hours_id>', methods=["POST"])
def update_office_hours_handler(tutor_id, office_hours_id):
	cursor = connection.cursor()
	office_hours = {}
	for field in ('location', 'weekday', 'start', 'end', 'course'):
		office_hours[field] = request.form.get(field)
	update_office_hours_query = """
		CALL update_office_hours({}, '{}', '{}', '{}', '{}', {}, {})
	""".format(office_hours_id, office_hours['location'], office_hours['weekday'], office_hours['start'],  office_hours['end'], tutor_id, office_hours['course'])
	print update_office_hours_query
	cursor.execute(update_office_hours_query)
	return redirect('/tutors/' + tutor_id + '/office-hours')

@app.route('/tutors', methods=['GET', 'POST'])
def tutors_handler():
	if logged_in()['teacher']:
		cursor = connection.cursor()
		if request.method == 'POST':
			tutor = {}
			for field in ('name', 'username', 'password'):
				tutor[field] = request.form.get(field)
			add_tutor_query = """
				CALL add_tutor('{}', '{}', '{}');
			""".format(tutor['name'], tutor['username'], tutor['password'])
			print add_tutor_query
			cursor.execute(add_tutor_query)
		tutor_query = """
			SELECT *
			FROM tutor
		"""
		cursor.execute(tutor_query)
		tutors = []
		for (tutor_id, name, login) in cursor.fetchall():
			tutor = {'id': tutor_id, 'name': name, 'username': login, 'email': login + "@schola.com"}
			tutors.append(tutor)
		return render_template('tutors.html', login=logged_in(), tutors=tutors)
	return redirect('/')

@app.route('/tutors/new')
def new_tutor_handler():
	if logged_in()['teacher']:
		return render_template('new-tutor.html', login=logged_in())
	return redirect('/')

@app.route('/tutors/<tutor_id>/delete', methods=['POST'])
def delete_tutor_handler(tutor_id):
	if logged_in()['teacher']:
		cursor = connection.cursor()
		delete_tutor_query = """
			CALL delete_tutor({});
		""".format(tutor_id)
		cursor.execute(delete_tutor_query)
		return redirect('/tutors')
	return redirect('/')

@app.errorhandler(404)
def missing_error(error):
	return render_template('404.html'), 500

@app.errorhandler(500)
def crash_error(error):
	return render_template('500.html'), 500

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port, debug=False)
