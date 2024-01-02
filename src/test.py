import unittest

from pyigdl import IGDownloader

class Test(unittest.TestCase):
    def test_execution(self):
        url = "https://www.instagram.com/p/C1KCbMyKw3R/"
        responseSize = len(IGDownloader(url))
        self.assertEqual(responseSize, 1)