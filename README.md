People engage with music on a daily basis, yet other than the annual cultural event known
as Spotify Wrapped, few ever examine their own listening behavior quantitatively -
including me. Recently, I finally made the push to start owning my own music and
maintaining my own music library, but in the process of deciding what music to buy by
scrolling through my playlists, I realized how little I knew about my own music tastes – what
genres I like, my favorite artists, my favorite songs from said artists, even naming a single
album from their discography – despite music being an extremely large chunk of how I
spend every day. The rest of the time, the music that people listen to is essentially a black
box, where if you peeked inside, you'd find the Spotify algorithm –a bot who’s sole goal is to
rack up the minutes you listen on their platform – belching out the most sonically identical
songs to the ones you listened to just before to keep you continually engaged. In my mind,
music has become disposable – just some background noise that makes every day just a
little less mundane than the one before it. In my wish to change this and learn more about
myself from a musical standpoint (and create a cool project), I decided to export my Spotify
listening history from the inception of my account, now four years in, in an attempt to
answer the question: What is my sonic self?

In this journey to learn about my “sonic self,” I wish to do the following: uncover temporal
patterns in my listening habits, identify measurable gaps between artist I play frequently
(and artists I actually finish songs by), and observe how my tastes have shifted across
distinct time periods. I also anticipate behavioral signals like skip rate and average play
duration will tell a much more honest story than raw play counts alone.

To address these questions defined in the previous paragraph, I plan to utilize Python and
pandas to clean and combine multiple JSON export files from Spotify. I also wish to export
Last.fm scrobble data from the Last.fm API via the pylast library. The cleaned data will be
exported as a CSV and imported into R, where I will utilize ggplot2 and tidyverse to
produced visualizations, including a listening-time trend, an hour-by-day-of-week
heatmap, top artist and track rankings, skip rate analysis, and a per-artist “era” chart
showing how my taste shifted across six-month windows.

Currently, I anticipate two big issues. The first issue is with Spotify’s skipped field, as it’s
known to be inconsistently populated and can create unreliable results for the skip-rate
analysis I plan to do. The other issue is that my Last.fm data may overlap with my Spotify
streaming data, as well as the fact that Last.fm data doesn’t track the play duration of a
song, making cross-platform comparison and cleaning potentially quite diVicult. This is an
individual project, so collaboration isn’t applicable, and progress will be managed through
iterative development across data cleaning, analysis, and visualization stages.
