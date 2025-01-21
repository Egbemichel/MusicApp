import flet as ft
from utils.colors import APP_BAR_BG, TEXT_COLOR

class AppBar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.bgcolor = APP_BAR_BG
        self.padding = 10
        self.content = ft.Row(
            controls=[
                ft.Image(
                    src="assets/Music_logo.png",
                    width=50,
                    height=50,
                    fit="contain",
                ),
                ft.Text(
                    value="MusicApp Dashboard",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_COLOR,
                ),
                ft.Container(
                    content=ft.CircleAvatar(
                        radius=20,
                        content=ft.Image(
                            src="assets/profile_placeholder.jpg",
                            fit="cover",
                        ),
                    ),
                    alignment=ft.alignment.center_right,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
