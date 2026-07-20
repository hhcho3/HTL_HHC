import random
import tkinter as tk
from tkinter import messagebox


class ReactionClickGame:
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 400
    GAME_SECONDS = 10
    TARGET_COUNT = 2
    TARGET_WIDTH = 10
    TARGET_HEIGHT = 3

    def __init__(self, root):
        self.root = root
        self.root.title("반응 속도 클릭 게임")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        self.score = 0
        self.time_left = self.GAME_SECONDS
        self.is_playing = False
        self.timer_job = None

        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=10)

        self.score_label = tk.Label(
            self.info_frame, text="점수: 0", font=("맑은 고딕", 14)
        )
        self.score_label.pack(side="left", padx=20)

        self.time_label = tk.Label(
            self.info_frame,
            text=f"남은 시간: {self.GAME_SECONDS}초",
            font=("맑은 고딕", 14),
        )
        self.time_label.pack(side="left", padx=20)

        self.start_button = tk.Button(
            self.root,
            text="게임 시작",
            font=("맑은 고딕", 14),
            command=self.start_game,
        )
        self.start_button.pack(pady=5)

        self.play_area = tk.Frame(
            self.root,
            width=self.WINDOW_WIDTH,
            height=300,
            bg="white",
            relief="solid",
            borderwidth=1,
        )
        self.play_area.pack(pady=10)
        self.play_area.pack_propagate(False)

        colors = ("tomato", "royalblue")
        self.target_buttons = []
        for index in range(self.TARGET_COUNT):
            button = tk.Button(
                self.play_area,
                text="클릭!",
                font=("맑은 고딕", 12, "bold"),
                bg=colors[index % len(colors)],
                fg="white",
                width=self.TARGET_WIDTH,
                height=self.TARGET_HEIGHT,
                command=lambda target_index=index: self.hit_target(target_index),
            )
            self.target_buttons.append(button)

    def start_game(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        self.score = 0
        self.time_left = self.GAME_SECONDS
        self.is_playing = True
        self.start_button.config(state="disabled")
        self.score_label.config(text="점수: 0")
        self.time_label.config(text=f"남은 시간: {self.time_left}초")

        for index in range(self.TARGET_COUNT):
            self.move_target(index)

        self.count_down()

    def hit_target(self, target_index):
        if not self.is_playing:
            return

        self.score += 1
        self.score_label.config(text=f"점수: {self.score}")
        self.move_target(target_index)

    def move_target(self, target_index):
        self.root.update_idletasks()

        button = self.target_buttons[target_index]
        area_width = self.play_area.winfo_width()
        area_height = self.play_area.winfo_height()
        target_width = button.winfo_reqwidth()
        target_height = button.winfo_reqheight()
        max_x = max(0, area_width - target_width)
        max_y = max(0, area_height - target_height)

        # 다른 표적과 겹치지 않는 위치를 우선해서 찾습니다.
        for _ in range(100):
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
            if not self.overlaps_other_target(
                target_index, x, y, target_width, target_height
            ):
                break

        button.place(x=x, y=y)

    def overlaps_other_target(self, target_index, x, y, width, height):
        for index, other in enumerate(self.target_buttons):
            if index == target_index or not other.winfo_ismapped():
                continue

            other_x = other.winfo_x()
            other_y = other.winfo_y()
            other_width = other.winfo_width()
            other_height = other.winfo_height()

            if (
                x < other_x + other_width
                and x + width > other_x
                and y < other_y + other_height
                and y + height > other_y
            ):
                return True
        return False

    def count_down(self):
        if self.time_left > 0:
            self.time_label.config(text=f"남은 시간: {self.time_left}초")
            self.time_left -= 1
            self.timer_job = self.root.after(1000, self.count_down)
        else:
            self.end_game()

    def end_game(self):
        self.is_playing = False
        self.timer_job = None
        self.time_label.config(text="남은 시간: 0초")

        for button in self.target_buttons:
            button.place_forget()

        self.start_button.config(state="normal")
        messagebox.showinfo("게임 종료", f"최종 점수는 {self.score}점입니다!")


if __name__ == "__main__":
    root = tk.Tk()
    game = ReactionClickGame(root)
    root.mainloop()
