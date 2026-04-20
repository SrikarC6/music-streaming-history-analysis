from manim import *
from manim_slides import Slide
import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter1d
from datetime import datetime
from itertools import product as iproduct

baskerville_template = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
)
baskerville_template.add_to_preamble(r"\usepackage{fontspec}")
baskerville_template.add_to_preamble(r"\setmainfont{Baskerville}")
Tex.set_default(tex_template=baskerville_template)

GLOBAL_DF = pd.read_csv("/Users/srikarc/College/sp-26/stt-180/ho-stt-180/Code/listening-history-clean.csv")
GLOBAL_DF = GLOBAL_DF[GLOBAL_DF['is_short_play'] == False]
for col in ['artist_name', 'track_name', 'album_name']:
    GLOBAL_DF[col] = GLOBAL_DF[col].astype(str).str.replace("&", r"\&").str.replace("$", r"\$").str.replace("%", r"\%")

class Presentation(Slide):
    def construct(self):

        # ---------------- Slide 1 ----------------
        title1 = Tex('Music Analytics').scale(2)

        caption1 = Tex('Understanding my "Sonic Self"', font_size=40)
        caption1.next_to(title1, direction=DOWN)

        author = Tex('Srikar Chitturi', font_size=40)
        author.next_to(title1, direction=DOWN)

        self.play(FadeIn(title1))
        self.wait(0.5)
        self.play(FadeIn(caption1, shift=UP))

        self.next_slide()

        self.play(Transform(caption1, author))

        self.next_slide()
        # ---------------- Slide 1 ----------------


        # ---------------- Slide 2 ----------------
        title2 = Tex('Introduction').scale(1.5).to_corner(UL)

        bullet21 = Tex('• Moving away from streaming', font_size=28)
        bullet22 = Tex('• Realized I don\'t know a lot about my music tastes', font_size=28)
        bullet23 = Tex('• Want to learn more about the music I like over the last 4 years', font_size=28)
        bullets2 = VGroup(bullet21, bullet22, bullet23).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        bullets2.next_to(title2, direction=DOWN, buff=0.5).align_to(title2, LEFT)

        spotify = SVGMobject('spotify-icon.svg').scale(0.8)

        apple_music = SVGMobject('apple-music-icon.svg').scale(0.8)
        apple_music[0].set_color("#FC3C44")
        apple_music[1:].set_color(WHITE)

        logos = VGroup(spotify, apple_music).arrange(RIGHT, buff=0.6)
        logos.next_to(bullet23, direction=DOWN, buff=0.6)
        logos.move_to([0, logos.get_y(), 0])

        self.wipe([title1, caption1, author], [title2])

        self.next_slide()

        self.play(FadeIn(bullet21, shift=UP))
        self.play(FadeIn(bullet22, shift=UP))
        self.play(FadeIn(bullet23, shift=UP))
        self.wait(0.5)
        self.play(Write(spotify))
        self.wait(0.7)
        self.play(Write(apple_music))

        self.next_slide()

        self.play(logos.animate.scale(0.5).to_corner(DR, buff=0.3))
        # ---------------- Slide 2 ----------------


        # ---------------- Slide 3 ----------------
        title3 = Tex('Questions to Answer').scale(1.5).to_corner(UL)
        self.wipe([title2, bullets2], title3)

        bullet311 = Tex('1. How has my total listening volume trended over time, and when during the', font_size=28)
        bullet312 = Tex('day and week do I listen most?', font_size=28).next_to(bullet311, direction=DOWN, buff=0.15, aligned_edge=LEFT)
        bullet31 = VGroup(bullet311, bullet312)

        bullet321 = Tex('2. Which artists and tracks do I engage with most deeply, and which do I skip', font_size=28)
        bullet322 = Tex('the most often?', font_size=28).next_to(bullet321, direction=DOWN, buff=0.15, aligned_edge=LEFT)
        bullet32 = VGroup(bullet321, bullet322)

        bullet33 = Tex('3. How have my artist and genre preferences shifted across distinct time periods?', font_size=28)
        bullet34 = Tex('4. Do my listening habits differ meaningfully between Spotify and Apple Music?', font_size=28)

        bullets3 = VGroup(bullet31, bullet32, bullet33, bullet34).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        bullets3.next_to(title3, direction=DOWN, buff=0.5).align_to(title3, LEFT)

        self.next_slide()

        self.play(FadeIn(bullet31, shift=UP))
        self.play(FadeIn(bullet32, shift=UP))
        self.play(FadeIn(bullet33, shift=UP))
        self.play(FadeIn(bullet34, shift=UP))
        self.wait(0.2)
        self.play(Circumscribe(spotify, color=WHITE))
        self.wait(0.3)
        self.play(Circumscribe(apple_music, color=WHITE))
        # ---------------- Slide 3 ----------------


        # ---------------- Slide 4 ----------------
        title4 = Tex("How?").scale(2)
        diagram_shift = RIGHT

        self.next_slide()
        self.wipe([title3, bullets3], [title4])
        self.wait()
        self.play(title4.animate.scale(0.75).to_corner(UL))
        self.wait(0.6)

        self.play(
            logos.animate
            .arrange(DOWN, buff=1)
            .scale(1.25)
            .next_to(title4, direction=DOWN, buff=1.1)
            .align_to(title4, LEFT)
            .shift(diagram_shift)
        )
        self.wait(0.6)

        convergence_point41 = LEFT * 3.5 + diagram_shift

        lastfm = SVGMobject('lastfm-icon.svg').scale(0.4)
        lastfm.move_to(apple_music).match_height(apple_music)

        arrow_top41 = Arrow(start=spotify.get_right(), end=convergence_point41, buff=0.1, tip_length=0.15)
        arrow_bottom41 = Arrow(start=apple_music.get_right(), end=convergence_point41, buff=0.1, tip_length=0.15)

        apple_music_backup = apple_music.copy()
        self.play(ReplacementTransform(apple_music, lastfm))
        self.wait(4)
        self.play(ReplacementTransform(lastfm, apple_music_backup))
        self.wait()
        apple_music = apple_music_backup

        data = SVGMobject('data-icon.svg').scale(0.4)
        data[0].set_color(WHITE)
        data.next_to(convergence_point41, buff=-0.025)

        convergence_point42 = RIGHT * 0.5 + diagram_shift
        arrow42 = Arrow(start=data.get_right(), end=convergence_point42, buff=0.1, tip_length=0.15)

        r = SVGMobject('r-icon.svg').scale(0.4)
        r.next_to(arrow42, buff=0.1)

        self.play(Create(arrow_top41), Create(arrow_bottom41))
        self.play(Write(data))
        self.play(Create(arrow42))
        self.play(Write(r))

        angles43 = [40, 15, -15, -40]
        horizontal_distance = 2
        arrows43 = VGroup(*[
            Arrow(
                start=r.get_right(),
                end=r.get_right() + RIGHT * horizontal_distance + UP * (horizontal_distance * np.tan(angle * DEGREES)),
                buff=0.1,
                tip_length=0.15
            )
            for angle in angles43
        ])
        self.play(Create(arrows43))

        rq_labels = ["RQ1", "RQ2", "RQ3", "RQ4"]
        text_group = VGroup(*[
            Tex(rq_labels[i], font_size=28).next_to(arrow.get_end(), RIGHT, buff=0.1)
            for i, arrow in enumerate(arrows43)
        ])
        self.play(Write(text_group))

        self.next_slide()
        # ---------------- Slide 4 ----------------


        # ---------------- Slide 5.1 ----------------
        title5 = Tex("RQ1: Temporal Patterns").to_corner(UL)
        self.play(FadeOut(Group(*self.mobjects)))
        self.play(FadeIn(title5))

        self.next_slide()

        # --- Data ---
        GLOBAL_DF['hours'] = GLOBAL_DF['minutes_played'] / 60
        GLOBAL_DF['source_label'] = GLOBAL_DF['source'].replace({"spotify": "Spotify", "apple_music": "Apple Music"})

        monthly = GLOBAL_DF.groupby(['month_label', 'source_label'])['hours'].sum().unstack(fill_value=0)
        if 'Spotify' not in monthly.columns: monthly['Spotify'] = 0
        if 'Apple Music' not in monthly.columns: monthly['Apple Music'] = 0

        total_vals = monthly.sum(axis=1).values
        y_max = int(np.ceil(max(total_vals) / 20.0)) * 20
        x_max = len(monthly)

        # --- Legend ---
        apple_box  = Square(side_length=0.2, fill_color="#FC3C44", fill_opacity=1, stroke_width=0)
        apple_text = Tex("Apple Music", font_size=20)
        apple_leg  = VGroup(apple_box, apple_text).arrange(RIGHT, buff=0.15)

        spot_box  = Square(side_length=0.2, fill_color="#1DB954", fill_opacity=1, stroke_width=0)
        spot_text = Tex("Spotify", font_size=20)
        spot_leg  = VGroup(spot_box, spot_text).arrange(RIGHT, buff=0.15)

        legend = VGroup(apple_leg, spot_leg).arrange(RIGHT, buff=0.8)
        legend.next_to(title5, DOWN, buff=0.15).set_x(0)

        # --- Axes ---
        axes = Axes(
            x_range=[0, x_max + 1, 1],
            y_range=[0, y_max, 20],
            x_length=11,
            y_length=4.2,
            tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
            x_axis_config={"include_ticks": False},
            y_axis_config={"numbers_to_include": np.arange(0, y_max + 1, 20)}
        )

        y_label = Tex("Hours", font_size=22).rotate(90 * DEGREES).next_to(axes, LEFT, buff=0.35)

        plot_base = VGroup(axes, y_label)
        plot_base.next_to(legend, DOWN, buff=0.25).set_x(0)

        # --- Grid lines ---
        grid_lines = VGroup()
        for y in range(20, y_max + 1, 20):
            line = Line(
                axes.c2p(0, y), axes.c2p(x_max + 1, y),
                color=GRAY, stroke_width=1, stroke_opacity=0.3
            )
            grid_lines.add(line)

        # --- Bars ---
        bar_width = (axes.x_length / (x_max + 1)) * 0.85
        bars = VGroup()
        for i, month in enumerate(monthly.index):
            x_coord = i + 1
            s_val = monthly.loc[month, 'Spotify']
            a_val = monthly.loc[month, 'Apple Music']

            if s_val > 0:
                s_height = axes.c2p(0, s_val)[1] - axes.c2p(0, 0)[1]
                s_rect = Rectangle(
                    width=bar_width, height=s_height,
                    fill_color="#1DB954", fill_opacity=1, stroke_width=0
                )
                s_rect.move_to(axes.c2p(x_coord, s_val / 2))
                bars.add(s_rect)

            if a_val > 0:
                a_height = axes.c2p(0, a_val)[1] - axes.c2p(0, 0)[1]
                a_rect = Rectangle(
                    width=bar_width, height=a_height,
                    fill_color="#FC3C44", fill_opacity=1, stroke_width=0
                )
                a_rect.move_to(axes.c2p(x_coord, s_val + (a_val / 2)))
                bars.add(a_rect)

        # --- X-axis ticks and labels ---
        x_ticks  = VGroup()
        x_labels = VGroup()
        for i, month in enumerate(monthly.index):
            x_coord = i + 1
            if i % 3 == 0:
                tick_bottom = axes.c2p(x_coord, 0)
                tick = Line(
                    start=tick_bottom,
                    end=tick_bottom + DOWN * 0.12,
                    color=WHITE, stroke_width=2
                )
                x_ticks.add(tick)

                dt = datetime.strptime(month, "%Y-%m")
                lbl = Tex(dt.strftime("%b '%y"), font_size=15)
                lbl.next_to(tick.get_bottom(), DOWN, buff=0.08)
                lbl.rotate(45 * DEGREES, about_point=lbl.get_corner(UR))
                lbl.shift(LEFT * 0.28)
                x_labels.add(lbl)

        # --- Trend line ---
        smoothed  = gaussian_filter1d(total_vals, sigma=2)
        trend_pts = [axes.c2p(i + 1, smoothed[i]) for i in range(len(smoothed))]
        trend_line = VMobject(color=PURPLE).set_stroke(width=4).set_points_smoothly(trend_pts)

        self.play(
            Create(axes),
            Create(grid_lines),
            Write(y_label),
            Create(x_ticks),
            Write(x_labels),
            FadeIn(legend, shift=DOWN)
        )
        self.wait(0.5)
        self.play(Create(bars), run_time=3)
        self.play(Create(trend_line), run_time=2)

        self.next_slide()
        # ---------------- Slide 5.1 ----------------


        # ---------------- Slide 5.2 ----------------
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob is not title5])

        # --- Data ---
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        heatmap_raw  = GLOBAL_DF.groupby(['day_of_week', 'hour']).size().reset_index(name='n')
        complete_idx = pd.DataFrame(list(iproduct(day_order, range(24))), columns=['day_of_week', 'hour'])
        heatmap_df5   = complete_idx.merge(heatmap_raw, on=['day_of_week', 'hour'], how='left').fillna(0)
        pivot        = heatmap_df5.pivot(index='day_of_week', columns='hour', values='n').reindex(day_order)
        n_max        = float(pivot.values.max())

        low_c  = ManimColor("#1a1a2e")
        high_c = ManimColor("#1DB954")

        grid_w, grid_h = 9.5, 2.8
        cell_w = grid_w / 24
        cell_h = grid_h / 7

        # --- Cells ---
        cells = VGroup()
        for ri, day in enumerate(day_order):
            for ci in range(24):
                t = float(pivot.loc[day, ci]) / n_max
                cell = Rectangle(
                    width=cell_w, height=cell_h,
                    fill_color=interpolate_color(low_c, high_c, t),
                    fill_opacity=1,
                    stroke_color=WHITE, stroke_width=0.4
                )
                cell.move_to([
                    -grid_w/2 + (ci + 0.5) * cell_w,
                    -grid_h/2 + (ri + 0.5) * cell_h,
                    0
                ])
                cells.add(cell)

        # --- Y-axis labels ---
        y_labels = VGroup()
        for ri, day in enumerate(day_order):
            lbl = Tex(day, font_size=15)
            lbl.move_to([
                -grid_w/2 - lbl.width/2 - 0.18,
                -grid_h/2 + (ri + 0.5) * cell_h,
                0
            ])
            y_labels.add(lbl)

        # --- X-axis labels ---
        x_labels = VGroup()
        for hour, label_str in {0: "12 am", 6: "6 am", 12: "12 pm", 18: "6 pm", 23: "11 pm"}.items():
            lbl = Tex(label_str, font_size=15)
            lbl.move_to([
                -grid_w/2 + (hour + 0.5) * cell_w,
                -grid_h/2 - 0.32,
                0
            ])
            x_labels.add(lbl)

        x_axis_title = Tex("Hour of day", font_size=18).move_to([0, -grid_h/2 - 0.68, 0])

        # --- Colorbar ---
        bar_x = grid_w/2 + 1.15
        bar_w = 0.28
        n_seg = 60

        colorbar = VGroup()
        for k in range(n_seg):
            t = k / (n_seg - 1)
            seg = Rectangle(
                width=bar_w, height=grid_h / n_seg,
                fill_color=interpolate_color(low_c, high_c, t),
                fill_opacity=1, stroke_width=0
            )
            seg.move_to([bar_x, -grid_h/2 + (k + 0.5) * (grid_h / n_seg), 0])
            colorbar.add(seg)

        cb_outline = Rectangle(
            width=bar_w, height=grid_h,
            stroke_color=WHITE, stroke_width=1.5, fill_opacity=0
        ).move_to([bar_x, 0, 0])

        plays_title = Tex("Plays", font_size=16).move_to([bar_x, grid_h/2 + 0.32, 0])

        cb_ticks = VGroup()
        v = 0
        while v <= n_max:
            t   = v / n_max
            y_p = -grid_h/2 + t * grid_h
            tick = Line(
                [bar_x + bar_w/2, y_p, 0],
                [bar_x + bar_w/2 + 0.13, y_p, 0],
                color=WHITE, stroke_width=1.5
            )
            lbl = Tex(str(int(v)), font_size=13).next_to(tick, RIGHT, buff=0.07)
            cb_ticks.add(tick, lbl)
            v += 50

        # --- Assemble and position ---
        chart = VGroup(cells, y_labels, x_labels, x_axis_title, colorbar, cb_outline, plays_title, cb_ticks)
        chart.next_to(title5, DOWN, buff=0.45)
        chart.set_x(0.55)

        self.play(FadeIn(y_labels), FadeIn(x_labels), Write(x_axis_title))
        self.play(Write(cells))
        self.play(
            Write(colorbar), Write(cb_outline),
            Write(plays_title), Write(cb_ticks)
        )

        # --- Observations ---
        bullet50 = Tex("Observations", font_size=30)
        bullet50.next_to(x_axis_title, direction=DOWN, buff=0.15)
        bullet50.align_to(title5, LEFT)

        self.play(Write(bullet50))

        bullet51 = Tex("• Music listening has decreased to low point in December 2024, but has been gradually increasing since", font_size=19)
        bullet52 = Tex("• Most listening during late-afternoon to evening (4pm-12am)", font_size=19)
        bullet53 = Tex("• Highest listening density during weekday evenings, lowest during weekend mornings", font_size=19)

        bullets5 = VGroup(bullet51, bullet52, bullet53).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        bullets5.next_to(bullet50, direction=DOWN, buff=0.3).align_to(bullet50, LEFT)

        self.play(FadeIn(bullet51, shift=UP))
        self.play(FadeIn(bullet52, shift=UP))
        self.play(FadeIn(bullet53, shift=UP))

        self.next_slide()
        # ---------------- Slide 5.2 ----------------


        # ---------------- Slide 6.1 ----------------
        title6 = Tex("RQ2: Engagement").to_corner(UL)
        self.wipe(Group(*self.mobjects), title6)

        # --- 1. DATA PREP ---
        artist_hours = GLOBAL_DF.groupby('artist_name')['minutes_played'].sum() / 60
        top_artists = artist_hours.nlargest(15).sort_values(ascending=True)
        track_plays = GLOBAL_DF.groupby(['track_name', 'artist_name']).size().reset_index(name='plays')
        top_tracks = track_plays.nlargest(15, 'plays').sort_values(by='plays', ascending=True)

        max_hours = top_artists.max()
        x_max_left = int(np.ceil(max_hours / 30) * 30)
        
        max_plays = top_tracks['plays'].max()
        x_max_right = int(np.ceil(max_plays / 50) * 50)

        # --- 2. EXPLICIT AXES POSITIONING (SHIFTED RIGHT) ---
        ax_left = Axes(
            x_range=[0, x_max_left + (x_max_left * 0.18), 30],
            y_range=[0.5, 15.5, 1],
            x_length=4.0,
            y_length=5.0,
            tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
            y_axis_config={"include_ticks": False, "include_numbers": False}
        ).move_to([-2.6, -0.8, 0]) # Shifted right from -3.5 to prevent left cut-off

        ax_right = Axes(
            x_range=[0, x_max_right + (x_max_right * 0.18), 50],
            y_range=[0.5, 15.5, 1],
            x_length=4.0,
            y_length=5.0,
            tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
            y_axis_config={"include_ticks": False, "include_numbers": False}
        ).move_to([4.2, -0.8, 0]) # Shifted right from 3.5 to fill the empty margin

        # --- Titles & X-Axis Labels ---
        title_left = Tex("Top 15 Artists", font_size=24).next_to(ax_left, UP, buff=0.4)
        title_right = Tex("Top 15 Tracks", font_size=24).next_to(ax_right, UP, buff=0.4)
        
        x_label_left = Tex("Hours", font_size=20).next_to(ax_left, DOWN, buff=0.3)
        x_label_right = Tex("Plays", font_size=20).next_to(ax_right, DOWN, buff=0.3)

        # --- Vertical Gridlines ---
        grid_lines = VGroup()
        for x in range(30, int(x_max_left) + 1, 30):
            grid_lines.add(Line(ax_left.c2p(x, 0.5), ax_left.c2p(x, 15.5), color=GRAY, stroke_opacity=0.3, stroke_width=1))
        for x in range(50, int(x_max_right) + 1, 50):
            grid_lines.add(Line(ax_right.c2p(x, 0.5), ax_right.c2p(x, 15.5), color=GRAY, stroke_opacity=0.3, stroke_width=1))

        # --- Left Chart (Artists) ---
        bars_left = VGroup()
        labels_left = VGroup()
        vals_left = VGroup()
        bar_height = 0.28

        for i, (artist, hours) in enumerate(top_artists.items(), start=1):
            w = ax_left.c2p(hours, 0)[0] - ax_left.c2p(0, 0)[0]
            
            bar = Rectangle(width=w, height=bar_height, fill_color=PURPLE, fill_opacity=1, stroke_width=0)
            bar.move_to(ax_left.c2p(hours / 2, i))
            bars_left.add(bar)

            lbl = Tex(artist, font_size=14).next_to(ax_left.c2p(0, i), LEFT, buff=0.15)
            labels_left.add(lbl)

            val = Tex(str(round(hours, 1)), font_size=14).next_to(bar, RIGHT, buff=0.1)
            vals_left.add(val)

        # --- Right Chart (Tracks) ---
        bars_right = VGroup()
        labels_right = VGroup()
        vals_right = VGroup()

        for i, row in enumerate(top_tracks.itertuples(), start=1):
            plays = row.plays
            w = ax_right.c2p(plays, 0)[0] - ax_right.c2p(0, 0)[0]
            
            bar = Rectangle(width=w, height=bar_height, fill_color=PURPLE, fill_opacity=1, stroke_width=0)
            bar.move_to(ax_right.c2p(plays / 2, i))
            bars_right.add(bar)

            lbl_text = f"{row.track_name} ({row.artist_name})"
            lbl = Tex(lbl_text, font_size=11).next_to(ax_right.c2p(0, i), LEFT, buff=0.15)
            labels_right.add(lbl)

            val = Tex(str(plays), font_size=14).next_to(bar, RIGHT, buff=0.1)
            vals_right.add(val)

        # --- Animate ---
        self.play(
            Create(ax_left), Create(ax_right),
            Create(grid_lines),
            Write(title_left), Write(title_right),
            Write(x_label_left), Write(x_label_right),
            Write(labels_left), Write(labels_right)
        )
        self.wait(0.5)
        
        self.play(
            Create(bars_left), 
            Create(bars_right), 
            run_time=3
        )
        self.play(
            Write(vals_left), 
            Write(vals_right)
        )

        self.next_slide()
        # ---------------- Slide 6.1 ----------------

        # ---------------- Slide 6.2 ----------------
        
        # ---------------- Slide 6.2 ----------------

class Test(Slide):
    def construct(self):
        pass