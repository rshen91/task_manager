"""Server file for Task Manager."""

#######################
#### Configuration ####
#######################

#Access local env variables
import os
# import quickstart

from jinja2 import StrictUndefined

# Flask: A class that we import. An instance of this class will be the
# WSGI application.

from flask import Flask, render_template, request, flash, redirect, session

#Use toolbar for debugging
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Goal, Task

from flask_bcrypt import Bcrypt

# Instantiates Flask and "__name__" informs Flask where to find files.
# Instantiates Flask. "__name__" is a special Python variable for the name of
# the current module. This is needed so that Flask knows where to look for
# templates, static files, and so on.
app = Flask(__name__, static_url_path='/static')

#Set a secret key to enable the flask session cookies and the debug toolbar
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "seKriTz")

# Prevents the need to restart server when HTML/CSS is changed.
app.jinja_env.auto_reload = True

# Raises an error when an undefined variable is used in Jinja2.
app.jinja_env.undefined = StrictUndefined

bcrypt = Bcrypt(app)


################ Login/out Registration #####################

@app.route("/register", methods=['POST'])
def register_form():
    """Register user."""

    # Grab user's inputted data.
    first = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    username = request.form.get('display_name')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirmation')

    # Make sure 'password' and 'password_confirm' match.
    if password != password_confirm:
        flash("The passwords do not match. Please type again.")
        return redirect("/")

    # Secure the users pw before storing in database.
    pw_hash = bcrypt.generate_password_hash(password)

    # Commit new user to database.
    user = User(first_name=first,
                last_name=last_name,
                email=email,
                username=username,
                password=pw_hash)

    db.session.add(user)
    db.session.commit()

    # Store new user info in session.
    user_id = db.session.query(User.id).filter_by(email=email).first()[0]
    session["user_id"] = user_id

    session["username"] = username
    session["user_email"] = email

    # Send confirmation msg and back to home page
    flash("Welcome, new user. Let's get things done!")
    return redirect("/landing")


@app.route('/')
def display_login():
    """Homepage. Login and registration displayed."""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_form():
    """Process login form."""

    # Grab the users input.
    email = request.form.get("email")
    password = bcrypt.generate_password_hash(request.form.get("password"))

    # Check that the user exists.
    uq = User.query
    user_object = uq.filter_by(email=email).first()

    if user_object and bcrypt.check_password_hash(password, user_object.password):
        flash("Hi again!")
        session["user_email"] = user_object.email
        session["user_id"] = user_object.user_id
        session["username"] = user_object.username

        return redirect("/landing")
    else:
        flash("Oops! Email / Password mismatch: Try again.")
        return redirect("/")


@app.route('/logout')
def logout_form():
    """Process logout form"""

    # Remove user from session.
    session.clear()
    flash("Logged out. Don't be gone for too long!")
    return render_template("logout.html")


###################### Core Routes ##########################


################ Render information on goals and tasks from Model #############
@app.route('/landing')
def landing():
    """Main page after login/registration."""

    username = session['username']

    return render_template("landing.html",
                           username=username)


@app.route('/goals')
def render_goals():
    """Queries DB to render the user's goals and takes them to goals.html"""

    if Goal.check_by_user_id(user_id) is False:
        flash("You have no goals currently! Would you like to add one?")
        return render_template('add_goal.html')
    else:

        user = User.check_by_user_id(user_id)
        goals = Goal.check_by_user_id(user_id)

    goals = db.session.query(Goal.active_goals).all()
    description = db.session.query(Goal.description).all()

    return render_template("goals.html",
                           goals=goals,
                           description=description)


@app.route('/tasks')
def render_tasks():
    """Queries DB for user's tasks and takes them to tasks.html"""

    user_id = session["user_id"]

    tasks = db.session.query(Task.task_name, Task.due_date).filter_by(user_id=user_id).all()

    return render_template("tasks.html",
                           tasks=tasks)


# @login_required
def make_new_task(task_name, due_date, priority, date_added, open_close_status, task_frequency):
    """Add a new task to the DB"""

    QUERY = """INSERT INTO Task (task_name, due_date, priority, date_added, open_close_status)
               VALUES (:task_name, :due_date, :priority, :date_added, :open_close_status)"""

    db_cursor = db.session.execute(QUERY, {'task_name': task_name,
                                           'due_date': due_date,
                                           'priority': priority,
                                           'date_added': date_added,
                                           'open_close_status': open_close_status})

    db.session.commit()

    print "Successfully added task: {}".format(task_name)


@app.route('/googlecalendar', methods=['GET'])
def google_map():
    return render_template("index-test.html")


@app.route('/testing')
def test_page():
    return render_template("testpage.html")


################### Helper Functions #######################

# Listening or requests
if __name__ == "__main__":

    #Set debug=True in order to invoke the DebugToolbarExtension
    app.debug = True

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # app.config['TRAP_HTTP_EXCEPTIONS'] = True
    # app.config['Testing'] = True
    #Use of debug toolbar
    DebugToolbarExtension(app)

    connect_to_db(app)

    #Create tables from models.py
    db.create_all(app=app)

    #Run app locally (full)
    #Points to port to use and turns on debugger
    app.run(port=5000, debug=True, host='0.0.0.0')

    #Run app via Heroku
    # PORT = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=PORT)
