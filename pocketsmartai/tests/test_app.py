import unittest
from app import app

class PocketSmartTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)

    def test_home_recommendation(self):
        r = self.client.post("/generate-home", json={
            "budget": 50000, "room": "Living Room", "style": "Modern"
        })
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json["ok"])

if __name__ == "__main__":
    unittest.main()
