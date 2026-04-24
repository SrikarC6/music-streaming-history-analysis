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

        bullet21 = Tex('• Moving away from streaming', font_size=35)
        bullet22 = Tex('• Realized I don\'t know a lot about my music tastes', font_size=35)
        bullet23 = Tex('• Want to learn more about the music I like over the last 4 years', font_size=35)
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

        self.play(FadeIn(bullet21, shift=UP))
        self.play(FadeIn(bullet22, shift=UP))
        self.play(FadeIn(bullet23, shift=UP))
        self.wait(0.5)
        self.play(Write(spotify))
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

        self.play(FadeIn(bullet31, shift=UP))
        self.play(FadeIn(bullet32, shift=UP))
        self.play(FadeIn(bullet33, shift=UP))
        self.play(FadeIn(bullet34, shift=UP))
        self.wait(0.3)
        self.play(Circumscribe(spotify, color=WHITE))
        self.wait(0.2)
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
        self.wait(2)
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
        self.wipe([*self.mobjects], title5)

        GLOBAL_DF['hours'] = GLOBAL_DF['minutes_played'] / 60
        GLOBAL_DF['source_label'] = GLOBAL_DF['source'].replace({"spotify": "Spotify", "apple_music": "Apple Music"})

        monthly = GLOBAL_DF.groupby(['month_label', 'source_label'])['hours'].sum().unstack(fill_value=0)
        if 'Spotify' not in monthly.columns: monthly['Spotify'] = 0
        if 'Apple Music' not in monthly.columns: monthly['Apple Music'] = 0

        total_vals = monthly.sum(axis=1).values
        y_max = int(np.ceil(max(total_vals) / 20.0)) * 20
        x_max = len(monthly)

        apple_box  = Square(side_length=0.2, fill_color="#FC3C44", fill_opacity=1, stroke_width=0)
        apple_text = Tex("Apple Music", font_size=20)
        apple_leg  = VGroup(apple_box, apple_text).arrange(RIGHT, buff=0.15)

        spot_box  = Square(side_length=0.2, fill_color="#1DB954", fill_opacity=1, stroke_width=0)
        spot_text = Tex("Spotify", font_size=20)
        spot_leg  = VGroup(spot_box, spot_text).arrange(RIGHT, buff=0.15)

        legend = VGroup(apple_leg, spot_leg).arrange(RIGHT, buff=0.8)
        legend.next_to(title5, DOWN, buff=0.15).set_x(0)

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

        grid_lines = VGroup()
        for y in range(20, y_max + 1, 20):
            line = Line(
                axes.c2p(0, y), axes.c2p(x_max + 1, y),
                color=GRAY, stroke_width=1, stroke_opacity=0.3
            )
            grid_lines.add(line)

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

        smoothed  = gaussian_filter1d(total_vals, sigma=2)
        trend_pts = [axes.c2p(i + 1, smoothed[i]) for i in range(len(smoothed))]
        trend_line = VMobject(color=PURPLE).set_stroke(width=4).set_points_smoothly(trend_pts)

        self.play(
            Create(axes), Create(grid_lines), Write(y_label),
            Create(x_ticks), Write(x_labels), FadeIn(legend, shift=DOWN)
        )
        self.wait(0.5)
        self.play(
            AnimationGroup(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.02),
            run_time=3
        )
        self.play(Create(trend_line), run_time=2)

        self.next_slide()
        # ---------------- Slide 5.1 ----------------


        # ---------------- Slide 5.2 ----------------
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob is not title5])
        self.add(title5)

        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        heatmap_raw  = GLOBAL_DF.groupby(['day_of_week', 'hour']).size().reset_index(name='n')
        complete_idx = pd.DataFrame(list(iproduct(day_order, range(24))), columns=['day_of_week', 'hour'])
        heatmap_df5   = complete_idx.merge(heatmap_raw, on=['day_of_week', 'hour'], how='left').fillna(0)
        pivot        = heatmap_df5.pivot(index='day_of_week', columns='hour', values='n').reindex(day_order)
        n_max        = float(pivot.values.max())

        low_c  = ManimColor("#1a1a2e")
        high_c = PURPLE
        grid_w, grid_h = 9.5, 2.8
        cell_w = grid_w / 24
        cell_h = grid_h / 7

        cells = VGroup()
        for ri, day in enumerate(day_order):
            for ci in range(24):
                t = float(pivot.loc[day, ci]) / n_max
                cell = Rectangle(
                    width=cell_w, height=cell_h,
                    fill_color=interpolate_color(low_c, high_c, t),
                    fill_opacity=1, stroke_color=WHITE, stroke_width=0.4
                )
                cell.move_to([
                    -grid_w/2 + (ci + 0.5) * cell_w,
                    -grid_h/2 + (ri + 0.5) * cell_h, 0
                ])
                cells.add(cell)

        y_labels = VGroup()
        for ri, day in enumerate(day_order):
            lbl = Tex(day, font_size=15)
            lbl.move_to([-grid_w/2 - lbl.width/2 - 0.18, -grid_h/2 + (ri + 0.5) * cell_h, 0])
            y_labels.add(lbl)

        x_labels = VGroup()
        for hour, label_str in {0: "12 am", 6: "6 am", 12: "12 pm", 18: "6 pm", 23: "11 pm"}.items():
            lbl = Tex(label_str, font_size=15)
            lbl.move_to([-grid_w/2 + (hour + 0.5) * cell_w, -grid_h/2 - 0.32, 0])
            x_labels.add(lbl)

        x_axis_title = Tex("Hour of day", font_size=18).move_to([0, -grid_h/2 - 0.68, 0])

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
            tick = Line([bar_x + bar_w/2, y_p, 0], [bar_x + bar_w/2 + 0.13, y_p, 0],
                        color=WHITE, stroke_width=1.5)
            lbl = Tex(str(int(v)), font_size=13).next_to(tick, RIGHT, buff=0.07)
            cb_ticks.add(tick, lbl)
            v += 50

        chart = VGroup(cells, y_labels, x_labels, x_axis_title, colorbar, cb_outline, plays_title, cb_ticks)
        chart.next_to(title5, DOWN, buff=0.45)
        chart.set_x(0.55)

        self.play(FadeIn(y_labels), FadeIn(x_labels), Write(x_axis_title))
        self.play(Write(cells))
        self.play(Write(colorbar), Write(cb_outline), Write(plays_title), Write(cb_ticks))

        bullet50 = Tex("Observations", font_size=30)
        bullet50.next_to(x_axis_title, direction=DOWN, buff=0.15)
        bullet50.align_to(title5, LEFT)
        self.play(Write(bullet50))

        bullet51 = Tex(r"\mbox{• Music listening has decreased to low point in December 2024, but has been gradually increasing since}", font_size=19)
        bullet52 = Tex(r"• Most listening during late-afternoon to evening (4pm-12am)", font_size=19, tex_environment="flushleft")
        bullet53 = Tex(r"• Highest listening density during weekday evenings, lowest during weekend mornings", font_size=19, tex_environment="flushleft")
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

        artist_hours = GLOBAL_DF.groupby('artist_name')['minutes_played'].sum() / 60
        top_artists  = artist_hours.nlargest(15).sort_values(ascending=True)
        track_plays  = GLOBAL_DF.groupby(['track_name', 'artist_name']).size().reset_index(name='plays')
        top_tracks   = track_plays.nlargest(15, 'plays').sort_values(by='plays', ascending=True)

        max_hours  = top_artists.max()
        x_max_left = int(np.ceil(max_hours / 30) * 30)
        max_plays   = top_tracks['plays'].max()
        x_max_right = int(np.ceil(max_plays / 50) * 50)

        # Axes shifted up so x-labels don't clip at screen bottom
        ax_left = Axes(
            x_range=[0, x_max_left + (x_max_left * 0.18), 30],
            y_range=[0.5, 15.5, 1],
            x_length=4.0, y_length=5.0, tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
            y_axis_config={"include_ticks": False, "include_numbers": False}
        ).move_to([-2.6, -0.5, 0])

        ax_right = Axes(
            x_range=[0, x_max_right + (x_max_right * 0.18), 50],
            y_range=[0.5, 15.5, 1],
            x_length=4.0, y_length=5.0, tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
            y_axis_config={"include_ticks": False, "include_numbers": False}
        ).move_to([4.2, -0.5, 0])

        title_left    = Tex("Top 15 Artists", font_size=24).next_to(ax_left, UP, buff=0.4)
        title_right   = Tex("Top 15 Tracks",  font_size=24).next_to(ax_right, UP, buff=0.4)
        x_label_left  = Tex("Hours", font_size=20).next_to(ax_left,  DOWN, buff=0.2)
        x_label_right = Tex("Plays", font_size=20).next_to(ax_right, DOWN, buff=0.2)

        grid_lines = VGroup()
        for x in range(30, int(x_max_left) + 1, 30):
            grid_lines.add(Line(ax_left.c2p(x, 0.5), ax_left.c2p(x, 15.5), color=GRAY, stroke_opacity=0.3, stroke_width=1))
        for x in range(50, int(x_max_right) + 1, 50):
            grid_lines.add(Line(ax_right.c2p(x, 0.5), ax_right.c2p(x, 15.5), color=GRAY, stroke_opacity=0.3, stroke_width=1))

        bar_height  = 0.28
        bars_left   = VGroup()
        labels_left = VGroup()
        vals_left   = VGroup()
        for i, (artist, hours) in enumerate(top_artists.items(), start=1):
            w   = ax_left.c2p(hours, 0)[0] - ax_left.c2p(0, 0)[0]
            bar = Rectangle(width=w, height=bar_height, fill_color=PURPLE, fill_opacity=1, stroke_width=0)
            bar.move_to(ax_left.c2p(hours / 2, i))
            bars_left.add(bar)
            lbl = Tex(artist, font_size=14).next_to(ax_left.c2p(0, i), LEFT, buff=0.15)
            labels_left.add(lbl)
            val = Tex(str(round(hours, 1)), font_size=14).next_to(bar, RIGHT, buff=0.1)
            vals_left.add(val)

        bars_right   = VGroup()
        labels_right = VGroup()
        vals_right   = VGroup()
        for i, row in enumerate(top_tracks.itertuples(), start=1):
            w   = ax_right.c2p(row.plays, 0)[0] - ax_right.c2p(0, 0)[0]
            bar = Rectangle(width=w, height=bar_height, fill_color=PURPLE, fill_opacity=1, stroke_width=0)
            bar.move_to(ax_right.c2p(row.plays / 2, i))
            bars_right.add(bar)
            lbl_text = f"{row.track_name} ({row.artist_name})"
            lbl = Tex(lbl_text, font_size=11).next_to(ax_right.c2p(0, i), LEFT, buff=0.15)
            labels_right.add(lbl)
            val = Tex(str(row.plays), font_size=14).next_to(bar, RIGHT, buff=0.1)
            vals_right.add(val)

        self.play(
            Create(ax_left), Create(ax_right), Create(grid_lines),
            Write(title_left), Write(title_right),
            Write(x_label_left), Write(x_label_right),
            Write(labels_left), Write(labels_right)
        )
        self.wait(0.5)
        self.play(
            AnimationGroup(*[GrowFromEdge(bar, LEFT) for bar in bars_left],  lag_ratio=0.05),
            AnimationGroup(*[GrowFromEdge(bar, LEFT) for bar in bars_right], lag_ratio=0.05),
            run_time=3
        )
        self.play(Write(vals_left), Write(vals_right))

        self.next_slide()
        
        # --- Camera punch-in ---
        objects_to_scale = Group(*[mob for mob in self.mobjects if mob is not title6])
        
        target_group = VGroup(
            title_right,
            bars_right[-5:],
            labels_right[-5:],
            vals_right[-5:]
        )
        
        scale_factor = config.frame_height / (target_group.height * 1.5)
        target_center = target_group.get_center()
        
        self.play(
            objects_to_scale.animate
            .scale(scale_factor, about_point=target_center)
            .shift(ORIGIN - target_center),
            run_time=1.5
        )

        self.next_slide()
        
        # --- Camera zoom-out ---
        self.play(
            objects_to_scale.animate
            .shift(target_center)
            .scale(1 / scale_factor, about_point=target_center),
            run_time=1.5
        )
        # ---------------- Slide 6.1 ----------------


        # ---------------- Slide 6.2 ----------------
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob is not title6])
        self.add(title6)

        skip_by_artist = (
            GLOBAL_DF.groupby('artist_name')
            .agg(
                plays     = ('track_name', 'count'),
                skip_rate = ('skipped', 'mean'),
                hours     = ('minutes_played', lambda x: x.sum() / 60)
            )
            .reset_index()
        )
        skip_by_artist   = skip_by_artist[skip_by_artist['plays'] >= 20]
        top_skipped      = skip_by_artist.nlargest(12, 'skip_rate').sort_values('skip_rate', ascending=True)
        top_hours_labels = skip_by_artist.nlargest(10, 'hours')

        ax_left = Axes(
            x_range=[0, 1.18, 0.25],
            y_range=[0.5, 12.5, 1],
            x_length=3.5, y_length=5.0, tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
            x_axis_config={"include_numbers": False, "include_ticks": False},
            y_axis_config={"include_ticks": False, "include_numbers": False}
        ).move_to([-3.2, -0.6, 0])

        title_left = Tex("Most-Skipped Artists", font_size=22).next_to(ax_left, UP, buff=0.3)

        sqrt_breaks = [0, 0.10, 0.25, 0.50, 0.75, 1.0]
        y_max_sqrt  = np.sqrt(1.08)
        x_max_hrs   = float(np.ceil(skip_by_artist['hours'].max() / 50) * 50 * 1.12)

        ax_right = Axes(
            x_range=[0, x_max_hrs, 20],
            y_range=[0, y_max_sqrt, 0.2],
            x_length=5.0, y_length=5.0, tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
            x_axis_config={"include_numbers": False, "include_ticks": False},
            y_axis_config={"include_ticks": False, "include_numbers": False}
        ).move_to([2.6, -0.6, 0])

        axis_y_right = ax_right.c2p(0, 0)[1]

        xticks_left = VGroup()
        for pct in [0, 0.25, 0.50, 0.75, 1.0]:
            tick_x = ax_left.c2p(pct, 0)[0]
            tick   = Line([tick_x, axis_y_right, 0], [tick_x, axis_y_right - 0.1, 0], color=WHITE, stroke_width=1.5)
            lbl    = Tex(f"{int(pct * 100)}\\%", font_size=13)
            lbl.move_to([tick_x, axis_y_right - 0.32, 0])
            xticks_left.add(tick, lbl)

        xlabel_left = Tex("Skip rate", font_size=18)
        xlabel_left.move_to([ax_left.get_center()[0], axis_y_right - 0.65, 0])

        grid_left = VGroup(*[
            Line(ax_left.c2p(pct, 0.5), ax_left.c2p(pct, 12.5), color=GRAY, stroke_opacity=0.3, stroke_width=1)
            for pct in [0.25, 0.50, 0.75, 1.0]
        ])

        bar_height  = 0.28
        bars_left   = VGroup()
        labels_left = VGroup()
        vals_left   = VGroup()
        for i, (_, row) in enumerate(top_skipped.iterrows(), start=1):
            w   = ax_left.c2p(row['skip_rate'], 0)[0] - ax_left.c2p(0, 0)[0]
            bar = Rectangle(width=w, height=bar_height, fill_color=PURPLE, fill_opacity=1, stroke_width=0)
            bar.move_to(ax_left.c2p(row['skip_rate'] / 2, i))
            bars_left.add(bar)
            lbl = Tex(row['artist_name'], font_size=13).next_to(ax_left.c2p(0, i), LEFT, buff=0.12)
            labels_left.add(lbl)
            val = Tex(f"{round(row['skip_rate'] * 100)}\\%", font_size=13).next_to(bar, RIGHT, buff=0.08)
            vals_left.add(val)

        title_right  = Tex("Hours vs Skip Rate", font_size=22).next_to(ax_right, UP, buff=0.3)
        ylabel_right = Tex("Skip rate", font_size=18).rotate(90 * DEGREES).next_to(ax_right, LEFT, buff=0.55)

        xticks_right = VGroup()
        for hrs in np.arange(0, x_max_hrs, 20):
            tick_x = ax_right.c2p(hrs, 0)[0]
            tick   = Line([tick_x, axis_y_right, 0], [tick_x, axis_y_right - 0.1, 0], color=WHITE, stroke_width=1.5)
            lbl    = Tex(str(int(hrs)), font_size=13)
            lbl.move_to([tick_x, axis_y_right - 0.32, 0])
            xticks_right.add(tick, lbl)

        xlabel_right = Tex("Hours played", font_size=18)
        xlabel_right.move_to([ax_right.get_center()[0], axis_y_right - 0.65, 0])

        yticks_right = VGroup()
        for br in sqrt_breaks:
            tick_y = ax_right.c2p(0, np.sqrt(br))[1]
            tick_x = ax_right.c2p(0, 0)[0]
            tick   = Line([tick_x - 0.1, tick_y, 0], [tick_x, tick_y, 0], color=WHITE, stroke_width=1.5)
            lbl    = Tex(f"{int(br * 100)}\\%", font_size=13)
            lbl.move_to([tick_x - 0.38, tick_y, 0])
            yticks_right.add(tick, lbl)

        grid_right = VGroup(*[
            Line(ax_right.c2p(0, np.sqrt(br)), ax_right.c2p(x_max_hrs, np.sqrt(br)),
                 color=GRAY, stroke_opacity=0.3, stroke_width=1)
            for br in sqrt_breaks if br > 0
        ])

        plays_min = skip_by_artist['plays'].min()
        plays_max = skip_by_artist['plays'].max()
        dot_r_min, dot_r_max = 0.04, 0.22
        dots = VGroup()
        for _, row in skip_by_artist.iterrows():
            t      = (row['plays'] - plays_min) / (plays_max - plays_min)
            radius = dot_r_min + t * (dot_r_max - dot_r_min)
            dot    = Circle(radius=radius, fill_color="#E13300", fill_opacity=0.55, stroke_width=0)
            dot.move_to(ax_right.c2p(row['hours'], np.sqrt(row['skip_rate'])))
            dots.add(dot)

        top_hours_sorted = top_hours_labels.sort_values('skip_rate', ascending=False)
        label_x_screen   = ax_right.get_right()[0] + 0.2
        chart_y_top      = ax_right.c2p(0, y_max_sqrt)[1]
        chart_y_bot      = ax_right.c2p(0, 0)[1]
        label_ys         = np.linspace(chart_y_top - 0.15, chart_y_bot + 0.15, len(top_hours_sorted))
        leader_group = VGroup()
        for j, (_, row) in enumerate(top_hours_sorted.iterrows()):
            dot_pos   = np.array(ax_right.c2p(row['hours'], np.sqrt(row['skip_rate'])))
            label_pos = np.array([label_x_screen, label_ys[j], 0])
            line      = Line(dot_pos, label_pos, color=GRAY_C, stroke_width=0.7)
            lbl       = Tex(row['artist_name'], font_size=11).next_to(label_pos, RIGHT, buff=0.05)
            leader_group.add(line, lbl)

        self.play(
            Create(ax_left), Create(ax_right),
            Create(grid_left), Create(grid_right),
            Write(title_left), Write(title_right),
            Write(xlabel_left), Write(xlabel_right),
            Write(ylabel_right),
            Write(xticks_left), Write(xticks_right),
            Write(yticks_right), Write(labels_left)
        )
        self.play(
            AnimationGroup(*[GrowFromEdge(bar, LEFT) for bar in bars_left], lag_ratio=0.05),
            FadeIn(dots), run_time=3
        )
        self.play(Write(vals_left), Write(leader_group))

        self.next_slide()
        # ---------------- Slide 6.2 ----------------


        # ---------------- Slide 7.1 ----------------
        title7 = Tex("RQ3: Artist \\& Genre Shifts").to_corner(UL)
        self.wipe([Group(*self.mobjects)], [title7])

        rq3_df = GLOBAL_DF.copy()
        rq3_df['date_parsed'] = pd.to_datetime(rq3_df['date'])
        rq3_df['half_year']   = rq3_df['date_parsed'].apply(
            lambda d: d.replace(month=1 if d.month <= 6 else 7, day=1)
        )

        era_raw = (
            rq3_df.groupby(['half_year', 'artist_name'], as_index=False)['minutes_played'].sum()
        )
        era_raw['hours'] = era_raw['minutes_played'] / 60
        era_data = (
            era_raw.sort_values(['half_year', 'hours', 'artist_name'], ascending=[True, False, True])
            .groupby('half_year', group_keys=False, as_index=False).head(5)
            .sort_values(['half_year', 'hours', 'artist_name'], ascending=[True, True, True])
            .reset_index(drop=True)
        )

        half_years  = sorted(era_data['half_year'].unique())
        all_artists = sorted(era_data['artist_name'].unique())
        n_periods   = len(half_years)

        ARTIST_PALETTE = [
            "#E63946", "#F4A261", "#2A9D8F", "#E9C46A", "#457B9D",
            "#A8DADC", "#264653", "#1D3557", "#F72585", "#7209B7",
            "#3A0CA3", "#4361EE", "#4CC9F0", "#06D6A0", "#118AB2",
            "#FFB703", "#FB8500", "#8338EC", "#3A86FF", "#FF006E",
            "#38B000", "#70E000", "#FFBE0B", "#D62828", "#023E8A",
            "#80B918", "#F48C06", "#B5E48C", "#9EF01A", "#FB5607",
        ]
        artist_color = {a: ARTIST_PALETTE[i % len(ARTIST_PALETTE)] for i, a in enumerate(all_artists)}
        y_max_era = int(np.ceil(era_data.groupby('half_year')['hours'].sum().max() / 20) * 20)

        ax_era = Axes(
            x_range=[0, n_periods + 0.5, 1],
            y_range=[0, y_max_era, 20],
            x_length=12.0,
            y_length=3.5,
            tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_ticks": False, "include_numbers": False}
        )
        y_label_era = Tex("Hours", font_size=20).rotate(90 * DEGREES).next_to(ax_era, LEFT, buff=0.9)
        plot_group_era = VGroup(ax_era, y_label_era)
        plot_group_era.next_to(title7, DOWN, buff=0.35).set_x(0)

        axis_x_era = ax_era.c2p(0, 0)[0]
        yticks_era = VGroup()
        for y_val in range(0, y_max_era + 1, 20):
            tick_y = ax_era.c2p(0, y_val)[1]
            tick   = Line([axis_x_era - 0.12, tick_y, 0], [axis_x_era, tick_y, 0], color=WHITE, stroke_width=2)
            lbl    = Tex(str(y_val), font_size=13)
            lbl.move_to([axis_x_era - 0.45, tick_y, 0])
            yticks_era.add(tick, lbl)

        grid_era = VGroup(*[
            Line(ax_era.c2p(0, y), ax_era.c2p(n_periods + 0.5, y),
                 color=GRAY, stroke_width=1, stroke_opacity=0.3)
            for y in range(20, y_max_era + 1, 20)
        ])

        bar_width = (ax_era.x_length / (n_periods + 0.5)) * 0.75
        bars_era  = VGroup()
        for pi, hy in enumerate(half_years):
            period_df  = era_data[era_data['half_year'] == hy].sort_values('hours', ascending=True)
            cumulative = 0.0
            x_coord    = pi + 0.5
            for _, row in period_df.iterrows():
                h     = row['hours']
                bar_h = ax_era.c2p(0, h)[1] - ax_era.c2p(0, 0)[1]
                bar   = Rectangle(
                    width=bar_width, height=bar_h,
                    fill_color=artist_color[row['artist_name']],
                    fill_opacity=0.9, stroke_width=0
                )
                bar.move_to(ax_era.c2p(x_coord, cumulative + h / 2))
                bars_era.add(bar)
                cumulative += h

        max_date_by_period = rq3_df.groupby('half_year')['date_parsed'].max()
        x_ticks_era  = VGroup()
        x_labels_era = VGroup()
        for pi, hy in enumerate(half_years):
            x_coord  = pi + 0.5
            tick_bot = ax_era.c2p(x_coord, 0)
            tick     = Line(tick_bot, tick_bot + DOWN * 0.12, color=WHITE, stroke_width=2)
            x_ticks_era.add(tick)

            lbl = Tex(hy.strftime("%b '%y"), font_size=13)

            lbl.next_to(tick.get_bottom(), DOWN, buff=0.08)
            lbl.rotate(45 * DEGREES, about_point=lbl.get_corner(UR))
            lbl.shift(LEFT * 0.22)
            x_labels_era.add(lbl)

        # --- Legend ---
        N_COLS_ERA = 10
        legend_items_era = []
        for artist in all_artists:
            box  = Square(side_length=0.16, fill_color=artist_color[artist], fill_opacity=1, stroke_width=0)
            lbl  = Tex(artist, font_size=10)
            item = VGroup(box, lbl).arrange(RIGHT, buff=0.08)
            legend_items_era.append(item)

        rows_era = []
        for i in range(0, len(legend_items_era), N_COLS_ERA):
            chunk = legend_items_era[i:i + N_COLS_ERA]
            row   = VGroup(*chunk).arrange(RIGHT, buff=0.40)
            rows_era.append(row)
        legend_era = VGroup(*rows_era).arrange(DOWN, buff=0.12)
        
        max_width = config.frame_width - 0.8
        if legend_era.width > max_width:
            legend_era.scale(max_width / legend_era.width)
            
        legend_era.next_to(ax_era, DOWN, buff=1.1)

        self.play(
            Create(ax_era), Create(grid_era), Write(y_label_era),
            Write(yticks_era), Create(x_ticks_era), Write(x_labels_era)
        )
        self.wait(0.3)
        self.play(
            AnimationGroup(*[GrowFromEdge(bar, DOWN) for bar in bars_era], lag_ratio=0.03),
            run_time=3
        )
        self.play(FadeIn(legend_era))

        self.next_slide()
        # ---------------- Slide 7.1 ----------------


        # ---------------- Slide 7.2 ----------------
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob is not title7])

        genre_df = rq3_df[rq3_df['genre'].notna() & (rq3_df['genre'] != 'Other')].copy()
        genre_era_raw = (
            genre_df.groupby(['half_year', 'genre'])['minutes_played']
            .sum().div(60).reset_index(name='hours')
        )
        genre_era_raw['pct'] = (
            genre_era_raw['hours']
            / genre_era_raw.groupby('half_year')['hours'].transform('sum')
        )
        genre_pivot = (
            genre_era_raw.pivot(index='half_year', columns='genre', values='pct')
            .fillna(0).sort_index()
        )
        half_years_g = list(genre_pivot.index)
        genres_list  = list(genre_pivot.columns)
        n_periods_g  = len(half_years_g)

        GENRE_COLORS = {
            "Blues":                "#4D908E",
            "Classical":            "#6D597A",
            "Comedy & Spoken Word": "#FF9FB1",
            "Country":              "#BC6C25",
            "Electronic & Dance":   "#F77F00",
            "Gospel & Religious":   "#B5A642",
            "Holiday":              "#6A994E",
            "Instrumental":         "#2D6A4F",
            "Jazz":                 "#577590",
            "Metal":                "#1B4332",
            "Pop":                  "#48CAE4",
            "R&B & Soul":           "#0096C7",
            "Rap & Hip-Hop":        "#4361EE",
            "Rock":                 "#9B5DE5",
            "Singer/Songwriter":    "#C77DFF",
            "Soundtrack & Score":   "#F15BB5",
            "World & Regional":     "#FF006E",
        }

        ax_genre = Axes(
            x_range=[0, n_periods_g + 0.5, 1],
            y_range=[0, 1.0, 0.25],
            x_length=12.0,
            y_length=3.5,
            tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_numbers": False}
        )
        y_label_genre = Tex("Share of listening", font_size=18).rotate(90 * DEGREES).next_to(ax_genre, LEFT, buff=0.9)
        plot_group_genre = VGroup(ax_genre, y_label_genre)
        plot_group_genre.next_to(title7, DOWN, buff=0.35).set_x(0)

        axis_x_g = ax_genre.c2p(0, 0)[0]
        yticks_g = VGroup()
        for pct_val in [0, 0.25, 0.50, 0.75, 1.0]:
            tick_y = ax_genre.c2p(0, pct_val)[1]
            tick   = Line([axis_x_g - 0.1, tick_y, 0], [axis_x_g, tick_y, 0], color=WHITE, stroke_width=1.5)
            lbl    = Tex(f"{int(pct_val * 100)}\\%", font_size=13)
            lbl.move_to([axis_x_g - 0.52, tick_y, 0])
            yticks_g.add(tick, lbl)

        x_ticks_g  = VGroup()
        x_labels_g = VGroup()
        for pi, hy in enumerate(half_years_g):
            x_coord  = pi + 0.5
            tick_bot = ax_genre.c2p(x_coord, 0)
            tick     = Line(tick_bot, tick_bot + DOWN * 0.12, color=WHITE, stroke_width=2)
            x_ticks_g.add(tick)

            lbl = Tex(hy.strftime("%b '%y"), font_size=13)

            lbl.next_to(tick.get_bottom(), DOWN, buff=0.08)
            lbl.rotate(45 * DEGREES, about_point=lbl.get_corner(UR))
            lbl.shift(LEFT * 0.22)
            x_labels_g.add(lbl)

        grid_genre = VGroup(*[
            Line(ax_genre.c2p(0, y), ax_genre.c2p(n_periods_g + 0.5, y),
                 color=GRAY, stroke_width=1, stroke_opacity=0.3)
            for y in [0.25, 0.50, 0.75, 1.0]
        ])

        area_polys = VGroup()
        cumsum_g   = np.zeros(n_periods_g)
        x_coords_g = [pi + 0.5 for pi in range(n_periods_g)]
        for genre in genres_list:
            pct_vals  = genre_pivot[genre].values
            upper_g   = cumsum_g + pct_vals
            upper_pts = [ax_genre.c2p(x, upper_g[i])  for i, x in enumerate(x_coords_g)]
            lower_pts = [ax_genre.c2p(x, cumsum_g[i]) for i, x in enumerate(x_coords_g)]
            poly      = Polygon(
                *(upper_pts + list(reversed(lower_pts))),
                fill_color=GENRE_COLORS.get(genre, "#888888"),
                fill_opacity=0.85, stroke_width=0.5, stroke_color=WHITE
            )
            area_polys.add(poly)
            cumsum_g = upper_g

        N_COLS_GENRE = 9
        legend_items_genre = []
        for genre in genres_list:
            box  = Square(side_length=0.22, fill_color=GENRE_COLORS.get(genre, "#888888"), fill_opacity=1, stroke_width=0)
            lbl  = Tex(genre.replace("&", r"\&"), font_size=13)
            item = VGroup(box, lbl).arrange(RIGHT, buff=0.12)
            legend_items_genre.append(item)

        rows_genre = []
        for i in range(0, len(legend_items_genre), N_COLS_GENRE):
            chunk = legend_items_genre[i:i + N_COLS_GENRE]
            row   = VGroup(*chunk).arrange(RIGHT, buff=0.35)
            rows_genre.append(row)
        legend_genre = VGroup(*rows_genre).arrange(DOWN, buff=0.15)
        legend_genre.next_to(ax_genre, DOWN, buff=1.1)

        self.play(
            Create(ax_genre), Create(grid_genre), Write(y_label_genre),
            Write(yticks_g), Create(x_ticks_g), Write(x_labels_g)
        )
        self.wait(0.3)
        self.play(
            AnimationGroup(*[FadeIn(poly) for poly in area_polys], lag_ratio=0.08),
            run_time=3
        )
        self.play(FadeIn(legend_genre))

        self.next_slide()
        # ---------------- Slide 7.2 ----------------


        # ---------------- Slide 8.1 ----------------
        title8 = Tex("RQ4: Platform Differences").to_corner(UL)
        self.wipe([Group(*self.mobjects)], [title8])

        if 'source_label' not in GLOBAL_DF.columns:
            GLOBAL_DF['source_label'] = GLOBAL_DF['source'].replace({"spotify": "Spotify", "apple_music": "Apple Music"})
        GLOBAL_DF['skipped_num'] = GLOBAL_DF['skipped'].astype(float)

        grouped   = GLOBAL_DF.groupby('source_label')
        plays     = grouped.size()
        hours     = grouped['minutes_played'].sum() / 60
        avg_min   = grouped['minutes_played'].mean()
        skip_rate = grouped['skipped_num'].mean() * 100

        def safe_get(series, key, fmt="{x}"):
            return fmt.format(x=series[key]) if key in series else "0"

        am_row  = ["Apple Music",
                   safe_get(plays, "Apple Music", "{x:,}"),
                   safe_get(hours, "Apple Music", "{x:.1f}"),
                   safe_get(avg_min, "Apple Music", "{x:.2f}"),
                   safe_get(skip_rate, "Apple Music", r"{x:.1f}\%")]
        sp_row  = ["Spotify",
                   safe_get(plays, "Spotify", "{x:,}"),
                   safe_get(hours, "Spotify", "{x:.1f}"),
                   safe_get(avg_min, "Spotify", "{x:.2f}"),
                   safe_get(skip_rate, "Spotify", r"{x:.1f}\%")]
        headers = [r"\textbf{Source}", r"\textbf{Plays}", r"\textbf{Hours}",
                   r"\textbf{Avg Min / Play}", r"\textbf{Skip Rate}"]

        mob_table_data = [[Tex(item, font_size=32) for item in row] for row in [headers, am_row, sp_row]]
        table = MobjectTable(mob_table_data, include_outer_lines=False,
                             line_config={"stroke_width": 1, "color": GRAY})
        table.get_vertical_lines().set_opacity(0)
        h_lines = table.get_horizontal_lines()
        for i, line in enumerate(h_lines):
            if i == 1: line.set_color(WHITE).set_stroke(width=2).set_opacity(1)
            else:      line.set_opacity(0)

        caption     = Tex("Listening behavior comparison: Spotify vs Apple Music.", font_size=36)
        table_group = VGroup(caption, table).arrange(DOWN, buff=0.8)
        table_group.next_to(title8, DOWN, buff=1.2).set_x(0)

        self.play(Write(caption))
        self.wait(0.2)
        self.play(Create(h_lines[1]), run_time=1)
        self.play(
            AnimationGroup(*[Write(row) for row in table.get_rows()], lag_ratio=0.15),
            run_time=3
        )

        self.next_slide()
        # ---------------- Slide 8.1 ----------------


        # ---------------- Slide 8.2 ----------------
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob is not title8])

        def clean_platform(p):
            p = str(p).lower()
            if "android" in p: return "Android"
            if "osx" in p or "mac" in p: return "Mac"
            if "windows" in p: return "Windows"
            if any(x in p for x in ["cast", "yamaha", "google"]): return "Cast / Speaker"
            if "chrome" in p: return "Chrome"
            if "fuse" in p or "tilt" in p: return "Apple Music"
            return "Other"

        if 'platform_clean' not in GLOBAL_DF.columns:
            GLOBAL_DF['platform_clean'] = GLOBAL_DF['platform'].apply(clean_platform)

        platform_summary = GLOBAL_DF.groupby('platform_clean')['minutes_played'].sum() / 60
        platform_summary = platform_summary.sort_values(ascending=True)
        max_hours   = platform_summary.max()
        x_max       = int(np.ceil(max_hours / 100.0)) * 100
        n_platforms = len(platform_summary)

        axes = Axes(
            x_range=[0, x_max + (x_max * 0.15), 100],
            y_range=[0.5, n_platforms + 0.5, 1],
            x_length=11, y_length=4.5, tips=False,
            axis_config={"color": WHITE, "stroke_width": 2},
            y_axis_config={"include_ticks": False, "include_numbers": False}
        ).next_to(title8, DOWN, buff=0.8).set_x(0)

        x_label = Tex("Hours", font_size=24).next_to(axes, DOWN, buff=0.4)

        grid_lines = VGroup()
        for x in range(100, int(x_max) + 1, 100):
            grid_lines.add(Line(axes.c2p(x, 0.5), axes.c2p(x, n_platforms + 0.5),
                                color=GRAY, stroke_opacity=0.3, stroke_width=1))

        x_ticks = VGroup()
        x_tick_labels = VGroup()
        for x in range(0, int(x_max) + 1, 100):
            tick  = Line(axes.c2p(x, 0.5), axes.c2p(x, 0.5) + DOWN * 0.1, color=WHITE, stroke_width=2)
            x_ticks.add(tick)
            t_lbl = Tex(str(x), font_size=18).next_to(tick, DOWN, buff=0.15)
            x_tick_labels.add(t_lbl)

        palette = {
            "Android": "#66C2A5", "Mac": "#A6D854", "Cast / Speaker": "#8DA0CB",
            "Apple Music": "#FC8D62", "Windows": "#E5C494", "Chrome": "#E78AC3", "Other": "#FFD92F"
        }

        bars = VGroup(); y_labels = VGroup(); vals = VGroup()
        bar_height = 0.75
        for i, (plat, hours) in enumerate(platform_summary.items(), start=1):
            w     = axes.c2p(hours, 0)[0] - axes.c2p(0, 0)[0]
            color = palette.get(plat, WHITE)
            bar   = Rectangle(width=w, height=bar_height, fill_color=color, fill_opacity=1, stroke_width=0)
            bar.move_to(axes.c2p(hours / 2, i))
            bars.add(bar)
            lbl = Tex(plat, font_size=20).next_to(axes.c2p(0, i), LEFT, buff=0.2)
            y_labels.add(lbl)
            val = Tex(str(int(round(hours, 0))), font_size=20).next_to(bar, RIGHT, buff=0.15)
            vals.add(val)

        self.play(
            Create(axes), Create(grid_lines),
            Create(x_ticks), Write(x_tick_labels),
            Write(x_label), Write(y_labels)
        )
        self.wait(0.3)
        self.play(
            AnimationGroup(*[GrowFromEdge(bar, LEFT) for bar in bars], lag_ratio=0.1),
            run_time=2.5
        )
        self.play(Write(vals))

        self.next_slide()
        # ---------------- Slide 8.2 ----------------


        # ---------------- Slide 9 ----------------
        title9 = Tex("Conclusion").to_corner(UL)
        self.wipe(Group(*self.mobjects), title9)

        bullet91 = Tex("• Behavioral Signatures: Late-evening weekday listening dominates,\\ with distinct shifts in genre and era preferences over time.", font_size=28, tex_environment="flushleft")
        bullet92 = Tex("• Engagement Nuance: Top artists highlight true long-term favorites,\\ while skip rates reveal passive, habit-driven consumption.", font_size=28, tex_environment="flushleft")
        bullet93 = Tex("• Methodological Limits: Play counts cannot distinguish active from passive\\ listening, and platform differences are confounded by life stages.", font_size=28, tex_environment="flushleft")
        bullet94 = Tex("• Data Constraints: While highly reliable, validity is limited by platform\\ quirks like unrecorded incognito sessions and missing track durations.", font_size=28, tex_environment="flushleft")
        bullet95 = Tex("• Future Extensions: Next steps include integrating API audio features\\ (tempo, energy) and academic calendars to explore mood-based clusters.", font_size=28, tex_environment="flushleft")

        bullets9 = VGroup(bullet91, bullet92, bullet93, bullet94, bullet95).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        bullets9.next_to(title9, DOWN, buff=0.8).align_to(title9, LEFT).shift(RIGHT * 0.5)

        self.play(FadeIn(bullet91, shift=UP))
        self.play(FadeIn(bullet92, shift=UP))
        self.play(FadeIn(bullet93, shift=UP))
        self.play(FadeIn(bullet94, shift=UP))
        self.play(FadeIn(bullet95, shift=UP))
        
        self.next_slide()
        # ---------------- Slide 9 ----------------


        # ---------------- Slide 10 ----------------
        title10 = Tex("Thanks for Listening!").scale(1.5).move_to(ORIGIN)
        bullet10 = Tex("Made with Manim", font_size=28).next_to(title10, DOWN, buff=0.5)

        self.wipe(Group(*self.mobjects), title10)
        self.play(Write(bullet10))
        self.wait(1)

        banner = ManimBanner().scale(0.5)
        self.play(ReplacementTransform(Group(title10, bullet10), banner))
        self.wait(0.5)
        self.play(banner.expand())
        # ---------------- Slide 10 ----------------