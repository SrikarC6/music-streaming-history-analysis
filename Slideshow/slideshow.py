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

        logos = VGroup(spotify, apple_music).arrange(RIGHT, buff=0.6)
        logos.next_to(bullet23, direction=DOWN, buff=0.6)
        logos.move_to([0, logos.get_y(), 0])

        self.wipe([title1, caption1, author], [title2])
        
        self.next_slide()

        self.play(FadeIn(bullet21, shift=UP))

        self.next_slide()

        self.play(FadeIn(bullet22, shift=UP))

        self.next_slide()

        self.play(FadeIn(bullet23, shift=UP))

        self.next_slide()

        self.play(Write(spotify))
        self.wait(1)
        self.play(Write(apple_music))

        self.next_slide()

        self.play(logos.animate.scale(0.5).to_corner(DR, buff=0.3))
        # ---------------- Slide 2 ----------------
        title3 = Text('Questions to Answer').scale(1.5).to_corner(UL)
        self.wipe([title2, bullets2], title3)

        bullet311 = Text('1. How has my total listening volume trended over time, and when during the', font_size=28)
        bullet312 = Text('day and week do I listen most?', font_size=28)
        bullet31 = VGroup(bullet311, bullet312).arrange(direction=DOWN, buff=0.15, aligned_edge=bullet311)

        bullet321 = Text('2. Which artists and tracks do I engage with most deeply, and which do I skip', font_size=28)   
        bullet322 = Text('the most often?', font_size=28)
        bullet32 = VGroup(bullet321, bullet322).arrange(direction=DOWN, aligned_edge=bullet321, buff=0.15)
        
        bullet33 = Text('3. How have my artist and genre preferences shifted across distinct time periods?', font_size=28)
        bullet34 = Text('4. Do my listening habits differ meaningfully between Spotify and Apple Music?', font_size=28)

        bullets3 = VGroup(bullet31, bullet32, bullet33, bullet34).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        bullets3.next_to(title3, direction=DOWN, buff=0.5).align_to(title3, LEFT)

        self.next_slide()

        self.play(FadeIn(bullet31, shift=UP))

        self.next_slide()

        self.play(FadeIn(bullet32, shift=UP))

        self.next_slide()

        self.play(FadeIn(bullet33, shift=UP))

        self.next_slide()

        self.play(FadeIn(bullet34, shift=UP))
        self.wait(0.2)
        self.play(Indicate(spotify))
        self.wait(0.3)
        self.play(Indicate(apple_music))

