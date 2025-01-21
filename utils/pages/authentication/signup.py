import flet as ft
from utils.colors import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_TERTIARY,
    BORDER_PRIMARY,
    MAIN_BACKGROUND,
    MAIN_ACCENT,
    MAIN_HIGHLIGHT,
    GRADIENT_PINK,
)
from utils.validation import Validation
from utils.db import Database


class Signup(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.db = Database()
        self.build_ui()

    def build_ui(self):
        def signup_user(e):
            name = name_field.value
            email = email_field.value
            password = password_field.value
            genre = genre_dropdown.value
            photo = None  # Placeholder for photo functionality

            if not all([name, email, password, genre]):
                status_text.value = "All fields are required!"
                status_text.color = MAIN_ACCENT
                status_text.update()
                return

            if not Validation.is_valid_email(email):
                status_text.value = "Invalid email format!"
                status_text.color = MAIN_ACCENT
                status_text.update()
                return

            if not Validation.is_valid_password(password):
                status_text.value = "Password must meet complexity requirements!"
                status_text.color = MAIN_ACCENT
                status_text.update()
                return

            if self.db.insert_user(name, email, password, genre, photo):
                status_text.value = "Sign up successful!"
                status_text.color = MAIN_HIGHLIGHT
                status_text.update()
                self.page.go("/login")
            else:
                status_text.value = "Email already exists!"
                status_text.color = MAIN_ACCENT
                status_text.update()

        name_field = ft.TextField(label="Name", color=TEXT_SECONDARY, border_color=BORDER_PRIMARY)
        email_field = ft.TextField(label="Email", color=TEXT_SECONDARY, border_color=BORDER_PRIMARY)
        password_field = ft.TextField(
            label="Password", password=True, can_reveal_password=True, color=TEXT_SECONDARY, border_color=BORDER_PRIMARY
        )
        genre_dropdown = ft.Dropdown(
            label="Favorite Genre",
            color=TEXT_SECONDARY,
            options=[
                ft.dropdown.Option("Pop"),
                ft.dropdown.Option("Rock"),
                ft.dropdown.Option("Jazz"),
                ft.dropdown.Option("Hip Hop"),
                ft.dropdown.Option("Classical"),
            ],
        )
        submit_button = ft.ElevatedButton(
            width=200,
            text="Sign Up",
            on_click=signup_user,
            style=ft.ButtonStyle(
                bgcolor=MAIN_ACCENT,
                color=MAIN_BACKGROUND,
                overlay_color=MAIN_HIGHLIGHT,
            ),
        )
        status_text = ft.Text("", size=16, color=TEXT_TERTIARY)

        self.content = ft.Container(
            expand=True,
            bgcolor=GRADIENT_PINK,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=400,
                        border=ft.border.all(2, BORDER_PRIMARY),
                        border_radius=15,
                        padding=20,
                        content=ft.Column(
                            controls=[
                                ft.Text("Sign Up", size=24, weight="bold", color=TEXT_PRIMARY),
                                name_field,
                                email_field,
                                password_field,
                                genre_dropdown,
                                submit_button,
                                status_text,
                                ft.TextButton(
                                    text="Already have an account? Login here.",
                                    on_click=lambda _: self.page.go("/login"),
                                    style=ft.ButtonStyle(color=MAIN_ACCENT),
                                ),
                            ],
                        ),
                    )
                ],
            ),
        )
