import tkinter as tk
from tkinter import messagebox
import random


# 순발력 테스트 클릭 게임을 관리하는 클래스입니다.
# 클래스는 관련 있는 변수와 기능을 한곳에 묶어 주는 상자라고 생각하면 됩니다.
class ReactionClickGame:
    # 게임 화면의 가로 크기를 정합니다.
    WINDOW_WIDTH = 600

    # 게임 화면의 세로 크기를 정합니다.
    WINDOW_HEIGHT = 400

    # 게임이 진행되는 시간을 초 단위로 정합니다.
    GAME_SECONDS = 10

    # 표적 버튼의 가로 크기를 정합니다.
    TARGET_WIDTH = 10

    # 표적 버튼의 세로 크기를 정합니다.
    TARGET_HEIGHT = 3

    # 프로그램이 처음 시작될 때 한 번 실행되는 함수입니다.
    def __init__(self, root):
        # tkinter가 만들어 준 가장 바깥쪽 창을 self.root라는 이름으로 저장합니다.
        self.root = root

        # 창의 제목 표시줄에 보일 글자를 정합니다.
        self.root.title("순발력 테스트 클릭 게임")

        # 창 크기를 "가로x세로" 형태로 지정합니다.
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

        # 사용자가 창 크기를 마음대로 바꾸지 못하게 고정합니다.
        self.root.resizable(False, False)

        # 현재 점수를 저장할 변수를 0으로 준비합니다.
        self.score = 0

        # 남은 시간을 저장할 변수를 10초로 준비합니다.
        self.time_left = self.GAME_SECONDS

        # 게임이 진행 중인지 기억하는 변수입니다. 처음에는 아직 시작 전이므로 False입니다.
        self.is_playing = False

        # 타이머 작업 번호를 저장할 변수입니다. 나중에 필요하면 예약된 타이머를 취소할 수 있습니다.
        self.timer_job = None

        # 게임 안내와 점수, 시간을 표시하는 위쪽 영역을 만듭니다.
        self.info_frame = tk.Frame(self.root)

        # 위쪽 영역을 창의 위에 배치합니다.
        self.info_frame.pack(pady=10)

        # 점수를 보여 줄 글자 라벨을 만듭니다.
        self.score_label = tk.Label(self.info_frame, text="점수: 0", font=("맑은 고딕", 14))

        # 점수 라벨을 왼쪽에 배치하고 오른쪽에 여백을 줍니다.
        self.score_label.pack(side="left", padx=20)

        # 남은 시간을 보여 줄 글자 라벨을 만듭니다.
        self.time_label = tk.Label(self.info_frame, text="남은 시간: 10초", font=("맑은 고딕", 14))

        # 시간 라벨을 점수 라벨 옆에 배치합니다.
        self.time_label.pack(side="left", padx=20)

        # 게임을 시작하는 버튼을 만듭니다.
        self.start_button = tk.Button(
            self.root,
            text="게임 시작",
            font=("맑은 고딕", 14),
            command=self.start_game,
        )

        # 시작 버튼을 화면에 배치합니다.
        self.start_button.pack(pady=5)

        # 표적 버튼이 움직일 넓은 놀이 공간을 만듭니다.
        self.play_area = tk.Frame(
            self.root,
            width=self.WINDOW_WIDTH,
            height=300,
            bg="white",
            relief="solid",
            borderwidth=1,
        )

        # 놀이 공간을 창 아래쪽에 배치합니다.
        self.play_area.pack(pady=10)

        # pack이나 grid가 안쪽 위젯 크기에 맞춰 프레임 크기를 바꾸지 못하게 합니다.
        self.play_area.pack_propagate(False)

        # 클릭할 표적 버튼을 만듭니다. 처음에는 숨겨 두었다가 게임이 시작되면 보여 줍니다.
        self.target_button = tk.Button(
            self.play_area,
            text="클릭!",
            font=("맑은 고딕", 12, "bold"),
            bg="tomato",
            fg="white",
            width=self.TARGET_WIDTH,
            height=self.TARGET_HEIGHT,
            command=self.hit_target,
        )

    # 시작 버튼을 눌렀을 때 실행되는 함수입니다.
    def start_game(self):
        # 점수를 다시 0점으로 초기화합니다.
        self.score = 0

        # 남은 시간을 다시 10초로 초기화합니다.
        self.time_left = self.GAME_SECONDS

        # 게임이 진행 중이라고 표시합니다.
        self.is_playing = True

        # 시작 버튼을 비활성화해서 게임 중에 다시 누르지 못하게 합니다.
        self.start_button.config(state="disabled")

        # 점수 라벨을 초기 점수로 다시 표시합니다.
        self.score_label.config(text="점수: 0")

        # 시간 라벨을 초기 시간으로 다시 표시합니다.
        self.time_label.config(text=f"남은 시간: {self.time_left}초")

        # 표적 버튼을 무작위 위치에 처음 배치합니다.
        self.move_target()

        # 1초마다 남은 시간을 줄이는 타이머를 시작합니다.
        self.count_down()

    # 표적 버튼을 클릭했을 때 실행되는 함수입니다.
    def hit_target(self):
        # 게임이 끝난 상태라면 점수가 오르지 않도록 바로 함수를 끝냅니다.
        if not self.is_playing:
            return

        # 표적을 맞혔으므로 점수를 1점 올립니다.
        self.score += 1

        # 화면의 점수 라벨에 새 점수를 표시합니다.
        self.score_label.config(text=f"점수: {self.score}")

        # 표적 버튼을 새로운 무작위 위치로 이동시킵니다.
        self.move_target()

    # 표적 버튼의 위치를 무작위로 바꾸는 함수입니다.
    def move_target(self):
        # 화면 배치 계산이 끝나도록 tkinter에게 잠깐 업데이트를 요청합니다.
        self.root.update_idletasks()

        # 놀이 공간의 실제 가로 크기를 가져옵니다.
        area_width = self.play_area.winfo_width()

        # 놀이 공간의 실제 세로 크기를 가져옵니다.
        area_height = self.play_area.winfo_height()

        # 표적 버튼의 실제 가로 크기를 가져옵니다.
        target_width = self.target_button.winfo_reqwidth()

        # 표적 버튼의 실제 세로 크기를 가져옵니다.
        target_height = self.target_button.winfo_reqheight()

        # 표적이 오른쪽 밖으로 나가지 않도록 가능한 x 좌표의 최댓값을 계산합니다.
        max_x = area_width - target_width

        # 표적이 아래쪽 밖으로 나가지 않도록 가능한 y 좌표의 최댓값을 계산합니다.
        max_y = area_height - target_height

        # 0부터 max_x 사이에서 무작위 x 좌표를 고릅니다.
        x = random.randint(0, max_x)

        # 0부터 max_y 사이에서 무작위 y 좌표를 고릅니다.
        y = random.randint(0, max_y)

        # place는 x, y 좌표를 직접 지정해서 위젯을 배치하는 방법입니다.
        self.target_button.place(x=x, y=y)

    # 1초마다 남은 시간을 줄이는 함수입니다.
    def count_down(self):
        # 남은 시간이 0초보다 크면 게임을 계속 진행합니다.
        if self.time_left > 0:
            # 시간 라벨에 현재 남은 시간을 표시합니다.
            self.time_label.config(text=f"남은 시간: {self.time_left}초")

            # 남은 시간을 1초 줄입니다.
            self.time_left -= 1

            # 1000밀리초, 즉 1초 뒤에 count_down 함수를 다시 실행하도록 예약합니다.
            self.timer_job = self.root.after(1000, self.count_down)

        # 남은 시간이 0초가 되면 게임을 끝냅니다.
        else:
            # 게임 종료 처리를 담당하는 함수를 실행합니다.
            self.end_game()

    # 게임이 끝났을 때 실행되는 함수입니다.
    def end_game(self):
        # 게임이 더 이상 진행 중이 아니라고 표시합니다.
        self.is_playing = False

        # 시간 라벨을 0초로 표시합니다.
        self.time_label.config(text="남은 시간: 0초")

        # 표적 버튼을 화면에서 숨깁니다.
        self.target_button.place_forget()

        # 시작 버튼을 다시 활성화해서 새 게임을 시작할 수 있게 합니다.
        self.start_button.config(state="normal")

        # 최종 점수를 팝업창으로 보여 줍니다.
        messagebox.showinfo("게임 종료", f"최종 점수는 {self.score}점입니다!")


# 이 파일을 직접 실행했을 때만 아래 코드가 실행됩니다.
if __name__ == "__main__":
    # tkinter 프로그램의 기본 창을 만듭니다.
    root = tk.Tk()

    # 위에서 만든 게임 클래스를 이용해 실제 게임 화면을 준비합니다.
    game = ReactionClickGame(root)

    # tkinter 이벤트 반복을 시작합니다. 이 줄이 있어야 창이 계속 열려 있고 버튼 클릭도 처리됩니다.
    root.mainloop()
