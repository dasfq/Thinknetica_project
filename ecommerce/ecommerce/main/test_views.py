from django.test import TestCase


class TestListViews(TestCase):

    def test_cars(self):
        response = self.client.get('/cars/')
        self.assertEqual(response.status_code, 200)

    def test_items(self):
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, 200)

    def test_service(self):
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)
