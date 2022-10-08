from bisect import bisect
from lib2to3.pgen2.token import LEFTSHIFT
from pickle import FALSE
from re import A, S
from tkinter import TOP
from cairo import FontWeight
from manim import *
from numpy import int_, size

class Main(Scene):
    _texTemplate = None

    def construct(self): 
        self.create_texTemplate()
        #self.triangle_sin2x()
        self.next_section("intro")
        self.intro(12)
        self.clear()
        self.next_section("approaches")
        self.other_approach(12)
        self.next_section("book")
        self.show_book(18)
        return
#        self.pause(0.5)
        self.clear()
        self.next_section()
        self.clear()
        self.display_rotation_matrix()
        self.pause(15)
        self.next_section()
        g = self.rotate180()
        self.next_section()
        self.matrixMult180(g)
        self.pause(0.5)
        self.display_rot2()
        g:VGroup = self.display_rot_pow2()
        self.next_section()
        self.display_rot_eq(g)
        self.pause(0.5)
        
        
        #self.play(theta_tracker.animate.increment_value(360))
    def triangle_sin2x(self):
        triangle = Polygon([-2, -1, 0], [2, -1, 0], [0, 3, 0])
        bisector = Line([0,-1,0], [0, 2.95, 0]).set_color(WHITE)
        angle = RightAngle(bisector, Line([-2, -1, 0], [0, -1, 0]), quadrant=(1,-1))
        group = VGroup(triangle, bisector, angle)

        self.play(FadeIn(group))

    def other_approach(self, pause = 1):
        cos_add = MathTex(r"\cos (\alpha + \beta) &= \cos \alpha \cos \beta - \sin \alpha \sin \beta \\" \
                r"\cos (\theta + \theta) &= cos\theta \cos \theta - \sin \theta \sin \theta \\" \
                r"\cos(2\theta) &= \boxed{\cos^2\theta - \sin^2\theta}", font_size=DEFAULT_FONT_SIZE)
        cos_add.to_edge(UL)
        img:ImageMobject = ImageMobject("wiki-visual.png").to_edge(DR)
        self.play(FadeIn(cos_add), FadeIn(img), run_time = 2)
        self.wait()
        self.pause(pause)
        self.play(FadeOut(cos_add), FadeOut(img))

    def init_plane(self)->tuple[Arrow, Text, Group, Group]:
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
        plane_group = self.create_plane()
        g = Group(dot, vec1)
        self.play(FadeIn(g, tip_text), run_time=0.5)

        return [vec1, tip_text, plane_group, g]

    def rotate180(self):
        '''
        '''
        vec1: Arrow = None
        tip_text: Text = None
        vec1, tip_text, g1, g2 = self.init_plane()

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
        self.play(theta_tracker.animate.set_value(180))
        tip_text = Text('(-1, 0)', font_size=DEFAULT_FONT_SIZE *
                        0.5).next_to(vec1.get_end(), UP)
        self.play(FadeIn(tip_text, tex))
        self.wait() 
        self.pause(3)
        #self.play(FadeOut(tip_text, theta_tracker, a, vec1, tex, g1, g2))
        a = Angle(vec_ref, vec1, radius=0.5, other_angle=False)
        vec1:Arrow = Arrow(ORIGIN, [-2, 0, 0], buff=0).set_color(RED) #need to recreate arrow that has no animations associated with it to display again without timing issues
        g1.add(tip_text, a, vec1)
        self.clear()
        self.wait()
        return g1


    def generate_rot(self)->Matrix:
        m = Matrix([["\cos \\theta", "-\sin\\theta"], ["\sin\\theta", "\cos\\theta"]], h_buff=2.6)
        brackets = m.get_brackets()
        brackets.set_color(BLUE)
        return m

    def display_rotation_matrix(self):
        m = self.generate_rot()

        self.add(m)
        self.pause(0.5)
        self.play(FadeOut(m))

    def matrixMult180(self, g):
        rot = Matrix([["\cos \\theta", "-\sin\\theta"], ["\sin\\theta", "\cos\\theta"]], h_buff=2)
        rot1 = Matrix([["\cos \pi", "-\sin \pi"], ["\sin \pi", "\cos \pi "]], h_buff=2)
        m = Matrix([["x"], ["y"]])
        m.next_to(rot)
        brackets = m.get_brackets()
        brackets.set_color(BLUE)
        rot.get_brackets().set_color(BLUE)
        rot1.get_brackets().set_color(BLUE)
        self.play(FadeIn(m, rot))
        self.pause(0.5)
        m1 = Matrix([[1], [0]])
        m1.get_brackets().set_color(BLUE)
        m1.next_to(rot)
        result_mat = Matrix([["-1"], ["0"]]).set_color(config.background_color)
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
        self.pause(0.5)

        self.animateMult180(rot1, m1, result_mat, g, equal)
    
    def animateMult180(self, m: Matrix, m1: Matrix, result_mat: Matrix, g, equal0):
        rows = m.get_rows()
        cols = m1.get_columns()
        equal = Tex("=")
        result_entries = result_mat.get_entries()
        final_ans = [MathTex(r"-1"), MathTex(r"0")]
        ans_animated = [] #needed to remove later


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
                ans_group = VGroup(ans, ans_display)
                self.play(FadeIn(equal, ans_group))
                self.wait()
                ans = ans.copy().set_color(YELLOW)
                ans_animated.append(ans)
                ans.generate_target()
                ans.target.move_to(result_entries[i]) 
                self.play(FadeOut(ans_group), MoveToTarget(ans))
                self.play(FadeOut(group_col, group_row, equal))
                result_entries[i].set_color(YELLOW) #stealthily reveal the entry even though it's being displayed by a text object
        
        self.play(FadeOut(m, m1, equal0, *ans_animated))
        self.wait()

        g.shift(3 * LEFT)
        result_mat.generate_target()
        m = Matrix([["x"], ["y"]])
        m.get_brackets().set_color(BLUE)
        m.shift(2.75*RIGHT) 
        equal = Tex("\\textbf{=}",font_size=DEFAULT_FONT_SIZE + 5, color=GREEN).next_to(m)
        result_mat.target.shift(4.15 * RIGHT)
        self.play(FadeIn(g, m, equal), MoveToTarget(result_mat))
        self.pause(0.5)
        self.play(FadeOut(g, m, equal, result_mat))
    
    def generate_rot_pow2(self)->VGroup:
        m = Matrix([["\cos \\theta", "-\sin\\theta"], ["\sin\\theta", "\cos\\theta"]], h_buff=2)
        brackets = m.get_brackets()
        brackets.set_color(BLUE)
        pow = MathTex(r"^2", font_size=DEFAULT_FONT_SIZE+30)
        pow.next_to(brackets[1].get_top())
        return VGroup(m, pow)
    
    def generate_rot_pow2_i(self)->VGroup:
        m1 = Matrix([["\cos \\theta", "-\sin\\theta"], ["\sin\\theta", "\cos\\theta"]], h_buff=2)
        m1.get_brackets().set_color(BLUE)
        m2 = m1.copy() 
        m2.next_to(m1)
        return VGroup(m1, m2)

    def generate_rot_pow2_r(self)->Matrix:
        m = Matrix([["\cos^2 \\theta - \sin^2 \\theta", "-2\sin\\theta\cos\\theta"], ["2\sin\\theta\cos\\theta", "\cos^2\\theta - \sin^2\\theta"]], h_buff=3.5)
        brackets = m.get_brackets()
        brackets.set_color(BLUE)
        return m
    
    def generate_title(self)->Tex:
        return Tex(r"\textbf{Double Angles}", font_size=100).shift(2*UP).set_color(BLUE)

    def display_rot_eq(self, group):
        left_mat = self.generate_rot2()
        left_mat.next_to(group[1], direction=LEFT)
        self.play(ReplacementTransform(group[0],left_mat))
        self.wait()
        left_entries = left_mat.get_entries()
        right_entries = group[2].get_entries()
        left_u1 = Underline(left_entries[0]).set_color(GOLD)
        right_u1 = Underline(right_entries[0]).set_color(GOLD)
        left_u2 = Underline(left_entries[2]).set_color(TEAL)
        right_u2 = Underline(right_entries[2]).set_color(TEAL)
        self.play(
            Create(left_u1), 
            Create(right_u1),
            left_entries[0].animate.set_color(GOLD),
            right_entries[0].animate.set_color(GOLD)
        )
        
        self.play(
            Create(left_u2), 
            Create(right_u2),
            left_entries[2].animate.set_color(TEAL),
            right_entries[2].animate.set_color(TEAL)
        )
        self.wait()
        self.pause(0.5)
        
        #cos_group = VGroup(left_entries[0].copy(), right_entries[1].copy(), left_u1, right_u1)
        #sin_group = VGroup(left_entries[2], right_entries[2], left_u2, right_u2)
        #cos_group.generate_target()
        #cos_group.
        title: Tex = self.generate_title()
        eq1 = Tex("\\textbf{=}").set_color(GOLD)
        eq2 = Tex("\\textbf{=}").set_color(TEAL)
        eq2.next_to(eq1, direction=3*DOWN)
        left_cos = VGroup(left_entries[0].copy(), left_u1)
        left_cos_anim = left_cos.animate.next_to(eq1, direction=LEFT)
        right_cos = VGroup(right_entries[0].copy(), right_u1)
        right_cos_anim = right_cos.animate.next_to(eq1)

        left_sin = VGroup(left_entries[2].copy(), left_u2)
        left_sin_anim = left_sin.animate.next_to(eq2, direction=LEFT)
        right_sin = VGroup(right_entries[2].copy(), right_u2)
        right_sin_anim = right_sin.animate.next_to(eq2)
