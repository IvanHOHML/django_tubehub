from django.test import TestCase

# Create your tests here.
from services import download
from song import forms
class SongTests(TestCase):
    def test_tubehub_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
    def test_download_invalid_url(self):
        form = forms.PlaylistForm({"url":"abc"})
        response = download.download(form)
        self.assertEqual(response['status_code'],404)
    def test_download_invalid_url(self):
        form = forms.PlaylistForm({"url":"abc"})
        response = download.download(form)
        self.assertEqual(response['status_code'],404)
