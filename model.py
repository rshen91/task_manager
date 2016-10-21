"""Models and database functions for Task Manager project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import datetime


##############################################################################
class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)

    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)

    username = db.Column(db.String(64),
                         unique=True,
                         nullable=False)

    password = db.Column(db.String(200),
                         nullable=False)

    profile_img = db.Column(db.String(200),
                            nullable=True)

    email = db.Column(db.String(64),
                      unique=True,
                      nullable=False)

    time_zone = db.Column(db.String(25),
                          nullable=True)

    # Define relationship tasks table
    tasks = db.relationship("Task",
                            backref=db.backref("users"))

    # Define relationship goal table
    goal = db.relationship("Goal",
                           backref=db.backref("users"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s username=%s email=%s>" % (self.user_id,
                                                           self.username,
                                                           self.email)

    @classmethod
    def check_by_email(cls, email):
        """See if user email is already in system"""

        if cls.query.filter(cls.email == email).first() is not None:
            return True
        else:
            return False

    def check_by_userid(cls, user_id):
        """Search user table by user_id"""

        return cls.query.filter(cls.user_id == user_id).one()


class Goal(db.Model):
    """Goals for an individual user of website."""

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))

    description = db.Column(db.Text,
                            nullable=False)

    created_date = db.Column(db.DateTime,
                             default=datetime.datetime.now())

    active_goal = db.Column(db.Boolean,
                            nullable=False,
                            default=True)  # may not need this in case

    time_toachieve = db.Column(db.String(50),
                               nullable=False)  # expected response month ,day, year, quarter, 6months

    goalcat_name = db.Column(db.String(50),
                             nullable=False)  # as dropdown in main screen

    user = db.relationship("User", backref=db.backref("relationships"))

    def __repr__(self):

        return "<goal_id=%s description=%s timeperiod=%s>" % (self.goal_id, self.description, self.timeperiod)

    @classmethod
    def check_by_user_id(cls, user_id):
        """Checks goal table, to ensure goal isnt already there"""

        if cls.query.filter(cls.user_id == user_id).first() is None:
            return False
        else:
            return cls.query.filter(cls.user_id == user_id).all()


class Task(db.Model):
    """Tasks"""

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, nullable=False)                     # can have value from 1 to 10
    date_added = db.Column(db.Date, default=datetime.datetime.utcnow())
    open_close_status = db.Column(db.Integer)                            # will have value 1 or 0 ,1 default for open tasks, 0 for closed tasks
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    task_frequency = db.Column(db.String(50), nullable=False)            # daily, weekly,monthly
    taskcat_name = db.Column(db.String(50), nullable=False)              # task category as dropdown, request.form.get

    def __init__(self, task_name, due_date, priority, date_added, open_close_status, user_id):
        self.task_name = task_name
        self.due_date = due_date
        self.priority = priority
        self.date_added = date_added
        self.open_close_status = open_close_status
        self.user_id = user_id

    def __repr__(self):
        return '<name={}>'.format(self.task_name)

    def open_tasks():
        return db.session.query(Task).filter_by(open_close_status='1').order_by(Task.due_date.asc())

    def closed_tasks():
        return db.session.query(Task).filter_by(open_close_status='0').order_by(Task.due_date.asc())

    user = db.relationship('User', backref='user_tasks')


class Reminders(db.Model):
    """Reminders for the user"""

    __tablename__ = "reminders"

    reminder_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.goal_id'))
    text_reminder = db.Column(db.String(5), nullable=True)  # if we want to use twilio for texts and mailgun for emails
    email_reminder = db.Column(db.String(5), nullable=True)

    goal = db.relationship('Goal', backref='reminders')
    user = db.relationship('User', secondary='goals', backref='reminders')

    def __repr__(self):

        return "<reminder_id=%s goal_id=%>" % (self.reminder_id, self.goal_id)


class GoalCompletion(db.Model):
    """Tracks completion of a goal"""

    __tablename__ = "trackcompletion"

    completion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.goal_id'))

    marked_complete = db.Column(db.DateTime,
                                nullable=True,
                                default=datetime.datetime.now())
    user_notes = db.Column(db.Text,
                           nullable=True)  # if user wants to comment while completing a goal

    goal = db.relationship('Goal', backref='trackcompletion')
    user = db.relationship('User', secondary='goals', backref='trackcompletion')

    def __repr__(self):

        return "<completion_id=%s marked_complete=%s>" % (self.completion_id, self.marked_complete)


#####################################################################################################


#need association tables , need class to track completion
# class LinkGoalTask(db.Model):
# """Association Model to connect Goals and Categories"""


#class Calendar/info if any



#need to add to server.py as part of delete task-

# def delete_entry(task_id):
#     new_id = task_id
#     task = db.session.query(Task).filter_by(task_id=new_id)
#     if session['user_id'] == task.first().user_id :
#         task.delete()
#         db.session.commit()
#         flash('The task was deleted. Would you like to add a new one?')
#         return redirect(#FIXME #URLNAME)




############################################################################
# extra class if reqd later-

# class TaskCategory(db.Model):
#     """Task categories for the goals""" #this will be a static list


#     __tablename__ = "taskcategories"

#     taskcat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     taskcat_name = db.Column(db.String(50), nullable=False)


#     tasks = db.relationship('Task', backref='taskcategories')

#     def __repr__(self):

#         return "<taskcat_id=%s taskcat_name=%s>" % (self.taskcat_id, self.taskcat_name)

# class GoalCategory(db.Model):
#     """Goal categories for the user""" #this will be a static list

#     __tablename__ = "goalcategories"

#     goalcat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     goalcat_name= db.Column(db.String(50), nullable=False)

#     goals = db.relationship('Goal', backref='goalcategories')

#     def __repr__(self):

#         return "<goalcat_id=%s goalcat_name=%s>" % (self.goalcat_id, self.goalcat_name)




############################################################################
def init_app():

    from server import app

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app, db_uri='postgres:///task_manager'):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


def example_data():
    """Create sample data."""

    user_1 = User(user_id=1,
                  first_name='Minnie',
                  last_name='Mouse',
                  username='Minnie',
                  password='MouseGal',
                  profile_img='static/img/minnie.jpg',
                  email='minnie@mouse.purr',
                  time_zone='PST')

    user_2 = User(user_id=2,
                  first_name='Lady',
                  last_name='Flash',
                  username='LadyFlash',
                  password='PowerfulLady',
                  profile_img='static/img/ladyflash.jpg',
                  email='lady@flash.pow',
                  time_zone='PST')

    #Add all to the database
    db.session.add_all([user_1, user_2])
    #Commit changes
    db.session.commit()

if __name__ == "__main__":
    """This is useful for running this module interactively. This will leave me
    in a state of being able to work with the database directly."""

    from server import app

    # Need to add to db.create_all()

    connect_to_db(app, "postgresql:///task_manager")
    print "Connected to DB."
