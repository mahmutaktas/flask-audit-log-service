import unittest
from app import app
from models import db
from event_manager.models import EventType, EventTypeField
from tests.helpers import database_helpers
from tests.helpers.constants import ACCESS_TOKEN
from tests import initial_data
from sqlalchemy import desc
import json
import copy
from enums.FieldTypeEnums import FieldType


class EventTypeTestCase(unittest.TestCase):

    def setUp(self):

        with app.app_context():
            db.init_app(app)
            db.create_all()
            db.session.begin_nested()
            db.session.commit()
            database_helpers.populate_db(db)

    def tearDown(self):

        with app.app_context():
            db.init_app(app)
            db.drop_all()
            db.session.commit()

    def test_create_event_type_success(self):

        tester = app.test_client(self)
        response = tester.post('/event/type/create', json=initial_data.EVENT_TYPE_DATA,
                               headers={"access-token": ACCESS_TOKEN})
        self.assertEqual(response.status_code, 200, msg="Does not equal 200")

        with app.app_context():

            event_type = EventType.query.order_by(desc(EventType.id)).first()

        self.assertEqual(
            event_type.name, initial_data.EVENT_TYPE_DATA["name"], msg="Names not match")
        self.assertEqual(
            event_type.service_name, initial_data.EVENT_TYPE_DATA["service_name"], msg="Service names not match")

    def test_create_event_type_fail(self):
        event_type_data = copy.deepcopy(initial_data.EVENT_TYPE_DATA)
        event_type_data["name"] = "register"
        event_type_data["service_name"] = "user-profile"

        tester = app.test_client(self)
        response = tester.post('/event/type/create', json=event_type_data,
                               headers={"access-token": ACCESS_TOKEN})
        self.assertEqual(response.status_code, 400, msg="Does not equal 400")

    def test_update_event_type_success(self):
        event_type_data = copy.deepcopy(initial_data.EVENT_TYPE_DATA)
        event_type_data["name"] = "add-cart-v2"

        tester = app.test_client(self)
        response = tester.post('/event/type/update/1', json=event_type_data,
                               headers={"access-token": ACCESS_TOKEN})
        self.assertEqual(response.status_code, 200, msg="Does not equal 200")

        with app.app_context():

            event_type = EventType.query.filter_by(id=1).first()

        self.assertEqual(
            event_type.name, "add-cart-v2", msg="Names not match")
        self.assertEqual(
            event_type.service_name, initial_data.EVENT_TYPE_DATA["service_name"], msg="Names not match")

    def test_update_event_type_fail(self):

        tester = app.test_client(self)
        response = tester.post('/event/type/update/2', json=initial_data.EVENT_TYPE_DATA,
                               headers={"access-token": ACCESS_TOKEN})
        self.assertEqual(response.status_code, 404, msg="Does not equal 404")


class EventTypeFieldTestCase(unittest.TestCase):

    def setUp(self):

        with app.app_context():
            db.init_app(app)
            db.create_all()
            db.session.begin_nested()
            db.session.commit()
            database_helpers.populate_db(db)

    def tearDown(self):

        with app.app_context():
            db.init_app(app)
            db.drop_all()
            db.session.commit()

    def test_create_event_type_success(self):

        tester = app.test_client(self)
        response = tester.post('/event/type-field/create', json=initial_data.EVENT_TYPE_FIELD_DATA,
                               headers={"access-token": ACCESS_TOKEN})
        self.assertEqual(response.status_code, 200, msg="Does not equal 200")

        with app.app_context():

            event_type_field = EventTypeField.query.order_by(desc(EventTypeField.created_date)).first()

        self.assertEqual(
            event_type_field.field_name,
            initial_data.EVENT_TYPE_FIELD_DATA["field_name"],
            msg="Field names not match")
        self.assertEqual(
            event_type_field.field_type,
            initial_data.EVENT_TYPE_FIELD_DATA["field_type"],
            msg="Field types not match")

    def test_create_event_type_field_fail(self):
        event_type_field_data = copy.deepcopy(initial_data.EVENT_TYPE_FIELD_DATA)
        event_type_field_data["field_name"] = "username"
        event_type_field_data["field_type"] = "String"

        tester = app.test_client(self)
        response = tester.post('/event/type-field/create', json=event_type_field_data,
                               headers={"access-token": ACCESS_TOKEN})
        self.assertEqual(response.status_code, 400, msg="Does not equal 400")

    def test_update_event_type_field_success(self):
        event_type_field_data = copy.deepcopy(initial_data.EVENT_TYPE_FIELD_DATA)
        event_type_field_data["field_name"] = "username"
        event_type_field_data["field_type"] = "DateTime"

        tester = app.test_client(self)
        response = tester.post('/event/type-field/update', json=event_type_field_data,
                               headers={"access-token": ACCESS_TOKEN})
        self.assertEqual(response.status_code, 200, msg="Does not equal 200")

        with app.app_context():

            event_type_field = EventTypeField.query.order_by(desc(EventTypeField.updated_date)).first()

        self.assertEqual(
            event_type_field.field_type,
            event_type_field_data["field_type"],
            msg="Field types not match")

    def test_update_event_type_field_fail(self):
        event_type_field_data = copy.deepcopy(initial_data.EVENT_TYPE_FIELD_DATA)
        event_type_field_data["field_name"] = "username2"

        tester = app.test_client(self)
        response = tester.post('/event/type-field/update', json=event_type_field_data,
                               headers={"access-token": ACCESS_TOKEN})
        self.assertEqual(response.status_code, 404, msg="Does not equal 404")

    def test_get_event_type_fields_by_event_type_id_success(self):

        tester = app.test_client(self)
        response = tester.get('/event/type-field/by-event-type/1', headers={"access-token": ACCESS_TOKEN})
        self.assertEqual(response.status_code, 200, msg="Does not equal 200")

        with app.app_context():

            event_type_fields = EventTypeField.query.filter_by(event_type_id=1).all()

        self.assertEqual(
            len(event_type_fields),
            len(json.loads(response.data.decode('utf-8'))["data"]),
            msg="Event type fields length not match")

    def test_get_event_type_fields_by_event_type_id_fail(self):

        tester = app.test_client(self)
        response = tester.get('/event/type-field/by-event-type/2', headers={"access-token": ACCESS_TOKEN})
        self.assertEqual(response.status_code, 404, msg="Does not equal 404")

    def test_get_field_types_success(self):
        field_types = [member.value for member in FieldType]

        tester = app.test_client(self)
        response = tester.get('/event/type-field/field-types', headers={"access-token": ACCESS_TOKEN})
        self.assertEqual(response.status_code, 200, msg="Does not equal 200")
        self.assertEqual(len(json.loads(response.data.decode('utf-8'))
                         ["data"]), len(field_types), msg="Field types length not match")


if __name__ == '__main__':
    unittest.main()
