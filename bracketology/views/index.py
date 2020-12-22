"""
Bracketology index (main) view.

URLs include:
/
"""
import flask, os, uuid, pprint, numpy
import bracketology
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


@bracketology.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    pp = pprint.PrettyPrinter(indent=4)

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    context = {}

    # Connect to database
    connection = bracketology.model.get_db()

    if flask.request.method == "POST":
        name = flask.request.form['artist']
        artist = spotify.search(q='artist:' + name, type='artist')["artists"]["items"][0]
        albums = spotify.artist_albums(artist["id"], album_type='album')["items"]
        singles = spotify.artist_albums(artist["id"], album_type='single')["items"]
        disco = numpy.concatenate((albums, singles), axis=None)
        
        toptracks = spotify.artist_top_tracks(artist["id"])

        filtered_album = {}
        for album in disco:
            filtered_album[album["name"]] = album["id"]
            songs = spotify.album_tracks(album["id"])["items"]
            print("\n")
            print("ALBUM", album["name"])
            for song in songs:
                print(song["name"])
                track = spotify.track(song["id"])
                cur = connection.execute(
                    "REPLACE INTO songs (id, name, artist, album, popularity)"
                    " VALUES (?, ?, ?, ?, ?);",
                    (track["id"], track["name"], artist["id"], album["id"], track["popularity"],)
                )
            
            
        """
        for name, id in filtered_album.items():
            songs = spotify.album_tracks(id)["items"]
            print("\n")
            print("ALBUM", name)
            for song in songs:
                print(song["name"])
                track = spotify.track(song["id"])
                cur = connection.execute(
                    "REPLACE INTO songs (id, name, artist, album, popularity)"
                    " VALUES (?, ?, ?, ?, ?);",
                    (track["id"], track["name"], artist["id"], album["id"], track["popularity"],)
                )
        """
        cur = connection.execute(
                "SELECT * FROM songs"
                " WHERE artist=? "
                " ORDER BY popularity DESC;",
                (artist["id"],)
            )
        
        songs = cur.fetchall()
        #pp.pprint(songs)

        cur = connection.execute(
                "SELECT * FROM songs"
                " WHERE name=? "
                " ORDER BY popularity DESC;",
                ("Runaway",)
            )
        
        runaway = cur.fetchone()
        

        context["songs"] = songs
        return flask.render_template("index.html", **context)

    return flask.render_template("index.html", **context)

