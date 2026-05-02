# Who Am I? An Exploratory Analysis of My Personal Music Listening History

[The presentation itself is available to view! Simply download the provided `presentation-stt-180-ho-srikar-chitturi.zip` file (located within the `Slideshow` folder), extract it, and open the `presentation-stt-180.html` file in your web browser.]

People engage with music on a daily basis, yet other than the annual cultural event known as Spotify Wrapped, few ever examine their own listening behavior quantitatively — including me. Recently, I finally made the push to start owning my own music and maintaining my own music library, but in the process of deciding what music to buy by scrolling through my playlists, I realized how little I knew about my own music tastes — what genres I like, my favorite artists, my favorite songs from said artists, even naming a single album from their discography — despite music being an extremely large chunk of how I spend every day. The rest of the time, the music that people listen to is essentially a black box, where if you peeked inside, you'd find the Spotify algorithm - a bot whose sole goal is to rack up the minutes you listen on their platform — belching out the most sonically identical songs to the ones you listened to just before to keep you continually engaged. In my mind, music has become disposable — just some background noise that makes every day just a little less mundane than the one before it. In my wish to change this and learn more about myself from a musical standpoint (and create a cool project), I decided to export my Spotify and Apple Music listening history from the inception of my account, now four years in, in an attempt to answer the question: What is my sonic self?

---

## Research Questions

In this journey to learn about my "sonic self," this project seeks to answer four questions:

1. **Temporal Patterns** — How has my total listening volume trended over time, and when during the day and week do I listen most?
2. **Engagement** — Which artists and tracks do I engage with most deeply, and which do I most often skip?
3. **Taste Evolution** — How have my artist and genre preferences shifted across distinct time periods?
4. **Platform Behavior** — Do my listening habits differ meaningfully between Spotify and Apple Music?

I anticipate that behavioral signals like skip rate and average play duration will tell a much more honest story than raw play counts alone, and that the era analysis will reveal distinct phases of musical taste corresponding to different periods of life.

---

## Project Structure

```
.
├── Streaming_History_Audio_*.json       # Raw Spotify exports (ignored by git)
├── Apple Music Play Activity.csv        # Raw Apple Music play activity (ignored by git)
├── Apple Music Library Tracks.json      # Apple Music library — genre metadata (ignored by git)
├── listening history clean.csv          # Combined cleaned output from Python (ignored by git)
├── data cleaning.py                     # Step 1 — Python cleaning script
├── listening history writeup.Rmd        # Step 2 — R Markdown write-up and analysis
├── .gitignore
└── README.md
```

---

## Prerequisites

