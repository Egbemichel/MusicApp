import flet as ft
from router import views_handler
from utils.db import Database

def main(page: ft.Page):
    # Set page properties
    page.title = "Music App"
    # page.theme_mode = ft.ThemeMode.LIGHT

    # Define what happens when the route changes
    def route_change(event):
        page.views.clear()  # Clear current views
        current_route = event.route
        if current_route in views_handler(page):
            page.views.append(views_handler(page)[current_route])  # Add the correct view
        else:
            page.views.append(ft.View(  # Fallback view for unknown routes
                route=current_route,
                controls=[ft.Text("404 - Page Not Found", color="red")]
            ))
        page.update()  # Update the page to reflect the changes

    # Attach the route change handler
    page.on_route_change = route_change

    # Navigate to the initial route
    page.go("/")

# Run the Flet app
ft.app(target=main, assets_dir="assets")
