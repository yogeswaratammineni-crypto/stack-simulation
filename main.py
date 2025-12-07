from manim import *

class FullStackSimulation(Scene):
    def construct(self):
        # Dark theme
        self.camera.background_color = BLACK

        # Stack configuration
        max_size = 6
        element_h = 0.7
        element_w = 2.5  # same width for stack and elements
        stack_x = 3.5
        stack_bottom_y = -2.5
        stack_elements = []

        # Step 1: Title
        title = Text("Stack Simulation", font_size=50, weight=BOLD, color=WHITE)
        self.play(Write(title))
        self.wait(1)

        # Step 2: Transform title into stack rectangle
        stack_rect = Rectangle(
            width=element_w,  # same width
            height=element_h * max_size + 0.2,
            stroke_width=4,
            color=BLUE
        ).move_to([stack_x, stack_bottom_y + (element_h * max_size + 0.2)/2, 0])
        self.play(Transform(title, stack_rect))
        self.wait(0.5)

        # Step 3: Stack size below stack
        size_text = Text(f"Size: 0 / {max_size}", font_size=26, color=WHITE)
        size_text.next_to(stack_rect, DOWN, buff=0.25)
        self.play(FadeIn(size_text))

        # Step 4: Operations log container
        op_log = VGroup()
        self.add(op_log)

        def add_operation(text_str):
            op_text = Text(text_str, font_size=26, color=WHITE)
            if len(op_log) == 0:
                op_text.to_edge(LEFT, buff=0.8).shift(UP*2)
            else:
                prev = op_log[-1]
                op_text.next_to(prev, DOWN, aligned_edge=LEFT, buff=0.2)
            op_log.add(op_text)
            self.play(FadeIn(op_text), run_time=0.5)

        # Top arrow + Top text
        top_arrow = Arrow(start=[0,0,0], end=[0,0,0], color=GREEN, buff=0.1)
        top_arrow.set_opacity(0)
        self.add(top_arrow)
        top_label = Text("Top", font_size=24, color=GREEN)
        top_label.set_opacity(0)
        self.add(top_label)

        # Update stack size
        def update_size():
            new_text = Text(f"Size: {len(stack_elements)} / {max_size}", font_size=26, color=WHITE)
            new_text.next_to(stack_rect, DOWN, buff=0.25)
            self.play(Transform(size_text, new_text), run_time=0.4)

        # Flash + shake for overflow/underflow
        def flash_and_shake():
            self.play(stack_rect.animate.set_color(RED))
            self.play(stack_rect.animate.shift(RIGHT*0.2))
            self.play(stack_rect.animate.shift(LEFT*0.4))
            self.play(stack_rect.animate.shift(RIGHT*0.2))
            self.play(stack_rect.animate.set_color(BLUE))

        # Update top arrow + top label smoothly
        def update_top_pointer():
            if stack_elements:
                top = stack_elements[-1]
                x_start = stack_rect.get_left()[0] - 0.7
                y = top.get_center()[1]
                x_end = top.get_left()[0] - 0.05
                self.play(
                    top_arrow.animate.put_start_and_end_on([x_start, y, 0], [x_end, y, 0]),
                    top_label.animate.move_to([x_start-0.3, y, 0]).set_opacity(1),
                    run_time=0.5
                )
                top_arrow.set_opacity(1)
            else:
                self.play(top_arrow.animate.set_opacity(0), top_label.animate.set_opacity(0), run_time=0.3)

        # Display temporary center text
        def show_center_text(text, duration=1.0):
            txt = Text(text, font_size=30, color=YELLOW)
            txt.move_to([-1.5,0,0])
            self.play(FadeIn(txt), run_time=0.3)
            self.wait(duration)
            self.play(FadeOut(txt), run_time=0.3)

        # PUSH
        def push(value):
            add_operation(f"Pushed - {value}")
            self.wait(0.5)
            if len(stack_elements) >= max_size:
                flash_and_shake()
                return
            rect = Rectangle(width=element_w, height=element_h, stroke_width=3, color=GREEN)
            label = Text(str(value), font_size=26, color=WHITE).move_to(rect.get_center())
            block = VGroup(rect, label)
            target_y = stack_bottom_y + element_h/2 + len(stack_elements)*element_h
            block.move_to([stack_x, target_y, 0])
            stack_elements.append(block)
            self.play(FadeIn(block), run_time=0.5)
            update_size()
            update_top_pointer()
            self.wait(0.3)

        # POP
        def pop():
            if not stack_elements:
                add_operation("Pop - Stack Empty")
                flash_and_shake()
                self.wait(0.3)
                return
            top_block = stack_elements.pop()
            add_operation(f"Popped - {top_block[1].text}")
            self.wait(0.5)
            self.play(top_block.animate.shift(UP*0.8 + RIGHT*0.8), FadeOut(top_block), run_time=0.6)
            update_size()
            update_top_pointer()
            self.wait(0.3)

        # PEEK
        def peek():
            if not stack_elements:
                add_operation("Peek - Stack Empty")
                flash_and_shake()
                self.wait(0.3)
                return
            top = stack_elements[-1]
            add_operation(f"Peek - {top[1].text}")
            show_center_text(f"Top element is {top[1].text}")
            update_top_pointer()
            self.wait(0.3)

        # isEmpty
        def isEmpty():
            msg = "Empty" if len(stack_elements)==0 else "Not Empty"
            add_operation(f"isEmpty() - {msg}")
            show_center_text(f"Stack is {msg}")
            self.wait(0.3)

        # isFull
        def isFull():
            msg = "Full" if len(stack_elements)==max_size else "Not Full"
            add_operation(f"isFull() - {msg}")
            show_center_text(f"Stack is {msg}")
            self.wait(0.3)

        # CLEAR
        def clear():
            add_operation("Clear()")
            self.wait(0.5)
            while stack_elements:
                blk = stack_elements.pop()
                self.play(blk.animate.shift(UP*0.9 + RIGHT*0.8), FadeOut(blk), run_time=0.35)
                update_size()
            update_top_pointer()
            self.wait(0.3)

        # Sequence of operations
        push(10)
        push(20)
        push(30)
        peek()
        pop()
        push(40)
        push(50)
        isEmpty()
        isFull()
        clear()

        self.wait(2)
