
from collective.sidebar import _
from collective.sidebar.controlpanel.config import PositionVocabulary
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class IControlPanel(Interface):
    enable_siteactions = schema.Bool(
        title=_(
            "controlpanel_sidebar_show_siteactions_title",
            default="Show Site Actions Section",
        ),
        description=_(
            "controlpanel_sidebar_show_siteactions_description",
            default=("Show Siteactions section."),
        ),
        required=False,
        default=True,
    )

    enable_sitelinks = schema.Bool(
        title=_(
            "controlpanel_sidebar_show_sitelinks_title",
            default="Show Site Links Section",
        ),
        description=_(
            "controlpanel_sidebar_show_sitelinks_description",
            default=("Show Sitelinks section."),
        ),
        required=False,
        default=True,
    )

    enable_navigation = schema.Bool(
        title=_(
            "controlpanel_sidebar_show_navigation_title",
            default="Show Navigation Section",
        ),
        description=_(
            "controlpanel_sidebar_show_navigation_description",
            default=("Show navigation section."),
        ),
        required=False,
        default=True,
    )

    root_nav = schema.Bool(
        title=_(
            "controlpanel_sidebar_show_root_nav_title",
            default="Root Level Navigation",
        ),
        description=_(
            "controlpanel_sidebar_show_root_nav_description",
            default=(
                "When enabled, the sidebar will display the root level navigation."
            ),
        ),
        required=False,
        default=False,
    )

    dynamic_navigation = schema.Bool(
        title=_(
            "controlpanel_sidebar_dynamic_navigation_title",
            default="Enable dynamic Navigation",
        ),
        description=_(
            "controlpanel_sidebar_dynamic_navigation_description",
            default=("Enable dynamic navigation inside sidebar."),
        ),
        required=False,
        default=True,
    )

    enable_actions = schema.Bool(
        title=_(
            "controlpanel_sidebar_show_actions_title",
            default="Show Actions Section",
        ),
        description=_(
            "controlpanel_sidebar_show_actions_description",
            default=(
                "Show actions section including object "
                "buttons for cut, copy, paste, etc."
            ),
        ),
        required=False,
        default=True,
    )

    enable_portlets = schema.Bool(
        title=_(
            "controlpanel_sidebar_show_portlets_title",
            default="Show Manage Portlets Section",
        ),
        description=_(
            "controlpanel_sidebar_show_portlets_description",
            default=("Show manage portlets link"),
        ),
        required=False,
        default=True,
    )

    enable_collapse = schema.Bool(
        title=_(
            "controlpanel_sidebar_enable_collapse_title",
            default="Collapsible Sections",
        ),
        description=_(
            "controlpanel_sidebar_enable_collapse_description",
            default=(
                "When enabled, the sidebar sections can be collapsed. "
                "This feature is only available when cookies are enabled."
            ),
        ),
        required=False,
        default=True,
    )

    sidebar_position = schema.Choice(
        title=_(
            "controlpanel_sidebar_sidebar_position_title",
            default="Sidebar Position",
        ),
        description=_(
            "controlpanel_sidebar_sidebar_position_description",
            default="Display the sidebar on the left or right.",
        ),
        vocabulary=PositionVocabulary,
        required=True,
        default="start",
    )

    mouse = schema.Bool(
        title=_(
            "controlpanel_mouse_title",
            default="Mouse activated",
        ),
        description=_(
            "controlpanel_mouse_description",
            default=("When enabled, the sidebar will be opened by mouse."),
        ),
        required=False,
        default=True,
    )

    mouse_area = schema.Int(
        title=_(
            "controlpanel_mouse_area_title",
            default="Mouse Activation Area",
        ),
        description=_(
            "controlpanel_mouse_area_description",
            default=("Enter the number of pixels to activate the sidebar."),
        ),
        required=False,
        default=30,
    )


class ControlPanelEditForm(RegistryEditForm):
    schema = IControlPanel
    schema_prefix = "collective.sidebar"
    label = _("collective_sidebar_title", default="Collective Sidebar")


ControlPanelView = layout.wrap_form(
    ControlPanelEditForm,
    ControlPanelFormWrapper,
)
