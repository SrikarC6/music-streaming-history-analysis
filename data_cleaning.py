import glob
import pandas as pd

spotify = pd.concat(
    [pd.read_json(f) for f in glob.glob('Streaming_History_Audio_*.json')],
    ignore_index=True
).drop_duplicates()

spotify_slim = pd.DataFrame({
    "datetime": pd.to_datetime(spotify['ts'], utc=True),
    "track_name": spotify['master_metadata_track_name'],
    "artist_name": spotify['master_metadata_album_artist_name'],
    "album_name": spotify['master_metadata_album_album_name'],
    "ms_played": spotify['ms_played'],
    "skipped": spotify['skipped'],
    "source": "spotify"
})