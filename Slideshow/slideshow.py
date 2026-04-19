from manim import *
from manim_slides import Slide

class Presentation(Slide):
    def construct(self):
        # ---------------- Slide 1 ----------------
        title1 = Text('Music Analytics').scale(2)
        caption1 = Text('Understanding my "Sonic Self"')
        caption1.next_to(title1, direction=DOWN)
        author = Text('Srikar Chitturi')
        author.next_to(title1, direction=DOWN)
        
        self.play(FadeIn(title1))
        self.wait(0.5)
        self.play(FadeIn(caption1, shift=UP))

        self.next_slide()

        self.play(Transform(caption1, author))

        self.wipe(title1, caption1, author)
        self.next_slide()
        # ---------------- Slide 1 ----------------


        # ---------------- Slide 2 ----------------
        title2 = Text('Introduction').scale(1).to_corner(UL)
        content21 = Text("" \
        "• Moving away from streaming")
        
        content22 = Text("" \
        "• Moving away from streaming" \
        "• Realized I don't know a lot about my music tastes")

        content23 = Text("" \
        "• Moving away from streaming" \
        "• Realized I don't know a lot about my music tastes" \
        "• Want to learn more about the music I like and listened to over last 4 years")

        self.play(FadeIn(title2))
        self.play()
        # ---------------- Slide 2 ----------------
        
