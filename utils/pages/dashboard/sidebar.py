import flet as ft
from utils.colors import SIDEBAR_BG, SIDEBAR_ICON_COLOR

class Sidebar(ft.Container):
    def __init__(self, page: ft.Page, db):
        super().__init__()
        self.page = page
        self.db = db

        # Sidebar UI
        self.bgcolor = SIDEBAR_BG
        self.padding = 10
        self.width = 250
        self.content = ft.Column(
            controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK, color=SIDEBAR_ICON_COLOR),
                    title=ft.Text("Library", color=SIDEBAR_ICON_COLOR),
                    on_click=lambda _: self.page.go("/dashboard/home"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.FAVORITE, color=SIDEBAR_ICON_COLOR),
                    title=ft.Text("Favorites", color=SIDEBAR_ICON_COLOR),
                    on_click=lambda _: self.page.go("/dashboard/favorites"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PLAYLIST_PLAY, color=SIDEBAR_ICON_COLOR),
                    title=ft.Text("Playlists", color=SIDEBAR_ICON_COLOR),
                    on_click=lambda _: self.page.go("/dashboard/playlists"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.ALBUM, color=SIDEBAR_ICON_COLOR),
                    title=ft.Text("Albums", color=SIDEBAR_ICON_COLOR),
                    on_click=lambda _: self.page.go("/dashboard/albums"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON, color=SIDEBAR_ICON_COLOR),
                    title=ft.Text("Artists", color=SIDEBAR_ICON_COLOR),
                    on_click=lambda _: self.page.go("/dashboard/artists"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.SETTINGS, color=SIDEBAR_ICON_COLOR),
                    title=ft.Text("Settings", color=SIDEBAR_ICON_COLOR),
                    on_click=lambda _: self.page.go("/dashboard/settings"),
                ),
            ],
            spacing=10,
        )
