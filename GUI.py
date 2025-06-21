import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk


def apply_css():

    screen = Gdk.Screen.get_default()
    provider = Gtk.CssProvider()
    provider.load_from_path("gui_styling.css")
    Gtk.StyleContext.add_provider_for_screen(
        screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


class TeamsWindow:
    def __init__(self, filename):

        # Load the Glade file to construct the GUI
        self.builder = Gtk.Builder()
        self.builder.add_from_file(filename)

        # Retrieve the main window from Glade and set up the close event
        self.window = self.builder.get_object("main_window")
        self.window.connect("destroy", Gtk.main_quit)

        self.teams = self.builder.get_object("teams")
        self.fields = self.builder.get_object("fields")

        self.teams_button = self.builder.get_object("teams_button")
        self.fields_button = self.builder.get_object("fields_button")

        # Event listener
        self.teams_button.connect("clicked", self.on_button_clicked)
        self.fields_button.connect("clicked", self.on_button_clicked)

    def post_init(self):
        self.teams.hide()
        self.fields.hide()

    # Events
    def on_button_clicked(self, button):
        id = Gtk.Buildable.get_name(button)
        self.teams.show()
        self.fields.show()

        if id == "teams_button":
            self.fields.hide()
        else:
            self.teams.hide()

    def run(self):
        self.window.show_all()
        self.post_init()
        Gtk.main()


if __name__ == "__main__":
    apply_css()  # Path to your CSS file
    app = TeamsWindow("GUI.glade")
    app.run()
