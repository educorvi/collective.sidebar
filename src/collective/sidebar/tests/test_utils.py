# -*- coding: utf-8 -*-

from collective.sidebar.testing import COLLECTIVE_SIDEBAR_INTEGRATION_TESTING
from plone import api

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
        self.assertEqual(crop("This should be:cropping", 20), "This should be...")  # noqa

    def test_get_icon(self):
        from collective.sidebar.utils import get_icon

        self.assertEqual(get_icon("_unknown_icon_"), "glyphicon glyphicon-menu-right")  # noqa
        self.assertEqual(get_icon("cut"), "glyphicon glyphicon-scissors")

        api.portal.set_registry_record(
            name="collective.sidebar.icon_font", value="Fontello"
        )  # noqa
        self.assertEqual(get_icon("_unknown_icon_"), "icon menu-right")
        self.assertEqual(get_icon("cut"), "icon cut")

        api.portal.set_registry_record(
            name="collective.sidebar.icon_font", value="Font Awesome"
        )  # noqa
        self.assertEqual(get_icon("_unknown_icon_"), "fas fa-angle-right")
        self.assertEqual(get_icon("cut"), "fas fa-cut")

        api.portal.set_registry_record(
            name="collective.sidebar.icon_font", value="Font Awesome Pro"
        )  # noqa
        self.assertEqual(get_icon("_unknown_icon_"), "far fa-angle-right")
        self.assertEqual(get_icon("cut"), "far fa-cut")

        api.portal.set_registry_record(
            name="collective.sidebar.icon_font", value="Font Awesome Light"
        )  # noqa
        self.assertEqual(get_icon("_unknown_icon_"), "fal fa-angle-right")
        self.assertEqual(get_icon("cut"), "fal fa-cut")

        api.portal.set_registry_record(
            name="collective.sidebar.icon_font", value="Font Awesome Duotone"
        )  # noqa
        self.assertEqual(get_icon("_unknown_icon_"), "fad fa-angle-right")
        self.assertEqual(get_icon("cut"), "fad fa-cut")
