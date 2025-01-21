import flet as ft
from utils.pages.authentication.login import Login
from utils.pages.authentication.signup import Signup
from utils.pages.welcome import Welcome
from utils.pages.dashboard.app_bar import AppBar
from utils.pages.dashboard.main_section import MainSection
from utils.pages.dashboard.sidebar import Sidebar
from utils.db import Database

# Define the handler for views based on routes
def views_handler(page: ft.Page):
    db = Database()  # Create an instance of the Database class
    return {
        "/": ft.View(
            route="/",
            controls=[Welcome(page)]
        ),
        "/login": ft.View(
            route="/login",
            controls=[Login(page)]
        ),
        "/signup": ft.View(
            route="/signup",
            controls=[Signup(page)]
        ),
        "/dashboard": ft.View(
            route="/dashboard",
            controls=[
                ft.Column(
                    controls=[
                        # App Bar
                        AppBar(page),
                        # Sidebar and Main Section Layout
                        ft.Row(
                            controls=[
                                Sidebar(page, db),   # Sidebar on the left
                                MainSection(page, db),  # Dynamic main section
                            ],
                            expand=True,  # Allow the row to stretch
                        ),
                    ],
                    expand=True,  # Allow the column to stretch vertically
                )
            ]
        ),
        "/dashboard/home": ft.View(
            route="/dashboard/home",
            controls=[MainSection(page, db, section="home")]
        ),
        "/dashboard/favorites": ft.View(
            route="/dashboard/favorites",
            controls=[MainSection(page, db, section="favorites")]
        ),
        "/dashboard/playlists": ft.View(
            route="/dashboard/playlists",
            controls=[MainSection(page, db, section="playlists")]
        ),
        "/dashboard/albums": ft.View(
            route="/dashboard/albums",
            controls=[MainSection(page, db, section="albums")]
        ),
        "/dashboard/artists": ft.View(
            route="/dashboard/artists",
            controls=[MainSection(page, db, section="artists")]
        ),
        "/dashboard/settings": ft.View(
            route="/dashboard/settings",
            controls=[MainSection(page, db,  section="settings")]
        ),
    }
