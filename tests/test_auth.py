import unittest
from app import app
from models import db
from user.models import User
from tests.helpers import database_helpers
from tests.helpers.constants import ACCESS_TOKEN
from tests import initial_data
from sqlalchemy import desc
import copy


class AuthTestCase(unittest.TestCase):

    def setUp(self):

        with app.app_context():
            db.init_app(app)
            db.create_all()
            db.session.begin_nested()
            db.session.commit()
            database_helpers.populate_db(db)

    def tearDown(self):

        db.init_app(app)
        with app.app_context():
            db.drop_all()
            db.session.commit()

    def test_login_success(self):

        tester = app.test_client(self)
        response = tester.post('/auth/login', json={"email": "testuser@gmail.com", "password": "123456"})
        self.assertEqual(response.status_code, 200, msg="Does not equal 200")

    def test_login_fail(self):

        tester = app.test_client(self)
        response = tester.post('/auth/login', json={"email": "testuser@gmail.com", "password": "1234567"})
        self.assertEqual(response.status_code, 401, msg="Does not equal 400")

    def test_create_user_success(self):

        tester = app.test_client(self)
        response = tester.post('/auth/register', json=initial_data.USER_DATA,
                               headers={"access-token": ACCESS_TOKEN})
        self.assertEqual(response.status_code, 200, msg="Does not equal 200")

        with app.app_context():

            user = User.query.order_by(desc(User.id)).first()

        self.assertEqual(
            user.email, initial_data.USER_DATA["email"], msg="Emails not match")

    def test_create_user_fail(self):
        user_data = copy.deepcopy(initial_data.USER_DATA)
        user_data["email"] = "testuser@gmail.com"

        tester = app.test_client(self)
        response = tester.post('/auth/register', json=user_data,
                               headers={"access-token": ACCESS_TOKEN})
        self.assertEqual(response.status_code, 400, msg="Does not equal 400")


if __name__ == '__main__':
    unittest.main()
