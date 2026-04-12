import glob
import json
import pandas as pd


# ── Config ────────────────────────────────────────────────────────────────────
YOUR_TIMEZONE = "America/New_York"

GENRE_MAP = {
    "Hip-Hop/Rap": "Rap & Hip-Hop", "Rap": "Rap & Hip-Hop",
    "Hip-Hop": "Rap & Hip-Hop", "Trap": "Rap & Hip-Hop",
    "Drill": "Rap & Hip-Hop", "Alternative Rap": "Rap & Hip-Hop",
    "Dirty South": "Rap & Hip-Hop", "Hardcore Rap": "Rap & Hip-Hop",
    "Chinese Hip-Hop": "Rap & Hip-Hop",
    "R&B/Soul": "R&B & Soul", "R&B": "R&B & Soul",
    "Acid Jazz": "R&B & Soul", "Neo-Soul": "R&B & Soul",
    "Contemporary R&B": "R&B & Soul",
    "Pop": "Pop", "Indie Pop": "Pop", "Pop Latino": "Pop",
    "French Pop": "Pop", "Vocal Pop": "Pop", "K-Pop": "Pop",
    "Mandopop": "Pop", "J-Pop": "Pop", "Indian Pop": "Pop",
    "Afro-Pop": "Pop", "Pop/Rock": "Pop",
    "Rock": "Rock", "Alternative": "Rock", "Hard Rock": "Rock",
    "Indie Rock": "Rock", "Punk": "Rock", "Pop Punk": "Rock",
    "Soft Rock": "Rock", "Rock y Alternativo": "Rock", "Surf": "Rock",
    "Metal": "Metal", "Hardcore": "Metal",
    "Death Metal/Black Metal": "Metal",
    "Electronic": "Electronic & Dance", "Electronica": "Electronic & Dance",
    "Dance": "Electronic & Dance", "House": "Electronic & Dance",
    "Disco": "Electronic & Dance", "Funk": "Electronic & Dance",
    "Jazz": "Jazz", "Vocal": "Jazz",
    "Soundtrack": "Soundtrack & Score", "Original Score": "Soundtrack & Score",
    "Orchestral": "Soundtrack & Score", "Video Game": "Soundtrack & Score",
    "Comedy": "Comedy & Spoken Word", "Parody": "Comedy & Spoken Word",
    "Spoken Word": "Comedy & Spoken Word",
    "Bollywood": "World & Regional", "Latin": "World & Regional",
    "Afrobeats": "World & Regional", "Worldwide": "World & Regional",
    "Reggae": "World & Regional",
    "Country": "Country",
    "Singer/Songwriter": "Singer/Songwriter",
    "Classical": "Classical",
    "Blues": "Blues",
    "Holiday": "Holiday", "Christmas": "Holiday", "Christmas: Pop": "Holiday",
    "Christian": "Gospel & Religious",
    "Easy Listening": "Easy Listening",
    "Instrumental": "Instrumental",
    "Fitness & Workout": "Other",
}


# ── 1. Spotify ─────────────────────────────────────────────────────────────────
spotify_raw = pd.concat(
    [pd.read_json(f) for f in glob.glob("Streaming_History_Audio_*.json")],
    ignore_index=True
).drop_duplicates()

spotify_raw = spotify_raw[spotify_raw["master_metadata_track_name"].notna()]

spotify_slim = pd.DataFrame({
    "datetime":    pd.to_datetime(spotify_raw["ts"], utc=True),
    "track_name":  spotify_raw["master_metadata_track_name"].values,
    "artist_name": spotify_raw["master_metadata_album_artist_name"].values,
    "album_name":  spotify_raw["master_metadata_album_album_name"].values,
    "ms_played":   spotify_raw["ms_played"].values,
    "skipped":     (spotify_raw["skipped"] |
                    spotify_raw["reason_end"].isin(["fwdbtn", "backbtn"])).values,
    "shuffle":     spotify_raw["shuffle"].values,
    "platform":    spotify_raw["platform"].str.lower().values,
    "source":      "spotify"
})


