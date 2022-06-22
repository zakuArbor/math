from pickle import FALSE
from manim import *
#import plane


class Main(Scene):
    _texTemplate = None

    def construct(self):
        """
        ax = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            axis_config={"font_size": 24, 
            "numbers_to_include": np.arange(-2, 2, 1), 
            },
            tips=False
        ).add_coordinates()
        ax.scale(0.9)
        #labels = ax.get_axis_labels(
            #Tex("$0, 2\pi$").scale(1.25).shift(2*LEFT + UP), Tex("$\\frac{\pi}{2}$").scale(1.25).shift(5*LEFT + UP)
        #)
        x_label = ax.get_x_axis_label(
            Tex(r"\textbf{0,}\bm{$2\pi$}", texTemplate=self._texTemplate).scale(0.75),
            edge=RIGHT,
            direction=0.01*UR,
            buff=2
        )
        nx_label = ax.get_x_axis_label(
            Tex(r"\bm{$\pi$}", texTemplate=self._texTemplate).scale(0.75),
            edge=LEFT,
            direction=0.01*UL,
            buff=1
        )
        y_label = ax.get_y_axis_label(
            Tex(r"\bm{$\frac{\pi}{2}$}", texTemplate=self._texTemplate).scale(1),
            edge=UP,
            direction=0.05*UR,
            buff=1
        )

        ny_label = ax.get_y_axis_label(
            Tex(r"\bm{$\frac{3\pi}{2}$}", texTemplate=self._texTemplate).scale(1),
            edge=DOWN,
            direction=0.05*DR,
            buff=1
        )

        self.add(ax, x_label, y_label, nx_label, ny_label)
        vec1 = Arrow(ORIGIN, [1, 0, 0], buff=0)
        vec1.set_color(RED)
        dot = Dot(ORIGIN)
        tip_text = Text('(1, 0)', font_size=30).next_to(vec1.get_end(), UR)
        self.add(dot, vec1, tip_text)

        """

        dot = Dot(ORIGIN)
        # Line(start = ORIGIN, end = [1, 0, 0], buff = 0)
        vec1 = Arrow(ORIGIN, [2, 0, 0], buff=0)
        vec1.set_color(RED)
        tip_text = Text('(1, 0)', font_size=DEFAULT_FONT_SIZE *
                        0.5).next_to(vec1.get_end(), UP)
        self.create_texTemplate()
        self.create_plane()
        self.add(dot, vec1, tip_text)

        theta_tracker = ValueTracker(0.1)
        vec_ref = vec1.copy()
        vec1.rotate_about_origin(0.01)
        
        vec1.add_updater(
            lambda x: x.become(vec_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=ORIGIN
            )
        )
        
        a = Angle(vec_ref, vec1, radius=0.5, other_angle=False)
        tex = MathTex(r"\theta").move_to(
            Angle(
                vec_ref, vec1, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.5)
        )
        tex2 = MathTex(r"\theta=\pi", color=RED)
        a.add_updater(
            lambda x: x.become(Angle(vec_ref, vec1, radius=0.5, other_angle=False))
        )
        tex.add_updater(
            lambda x: x.move_to(
                Angle(
                    vec_ref.copy().rotate_about_origin(1), vec1, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
                ).point_from_proportion(0.5)
            )
        )
        self.add(a)
        self.wait()
        self.play(FadeOut(tip_text))
        self.play(theta_tracker.animate.set_value(180), run_time=2)
        tip_text = Text('(-1, 0)', font_size=DEFAULT_FONT_SIZE *
                        0.5).next_to(vec1.get_end(), UP)
        self.play(FadeIn(tip_text, tex))
        self.wait()
        
        #self.play(theta_tracker.animate.increment_value(360))

    def create_texTemplate(self):
        self._texTemplate = TexTemplate()
        self._texTemplate.add_to_preamble(r"\usepackage{bm}")

    def create_plane(self):
        plane = NumberPlane(
            x_range=[-3, 3, 2], y_range=(-3, 3, 2), axis_config={})
        x_label = plane.get_x_axis_label(Tex(r"\textbf{0,}\bm{$2\pi$}", tex_template=self._texTemplate).scale(1),
                                         edge=RIGHT,
                                         direction=RIGHT,
                                         buff=0.1)
        nx_label = plane.get_x_axis_label(
            Tex(r"\bm{$\pi$}", tex_template=self._texTemplate).scale(1),
            edge=LEFT,
            direction=LEFT,
            buff=0.1
        )
        y_label = plane.get_y_axis_label(
            Tex(r"\bm{$\frac{\pi}{2}$}",
                tex_template=self._texTemplate).scale(1),
            edge=UP,
            direction=UP,
            buff=0.2
        )

        ny_label = plane.get_y_axis_label(
            Tex(r"\bm{$\frac{3\pi}{2}$}",
                tex_template=self._texTemplate).scale(1),
            edge=DOWN,
            direction=DOWN,
            buff=1
        )
        self.add(plane, x_label, nx_label, y_label, ny_label)
        # vec2.set_color(RED)
        # self.add(vec2)
#        self.play(DrawBorderThenFill(plane))
#        self.play(GrowArrow(vec1), run_time = 1)
#        self.wait()
#        arrow = Arrow(ORIGIN, [1, 0, 0], buff=0)
#        arrow2 = Arrow(ORIGIN, [0, 1, 0], buff=0)
#        self.add(arrow, arrow2)
        #numberplane = NumberPlane()
#        origin_text = Text('(0, 0)').next_to(dot, DOWN)
#        tip_text = Text('(2, 2)').next_to(arrow.get_end(), RIGHT)
#        self.add(dot, arrow, tip_text)

        # self.play(Create(circle))  # show the circle on screen
