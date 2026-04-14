from collective.sidebar.browser.sidebar import SidebarViewlet
from collective.sidebar.testing import COLLECTIVE_SIDEBAR_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import SITE_OWNER_NAME

import unittest


class TestSidebarFunctional(unittest.TestCase):
    layer = COLLECTIVE_SIDEBAR_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        login(self.portal, SITE_OWNER_NAME)
        self.nav_data_view = api.content.get_view(
            name="navData",
            context=self.portal,
            request=self.request,
        )
        self.viewlet = self.nav_data_view.render_viewlet

    def test_profile_section(self):
        self.viewlet(context=self.portal, request=self.request)
        self.assertIn(
            '<span>admin</span>',
            self.viewlet(context=self.portal, request=self.request),
        )
        # Login with user that has fullname property set
        logout()
        login(self.portal, "mmustermann")
        self.assertIn(
            '<span>mmustermann</span>',
            self.viewlet(context=self.portal, request=self.request),
        )

    def test_link_section(self):
        self.assertIn(
            '<div class="sidebar-section pb-3" id="section-links" >',
            self.viewlet(context=self.portal, request=self.request),
        )
        # Login with user that has fullname property set
        ac = self.portal.portal_actions.sidebar_links
        ac["home"].visible = False
        ac["login"].visible = False
        ac["logout"].visible = False
        self.assertNotIn(
            '<div class="sidebar-section pb-3" id="section-links" >',
            self.viewlet(context=self.portal, request=self.request),
        )
        logout()

    def test_back_button(self):
        # Go to portal_root -> no back button
        self.assertNotIn(
            '<a class="link-back link-folder"',
            self.viewlet(context=self.portal, request=self.request),
        )

        # Go to empty folder -> back button
        demo = api.content.create(
            type="Folder",
            container=self.portal,
            id="demo",
            title="Demo",
            description="Test",
        )
        # MR is up to fix this
        self.assertIn(
            '<a class="nav-link link-back link-folder" href="http://nohost/plone"',
            self.viewlet(context=demo, request=self.request),
        )

        # Go to filled folder -> back button
        link = api.content.create(
            type="Link",
            container=demo,
            id="test",
            title="Test",
            remoteUrl="${portal_url}/test_rendering",
        )
        self.assertIn(
            '<a class="nav-link link-back link-folder" href="http://nohost/plone"',
            self.viewlet(context=demo, request=self.request),
        )

        # Go to item in folder -> back button
        self.assertIn(
            '<a class="nav-link link-back link-folder" href="http://nohost/plone/demo"',
            self.viewlet(context=link, request=self.request),
        )

        # Go to default page on front page -> no back button
        page = api.content.create(
            type="Document",
            container=self.portal,
            id="test-page",
            title="Test Page",
        )
        self.portal.setDefaultPage("test-page")
        self.assertNotIn(
            '<a class="nav-link link-back link-folder"',
            self.viewlet(context=page, request=self.request),
        )

        # Go to default page on folder -> back button
        page2 = api.content.create(
            type="Document",
            container=demo,
            id="test-page2",
            title="Test Page2",
        )
        demo.setDefaultPage("test-page2")
        self.assertIn(
            '<a class="nav-link link-back link-folder" href="http://nohost/plone" >',
            self.viewlet(context=page2, request=self.request),
        )

    def test_content_can_be_added(self):
        demo = api.content.create(
            type="Folder",
            container=self.portal,
            id="demo",
            title="Demo",
            description="Test",
        )
        self.portal.setDefaultPage("demo")
        self.assertIn(
            '<a class="nav-link" href="http://nohost/plone/demo/@@folder_factories" >',
            self.viewlet(context=demo, request=self.request),
        )

    def test_check_item(self):
        # Normal folder -> folder should be shown
        # Normal item -> parent should be shown
        demo = api.content.create(
            type="Folder",
            container=self.portal,
            id="demo",
            title="Demo",
            description="Test",
        )
        self.assertIn(
            'Demo',
            self.viewlet(context=self.portal, request=self.request),
        )
        pagey = api.content.create(
            type="Document",
            container=demo,
            id="pagey",
            title="Pagey",
        )
        self.assertIn(
            'Pagey',
            self.viewlet(context=demo, request=self.request),
        )
        self.assertIn(
            'Pagey',
            self.viewlet(context=pagey, request=self.request),
        )

        # Exclude item from nav -> should not be shown
        pagey.exclude_from_nav = True
        pagey.reindexObject()
        self.assertNotIn(
            'Pagey',
            self.viewlet(context=demo, request=self.request),
        )

        # default-page -> should not be shown?
        pagey.exclude_from_nav = False
        pagey.reindexObject()
        demo.setDefaultPage("pagey")
        self.assertNotIn(
            'Pagey',
            self.viewlet(context=demo, request=self.request),
        )

    def test_root_nav(self):
        api.portal.set_registry_record(
            name="collective.sidebar.root_nav",
            value=True,
        )
        api.content.create(
            type="Folder",
            container=self.portal,
            id="testi",
            title="Testi",
            description="Testi im Root Level",
        )
        demo = api.content.create(
            type="Folder",
            container=self.portal,
            id="demo",
            title="Demo",
            description="Test",
        )
        pagey = api.content.create(
            type="Document",
            container=demo,
            id="pagey",
            title="Pagey",
        )
        self.assertIn(
            'Testi',
            self.viewlet(context=self.portal, request=self.request),
        )
        self.assertIn(
            'Demo',
            self.viewlet(context=self.portal, request=self.request),
        )
        self.assertNotIn(
            'Pagey',
            self.viewlet(context=self.portal, request=self.request),
        )
        self.assertIn(
            'Testi',
            self.viewlet(context=demo, request=self.request),
        )
        self.assertIn(
            'Demo',
            self.viewlet(context=demo, request=self.request),
        )
        self.assertNotIn(
            'Pagey',
            self.viewlet(context=demo, request=self.request),
        )
        self.assertIn(
            'Testi',
            self.viewlet(context=pagey, request=self.request),
        )
        self.assertIn(
            'Demo',
            self.viewlet(context=pagey, request=self.request),
        )
        self.assertNotIn(
            'Pagey',
            self.viewlet(context=pagey, request=self.request),
        )

    def test_get_items(self):
        # Create tree of folder1 -> item1+item2+folder2->item3
        folder1 = api.content.create(
            type="Folder",
            container=self.portal,
            id="folder1",
            title="Folder1",
            description="",
        )
        item1 = api.content.create(
            type="Document",
            container=folder1,
            id="item1",
            title="Item1",
            description="",
        )
        item2 = api.content.create(
            type="Document",
            container=folder1,
            id="item2",
            title="Item2",
            description="",
        )
        folder2 = api.content.create(
            type="Folder",
            container=folder1,
            id="folder2",
            title="Folder2",
            description="",
        )
        item3 = api.content.create(
            type="Document",
            container=folder2,
            id="item3",
            title="Item3",
            description="",
        )

        v_portal = self.viewlet(context=self.portal, request=self.request)
        v_folder1 = self.viewlet(context=folder1, request=self.request)
        v_item1 = self.viewlet(context=item1, request=self.request)
        v_item2 = self.viewlet(context=item2, request=self.request)
        v_folder2 = self.viewlet(context=folder2, request=self.request)
        v_item3 = self.viewlet(context=item3, request=self.request)

        self.assertIn('Folder1', v_portal)
        self.assertNotIn('Folder2', v_portal)
        self.assertNotIn('Item1', v_portal)
        self.assertNotIn('Item2', v_portal)
        self.assertNotIn('Item3', v_portal)

        self.assertIn('Folder2', v_folder1)
        self.assertIn('Item1', v_folder1)
        self.assertIn('Item2', v_folder1)
        self.assertNotIn('Item3', v_folder1)

        self.assertNotIn('Folder1', v_item1)
        self.assertIn('Folder2', v_item1)
        self.assertIn('Item1', v_item1)
        self.assertIn('Item2', v_item1)
        self.assertNotIn('Item3', v_item1)

        self.assertNotIn('Folder1', v_item2)
        self.assertIn('Folder2', v_item2)
        self.assertIn('Item1', v_item2)
        self.assertIn('Item2', v_item2)
        self.assertNotIn('Item3', v_item2)

        self.assertNotIn('Folder1', v_folder2)
        self.assertNotIn('Item1', v_folder2)
        self.assertNotIn('Item2', v_folder2)
        self.assertIn('Item3', v_folder2)

        self.assertNotIn('Folder1', v_item3)
        self.assertNotIn('Folder2', v_item3)
        self.assertNotIn('Item1', v_item3)
        self.assertNotIn('Item2', v_item3)
        self.assertIn('Item3', v_item3)

    def test_workflows(self):
        item1 = api.content.create(
            type="Document",
            container=self.portal,
            id="item1",
            title="Item1",
            description="",
        )
        self._check_in_private_state(item1)
        api.content.transition(obj=self.portal["item1"], transition="publish")
        self._check_in_published_state(item1)
        api.content.transition(obj=item1, transition="retract")
        api.content.transition(obj=self.portal["item1"], transition="submit")
        self._check_in_pending_state(item1)
        api.content.transition(obj=item1, transition="retract")
        self._check_in_private_state(item1)
        api.content.transition(obj=item1, transition="submit")
        api.content.transition(obj=item1, transition="publish")
        api.content.transition(obj=item1, transition="reject")
        self._check_in_private_state(item1)
        api.content.transition(obj=item1, transition="publish")
        self._check_in_published_state(item1)

    def _check_in_published_state(self, item1):
        self.assertEqual(api.content.get_state(item1), "published")
        v = self.viewlet(context=item1, request=self.request)
        self.assertIn(
            '<span class="nav-link state-published">', v
        )
        self.assertNotIn(
            'href="http://nohost/plone/item1/content_status_modify?workflow_action=publish',
            v,
        )
        self.assertNotIn(
            'href="http://nohost/plone/item1/content_status_modify?workflow_action=submit',
            v,
        )
        self.assertIn(
            'href="http://nohost/plone/item1/content_status_modify?workflow_action=reject',
            v,
        )
        self.assertIn(
            'href="http://nohost/plone/item1/content_status_modify?workflow_action=retract',
            v,
        )
        self.assertIn('href="http://nohost/plone/item1/content_status_history', v)

    def _check_in_pending_state(self, item1):
        self.assertEqual(api.content.get_state(item1), "pending")
        v = self.viewlet(context=item1, request=self.request)
        self.assertIn(
            '<span class="nav-link state-pending">', v
        )
        self.assertIn(
            'href="http://nohost/plone/item1/content_status_modify?workflow_action=publish',
            v,
        )
        self.assertNotIn(
            'href="http://nohost/plone/item1/content_status_modify?workflow_action=submit',
            v,
        )
        self.assertIn(
            'href="http://nohost/plone/item1/content_status_modify?workflow_action=reject',
            v,
        )
        self.assertIn(
            'href="http://nohost/plone/item1/content_status_modify?workflow_action=retract',
            v,
        )
        self.assertIn('href="http://nohost/plone/item1/content_status_history', v)

    def _check_in_private_state(self, item1):
        self.assertEqual(api.content.get_state(item1), "private")
        v = self.viewlet(context=item1, request=self.request)
        self.assertIn(
            '<span class="nav-link state-private">', v
        )
        self.assertIn(
            'href="http://nohost/plone/item1/content_status_modify?workflow_action=publish',
            v,
        )
        self.assertIn(
            'href="http://nohost/plone/item1/content_status_modify?workflow_action=submit',
            v,
        )
        self.assertNotIn(
            'href="http://nohost/plone/item1/content_status_modify?workflow_action=reject',
            v,
        )
        self.assertNotIn(
            'href="http://nohost/plone/item1/content_status_modify?workflow_action=retract',
            v,
        )
        self.assertIn('href="http://nohost/plone/item1/content_status_history', v)

    def test_workflow_colors(self):
        view = SidebarViewlet(self.portal, self.request, None, None)
        self.assertEqual(view.has_workflow_state_color(), "with-state-color")

    def test_actions(self):
        demo = api.content.create(
            type="Folder",
            container=self.portal,
            id="demo",
            title="Demo",
            description="Test",
        )
        v = self.viewlet(context=demo, request=self.request)
        self.assertIn('href="http://nohost/plone/demo/object_cut?_authenticator=', v)
        # These actions are added in profiles/testing/actions.xml:
        self.assertIn("Test-Action", v)
        self.assertIn("No-Url-Action", v)
        self.assertIn("No-Icon-Action", v)

    def test_addable_items(self):
        # Test what can be added to normal folder
        demo = api.content.create(
            type="Folder",
            container=self.portal,
            id="demo",
            title="Demo",
            description="Test",
        )
        v = self.viewlet(context=demo, request=self.request)
        self.assertIn('href="http://nohost/plone/demo/++add++Image', v)
        self.assertIn('href="http://nohost/plone/demo/++add++File', v)
        self.assertIn('href="http://nohost/plone/demo/++add++Collection', v)
        self.assertIn('href="http://nohost/plone/demo/++add++News Item', v)
        self.assertIn('href="http://nohost/plone/demo/++add++Folder', v)
        self.assertIn('href="http://nohost/plone/demo/++add++Document', v)
        self.assertIn('href="http://nohost/plone/demo/++add++Event', v)

        # Restrict what can be added to a folder and test it
        folder_fti = self.portal.portal_types["Folder"]
        folder_fti.manage_changeProperties(
            filter_content_types=True, allowed_content_types=[]
        )
        v = self.viewlet(context=demo, request=self.request)
        self.assertNotIn('href="http://nohost/plone/demo/++add++Image', v)
        self.assertNotIn('href="http://nohost/plone/demo/++add++File', v)
        self.assertNotIn('href="http://nohost/plone/demo/++add++Collection', v)
        self.assertNotIn('href="http://nohost/plone/demo/++add++News Item', v)
        self.assertNotIn('href="http://nohost/plone/demo/++add++Folder', v)
        self.assertNotIn('href="http://nohost/plone/demo/++add++Document', v)
        self.assertNotIn('href="http://nohost/plone/demo/++add++Event', v)
        self.assertNotIn("sidebar-section-add", v)

    def test_default_page_and_view_link(self):
        demo = api.content.create(
            type="Folder",
            container=self.portal,
            id="demo",
            title="Demo",
            description="Test",
        )
        demo2 = api.content.create(
            type="Folder",
            container=self.portal,
            id="demo2",
            title="Demo2",
            description="Test",
        )
        self.portal.setDefaultPage("demo")
        v = self.viewlet(context=self.portal, request=self.request)
        self.assertIn(
            'class="nav-link pat-plone-modal" href="http://nohost/plone/select_default_view" >',
            v,
        )
        self.assertIn(
            'class="nav-link pat-plone-modal" href="http://nohost/plone/select_default_page" >',
            v,
        )
        v = self.viewlet(context=demo, request=self.request)
        self.assertIn(
            'class="nav-link pat-plone-modal" href="http://nohost/plone/select_default_view" >',
            v,
        )
        self.assertIn(
            'class="nav-link pat-plone-modal" href="http://nohost/plone/select_default_page" >',
            v,
        )
        v = self.viewlet(context=demo2, request=self.request)
        self.assertIn(
            'class="nav-link pat-plone-modal" href="http://nohost/plone/demo2/select_default_view" >',
            v,
        )
        self.assertIn(
            'class="nav-link pat-plone-modal" href="http://nohost/plone/demo2/select_default_page" >',
            v,
        )

    def test_sidebar_ajax(self):
        self.assertIsNone(self.nav_data_view(None))
        self.assertIsNotNone(self.nav_data_view(render=True))