# ── 2. Apple Music Library — genre + metadata lookup ─────────────────────────
with open("Apple Music Library Tracks.json") as f:
    library = pd.DataFrame(json.load(f))

library_lookup = (
    library[["Title", "Artist", "Album", "Genre", "Track Duration"]]
    .copy()
    .assign(song_key=lambda d: d["Title"].str.strip().str.lower())
    .drop_duplicates("song_key")
    .rename(columns={
        "Artist":         "artist_name",
        "Album":          "album_name",
        "Genre":          "genre_raw",
        "Track Duration": "track_duration_ms"
    })
)


# ── 3. Apple Music Play Activity ───────────────────────────────────────────────
apple_raw = pd.read_csv("Apple Music Play Activity.csv")

apple_raw = apple_raw[
    (apple_raw["Event Type"] == "PLAY_END") &
    (apple_raw["Media Type"] == "AUDIO")
].copy()

apple_raw["song_key"] = apple_raw["Song Name"].str.strip().str.lower()

apple_raw = apple_raw.merge(
    library_lookup[["song_key", "artist_name", "album_name",
                    "genre_raw", "track_duration_ms"]],
    on="song_key",
    how="left"
)

apple_slim = pd.DataFrame({
    "datetime":    pd.to_datetime(apple_raw["Event Start Timestamp"], format="ISO8601", utc=True),
    "track_name":  apple_raw["Song Name"].values,
    "artist_name": apple_raw["artist_name"].values,
    "album_name":  apple_raw["album_name"].values,
    "ms_played":   apple_raw["Play Duration Milliseconds"].values,
    "skipped":     apple_raw["End Reason Type"].isin(
                       ["TRACK_SKIPPED_FORWARDS", "TRACK_SKIPPED_BACKWARDS"]).values,
    "shuffle":     (apple_raw["Shuffle Play"] == "SHUFFLE_ON").values,
    "platform":    apple_raw["Client Platform"].str.lower().values,
    "source":      "apple_music"
})


# ── 4. Combine ─────────────────────────────────────────────────────────────────
combined = pd.concat([spotify_slim, apple_slim], ignore_index=True)

combined = combined.dropna(subset=["track_name", "artist_name"])


# ── 5. Shared derived columns ─────────────────────────────────────────────────
combined["minutes_played"] = combined["ms_played"] / 60_000
combined["is_short_play"]  = combined["ms_played"] < 30_000

combined["datetime_local"] = combined["datetime"].dt.tz_convert(YOUR_TIMEZONE)
combined["date"]        = combined["datetime_local"].dt.date.astype(str)
combined["year"]        = combined["datetime_local"].dt.year
combined["month"]       = combined["datetime_local"].dt.month
combined["month_label"] = combined["datetime_local"].dt.strftime("%Y-%m")
combined["day_of_week"] = combined["datetime_local"].dt.day_name()
combined["hour"]        = combined["datetime_local"].dt.hour


# ── 6. Genre ──────────────────────────────────────────────────────────────────
artist_genre_lookup = (
    library[["Artist", "Genre"]]
    .dropna()
    .drop_duplicates("Artist")
    .set_index("Artist")["Genre"]
    .to_dict()
)
combined["genre_raw"] = combined["artist_name"].map(artist_genre_lookup)

combined["genre"] = combined["genre_raw"].map(GENRE_MAP).fillna("Other")


# ── 7. Sort and export ────────────────────────────────────────────────────────
combined = combined.sort_values("datetime").reset_index(drop=True)

print(f"\nSpotify records:     {(combined['source'] == 'spotify').sum():,}")
print(f"Apple Music records: {(combined['source'] == 'apple_music').sum():,}")
print(f"Total records:       {len(combined):,}")
print(f"Date range:          {combined['date'].min()} → {combined['date'].max()}")
print(f"Genre coverage:      {combined['genre'].ne('Other').mean():.1%}")

combined.to_csv("listening history clean.csv", index=False)
print("\n✓ Saved to listening history clean.csv")