### Python
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas
```

### R
```r
install.packages(c("tidyverse", "lubridate", "scales", "patchwork", "knitr"))
```

---

## Step 1 — Export Your Data

### Spotify
Request your extended streaming history at **spotify.com/account/privacy**. Spotify emails you a `.zip` within ~30 days containing one or more `Streaming_History_Audio_*.json` files. Drop all of them in the project folder — the cleaning script picks them all up automatically.

### Apple Music
Request your data at **privacy.apple.com**. Apple delivers a `.zip` within up to 7 days. You need two files from inside the export:

```
Apple Music Play Activity.csv          ← individual listen events
Apple Music Library Tracks.json        ← your library with genre metadata
```

Place both in the project folder alongside the Spotify files.

> **Heads up:** Plan around the Apple Music export window if you're working against a deadline — 7 days has a way of sneaking up on you.

---

## Step 2 — Clean and Combine with Python

Open `data cleaning.py` and set your timezone at the top:

```python
YOUR_TIMEZONE = "America/New_York"   # e.g. "America/Chicago", "America/Los_Angeles"
```

The script loads both Spotify and Apple Music exports, normalizes them to a shared schema, enriches every record with genre data from the Apple Music library, and exports a single combined CSV. Then run:

```bash
python3 "data cleaning.py"
```

This produces `listening history clean.csv`.

### What the Cleaning Does

**Spotify**
- Loads all `Streaming_History_Audio_*.json` files at once via glob, concatenates and deduplicates them
- Filters to music only — rows with no `master_metadata_track_name` (podcasts, audiobooks) are dropped
- Parses UTC timestamps and derives `hour`, `day_of_week`, `month_label`, `year`, `date`
- Converts `ms_played` → `minutes_played`
- Builds a reliable `skipped` flag by OR-ing Spotify's native field with `reason_end` being `"fwdbtn"` or `"backbtn"` — the native flag alone is known to be inconsistently populated
- Flags plays under 30 seconds as `is_short_play` to filter out accidental taps

**Apple Music**
- Filters `Apple Music Play Activity.csv` to `PLAY_END` + `AUDIO` rows only — the events that actually represent a completed listen attempt
- Joins to `Apple Music Library Tracks.json` on track title to recover artist name, album, and genre
- Derives a `skipped` flag from `End Reason Type` being `TRACK_SKIPPED_FORWARDS` or `TRACK_SKIPPED_BACKWARDS`
- Parses `Event Start Timestamp` in ISO8601 format (mixed millisecond precision — the `format="ISO8601"` argument handles this)

**Genre Enrichment**
- Builds an artist → genre lookup from the Apple Music library, which contains metadata for 9,326 tracks — 6,779 of which were imported directly from Spotify
- Maps raw genre tags (68 total) into 12 broad buckets via `GENRE_MAP` (e.g., `"Hip-Hop/Rap"`, `"Trap"`, and `"Drill"` all become `"Rap & Hip-Hop"`)
- Achieves 90.5% genre coverage across the combined dataset — no external API needed

### Output Columns

| Column | Description |
|---|---|
| `datetime` | UTC timestamp of the listen |
| `datetime_local` | Timestamp converted to your local timezone |
| `year`, `month`, `hour` | Derived time components for grouping |
| `month_label` | `"YYYY-MM"` string for monthly trend plots |
| `day_of_week` | Full day name e.g. `"Monday"` |
| `date` | Date string `"YYYY-MM-DD"` |
| `track_name` | Track title |
| `artist_name` | Artist name |
| `album_name` | Album name |
| `ms_played` | Raw milliseconds played |
| `minutes_played` | `ms_played` converted to minutes |
| `skipped` | Whether the track was skipped |
| `shuffle` | Whether shuffle was active |
| `is_short_play` | `TRUE` if played less than 30 seconds |
| `platform` | Raw platform string from the export |
| `source` | `"spotify"` or `"apple_music"` |
| `genre_raw` | Original genre tag from Apple Music library |
| `genre` | Normalized broad genre bucket |

---

## Step 3 — Analyse in R

Open `listening history writeup.Rmd` in RStudio with `listening history clean.csv` in the same folder and knit to PDF. The write-up is structured around the four research questions above, with each section containing the relevant code chunks (all `echo = FALSE`), visualizations, and written analysis. Plots produced include:

- **Monthly listening time** — hours per month stacked by source, with overall trend line
- **Listening heatmap** — hour of day × day of week play count grid
- **Top 15 artists** — ranked by total hours played
- **Top 15 tracks** — ranked by play count
- **Most-skipped artists** — skip rate among artists with ≥20 plays
- **Engagement scatter** — hours played vs skip rate, bubble-sized by play count
- **Artist era chart** — top 5 artists per 6-month window
- **Genre evolution** — genre share of listening as a stacked area chart over time
- **Platform comparison table** — Spotify vs Apple Music on plays, hours, avg duration, skip rate
- **Device breakdown** — total hours by platform (Android, Mac, Windows, Cast, etc.)

---

## Notes

- Spotify's `skipped` field is unreliable on its own — the cleaning script supplements it with `reason_end` to catch button-press skips that the native flag misses
- Plays under 30 seconds (`is_short_play = TRUE`) are filtered out of all analysis — they're noise, not listening
- Apple Music's `Container Artist Name` field is null in ~99% of play events, so artist recovery depends entirely on the library join; tracks not in your library (~28%) are dropped
- All raw data files are excluded from version control via `.gitignore` — they're large, personal, and nobody else needs them
