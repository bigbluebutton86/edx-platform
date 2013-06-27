from django.test import TestCase
from models import TrackingLog


class TrackingTest(TestCase):
    requests = [
        {"event": "my_event", "event_type": "my_event_type", "page": "my_page"},
        {"event": "{'json': 'object'}", "event_type": unichr(512), "page": "my_page"}
    ]

    def test_post_answers_to_log(self, requests=requests):
        """
        Checks that student answer requests submitted to track.views via POST
        are correctly logged in the TrackingLog db table
        """
        for request_params in requests:
            response = self.client.post("/event", request_params)
            self.assertEqual(response.status_code, 200)
            tracking_logs = TrackingLog.objects.order_by('-dtcreated')
            log = tracking_logs[0]
            self.assertEqual(log.event, request_params["event"])
            self.assertEqual(log.event_type, request_params["event_type"])
            self.assertEqual(log.page, request_params["page"])

    def test_get_answers_to_log(self, requests=requests):
        """
        Checks that student answer requests submitted to track.views via GET
        are correctly logged in the TrackingLog db table
        """
        for request_params in requests:
            response = self.client.get("/event", request_params)
            self.assertEqual(response.status_code, 200)
            tracking_logs = TrackingLog.objects.order_by('-dtcreated')
            log = tracking_logs[0]
            self.assertEqual(log.event, request_params["event"])
            self.assertEqual(log.event_type, request_params["event_type"])
            self.assertEqual(log.page, request_params["page"])
