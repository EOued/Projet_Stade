import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

class MyApp:
    def __init__(self):

        # Load the Glade file to construct the GUI

        self.builder = Gtk.Builder()
        self.builder.add_from_file("UI.glade")


        # Retrieve the main window from Glade and set up the close event

        self.window = self.builder.get_object("teams_window")
        self.window.connect("destroy", Gtk.main_quit)



        # Variable to toggle the background color

        self.color_toggle = False

    def run(self):
        self.window.show_all()
        Gtk.main()

if __name__ == "__main__":
    app = MyApp()
    app.run()

