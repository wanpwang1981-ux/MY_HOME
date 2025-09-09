# =============================================================================
# >> IMPORTS
# =============================================================================
import tkinter as tk
from tkinter import messagebox
try:
    from PIL import Image, ImageTk
except ImportError:
    messagebox.showerror("缺少函式庫", "請安裝 Pillow 函式庫: pip install Pillow")
    exit()
import random

# =============================================================================
# >> CLASSES
# =============================================================================
class WhacAMole(tk.Tk):
    """打地鼠遊戲主類別"""

    def __init__(self):
        """初始化遊戲視窗和變數"""
        super().__init__()
        self.title("打地鼠")
        self.geometry("600x700")
        self.resizable(False, False)

        # -- 載入圖片 --
        self.load_images()

        # -- 遊戲變數 --
        self.score = 0
        self.time_left = 30
        self.game_over = False
        self.current_mole_index = -1

        # -- 介面元素 --
        self.create_widgets()

        # -- 啟動遊戲循環 --
        self.show_mole()
        self.update_timer()

    def load_images(self):
        """載入並處理遊戲所需的圖片"""
        try:
            mole_image = Image.open("assets/mole.png").resize((100, 80), Image.Resampling.LANCZOS)
            self.mole_photo = ImageTk.PhotoImage(mole_image)
            hole_image = Image.open("assets/hole.png").resize((120, 60), Image.Resampling.LANCZOS)
            self.hole_photo = ImageTk.PhotoImage(hole_image)
        except FileNotFoundError:
            messagebox.showerror("錯誤", "找不到圖片資源，請確認 'assets' 資料夾中有 mole.png 和 hole.png")
            self.destroy()
        except Exception as e:
            messagebox.showerror("錯誤", f"載入圖片時發生錯誤: {e}")
            self.destroy()

    def create_widgets(self):
        """建立遊戲介面的所有元件"""
        # 標題
        title_label = tk.Label(self, text="打地鼠遊戲", font=("Arial", 30, "bold"))
        title_label.pack(pady=10)

        # 分數和時間框架
        info_frame = tk.Frame(self)
        info_frame.pack(pady=10)

        # 分數
        self.score_label = tk.Label(info_frame, text=f"分數: {self.score}", font=("Arial", 20))
        self.score_label.grid(row=0, column=0, padx=20)

        # 時間
        self.time_label = tk.Label(info_frame, text=f"時間: {self.time_left}", font=("Arial", 20))
        self.time_label.grid(row=0, column=1, padx=20)

        # 地鼠洞框架
        self.mole_frame = tk.Frame(self, bg="#4A2A00") # 深咖啡色背景
        self.mole_frame.pack(pady=20)

        # 建立地鼠洞
        self.holes = []
        for i in range(9):
            hole = tk.Label(self.mole_frame, image=self.hole_photo, bd=0, bg="#4A2A00")
            hole.grid(row=i//3, column=i%3, padx=15, pady=15)
            hole.bind("<Button-1>", lambda event, index=i: self.whack(index))
            self.holes.append(hole)

    def update_timer(self):
        """每秒更新計時器"""
        if self.time_left > 0 and not self.game_over:
            self.time_left -= 1
            self.time_label.config(text=f"時間: {self.time_left}")
            self.after(1000, self.update_timer)
        elif not self.game_over:
            self.end_game()

    def show_mole(self):
        """在地鼠洞中隨機顯示地鼠"""
        if self.game_over:
            return

        # 隱藏上一隻地鼠
        if self.current_mole_index != -1:
            self.holes[self.current_mole_index].config(image=self.hole_photo)

        # 隨機選擇一個新洞來顯示地鼠
        self.current_mole_index = random.randint(0, 8)
        self.holes[self.current_mole_index].config(image=self.mole_photo)

        # 設定下一隻地鼠出現的時間 (800ms 到 1500ms 之間)
        self.after(random.randint(800, 1500), self.show_mole)

    def whack(self, index):
        """處理玩家點擊地鼠的事件"""
        if self.game_over:
            return

        # 檢查是否點擊到有地鼠的洞
        if index == self.current_mole_index:
            self.score += 1
            self.score_label.config(text=f"分數: {self.score}")
            # 立即隱藏地鼠，避免重複計分
            self.holes[self.current_mole_index].config(image=self.hole_photo)
            self.current_mole_index = -1

    def end_game(self):
        """結束遊戲並顯示最終分數"""
        self.game_over = True
        self.time_label.config(text="時間到!")

        # 確保最後一隻地鼠消失
        if self.current_mole_index != -1:
            self.holes[self.current_mole_index].config(image=self.hole_photo)

        # 顯示重新開始按鈕
        self.restart_button = tk.Button(self, text="重新開始", font=("Arial", 20), command=self.restart_game)
        self.restart_button.pack(pady=20)

    def restart_game(self):
        """重置遊戲狀態以重新開始"""
        # 重置變數
        self.score = 0
        self.time_left = 30
        self.game_over = False

        # 更新介面
        self.score_label.config(text=f"分數: {self.score}")
        self.time_label.config(text=f"時間: {self.time_left}")
        self.restart_button.destroy()

        # 重新啟動遊戲循環
        self.show_mole()
        self.update_timer()

# =============================================================================
# >> MAIN
# =============================================================================
if __name__ == "__main__":
    game = WhacAMole()
    game.mainloop()
