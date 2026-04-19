from manim import *
import unicodedata
import numpy as np
from PIL import Image

FONT = "Arial"

class SVDScene(Scene):

    def VText(self, text, size=30, color=WHITE):
        text = unicodedata.normalize("NFC", text)
        return Text(text, font=FONT, font_size=size, color=color)

    def wipe(self):
        self.play(*[FadeOut(m) for m in self.mobjects])

    # =========================
    # CONSTRUCT
    # =========================
    def construct(self):

        # CHÉO HOÁ
        self.intro_full() 
        self.intro_matrix()
        self.eigenvalues_diag()
        self.lambda1_full()
        self.lambda3_full()
        self.lambda4_full()
        self.final_diagonalization()

        self.wipe()  # chỉ wipe sau khi xong cả block

        # SVD
        self.intro_svd()
        self.compute_ATA()
        self.eigenvalues_svd()
        self.eigenvectors_svd()
        self.normalize_vectors()
        self.sigma()
        self.compute_U()
        self.final_svd()

        self.wipe()

        # EXPLAIN
        self.svd_explain()

        self.wipe()

        # VISUAL
        self.geometry()

        self.wipe()

        # ỨNG DỤNG
        self.compression()

    # ==================================================
    # INTRO
    # ==================================================

    def intro_full(self):

        # GIỚI THIỆU
        start_1 = Text(
            "Xin chào thầy cô và các bạn",
            font="Arial",
            weight=BOLD
        ).scale(0.6)

        start_2 = Text(
            "Trong video này, nhóm chúng em xin được phép giới thiệu",
            font="Arial",
            weight=BOLD
        ).scale(0.5)

        start_3 = Text(
            "về Phân rã và Chéo hóa ma trận",
            font="Arial",
            weight=BOLD
        ).scale(0.5)

        group_1 = VGroup(start_2, start_3).arrange(DOWN)
        group_1.set_color_by_gradient(BLUE, TEAL)

        group = Text(
            "Nhóm 13 – 24CTT1 – HCMUS",
            font="Arial"
        ).scale(0.5).to_edge(DOWN)

        subtitle = Text(
            "Singular Value Decomposition (SVD)"
        ).scale(0.7)
        subtitle.next_to(group_1, DOWN)

        self.play(FadeIn(group))

        self.play(FadeIn(start_1))
        self.wait(1.5)
        self.play(FadeOut(start_1))

        self.play(FadeIn(group_1))
        self.wait(1.5)

        # GIỮ FILE TRÊN ĐẦU
        self.play(
            group_1.animate.scale(0.8).to_edge(UP),
            run_time=1
        )

        self.play(Write(subtitle))
        self.wait(1)
        self.play(FadeOut(subtitle), FadeOut(group))

        # QUESTION
        question = Text(
            "Ma trận thực sự làm gì với không gian?",
            font="Arial",
            color=YELLOW
        ).scale(0.6)

        question_0 = Text(
            "Chúng ta hãy cùng tìm hiểu qua video này",
            font="Arial",
            color=YELLOW
        ).scale(0.6)

        question_1 = Text(
            "Let's go!!",
            font="Arial",
            color=YELLOW
        ).scale(0.6)

        self.play(FadeOut(group_1))

        self.play(Write(question))
        self.wait(1.5)

        self.play(Transform(question, question_0), run_time=1.2)
        self.wait(1.2)

        self.play(Transform(question, question_1), run_time=1)
        self.wait(1)

        self.play(FadeOut(question))

        # VISUAL VECTOR
        plane = NumberPlane()
        vec = Arrow(ORIGIN, [2, 1, 0], buff=0, color=RED)

        Ex1 = Text(
            "Đây là 1 vector",
            font="Arial",
            color=YELLOW
        ).scale(0.6).to_edge(UP*2)

        Ex2 = Text(
            "Ma trận giúp chúng ta có thể quay vector này!",
            font="Arial",
            color=YELLOW
        ).scale(0.6).to_edge(UP*2)

        self.play(Create(plane))
        self.play(GrowArrow(vec))
        self.wait(1)

        self.play(Write(Ex1))
        self.wait(1.5)
        self.play(FadeOut(Ex1))

        self.play(Write(Ex2))
        self.wait(1.5)

        # QUAY VECTOR
        for _ in range(4):
            self.play(
                Rotate(vec, angle=PI/4, about_point=ORIGIN),
                run_time=0.8
            )

        self.wait(1)

        self.play(Rotate(vec, angle=2*PI), run_time=2)
        self.wait(1)

        # CHUYỂN ĐỔI MA TRẬN
        self.play(FadeOut(plane, vec, Ex2))

        t1 = Text(
            "Vậy ma trận thực sự đã làm gì?",
            font="Arial",
            color=YELLOW
        ).scale(0.6)

        self.play(Write(t1))
        self.wait(1.5)

        t2 = Text(
            "Chúng ta sẽ bắt đầu với một ma trận cụ thể",
            font="Arial"
        ).scale(0.6)

        self.play(Transform(t1, t2))
        self.wait(1.2)

        t3 = Text(
            "Xét ma trận A sau:",
            font="Arial",
            color=BLUE
        ).scale(0.6)

        self.play(Transform(t1, t3))
        self.wait(1)

        self.play(FadeOut(t1))

    # CHÉO HOÁ MA TRẬN
    def intro_matrix(self):

        title = self.VText("Chéo hóa ma trận", 42, BLUE).to_edge(UP)

        A = MathTex(
            r"A=\begin{pmatrix}2&1&0\\1&2&0\\0&0&4\end{pmatrix}"
        ).scale(1.2)

        self.play(FadeIn(title))
        self.play(Write(A))
        self.wait(1)

        # XOÁ FULL TRƯỚC KHI QUA BƯỚC TIẾP
        self.play(FadeOut(title), FadeOut(A))


    def eigenvalues_diag(self):

        title = self.VText("Tìm trị riêng", 42, BLUE).to_edge(UP)

        l1 = MathTex(r"P_A(\lambda)=\det(A-\lambda I)")

        l2 = MathTex(
            r"=\det\begin{pmatrix}2-\lambda&1&0\\1&2-\lambda&0\\0&0&4-\lambda\end{pmatrix}"
        )

        l3 = MathTex(r"=(4-\lambda)((2-\lambda)^2-1)")
        l4 = MathTex(r"=(4-\lambda)(\lambda-1)(\lambda-3)")

        group = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.5).scale(0.9)
        group.next_to(title, DOWN)

        self.play(FadeIn(title))

        for g in group:
            self.play(Write(g))
            self.wait(0.6)

        result = MathTex(r"\lambda=1,3,4").set_color(YELLOW)
        result.next_to(group, DOWN)

        self.play(FadeIn(result))
        self.wait(1)

        # XOÁ FULL TRƯỚC KHI QUA BƯỚC TIẾP
        self.play(FadeOut(title), FadeOut(group), FadeOut(result))


    def lambda1_full(self):

        title = self.VText("Giải hệ với λ = 1", 40, BLUE).to_edge(UP)

        step1 = MathTex(
            r"A-I=\begin{pmatrix}1&1&0\\1&1&0\\0&0&3\end{pmatrix}"
        )

        step2 = MathTex(r"R_2 \leftarrow R_2 - R_1")

        step3 = MathTex(
            r"\rightarrow\begin{pmatrix}1&1&0\\0&0&0\\0&0&3\end{pmatrix}"
        )

        # ĐẶT PHẢI
        step4 = MathTex(r"x+y=0")
        step5 = MathTex(r"z=0")
        step6 = MathTex(r"y=-x")

        vec = MathTex(
            r"\begin{pmatrix}x\\y\\z\end{pmatrix}"
            r"=\begin{pmatrix}x\\-x\\0\end{pmatrix}"
        )

        v1 = MathTex(
            r"v_1=\begin{pmatrix}1\\-1\\0\end{pmatrix}"
        ).set_color(GREEN)

        #  NHÓM TRÁI
        left_group = VGroup(
            step1, step2, step3
        ).arrange(DOWN, buff=0.6).scale(0.8)

        left_group.next_to(title, DOWN, buff=1)

        # NHÓM PHẢI
        right_group = VGroup(
            step4, step5, step6, vec, v1
        ).arrange(DOWN, buff=0.5).scale(0.75)

        right_group.next_to(left_group, RIGHT, buff=2)

        # ANIMATION
        self.play(FadeIn(title))

        # BÊN TRÁI
        for step in left_group:
            self.play(Write(step))
            self.wait(0.4)

        # BÊN PHẢI
        for step in right_group:
            self.play(Write(step))
            self.wait(0.4)

        self.wait(1.2)

        # XOÁ
        self.play(
            FadeOut(title),
            FadeOut(left_group),
            FadeOut(right_group)
        )


    def lambda3_full(self):

        title = self.VText("Giải hệ với λ = 3", 40, BLUE).to_edge(UP)

        step1 = MathTex(
            r"A-3I=\begin{pmatrix}-1&1&0\\1&-1&0\\0&0&1\end{pmatrix}"
        )

        step2 = MathTex(r"R_2 \leftarrow R_2 + R_1")

        step3 = MathTex(
            r"\rightarrow\begin{pmatrix}-1&1&0\\0&0&0\\0&0&1\end{pmatrix}"
        )

        step4 = VGroup(
            MathTex(r"x=y"),
            MathTex(r"z=0")
        ).arrange(DOWN, buff=0.3)

        v2 = MathTex(
            r"v_2=\begin{pmatrix}1\\1\\0\end{pmatrix}"
        ).set_color(GREEN)

        # NHÓM
        left_group = VGroup(
            step1, step2, step3, step4
        ).arrange(DOWN, buff=0.5).scale(0.85)

        left_group.next_to(title, DOWN, buff=0.8)

        v2.scale(0.9)
        v2.next_to(left_group, RIGHT, buff=1.5)

        # ANIMATION
        self.play(FadeIn(title))

        for step in left_group:
            self.play(Write(step))
            self.wait(0.4)

        self.play(Write(v2))
        self.wait(1.2)

        # XOÁ
        self.play(
            FadeOut(title),
            FadeOut(left_group),
            FadeOut(v2)
        )

    def lambda4_full(self):

        title = self.VText("Giải hệ với λ = 4", 40, BLUE).to_edge(UP)

        step1 = MathTex(
            r"A-4I=\begin{pmatrix}-2&1&0\\1&-2&0\\0&0&0\end{pmatrix}"
        )

        step2 = VGroup(
            MathTex(r"x=y=0"),
            self.VText("z là biến tự do", 28)
        ).arrange(DOWN)

        v3 = MathTex(
            r"v_3=\begin{pmatrix}0\\0\\1\end{pmatrix}"
        ).set_color(GREEN)

        group = VGroup(step1, step2, v3)\
            .arrange(DOWN, buff=0.45).scale(0.9)

        group.next_to(title, DOWN)

        self.play(FadeIn(title))
        self.play(Write(step1))
        self.play(FadeIn(step2))
        self.play(Write(v3))
        self.wait(1)

        # XOÁ FULL TRƯỚC KHI QUA BƯỚC TIẾP
        self.play(FadeOut(title), FadeOut(group))


    def final_diagonalization(self):

        title = self.VText("Kết luận chéo hóa", 42, BLUE).to_edge(UP)

        # PHASE 1: P, D, P^-1
        P = MathTex(
            r"P=\begin{pmatrix}1&1&0\\-1&1&0\\0&0&1\end{pmatrix}"
        )

        D = MathTex(
            r"D=\begin{pmatrix}1&0&0\\0&3&0\\0&0&4\end{pmatrix}"
        )

        Pinv = MathTex(
            r"P^{-1}=\frac{1}{2}\begin{pmatrix}1&-1&0\\1&1&0\\0&0&2\end{pmatrix}"
        )

        group1 = VGroup(P, D, Pinv).arrange(DOWN, buff=0.6).scale(0.9)
        group1.next_to(title, DOWN)

        self.play(FadeIn(title))
        self.play(Write(group1))
        self.wait(2)

        # PHASE 2: A = PDP^-1
        self.play(FadeOut(group1))

        A_expand = MathTex(
            r"A = "
            r"\begin{pmatrix}1&1&0\\-1&1&0\\0&0&1\end{pmatrix}"
            r"\begin{pmatrix}1&0&0\\0&3&0\\0&0&4\end{pmatrix}"
            r"\frac{1}{2}\begin{pmatrix}1&-1&0\\1&1&0\\0&0&2\end{pmatrix}"
        ).scale(0.75)

        A_expand.next_to(title, DOWN)

        self.play(Write(A_expand))
        self.wait(2)

        # PHASE 3: KẾT QUẢ A
        A_result = MathTex(
            r"A=\begin{pmatrix}2&1&0\\1&2&0\\0&0&4\end{pmatrix}"
        ).set_color(YELLOW)

        A_result.next_to(A_expand, DOWN)

        self.play(Write(A_result))
        self.wait(2)

        # PHASE 4: LUỸ THỪA
        self.play(FadeOut(A_expand), FadeOut(A_result))

        Ak1 = MathTex(r"A^k = P D^k P^{-1}")

        Ak2 = MathTex(
            r"D^k = \begin{pmatrix}1^k&0&0\\0&3^k&0\\0&0&4^k\end{pmatrix}"
        )

        Ak3 = MathTex(
            r"A^k = P \begin{pmatrix}1^k&0&0\\0&3^k&0\\0&0&4^k\end{pmatrix} P^{-1}"
        ).set_color(YELLOW).scale(0.9)

        group2 = VGroup(Ak1, Ak2, Ak3).arrange(DOWN, buff=0.5)
        group2.next_to(title, DOWN)

        self.play(Write(group2))
        self.wait(3)

        # xoá full trước khi qua bước tiếp
        self.play(FadeOut(title), FadeOut(group2))


    # ==================================================
    # SVD (PHẦN ĐẦU)
    # ==================================================
    def intro_svd(self):

        title = self.VText("Phân rã SVD từng bước", 40, BLUE).to_edge(UP)
        A = Matrix([[2,1],[1,2],[1,0]]).scale(0.9)

        self.play(FadeIn(title), FadeIn(A))
        self.wait(4)

        # XOÁ FULL TRƯỚC KHI QUA BƯỚC TIẾP
        self.play(FadeOut(title), FadeOut(A))


    def compute_ATA(self):

        title = self.VText("Tính AᵀA", 40, BLUE).to_edge(UP)
        ATA = Matrix([[6,4],[4,5]]).scale(0.9)

        self.play(FadeIn(title), FadeIn(ATA))
        self.wait(4)

        # XOÁ FULL TRƯỚC KHI QUA BƯỚC TIẾP
        self.play(FadeOut(title), FadeOut(ATA))


    def eigenvalues_svd(self):

        title = self.VText("Tìm trị riêng của AᵀA", 40, BLUE).to_edge(UP)

        d1 = MathTex(r"\det(A^T A - \lambda I)=0")
        d2 = MathTex(r"=\begin{vmatrix}6-\lambda&4\\4&5-\lambda\end{vmatrix}")
        d3 = MathTex(r"=(6-\lambda)(5-\lambda)-16")
        d4 = MathTex(r"=\lambda^2 - 11\lambda +14")
        d5 = MathTex(r"\lambda=\frac{11\pm\sqrt{65}}{2}")

        group = VGroup(d1,d2,d3,d4,d5)\
            .arrange(DOWN, buff=0.4).scale(0.7)

        group.next_to(title, DOWN)

        self.play(FadeIn(title))

        for g in group:
            self.play(Write(g))
            self.wait(0.8)

        self.wait(2)

        # XOÁ FULL TRƯỚC KHI QUA BƯỚC TIẾP
        self.play(FadeOut(title), FadeOut(group))



    def eigenvectors_svd(self):

        title = self.VText("Tìm vector riêng của AᵀA", 40, BLUE).to_edge(UP)

        # BƯỚC 1: LẬP HỆ
        s1 = MathTex(r"(A^T A - \lambda I)v = 0")

        s2 = MathTex(
            r"\begin{pmatrix}6-\lambda & 4 \\ 4 & 5-\lambda\end{pmatrix}"
            r"\begin{pmatrix}x \\ y\end{pmatrix} = 0"
        )

        s3 = VGroup(
            self.VText("Đặt", 28),
            MathTex(r"v = \begin{pmatrix}1 \\ t\end{pmatrix}")
        ).arrange(RIGHT)

        group1 = VGroup(s1, s2, s3).arrange(DOWN, buff=0.5).scale(0.9)
        group1.next_to(title, DOWN)

        self.play(FadeIn(title))
        for g in group1:
            self.play(Write(g))
            self.wait(0.6)

        self.wait(1)

        # BƯỚC 2: GIẢI t
        self.play(FadeOut(group1))

        s4 = MathTex(r"(6-\lambda)\cdot 1 + 4t = 0")
        s5 = MathTex(r"4t = \lambda - 6")
        s6 = MathTex(r"t = \frac{\lambda - 6}{4}").set_color(YELLOW)

        group2 = VGroup(s4, s5, s6).arrange(DOWN, buff=0.5)
        group2.next_to(title, DOWN)

        for g in group2:
            self.play(Write(g))
            self.wait(0.6)

        self.wait(1)

        # BƯỚC 3: VECTOR RIÊNG
        self.play(FadeOut(group2))

        lam1 = MathTex(r"\lambda_1 = \frac{11 + \sqrt{65}}{2}")
        v1 = MathTex(
            r"v_1 = \begin{pmatrix}1 \\ \frac{\lambda_1 - 6}{4}\end{pmatrix}"
        ).set_color(GREEN)

        lam2 = MathTex(r"\lambda_2 = \frac{11 - \sqrt{65}}{2}")
        v2 = MathTex(
            r"v_2 = \begin{pmatrix}1 \\ \frac{\lambda_2 - 6}{4}\end{pmatrix}"
        ).set_color(GREEN)

        group3 = VGroup(lam1, v1, lam2, v2).arrange(DOWN, buff=0.5).scale(0.9)
        group3.next_to(title, DOWN)

        for g in group3:
            self.play(Write(g))
            self.wait(0.6)

        self.wait(2)

        # BƯỚC 4: CHUẨN HOÁ → V
        self.play(FadeOut(group3))

        v_norm = MathTex(
            r"v_i = \frac{1}{\sqrt{1+t_i^2}} \begin{pmatrix}1 \\ t_i\end{pmatrix}"
        )

        V = MathTex(
            r"V = (v_1 \ v_2)"
        ).set_color(YELLOW)

        group4 = VGroup(v_norm, V).arrange(DOWN, buff=0.6)
        group4.next_to(title, DOWN)

        self.play(Write(v_norm))
        self.play(Write(V))
        self.wait(2)

        # BƯỚC 5: Σ
        self.play(FadeOut(group4))

        sigma = MathTex(
            r"\Sigma = \begin{pmatrix}\sqrt{\lambda_1} & 0 \\ 0 & \sqrt{\lambda_2}\end{pmatrix}"
        ).set_color(YELLOW)

        self.play(Write(sigma))
        self.wait(2)

        # BƯỚC 6: U
        self.play(FadeOut(sigma))

        U = MathTex(
            r"u_i = \frac{A v_i}{\sigma_i}"
        )

        U_mat = MathTex(
            r"U = (u_1 \ u_2)"
        ).set_color(YELLOW)

        group6 = VGroup(U, U_mat).arrange(DOWN, buff=0.6)
        group6.next_to(title, DOWN)

        self.play(Write(U))
        self.play(Write(U_mat))
        self.wait(2)

        # KẾT LUẬN
        self.play(FadeOut(group6))

        final1 = MathTex(r"A = U \Sigma V^T").set_color(YELLOW)

        final2 = VGroup(
            MathTex(r"V^T"),
            self.VText("là chuyển vị của V", 28)
        ).arrange(RIGHT)

        final_group = VGroup(final1, final2).arrange(DOWN, buff=0.6)
        final_group.next_to(title, DOWN)

        self.play(Write(final1))
        self.play(Write(final2))

        self.play(FadeOut(title), FadeOut(final_group))

        self.wait(3)

    def normalize_vectors(self):

        title = self.VText("Chuẩn hóa vector riêng", 40, BLUE).to_edge(UP)
        ex_1 = self.VText("ti là giá trị ứng với λi", 28).to_edge(DOWN)

        s1 = MathTex(
            r"v_i = \frac{1}{\sqrt{1+t_i^2}} \begin{bmatrix}1\\t_i\end{bmatrix}"
        )

        self.play(FadeIn(title), FadeIn(ex_1), Write(s1))
        self.wait(4.5)

        # XOÁ FULL TRƯỚC KHI QUA BƯỚC TIẾP
        self.play(FadeOut(title), FadeOut(ex_1), FadeOut(s1))


    def sigma(self):

        title = self.VText("Tính các giá trị suy biến", 40, BLUE).to_edge(UP)

        s1 = MathTex(r"\sigma_i = \sqrt{\lambda_i}")

        self.play(FadeIn(title), Write(s1))
        self.wait(4.5)

    # XOÁ 
        self.play(FadeOut(title), FadeOut(s1))


    def compute_U(self):

        title = self.VText("Tính U từ Av/σ", 40, BLUE).to_edge(UP)

        s1 = MathTex(r"u_i = \frac{Av_i}{\sigma_i}")

        self.play(FadeIn(title), Write(s1))
        self.wait(4.5)

    # XOÁ 
        self.play(FadeOut(title), FadeOut(s1))

    def final_svd(self):

        title = self.VText("Từ đó, ta có kết quả phân rã", 40, BLUE).to_edge(UP)

        s1 = MathTex(r"A = U \Sigma V^T").set_color(YELLOW)

        self.play(FadeIn(title), Write(s1))
        self.wait(4)

    # XOÁ FULL TRƯỚC KHI QUA BƯỚC TIẾP
        self.play(FadeOut(title), FadeOut(s1))

    # EXPLAIN
    def svd_explain(self):

        title = self.VText("Ý nghĩa của SVD", 40, BLUE).to_edge(UP)

        g = VGroup(
            MathTex(r"A = U \Sigma V^T"),
            self.VText("Vᵀ: xoay hệ trục ban đầu", 28),
            self.VText("Σ: kéo giãn theo trục chính", 28),
            self.VText("U: xoay sang hệ mới", 28),
            self.VText("Giữ k giá trị suy biến σ lớn nhất", 28, YELLOW)
        ).arrange(DOWN, buff=0.5)

        g.next_to(title, DOWN)

        self.play(FadeIn(title))

        for x in g:
            self.play(FadeIn(x))
            self.wait(0.6)

        self.wait(5)

        # XOÁ FULL
        self.play(FadeOut(title), FadeOut(g))


    # HÌNH HỌC
    def geometry(self):

        title = self.VText("Trực quan SVD", 40, BLUE).to_edge(UP)
        label = self.VText("Xoay → kéo giãn → xoay", 32, BLUE).to_edge(DOWN)

        axes = NumberPlane()
        circle = Circle(radius=2, color=WHITE)

        e1 = Arrow(ORIGIN, RIGHT*2, color=RED, buff=0)
        e2 = Arrow(ORIGIN, UP*2, color=GREEN, buff=0)

        vec = Arrow(ORIGIN, [2,1,0], color=YELLOW, buff=0)

        space = VGroup(axes, circle, e1, e2)

        self.play(FadeIn(title), FadeIn(label))
        self.play(Create(axes), Create(circle))
        self.play(GrowArrow(e1), GrowArrow(e2), GrowArrow(vec))
        self.wait(1)

        # BƯỚC 1
        theta = PI/6

        def rotate_vt(p):
            x, y, z = p
            return np.array([
                x*np.cos(theta) + y*np.sin(theta),
                -x*np.sin(theta) + y*np.cos(theta),
                z
            ])

        space1 = space.copy()
        space1.apply_function(rotate_vt)

        v1 = rotate_vt([2,1,0])

        self.play(
            Transform(space, space1),
            Transform(vec, Arrow(ORIGIN, v1, color=BLUE, buff=0)),
            run_time=2.5
        )

        # BƯỚC 2
        Sigma = np.array([[2,0],[0,0.5]])

        def scale_sigma(p):
            x, y, z = p
            new = Sigma @ np.array([x,y])
            return np.array([new[0], new[1], z])

        axes2 = axes.copy()
        axes2.apply_function(scale_sigma)

        circle2 = circle.copy()
        circle2.apply_function(scale_sigma)

        e1_2 = e1.copy()
        e1_2.apply_function(scale_sigma)

        e2_2 = e2.copy()
        e2_2.apply_function(scale_sigma)

        space2 = VGroup(axes2, circle2, e1_2, e2_2)

        v2 = Sigma @ np.array([v1[0], v1[1]])

        self.play(
            Transform(space, space2),
            Transform(vec, Arrow(ORIGIN, [v2[0], v2[1], 0], color=GREEN, buff=0)),
            run_time=2.5
        )

        # BƯỚC 3
        theta2 = PI/4

        def rotate_u(p):
            x, y, z = p
            return np.array([
                x*np.cos(theta2) - y*np.sin(theta2),
                x*np.sin(theta2) + y*np.cos(theta2),
                z
            ])

        space3 = space2.copy()
        space3.apply_function(rotate_u)

        v3 = rotate_u([v2[0], v2[1], 0])

        self.play(
            Transform(space, space3),
            Transform(vec, Arrow(ORIGIN, v3, color=RED, buff=0)),
            run_time=2.5
        )

        self.wait(2)

        # xoá full trước khi qua bước tiếp
        self.play(FadeOut(title), FadeOut(label), FadeOut(space), FadeOut(vec))


    # NÉN ẢNH
    def compression(self):

        title = self.VText("Ứng dụng nén ảnh bằng SVD", 40, BLUE).to_edge(UP)
        self.play(FadeIn(title))

        # PHẦN 1: GIẢI THÍCH

        intro_img = ImageMobject("assets/svd_diagram.jpg").scale(0.9)

        intro_text = self.VText(
            "Ma trận có thể phân rã thành U, Σ, Vᵀ",
            30
        ).to_edge(DOWN)

        self.play(FadeIn(intro_img))
        self.play(Write(intro_text))
        self.wait(3)

        formula = MathTex(r"A = U \Sigma V^T").to_edge(DOWN)
        self.play(Transform(intro_text, formula))
        self.wait(2)

        self.play(FadeOut(intro_img), FadeOut(intro_text))

        # PHẦN 2: BIỂU ĐỒ CÁC GIÁ TRỊ SUY BIẾN

        graph = ImageMobject("assets/singular_values.jpg").scale(0.8)
        self.play(FadeIn(graph))
        self.wait(2)

        highlight = self.VText(
            "Các giá trị suy biến lớn chứa nhiều thông tin nhất",
            28,
            YELLOW
        ).to_edge(DOWN)

        highlight_n = self.VText(
            "Các giá trị suy biến nhỏ chứa ít thông tin hơn",
            28,
            YELLOW
        ).to_edge(DOWN)

        self.play(Write(highlight))
        self.wait(2)

        self.play(Transform(highlight, highlight_n))
        self.wait(2)

        conclusion = self.VText(
            "Giữ k giá trị lớn nhất → giữ phần lớn thông tin",
            28
        ).to_edge(DOWN)

        self.play(Transform(highlight, conclusion))
        self.wait(2)

        self.play(FadeOut(graph), FadeOut(highlight))

        # PHẦN 3: DEMO NÉN ẢNH

        img = Image.open("assets/Kazuha.jpg").convert("L").resize((256,256))
        A = np.array(img)

        U, S, VT = np.linalg.svd(A)

        base = ImageMobject(A).scale(1.8)
        base.next_to(title, DOWN)

        k_text = self.VText("k = 200", 28).next_to(base, DOWN)

        self.play(FadeIn(base), FadeIn(k_text))
        self.wait(1)

        for k in range(200, 5, -10):

            A_k = U[:, :k] @ np.diag(S[:k]) @ VT[:k, :]
            A_k = np.clip(A_k, 0, 255)

            new_img = ImageMobject(A_k).scale(1.8)
            new_img.move_to(base.get_center())

            new_text = self.VText(f"k = {k}", 28)
            new_text.move_to(k_text.get_center())

            self.play(
                Transform(base, new_img),
                Transform(k_text, new_text),
                run_time=0.4
            )

        self.wait(1)

        # PHẦN 4: KẾT LUẬN

        final1 = self.VText("k càng lớn → giữ nhiều thông tin hơn", 30)
        final2 = self.VText("k càng nhỏ → mất nhiều chi tiết", 30, YELLOW)

        final_group = VGroup(final1, final2).arrange(DOWN, buff=0.4)
        final_group.next_to(base, DOWN, buff=1)

        self.play(Write(final1))
        self.wait(0.5)
        self.play(Write(final2))
        self.wait(2)

        # XOÁ FULL
        self.play(
            FadeOut(title),
            FadeOut(base),
            FadeOut(k_text),
            FadeOut(final_group)
        )
