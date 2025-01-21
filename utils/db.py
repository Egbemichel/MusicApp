import sqlite3

class Database:
    def __init__(self, db_name="music_app.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.create_users_table()
        self.create_songs_table()
        self.create_playlists_table()
        self.create_favorites_table()
        self.create_artists_table()
        self.create_artists_songs()
        self.create_albums_table()
        self.create_albums_songs()
        self.create_playlists_songs()

    def create_users_table(self):
        try:
            with self.connection:
                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        genre TEXT NOT NULL,
                        photo BLOB
                    );
                """)
        except sqlite3.Error as e:
            print(f"An error occurred while creating users table: {e}")
    
    def create_songs_table(self):
        try:
            with self.connection:
                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS songs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        artist TEXT,
                        album_image TEXT,
                        song_url TEXT
                    );
                """)
        except sqlite3.Error as e:
            print(f"An error occurred while creating songs table: {e}")

    def create_playlists_table(self):
        try:
            with self.connection:
                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS playlists (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,                   
                        created_by INTEGER,                   
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
        except sqlite3.Error as e:
            print(f"An error occurred while creating playlists table: {e}")

    def create_playlists_songs(self):
        try:
            with self.connection:
                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS playlists_songs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        playlist_id INTEGER NOT NULL,         
                        song_id INTEGER NOT NULL,             
                        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                        FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE, 
                        FOREIGN KEY (song_id) REFERENCES songs (id) ON DELETE CASCADE
                    );
                """)
        except sqlite3.Error as e:
            print(f"An error occurred while creating playlists table: {e}")

    def create_artists_table(self):
        try:
            with  self.connection:
                self.connection.execute("""
                   CREATE TABLE IF NOT EXISTS artists (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,                   
                        created_by INTEGER,                   
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
""")
        except sqlite3.Error as e:
            print(f"An error ocurred while creating artist table:  {e}")   

    def create_artists_songs(self):
        try:
            with self.connection:
                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS artist_songs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        artist_id INTEGER NOT NULL,         
                        song_id INTEGER NOT NULL,             
                        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                        FOREIGN KEY (artist_id) REFERENCES playlists (id) ON DELETE CASCADE, 
                        FOREIGN KEY (song_id) REFERENCES songs (id) ON DELETE CASCADE
                    );
                """)
        except sqlite3.Error as e:
            print(f"An error occurred while creating artist table: {e}")  

    def create_albums_table(self):
        try:
            with  self.connection:
                self.connection.execute("""
                   CREATE TABLE IF NOT EXISTS albums (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,                   
                        created_by INTEGER,                   
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
""")
        except sqlite3.Error as e:
            print(f"An error ocurred while creating albums table:  {e}")  

    def create_albums_songs(self):
        try:
            with self.connection:
                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS album_songs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        album_id INTEGER NOT NULL,         
                        song_id INTEGER NOT NULL,             
                        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                        FOREIGN KEY (album_id) REFERENCES playlists (id) ON DELETE CASCADE, 
                        FOREIGN KEY (song_id) REFERENCES songs (id) ON DELETE CASCADE
                    );
                """)
        except sqlite3.Error as e:
            print(f"An error occurred while creating playlists table: {e}")  


    def create_favorites_table(self):
        try:
            with self.connection:
                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    song_id INTEGER,
                    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
                    );
                """)
        except sqlite3.Error as e:
            print(f"An error occurred while creating playlists table: {e}")

    def insert_user(self, name, email, password, genre, photo):
        try:
            with self.connection:
                self.connection.execute("""
                    INSERT INTO users (name, email, password, genre, photo)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, email, password, genre, photo))
            return True
        except sqlite3.IntegrityError:
            return False

    def validate_user(self, email, password):
        with self.connection:
            user = self.connection.execute("""
                SELECT * FROM users WHERE email = ? AND password = ?
            """, (email, password)).fetchone()
        return user is not None
    
    def fetch_songs(self):
       query = "SELECT * FROM songs"  # Assuming you have a table named "songs"
       cursor = self.connection.cursor()  # Create a cursor object
       cursor.execute(query)  # Execute the query
       results = cursor.fetchall()  # Fetch all the results
       cursor.close()  # Close the cursor
       return results  # Return list of songs
    
    def fetch_favorites(self):
        query = "SELECT song_id FROM favorites"
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results # Return list of favorite songs
    
    

    def add_song(self, title, artist, album_image, song_url):
        query = "INSERT INTO songs (title, artist, album_image, song_url) VALUES (?, ?, ?, ?)"
        self.connection.execute(query, (title, artist, album_image, song_url))
        self.connection.commit()

    def delete_song(self, song_id):
        query = "DELETE FROM songs WHERE id = ?"
        self.connection.execute(query, (song_id,))
        self.connection.commit()

    def remove_from_favorites(self, song_id):
        query = "DELETE FROM favorites WHERE id = ?"
        self.connection.execute(query, (song_id,))
        self.connection.commit()

    def add_to_favorites(self, song_id):
        query = "INSERT INTO favorites (song_id) VALUES (?)"
        self.connection.execute(query, (song_id,))
        self.connection.commit()

    def get_song_details(self):
     query = """
        SELECT * 
        FROM songs 
        WHERE id IN (SELECT song_id FROM favorites)
    """
     cursor = self.connection.cursor()
     cursor.execute(query)
     results = cursor.fetchone()
     cursor.close()
     return results  # Return all details of favorite songs



    def __del__(self):
        if self.connection:
            self.connection.close()
