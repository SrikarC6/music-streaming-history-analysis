from manim import *
from manim_slides import Slide

class Presentation(Slide):
    def construct(self):
        # ---------------- Slide 1 ----------------
        title1 = Text('Music Analytics').scale(2)
        caption1 = Text('Understanding my "Sonic Self"', font_size=40)
        caption1.next_to(title1, direction=DOWN)
        author = Text('Srikar Chitturi', font_size=40)
        author.next_to(title1, direction=DOWN)
        
        self.play(FadeIn(title1))
        self.wait(0.5)
        self.play(FadeIn(caption1, shift=UP))

        self.next_slide()

        self.play(Transform(caption1, author))

        self.next_slide()
        # ---------------- Slide 1 ----------------


        # ---------------- Slide 2 ----------------
        title2 = Text('Introduction').scale(1.5).to_corner(UL)
        
        bullet21 = Text('• Moving away from streaming', font_size=28)
        bullet22 = Text('• Realized I don\'t know a lot about my music tastes', font_size=28)
        bullet23 = Text('• Want to learn more about the music I like over the last 4 years', font_size=28)

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
        title3 = Text('Questions to Answer').scale(1.5).to_corner(UL)
        self.wipe([title2, bullets2], title3)

        bullet311 = Text('1. How has my total listening volume trended over time, and when during the', font_size=28)
        bullet312 = Text('day and week do I listen most?', font_size=28).next_to(bullet311, direction=DOWN, buff=0.15, aligned_edge=LEFT)
        bullet31 = VGroup(bullet311, bullet312)

        bullet321 = Text('2. Which artists and tracks do I engage with most deeply, and which do I skip', font_size=28)   
        bullet322 = Text('the most often?', font_size=28).next_to(bullet321, direction=DOWN, buff=0.15, aligned_edge=LEFT)
        bullet32 = VGroup(bullet321, bullet322)
        
        bullet33 = Text('3. How have my artist and genre preferences shifted across distinct time periods?', font_size=28)
        bullet34 = Text('4. Do my listening habits differ meaningfully between Spotify and Apple Music?', font_size=28)

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
        title4 = Text("How?").scale(2)

        diagram_shift = RIGHT

        convergence_point41 = LEFT * 3.5 + diagram_shift
        lastfm = SVGMobject('lastfm-icon.svg').scale(0.4)
        data = SVGMobject('data-icon.svg').scale(0.4)
        data[0].set_color(WHITE)
        data.next_to(convergence_point41, buff=-0.025)
        
        convergence_point42 = RIGHT * 0.5 + diagram_shift
        arrow42 = Arrow(start=data.get_right(), end=convergence_point42, buff=0.1, tip_length=0.15)
        r = SVGMobject('r-icon.svg').scale(0.4)
        r.next_to(arrow42, buff=0.1)

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

        lastfm.move_to(apple_music).match_height(apple_music)
        arrow_top41 = Arrow(start=spotify.get_right(), end=convergence_point41, buff=0.1, tip_length=0.15)
        arrow_bottom41 = Arrow(start=apple_music.get_right(), end=convergence_point41, buff=0.1, tip_length=0.15)
        apple_music_backup = apple_music.copy()

        self.play(ReplacementTransform(apple_music, lastfm))
        self.wait(2.5)
        self.play(ReplacementTransform(lastfm, apple_music_backup))
        self.wait()
        apple_music = apple_music_backup
        
        self.play(
            Create(arrow_top41), 
            Create(arrow_bottom41)
        )
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

        labels = ["RQ1", "RQ2", "RQ3", "RQ4"]
        text_group = VGroup()
        for i, arrow in enumerate(arrows43):
            label = Text(labels[i], font_size=24)
            label.next_to(arrow.get_end(), RIGHT, buff=0.1) 
            text_group.add(label)
        self.play(Write(text_group))
        # ---------------- Slide 4 ----------------

        # ---------------- Slide 5 ----------------

        # ---------------- Slide 5 ----------------
        


class Test(Scene):
    def construct(self):
        pass