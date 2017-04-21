"""Tests for API endpoints."""
import unittest
import json

# local imports
from app import app


class APIEndpointsTestCase(unittest.TestCase):
    """Test for API endpoints."""

    def setUp(self):
        """Test wide variables."""
        self.app = app.app_context()
        self.client = app.test_client()

    def test_fetch_all_bucketlists(self):
        """Test that endpoint fetches all bucketlists."""
        response = self.client.get("/v1/bucketlists/")
        self.assertEqual(response.status_code, 200)

    def test_fetch_single_bucketlist(self):
        """Test that endpoint fetches a single bucketlist."""
        response = self.client.get('/v1/bucketlists/1/')
        self.assertEqual(response.status_code, 200)

    def test_post_new_bucketlist(self):
        """Test endpoint saves new bucketlist."""
        new_bucketlist = {
            "name": "Crack Game theory."
        }
        response = self.client.post('/v1/bucketlists/', data=json.dumps(
            new_bucketlist))
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()