import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk


class TeamsWindow:
    def __init__(self, filename):

        # Load the Glade file to construct the GUI
        self.builder = Gtk.Builder()
        self.builder.add_from_file(filename)

        # Retrieve the main window from Glade and set up the close event
        self.window = self.builder.get_object("teams_window")
        self.window.connect("destroy", Gtk.main_quit)

        # Objects

        self.teams_treeview_ls = self.builder.get_object("teams_liststore")

        # Entries
        self.name_entry = self.builder.get_object("name_entry")
        self.gameformat_entry = self.builder.get_object("gameformat_entry")
        self.gameformat_entry.set_active(0)
        self.time_entry = self.builder.get_object("time_entry")
        self.gametime_priority_entry = self.builder.get_object(
            "gametime_priority_entry"
        )
        self.gameformat_priority_entry = self.builder.get_object(
            "gameformat_priority_entry"
        )
        self.gameformat_priority_entry.set_active(0)

        self.team_add_button = self.builder.get_object("team_add_button")
        self.team_add_button.connect(
            "clicked",
            lambda widget: self.add_team(
                self.name_entry.get_text(),
                self.combo_text(self.gameformat_entry),
                int(self.time_entry.get_text()),
                int(self.gametime_priority_entry.get_text()),
                self.combo_text(self.gameformat_priority_entry)
            ),
        )

    def combo_text(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            return model[tree_iter][0]
        else:
            entry = combo.get_child()
            return entry.get_text()

    def add_team(self, name, gameformat, time, gametime_priority, gameformat_priority):
        self.teams_treeview_ls.append(
            [name, gameformat, time, gametime_priority, gameformat_priority]
        )

    def run(self):
        self.window.show_all()
        Gtk.main()


if __name__ == "__main__":
    app = TeamsWindow("teams_window.glade")
    app.run()
