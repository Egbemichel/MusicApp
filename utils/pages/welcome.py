import flet as ft

class Welcome(ft.Container):  # Using ft.Container for the welcome page
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        # Build the UI for the welcome page
        self.content = ft.Column(
            alignment="center",
            controls=[
                ft.Row(
                    alignment="center",
                    controls=[
                        ft.Container(
                            width=400,
                            content=ft.Column(
                                controls=[
                                    ft.Text("Welcome to MusicApp!", size=30, weight="bold"),
                                    ft.Text("Your music journey starts here."),
                                ]
                            ),
                        ),
                        ft.Container(
                            width=400,
                            content=ft.Image(src="./assets/ivy1.jpg", width=300),
                        ),
                    ],
                ),
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.ElevatedButton(
                        text="Next",
                        on_click=lambda _: self.page.go("/signup"),  # Navigate to signup
                        width=200,
                    ),
                ),
            ],
        )
