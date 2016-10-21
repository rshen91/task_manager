import unittest
from unittest import TestCase
from server import app
from model import connect_to_db, db, User, example_data


class FlaskTestRoutes(TestCase):
    """Flask tests before user is logged in."""

############### Testing Necessities ##############

    def setUp(self):
        """To do before every test."""

        #Get the Flask test client
        self.client = app.test_client()

        #Show Flask errors that happen during tests
        app.config['TESTING'] = True

################### Test Routes ##################

    def test_home_route(self):
        """Test route to homepage."""

        #Go to homepage
        result = self.client.get("/")

        #Does the page render
        self.assertIn('<h2>Please Sign In</h2>', result.data)

        #Does data make it to the DOM
        # self.assertIn('Connect!', result.data)


################# Test Database #################
class FlaskTestDatabase(TestCase):
    """Flask tests that use the test database"""

    def setUp(self):
        """To do before each test"""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database.
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data.
        db.create_all()

        example_data()

    def test_find_user_by_username(self):
        """Can we find a user in the database"""

        #Query the database for a user
        user = User.query.filter_by(username='Minnie').first()
        #What the result of query should be:
        self.assertEqual(user.time_zone, 'PST')

    def tearDown(self):
        """Things to do at end of every test"""

        # Close the session.
        db.session.close()

        # Drop the database.
        db.drop_all()

    def test_find_user_by_email(self):
        """Can we find a user in the database"""

        #Query the database for a user
        user = User.query.filter_by(email='lady@flash.pow').first()

        #Query results should be:
        self.assertEqual(user.username, 'LadyFlash')

    def test_process_login(self):
        """Is the login form processed correctly"""

        #Process login form
        result = self.client.post('/login',
                                  data={'email': 'lady@flash.pow', 'password': 'PowerfulLady'},
                                  follow_redirects=True)

        #Flash message should appear when user logs in
        self.assertIn('Welcome back', result.data)

    def test_process_login_incorrect_password(self):
        """Is login form processed correctly when user types wrong password"""

        #Process login form with incorrect password
        result = self.client.post('/',
                                  data={'email': 'minnie@mouse.purr', 'password': 'Mousey'},
                                  follow_redirects=True)
        #Should get ok status code from / route
        self.assertEqual(result.status_code, 200)
        #Flash message should appear when user types wrong password
        self.assertIn('Incorrect password', result.data)

    def test_process_login_user_does_not_exist(self):
        """Is login form processed correctly when user is not in database"""

        #Process login form when user does not exists
        result = self.client.post('/login',
                                  data={'email': 'lady@flash.po',
                                        'password': 'PowerfulLady'}, follow_redirects=True)
        #Should get ok status code from / route
        self.assertEqual(result.status_code, 200)
        #Flash message should appear when user is not in database
        self.assertIn('Please create an account', result.data)

    def test_process_registration(self):
        """Is the registration form processed correctly"""

        #Process registration form when user is new
        result = self.client.post('/register', data={'email': 'Test@tester.test',
                                                     'username': 'pswd',
                                                     'password': 99999,
                                                     'phone_number': '888-888-8888'},
                                  follow_redirects=True)
        #Should get ok status code from / route
        self.assertEqual(result.status_code, 200)
        #Flash message should appear when user is not in database
        self.assertIn('Welcome, new user. Wanna get things done?', result.data)

    def test_process_registration_email_already_in_database(self):
        """Is registration form processed correctly when email is already in database"""

        #Process registration form when user email is already in use
        result = self.client.post('/register', data={'email': 'Test@tester.test',
                                                     'username': 'pswd',
                                                     'password': 99999,
                                                     'phone_number': '888-888-8888'},
                                  follow_redirects=True)
        #Should get ok status code from / route
        self.assertEqual(result.status_code, 200)
        #Flash message should appear when user is not in database
        self.assertIn('That email is already taken',
                      result.data)

################# Test Login/out #################

class FlaskTestsLoggedIn(TestCase):
    """Flask test with user logged in to session"""

    def setUp(self):
        """Things to do before each test"""

        #Show Flask errors that happen during tests
        app.config['TESTING'] = True

        app.config['SECRET_KEY'] = 'seKriTz'

        #Get the Flask test client
        self.client = app.test_client()

        #Add user to the session
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_base_homepage(self):
        """Test that user is redirected to homepage if logged in"""

        #Go to the homepage, while logged in
        result = self.client.get('/', follow_redirects=True)
        #Should get ok status code from / route
        self.assertEqual(result.status_code, 200)
        #Should see title of page
        # self.assertIn('<h2>Home</h2>', result.data)

    def test_login_form(self):
        """Test that user if redirected to the homepage if logged in"""

        #Go to login form, while logged in
        result = self.client.get('/login', follow_redirects=True)
        #Should get ok status code from / route
        self.assertEqual(result.status_code, 200)
        #Should see title of page
        # self.assertIn('<h2>Login</h2>', result.data)

    def test_logout(self):
        """Is the user able to logout"""

        #Go to logout route
        result = self.client.get('/logout', follow_redirects=True)
        #Should get ok status code from / route
        self.assertEqual(result.status_code, 200)
        #Flash message should appear when user logs out
        # self.assertIn('Logged out. Don't be gone for too long!', result.data)


if __name__ == "__main__":
    unittest.main()