#        left = VGroup(left_cos, left_sin).animate.next_to(eq1, direction=LEFT)
#        right = VGroup(right_cos, right_sin).animate.next_to(eq1, direction=RIGHT)
        self.play(
            left_cos_anim,
            left_sin_anim, 
            right_cos_anim,
            right_sin_anim, 
            FadeIn(title, eq1, eq2), 
            FadeOut(group, left_mat),
        )
        self.wait()
        group = Group(left_cos, right_cos, left_sin, right_sin, eq1, eq2)
        self.play(group.animate.scale(1.5))

    def display_rot_pow2(self)->VGroup:
        m_group = self.generate_rot_pow2()
        self.play(FadeIn(m_group))
        m_group.generate_target()
        m_group.target.shift(4*LEFT)
        equal = Tex("\\textbf{=}", font_size = DEFAULT_FONT_SIZE+20)
        self.play(MoveToTarget(m_group))
        equal.next_to(m_group)
        g_imm = self.generate_rot_pow2_i()
        g_imm.next_to(equal)
        self.play(FadeIn(g_imm, equal))
        self.pause(0.5)
        m2 = self.generate_rot_pow2_r()
        m2.next_to(equal)
        self.play(ReplacementTransform(g_imm, m2))
        self.pause(0.5)
        rect = SurroundingRectangle(m2.get_columns()[0])
        self.play(FadeIn(rect))
        self.wait()
        self.pause(0.5)
        self.play(FadeOut(rect))
        return VGroup(m_group, equal, m2)

    def generate_rot2(self)->Matrix:
        m = Matrix([["\cos 2\\theta", "-\sin 2\\theta"], ["\sin 2\\theta", "\cos 2\\theta"]], h_buff=2.6)
        brackets = m.get_brackets()
        brackets.set_color(BLUE)
        return m

    def display_rot2(self):
        m = self.generate_rot()
        entries = m.get_entries()
        m2 = self.generate_rot2()
        cos2 = MathTex(r"\cos 2\theta").move_to(2*UP + LEFT)
        sin2 = MathTex(r"\sin 2\theta")
        sin2.next_to(cos2, buff=RIGHT)
        self.play(FadeIn(m, cos2, sin2))
        self.wait()
        #self.add(index_labels(cos2[0])) #displays numbering labels on each character for debugging
        cos2[0][3:5].set_color(RED)
        sin2[0][3:5].set_color(RED)
        cos2_2 = cos2.copy()
        sin2_2 = MathTex(r"-\sin 2\theta").move_to(sin2)
        sin2_2[0][4:6].set_color(RED)
        cos2.generate_target()
        sin2.generate_target()
        cos2_2.generate_target()
        sin2_2.generate_target()
        #ReplacementTransform
        cos2.target.move_to(entries[0])
        cos2_2.target.move_to(entries[3])
        sin2.target.move_to(entries[2][0][1])
        sin2_2.target.move_to(entries[1])
        self.wait()
        self.pause(0.5)
        self.play(
            MoveToTarget(cos2), 
            FadeOut(entries[0]),
            MoveToTarget(cos2_2),
            FadeOut(entries[3]),
            MoveToTarget(sin2),
            FadeOut(entries[1]),
            MoveToTarget(sin2_2),
            FadeOut(entries[2]),
        )
        self.wait()
        self.play(FadeOut(*self.mobjects))

    def intro(self, pause = 1):
        '''
        '''
        title: Tex = self.generate_title() 
        ids: Tex = Tex(r"\bm{$\cos2\theta$ \quad $\sin2\theta$}", color=GREEN, tex_template=self._texTemplate, font_size=80).next_to(title, 4*DOWN)

        self.add(title)
        self.play(FadeIn(ids), run_time=3)
        self.pause(pause)

    def tex(self, text, color=None, template=None):
        template = self._texTemplate if not template else template


    
    def show_book(self, pause = 1):
        img:ImageMobject = ImageMobject("math-girls-cover.jpg")
        img.scale_to_fit_height(config.frame_height)
        self.play(FadeIn(img), run_time = 2)
        self.wait()
        self.pause(pause)
        self.play(FadeOut(img), run_time=2)
        

    def create_texTemplate(self):
        '''
        Create tex template to add new Tex packages to the project

        Mutates:
            _texTemplate: a TexTemplate object
        '''
        self._texTemplate = TexTemplate()
        self._texTemplate.add_to_preamble(r"\usepackage{bm}")

    def create_plane(self)->Group:
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
        self.play(FadeIn(g), run_time=0.5)
        return g
