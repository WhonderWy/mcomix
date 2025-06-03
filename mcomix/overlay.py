from mcomix import run
from gi.repository import Gtk, Gdk

class PageOverlay(Gtk.Window):
    def __init__(self, main_window, text="001/100", font_size=20, text_color="#ffffff", opacity=0.5):
        super().__init__(title="Overlay Page Count")

        self.set_decorated(False)  # No window borders
        self.set_keep_above(True)  # Stay on top
        self.set_resizable(False)
        self.set_app_paintable(True)
        self.set_visual(self.get_screen().get_rgba_visual())  # Allow transparency
        self.set_opacity(opacity)

        # Create the label
        self.label = Gtk.Label(label=text)
        self.update_label(text)  # Initialize label

        # Apply CSS for customization
        css_provider = Gtk.CssProvider()
        css = f"""
            label {{
                font-size: {font_size}px;
                color: {text_color};
                padding: 5px;
            }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.add(self.label)

        # Position overlay near bottom right
        screen_width = Gdk.Screen.get_default().width()
        screen_height = Gdk.Screen.get_default().height()
        self.move(screen_width - 100, screen_height - 50)

        self.show_all()

    def update_label(self, text):
        """Update the label dynamically when page count changes."""
        self.label.set_text(text)