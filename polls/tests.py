from django.test import TestCase


class PollsView(TestCase):

    def test_route_to_polls(self):
        response = self.client.get('/polls/')
        self.assertEqual(response.status_code, 200)
