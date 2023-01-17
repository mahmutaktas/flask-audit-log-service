import unittest
from unittest.mock import patch
from app import app
from models import db
from tests.helpers import database_helpers
from tests.helpers.constants import ACCESS_TOKEN
from tests import initial_data
from sqlalchemy import desc
import json
import copy


class EventLogTestCase(unittest.TestCase):

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

    @patch('event_log.services.event_log_services.add_event_log')
    def test_add_event_log_success(self, mock_helper):
        mock_helper.return_value = {"success": True}

        tester = app.test_client(self)
        response = tester.post(
            '/event/log/add',
            json=initial_data.EVENT_LOG_DATA,
            headers={"access-token": ACCESS_TOKEN})

        self.assertEqual(response.status_code, 200, msg="Does not equal 200")

    @patch('event_log.services.event_log_services.add_event_log')
    def test_add_event_log_fail(self, mock_helper):
        mock_helper.return_value = {"success": False}, 404
        event_log_data = copy.deepcopy(initial_data.EVENT_LOG_DATA)
        event_log_data["event_type"]["name"] = "register-v2"

        tester = app.test_client(self)
        response = tester.post(
            '/event/log/add',
            json=event_log_data,
            headers={"access-token": ACCESS_TOKEN})

        self.assertEqual(response.status_code, 404, msg="Does not equal 404")

    @patch('event_log.services.event_log_services.add_bulk_event_log_by_event_type')
    def test_add_bulk_event_log_by_event_type_success(self, mock_helper):
        mock_helper.return_value = {"success": True}

        tester = app.test_client(self)
        response = tester.post(
            '/event/log/add-bulk',
            json=initial_data.BULK_EVENT_LOG_DATA,
            headers={"access-token": ACCESS_TOKEN})

        self.assertEqual(response.status_code, 200, msg="Does not equal 200")

    @patch('event_log.services.event_log_services.add_bulk_event_log_by_event_type')
    def test_add_bulk_event_log_by_event_type_fail(self, mock_helper):
        mock_helper.return_value = {"success": False}, 404
        bulk_event_log_data = copy.deepcopy(initial_data.BULK_EVENT_LOG_DATA)
        bulk_event_log_data["event_type"]["name"] = "register-v2"

        tester = app.test_client(self)
        response = tester.post(
            '/event/log/add-bulk',
            json=bulk_event_log_data,
            headers={"access-token": ACCESS_TOKEN})

        self.assertEqual(response.status_code, 404, msg="Does not equal 404")

    @patch('event_log.services.event_log_services.get_event_log_by_id')
    def test_get_event_log_by_id_success(self, mock_helper):

        mock_helper.return_value = {"count": 1, "data": []}

        tester = app.test_client(self)
        response = tester.get('/event/log/asdfg', headers={"access-token": ACCESS_TOKEN})

        self.assertEqual(response.status_code, 200, msg="Does not equal 200")
        self.assertEqual(response.json["count"], 1, msg="Does not equal 1")

    @patch('event_log.services.event_log_services.get_event_logs_by_query')
    def test_get_event_logs_by_query_success(self, mock_helper):

        mock_helper.return_value = {"count": 2, "data": []}

        tester = app.test_client(self)
        response = tester.post(
            '/event/log/query',
            json=initial_data.EVENT_LOG_QUERY,
            headers={
                "access-token": ACCESS_TOKEN})

        self.assertEqual(response.status_code, 200, msg="Does not equal 200")
        self.assertEqual(response.json["count"], 2, msg="Does not equal 2")
