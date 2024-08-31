import unittest

from pyigdl import IGDownloader

class Test(unittest.TestCase):
    def test_execution(self):
        url = "https://www.instagram.com/reel/C-0CTl6o7SO"
        responseSize = len(IGDownloader(url))
        self.assertEqual(responseSize, 1)
    
    def test_carousel(self):
        url = "https://www.instagram.com/p/C_B03_ry0aK/?"
        resp = IGDownloader(url)
        self.assertEqual(len(resp), 9)

    def test_single_photo_post(self):
        url = "https://www.instagram.com/p/C-5szP6xjoC"
        resp = IGDownloader(url)
        self.assertEqual(len(resp), 1)
