import tkinter as tk
from tkinter import messagebox


class GomokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("五子棋游戏")

        # 游戏参数
        self.board_size = 15
        self.cell_size = 40
        self.board_width = self.board_size * self.cell_size
        self.board_height = self.board_size * self.cell_size
        self.current_player = 1  # 1: 黑子, 2: 白子
        self.game_over = False
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]

        # 创建UI
        self.create_widgets()

    def create_widgets(self):
        # 创建主框架
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        # 创建画布
        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.board_width,
            height=self.board_height,
            bg="#E8C19D",  # 棋盘背景色
            highlightthickness=0
        )
        self.canvas.pack()

        # 绘制棋盘网格
        self.draw_board()

        # 绑定鼠标点击事件
        self.canvas.bind("<Button-1>", self.on_click)

        # 创建状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("黑方回合")
        self.status_bar = tk.Label(self.main_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 创建控制按钮
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(pady=10)

        self.reset_button = tk.Button(self.control_frame, text="重置游戏", command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.undo_button = tk.Button(self.control_frame, text="悔棋", command=self.undo_move)
        self.undo_button.pack(side=tk.LEFT, padx=5)

        # 历史记录
        self.move_history = []

    def draw_board(self):
        # 绘制网格线
        for i in range(self.board_size):
            # 横线
            self.canvas.create_line(
                self.cell_size,
                self.cell_size * (i + 1),
                self.board_width - self.cell_size,
                self.cell_size * (i + 1),
                width=1
            )
            # 竖线
            self.canvas.create_line(
                self.cell_size * (i + 1),
                self.cell_size,
                self.cell_size * (i + 1),
                self.board_height - self.cell_size,
                width=1
            )

        # 绘制天元和星位
        star_points = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
        for x, y in star_points:
            self.canvas.create_oval(
                self.cell_size * (x + 1) - 4,
                self.cell_size * (y + 1) - 4,
                self.cell_size * (x + 1) + 4,
                self.cell_size * (y + 1) + 4,
                fill="black"
            )

    def on_click(self, event):
        if self.game_over:
            return

        # 计算点击位置对应的棋盘坐标
        x = round((event.x - self.cell_size) / self.cell_size)
        y = round((event.y - self.cell_size) / self.cell_size)

        # 检查坐标是否在有效范围内
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            # 检查是否已落子
            if self.board[x][y] == 0:
                # 记录落子
                self.board[x][y] = self.current_player
                self.move_history.append((x, y))

                # 绘制棋子
                color = "black" if self.current_player == 1 else "white"
                self.canvas.create_oval(
                    self.cell_size * (x + 1) - 15,
                    self.cell_size * (y + 1) - 15,
                    self.cell_size * (x + 1) + 15,
                    self.cell_size * (y + 1) + 15,
                    fill=color,
                    outline="black" if color == "white" else ""
                )

                # 检查胜负
                if self.check_win(x, y, self.current_player):
                    winner = "黑方" if self.current_player == 1 else "白方"
                    self.status_var.set(f"{winner}获胜！")
                    messagebox.showinfo("游戏结束", f"{winner}获胜！")
                    self.game_over = True
                    return

                # 切换玩家
                self.current_player = 2 if self.current_player == 1 else 1
                self.status_var.set(f"{'黑方' if self.current_player == 1 else '白方'}回合")

    def check_win(self, x, y, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dx, dy in directions:
            count = 1

            # 正方向检查
            for i in range(1, 5):
                nx, ny = x + dx * i, y + dy * i
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.board[nx][ny] == player:
                        count += 1
                    else:
                        break
                else:
                    break

            # 反方向检查
            for i in range(1, 5):
                nx, ny = x - dx * i, y - dy * i
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.board[nx][ny] == player:
                        count += 1
                    else:
                        break
                else:
                    break

            if count >= 5:
                return True

        return False

    def reset_game(self):
        # 清空棋盘
        self.canvas.delete("all")
        self.draw_board()

        # 重置游戏状态
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 1
        self.game_over = False
        self.move_history = []
        self.status_var.set("黑方回合")

    def undo_move(self):
        if not self.move_history or self.game_over:
            return

        # 移除最后一步
        x, y = self.move_history.pop()
        self.board[x][y] = 0

        # 重绘棋盘
        self.canvas.delete("all")
        self.draw_board()

        # 重绘所有棋子
        for i in range(len(self.move_history)):
            mx, my = self.move_history[i]
            player = 1 if i % 2 == 0 else 2
            color = "black" if player == 1 else "white"

            self.canvas.create_oval(
                self.cell_size * (mx + 1) - 15,
                self.cell_size * (my + 1) - 15,
                self.cell_size * (mx + 1) + 15,
                self.cell_size * (my + 1) + 15,
                fill=color,
                outline="black" if color == "white" else ""
            )

        # 切换回上一个玩家
        self.current_player = 1 if len(self.move_history) % 2 == 0 else 2
        self.status_var.set(f"{'黑方' if self.current_player == 1 else '白方'}回合")


if __name__ == "__main__":
    root = tk.Tk()
    game = GomokuGame(root)
    root.mainloop()