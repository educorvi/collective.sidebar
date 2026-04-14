from collective.sidebar.testing import COLLECTIVE_SIDEBAR_INTEGRATION_TESTING

import unittest


class TestSidebarUtilsFunctional(unittest.TestCase):
    layer = COLLECTIVE_SIDEBAR_INTEGRATION_TESTING

    def test_crop(self):
        from collective.sidebar.utils import crop

        self.assertEqual(crop("just text", 6), "just...")
        self.assertEqual(crop("just text", 100), "just text")
        self.assertEqual(crop(".sonderzeichen:,;", 15), "sonderzeichen...")
        self.assertEqual(crop(".sonderzeichen:,;", 18), ".sonderzeichen:,;")
        self.assertEqual(crop("12345678910", 5), "12345...")
        self.assertEqual(crop("This should be:cropping", 20), "This should be...")
