import flet as ft
from utils.colors import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BORDER_PRIMARY,
    MAIN_BACKGROUND,
    MAIN_ACCENT,
    MAIN_HIGHLIGHT,
)
from utils.db import Database


class Login(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.db = Database()
        self.build_ui()

    def build_ui(self):
        def login_user(e):
            email = email_field.value
            password = password_field.value

            if not email or not password:
                status_text.value = "All fields are required!"
                status_text.color = MAIN_ACCENT
                status_text.update()
                return

            if self.db.validate_user(email, password):
                status_text.value = "Login successful!"
                status_text.color = MAIN_HIGHLIGHT
                status_text.update()
                self.page.go("/dashboard")
            else:
                status_text.value = "Invalid email or password!"
                status_text.color = MAIN_ACCENT
                status_text.update()

        email_field = ft.TextField(label="Email", color=TEXT_SECONDARY, border_color=BORDER_PRIMARY)
        password_field = ft.TextField(
            label="Password", password=True, can_reveal_password=True, color=TEXT_SECONDARY, border_color=BORDER_PRIMARY
        )
        submit_button = ft.ElevatedButton(
            width=200,
            text="Login",
            on_click=login_user,
            style=ft.ButtonStyle(
                bgcolor=MAIN_ACCENT,
                color=MAIN_BACKGROUND,
                overlay_color=MAIN_HIGHLIGHT,
            ),
        )
        status_text = ft.Text("", size=16, color=TEXT_PRIMARY)

        self.content = ft.Container(
            expand=True,
            bgcolor=MAIN_BACKGROUND,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=400,
                        border=ft.border.all(2, BORDER_PRIMARY),
                        border_radius=15,
                        padding=25,
                        content=ft.Column(
                            controls=[
                                ft.Text("Login", size=24, weight="bold", color=TEXT_PRIMARY),
                                email_field,
                                password_field,
                                submit_button,
                                status_text,
                                ft.TextButton(
                                    text="Don't have an account? Sign up here.",
                                    on_click=lambda _: self.page.go("/signup"),
                                    style=ft.ButtonStyle(color=MAIN_ACCENT),
                                ),
                            ],
                        ),
                    )
                ],
            ),
        )
