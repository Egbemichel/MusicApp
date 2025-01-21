import flet as ft
from utils.colors import MAIN_BG, TEXT_COLOR
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
# from playsound import playsound  # Add the playsound module for audio playback
import pygame  # Import pygame for audio playback

class MainSection(ft.Container):
    def __init__(self, page: ft.Page, db, section="home"):
        super().__init__()
        print("Initializing MainSection...")  # Debugging
        self.page = page
        self.db = db
        self.bgcolor = MAIN_BG
        self.expand = True
        self.padding = 10
        self.section = section  # Set the section dynamically

        print(f"bgcolor: {self.bgcolor}, expand: {self.expand}, padding: {self.padding}, section: {self.section}")  # Debugging

        # Initialize content based on the section
        self.content = self.get_section_content(self.section)  # Debugging

        # Initialize flag to ensure update is only triggered after initialization
        self.initialized = False

        # Initialize Pygame mixer for audio playback
        pygame.mixer.init()

        # Current song state
        self.current_song = None
        self.is_playing = False

        # File picker
        self.file_picker = ft.FilePicker(on_result=self.file_selected)
        self.page.overlay.append(self.file_picker)

        # Player UI elements
        self.player_section = ft.Container(visible=False, expand=True)

    def file_selected(self, e: ft.FilePickerResultEvent):
        """Handle the selected file from the file picker."""
        if e.files:
            selected_file_path = e.files[0].path
            print(f"Selected file: {selected_file_path}")

            # Extract song metadata (you might use a library like mutagen for this)
            try:
                audio = MP3(selected_file_path, ID3=EasyID3)
                title = audio.get("title", ["Unknown Title"])[0]
                artist = audio.get("artist", ["Unknown Artist"])[0]
            except Exception as err:
                print(f"Error extracting metadata: {err}")
                title = os.path.basename(selected_file_path)
                artist = "Unknown Artist"

            # Save to the database
            self.db.add_song(
                title=title,
                artist=artist,
                album_image="./assets/default.jpg",  # Placeholder, use an actual image URL or path
                song_url=selected_file_path
            )
            print(f"Song '{title}' by '{artist}' added to the database.")

            # Update the UI with the new song list
            self.content = self.load_songs_content()
            self.page.update()

            # Show a SnackBar to confirm upload
            snack_bar = ft.SnackBar(content=ft.Text(f"Uploaded: {title} by {artist}"))
            if snack_bar not in self.page.overlay:
                self.page.overlay.append(snack_bar)
            snack_bar.visible = True
            self.page.update()
        else:
            print("No file selected.")

    def get_section_content(self, section):
        """Return content based on the section parameter."""
        if section == "home":
            return self.load_songs_content()
        # Other sections (favorites, recommendations, etc.) can be added here as needed
        elif section == "favorites":
            return self.load_favorites_content()
            pass
        elif section == "playlists":
            # return self.load_playlists_content() # in the playlist page 
            pass
        elif section == "albums":
            # return self.load_albums_content()
            pass
        elif  section == "artists":
            # return self.load_artists_content()
            pass
        elif section == "settings":
            # return self.load_settings_content()
            pass
        else:
         return ft.Text(
            value="Page Not Found",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=TEXT_COLOR,
        )

    def load_favorites_content(self):
     """Display the list of favorite songs from the database."""
     favorite_songs = self.db.fetch_favorites()  # Assuming the method fetches songs from the 'favorites' table
     song_items = []

     if not favorite_songs:
        song_items.append(ft.Text(value="No favorite songs available", size=18, color=TEXT_COLOR))

     for song in favorite_songs:
        song_id = song
        # You may need to fetch the rest of the song details (title, artist, album_image) from the database
        song_details = self.db.get_song_details() 
        print(f"song_details: {song_details}")  # Debugging # Assuming there's a method to fetch details for each song
        id, title, artist, album_image, song_url = song_details
        
        song_item = ft.Row(
            controls=[
                ft.Image(src=album_image, width=50, height=50),
                ft.Column(
                    controls=[
                        ft.Text(value=title, size=16, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                        ft.Text(value=artist, size=14, color=TEXT_COLOR)
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.PLAY_ARROW,
                            on_click=lambda e, song_url=song_url: self.play_song(song_url, title, artist, album_image)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            on_click=lambda e, song_id=song_id: self.remove_from_favorites(song_id)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
            ],
            expand=True
        )
        song_items.append(song_item)
        

    # Add the file picker button (optional)
     song_items.append(
        ft.ElevatedButton(
            width=150,
            text="Upload",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=lambda _: self.file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["mp3", "wav", "ogg"]
            )
        )
    )

     return ft.Column(controls=song_items)
    

    def remove_from_favorites(self, song_id):
        """Remove a song from the favorites."""
        self.db.remove_from_favorites(song_id)
        print(f"Song {song_id} removed from favorites.")
        self.load_favorites_content()  # Reload the favorite songs content
        self.page.update()
    


    def load_songs_content(self):
        """Display the list of songs from the database."""
        songs = self.db.fetch_songs()
        song_items = []

        if not songs:
            song_items.append(ft.Text(value="No songs available", size=18, color=TEXT_COLOR))

        for song in songs:
            song_id, title, artist, album_image, song_url = song
            song_item = ft.Row(
                controls=[
                    ft.Image(src=album_image, width=50, height=50),
                    ft.Column(
                        controls=[
                            ft.Text(value=title, size=16, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                            ft.Text(value=artist, size=14, color=TEXT_COLOR)
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.PLAY_ARROW,
                                on_click=lambda e, song_url=song_url: self.play_song(song_url, title, artist, album_image)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.FAVORITE,
                                on_click=lambda e, song_id=song_id: self.add_to_favorites(song_id)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                on_click=lambda e, song_id=song_id: self.delete_song(song_id)
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END
                    ),
                ],
                expand=True
            )
            song_items.append(song_item)

        # Add the file picker button
        song_items.append(
            ft.ElevatedButton(
                width=150,
                text="Upload",
                icon=ft.Icons.UPLOAD_FILE,
                on_click=lambda _: self.file_picker.pick_files(
                    allow_multiple=False,
                    allowed_extensions=["mp3", "wav", "ogg"]
                )
            )
        )

        return ft.Column(controls=song_items)

    def play_song(self, song_url, title, artist, album_image):
        """Handle playing the song."""
        print(f"Playing song: {song_url}")
        
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.load(song_url)
            pygame.mixer.music.play()
            self.is_playing = True

        self.update_player_section(title, artist, album_image, song_url)

    def update_player_section(self, title, artist, album_image, song_url):
        """Update the player section UI."""
        self.current_song = song_url  # Set the current song
        self.player_section.visible = True  # Show the player section
        self.page.update()

        # Update the player UI with song details
        self.player_section.controls = [
            ft.Column(
                controls=[
                    ft.Image(src=album_image, width=200, height=200),
                    ft.Text(value=title, size=24, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                    ft.Text(value=artist, size=18, color=TEXT_COLOR),
                    ft.ProgressBar(value=0, width=300),  # Placeholder progress bar
                    ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.Icons.PAUSE, on_click=lambda e: self.toggle_play_pause()),
                            ft.IconButton(icon=ft.Icons.SKIP_NEXT, on_click=lambda e: self.next_song()),
                            ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS, on_click=lambda e: self.previous_song())
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ]

        self.page.update()

    def toggle_play_pause(self):
        """Toggle play/pause when the button is clicked."""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True

        self.update()

    def next_song(self):
        """Handle the next song functionality (example logic)."""
        print("Playing next song...")
        # Implement logic to play next song here (e.g., based on the database or a playlist)
        self.play_song(self.current_song, "Next Song", "Next Artist", "./assets/next_song.jpg")

    def previous_song(self):
        """Handle the previous song functionality (example logic)."""
        print("Playing previous song...")
        # Implement logic to play previous song here (e.g., based on the database or a playlist)
        self.play_song(self.current_song, "Previous Song", "Previous Artist", "./assets/prev_song.jpg")

    def add_to_favorites(self, song_id):
        """Add song to favorites."""
        self.db.add_to_favorites(song_id)
        print(f"Song {song_id} added to favorites.")

    def delete_song(self, song_id):
        """Delete a song from the database."""
        self.db.delete_song(song_id)
        print(f"Song {song_id} deleted from the database.")
        self.load_songs_content()  # Reload the song list after deletion

    def update_content(self, route_change_event):
        """Handle content update based on the route change."""
        route = route_change_event.data  # Extract the route string from the event
        print(f"Route change detected: {route}")  # Debugging

        # Check if the controls have been initialized
        if not self.initialized:
            print("MainSection is not fully initialized yet. Skipping update.")  # Debugging
            return

        section = route.split("/")[-1]  # Extract the section from the route
        print(f"Extracted section: {section}")  # Debugging

        if section != self.section:
            self.section = section
            self.content = self.get_section_content(self.section)  # Update the section content
            self.page.update()
            print(f"MainSection updated to {self.section}")  # Debugging


    def build(self):
        """Build and initialize MainSection."""
        if not self.initialized:  # Check if already initialized
            print("Building MainSection...")  # Debugging
            # Mark as initialized after building
            self.initialized = True
            print("MainSection fully initialized.")  # Debugging
            # Set the route change listener, ensuring it's only done once
            self.page.on_route_change = self.update_content
            print("Route change listener set.")  # Debugging
        return self.content
