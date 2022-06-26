from lib2to3.pgen2.token import LEFTSHIFT
from pickle import FALSE
from re import A, S
from cairo import FontWeight
from manim import *
from numpy import int_
#import plane


class Main(Scene):
    _texTemplate = None

    def construct(self): 
        self.create_texTemplate()
        self.matrixMult180()
        return
        self.next_section()
        self.intro()
        self.pause(5)
        self.clear()
        self.next_section()
        self.show_book()
        self.pause(1)
        self.clear()
        self.next_section()
        self.clear()
        self.display_rotation_matrix()
        self.next_section()
        self.rotate180()

        
        #self.play(theta_tracker.animate.increment_value(360))

    def init_plane(self)->tuple[Arrow, Text]:
        '''
        Sets up the initial plane with a vector drawn and returns the drawn vector

        Returns: a tuple containing with cardinality of 2
            vector (type: Arrow) drawn on the board
            text (type: Text) that specifies the coordinate of the vector
        '''
        dot: Dot = Dot(ORIGIN)
        vec1:Arrow = Arrow(ORIGIN, [2, 0, 0], buff=0)
        vec1.set_color(RED)
        tip_text:Text = Text('(1, 0)', font_size=DEFAULT_FONT_SIZE *
                        0.5).next_to(vec1.get_end(), UP)
        self.create_plane()
        g = Group(dot, vec1, tip_text)
        self.play(FadeIn(g), run_time=5)
        return (vec1, tip_text)

    def rotate180(self):
        '''
        '''
        vec1: Arrow = None
        tip_text: Text = None
        vec1, tip_text = self.init_plane()

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

    def display_rotation_matrix(self):
        m = Matrix([["\cos \\theta", "-\sin\\theta"], ["\sin\\theta", "\cos\\theta"]], h_buff=2.6)
        brackets = m.get_brackets()
        brackets.set_color(BLUE)

        self.add(m)
        self.pause(5)
        self.play(FadeOut(m))

    def matrixMult180(self):
        rot = Matrix([["\cos \\theta", "-\sin\\theta"], ["\sin\\theta", "\cos\\theta"]], h_buff=2)
        rot1 = Matrix([["\cos \pi", "-\sin \pi"], ["\sin \pi", "\cos \pi "]], h_buff=2)
        m = Matrix([["x"], ["y"]])
        m.next_to(rot)
        brackets = m.get_brackets()
        brackets.set_color(BLUE)
        rot.get_brackets().set_color(BLUE)
        rot1.get_brackets().set_color(BLUE)
        self.play(FadeIn(m, rot))
        self.pause(1)
        m1 = Matrix([[1], [0]])
        m1.get_brackets().set_color(BLUE)
        m1.next_to(rot)
        result_mat = Matrix([["x"], ["x"]]).set_color(config.background_color)
        result_mat.get_brackets().set_color(BLUE)
        self.play(
            ReplacementTransform(rot, rot1, dim_to_match=1),
            ReplacementTransform(m, m1, dim_to_match=1),
            run_time=1
        )
        self.remove(rot, brackets)
        self.wait()

        #move matrix to the left
        group = VGroup(rot1, m1)
        group.generate_target()
        group.target.shift(4*LEFT)
        self.play(MoveToTarget(group))
        equal = Tex("\\textbf{=}", font_size=DEFAULT_FONT_SIZE + 5, color=GREEN).next_to(group)
        result_mat.next_to(equal)
        self.play(FadeIn(equal, result_mat))
        self.pause(1)

        self.animateMult180(rot1, m1, result_mat)

        #self.play(FadeOut(m))
    def animateMult180(self, m: Matrix, m1: Matrix, result_mat: Matrix):
        rows = m.get_rows()
        cols = m1.get_columns()
        equal = Tex("=")
        result_entries = result_mat.get_entries()
        #int_ans = [MathTex(r"= -1 + 0"), MathTex(r"= 0 + 0")]
        final_ans = [MathTex(r"1"), MathTex(r"0")]
        for i in range(len(rows)):
            
            for j in range(len(cols)):
                group_row = VGroup(SurroundingRectangle(rows[i]).set_color(PURPLE), rows[i].copy())
                group_col = VGroup(SurroundingRectangle(cols[j]).set_color(PURPLE), cols[j].copy())
                group_row.generate_target()
                group_col.generate_target()
                group_row.target.move_to(2*DOWN + 1.5 * LEFT)
                group_col.target.move_to(2*DOWN + 0.5 * RIGHT)
                self.play(FadeIn(group_row, group_col))
                self.play(MoveToTarget(group_row), MoveToTarget(group_col))
                ans = final_ans[i]
                equal = equal.copy().next_to(group_col)
                ans.next_to(equal) 
                ans_display = SurroundingRectangle(ans).set_color(RED)
                ans_group = VGroup(equal, ans, ans_display)
                self.play(FadeIn(ans_group))
                self.wait()
                ans = ans.copy().set_color(YELLOW)
                ans.generate_target()
                ans.target.move_to(result_entries[i]) 
                self.play(MoveToTarget(ans))
                self.play(FadeOut(group_col, group_row, ans_group))


    def intro(self):
        '''
        '''
        title: Tex = Tex(r"\textbf{Double Angles}", font_size=144).shift(UP)
        ids: Tex = Tex(r"\bm{$\cos2\theta$ \quad $\sin2\theta$}", color=RED, tex_template=self._texTemplate, font_size=100).next_to(title, 2*DOWN)

        self.add(title)
        self.play(FadeIn(ids), run_time=2)

    def tex(self, text, color=None, template=None):
        template = self._texTemplate if not template else template


    
    def show_book(self):
        img:ImageMobject = ImageMobject("math-girls-cover.jpg")
        img.scale_to_fit_height(config.frame_height)
        self.play(FadeIn(img))
        self.wait()
        self.play(FadeOut(img), run_time=2)
        

    def create_texTemplate(self):
        '''
        Create tex template to add new Tex packages to the project

        Mutates:
            _texTemplate: a TexTemplate object
        '''
        self._texTemplate = TexTemplate()
        self._texTemplate.add_to_preamble(r"\usepackage{bm}")

    def create_plane(self):
        '''
        Draw the 2d plane with the angles of each axis labelled in radians
        '''
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
        g = Group(plane, x_label, nx_label, y_label, ny_label)
        self.play(FadeIn(g), run_time=5)
