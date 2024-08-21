import unittest

from .pyigdl import IGDownloader

class Test(unittest.TestCase):
    def test_execution(self):
        url = "https://www.instagram.com/reel/C-0CTl6o7SO"
        responseSize = len(IGDownloader(url))
        self.assertEqual(responseSize, 1)