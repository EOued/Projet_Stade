import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

import uuid


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
        self.teams_grid = self.builder.get_object("teams_grid")

        self.fields = self.builder.get_object("fields")
        self.fields_grid = self.builder.get_object("fields_grid")

        self.teams_button = self.builder.get_object("teams_button")
        self.fields_button = self.builder.get_object("fields_button")
        self.settings_button = self.builder.get_object("settings_button")

        self.menu = self.builder.get_object("menu")

        # variables

        self.cur_grid = None
        self.cur_row = float("NaN")

        self.signal_ids = {}

        # Event listener
        self.teams_button.connect("clicked", self.on_button_clicked)
        self.fields_button.connect("clicked", self.on_button_clicked)

        self.builder.get_object("insert").connect("activate", self.insert_row)
        self.builder.get_object("delete").connect("activate", self.delete_row)

        self.menu.connect(
            "selection-done", lambda self: setattr(self, "cur_row", float("NaN"))
        )

    def post_init(self):
        self.teams.hide()
        self.fields.hide()
        self.settings_button.hide()

        self.populate_grid_click_events(self.fields_grid)
        self.populate_grid_click_events(self.teams_grid)

        self.cur_grid = self.teams_grid

        filler_id = f"{Gtk.Buildable.get_name(self.cur_grid)}_filler"
        filler = self.builder.get_object(filler_id)
        top_attach = (
            self.cur_grid.child_get_property(filler, "top-attach")
            if self.cur_grid
            else 0
        )
        height = (
            self.cur_grid.child_get_property(filler, "height") if self.cur_grid else 0
        )

    # Events

    def on_button_clicked(self, button):
        id = Gtk.Buildable.get_name(button)
        self.teams.show()
        self.fields.show()

        if id == "teams_button":
            self.cur_grid = self.teams_grid
            self.fields.hide()
        else:
            self.cur_grid = self.fields_grid
            self.teams.hide()

    def populate_grid_click_events(self, grid):
        children = grid.get_children()
        for widget in children:

            row = grid.child_get_property(widget, "top-attach")
            if row == 0:
                continue
            id = uuid.uuid4()
            Gtk.Buildable.set_name(widget, f"{id}")

            self.signal_ids[f"{id}"] = widget.connect(
                "button-press-event", self.on_right_click, row
            )
            widget.set_size_request(-1, 50)

    def on_right_click(self, widget, event, row):
        if event.button == Gdk.BUTTON_SECONDARY:
            self.menu.popup_at_pointer(event)
            self.cur_row = row
            return True
        return False

    # Grid filler widget

    def delete_row(self, widget):
        if self.cur_grid == None:
            return

        filler_id = f"{Gtk.Buildable.get_name(self.cur_grid)}_filler"
        filler = self.builder.get_object(filler_id)
        filler_top_attach = self.cur_grid.child_get_property(filler, "top-attach")

        if self.cur_row == 1 and filler_top_attach == 2:
            self.reset_row(1)
            return

        for child in list(self.cur_grid.get_children()):
            row = self.cur_grid.child_get_property(child, "top-attach")
            if row == self.cur_row:
                child.destroy()

        self.grid_filler_widget_resize()
        self.grid_elements_move_up(self.cur_row)

    def grid_elements_move_up(self, row):
        if self.cur_grid == None:
            return
        filler_id = f"{Gtk.Buildable.get_name(self.cur_grid)}_filler"
        filler = self.builder.get_object(filler_id)
        for child in self.cur_grid.get_children():
            top_attach = self.cur_grid.child_get_property(child, "top-attach")
            if top_attach < row:
                continue
            #    if child == filler:
            #        continue
            self.cur_grid.child_set_property(child, "top-attach", top_attach - 1)

            id = Gtk.Buildable.get_name(child)
            child.disconnect(self.signal_ids[Gtk.Buildable.get_name(child)])
            self.signal_ids[f"{id}"] = child.connect(
                "button-press-event", self.on_right_click, top_attach - 1
            )

    def grid_filler_widget_resize(self):
        if self.cur_grid is None:
            return

        filler_id = f"{Gtk.Buildable.get_name(self.cur_grid)}_filler"
        filler = self.builder.get_object(filler_id)
        filler.show()
        top_attach = (
            self.cur_grid.child_get_property(filler, "top-attach")
            if self.cur_grid
            else 0
        )
        height = (
            self.cur_grid.child_get_property(filler, "height") if self.cur_grid else 0
        )

        self.cur_grid.child_set_property(filler, "height", height + 1)

    def reset_row(self, row):
        if self.cur_grid == None:
            return
        for child in self.cur_grid.get_children():
            if isinstance(child, Gtk.ComboBox):
                child.set_active(0)
            if isinstance(child, Gtk.SpinButton):
                child.set_value(0)
            if isinstance(child, Gtk.Entry):
                child.set_text("")

    def insert_row(self, _):
        empty_row = self.grid_filler_widget_free_row(_)
        self.grid_duplicate_row(empty_row - 1, empty_row)

    def grid_filler_widget_free_row(self, _):
        filler_id = f"{Gtk.Buildable.get_name(self.cur_grid)}_filler"
        filler = self.builder.get_object(filler_id)
        top_attach = (
            self.cur_grid.child_get_property(filler, "top-attach")
            if self.cur_grid
            else 0
        )
        height = (
            self.cur_grid.child_get_property(filler, "height") if self.cur_grid else 0
        )

        if self.cur_grid:
            self.cur_grid.child_set_property(filler, "top-attach", top_attach + 1)
            # If the filler is taking one row, we don't need to decrement its height. Thus, we can hide it
            if height != 1:
                self.cur_grid.child_set_property(filler, "height", height - 1)
            else:
                filler.hide()

        return top_attach

    def grid_duplicate_row(self, row_org, row_des):
        if self.cur_grid is None:
            return
        for child in self.cur_grid.get_children():
            x = self.cur_grid.child_get_property(child, "left-attach")
            y = self.cur_grid.child_get_property(child, "top-attach")

            if y != row_org:
                continue

            child_copy = GObject.new(child.__gtype__)
            if isinstance(child, Gtk.ComboBox):
                liststore = child.get_model()
                child_copy.set_model(liststore)
                renderer = Gtk.CellRendererText()
                child_copy.pack_start(renderer, True)
                child_copy.add_attribute(renderer, "text", 0)
                child_copy.set_active(0)
            if isinstance(child, Gtk.SpinButton):
                original_adjustment = child.get_adjustment()
                adjustment = Gtk.Adjustment(
                    value=0,
                    lower=original_adjustment.get_lower(),
                    upper=original_adjustment.get_upper(),
                    step_increment=1,
                    page_increment=original_adjustment.get_page_increment(),
                    page_size=0,
                )
                child_copy.set_adjustment(adjustment)

            id = uuid.uuid4()
            Gtk.Buildable.set_name(child_copy, f"{id}")

            self.signal_ids[f"{id}"] = child_copy.connect(
                "button-press-event", self.on_right_click, row_des
            )
            child_copy.set_size_request(-1, 50)

            self.cur_grid.attach(child_copy, x, row_des, 1, 1)
            child_copy.show()

    def run(self):
        self.window.show_all()
        self.post_init()
        Gtk.main()


if __name__ == "__main__":
    apply_css()  # Path to your CSS file
    app = TeamsWindow("ui/GUI.glade")
    app.run()
