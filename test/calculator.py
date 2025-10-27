import tkinter as tk
from tkinter import messagebox

# 계산기 클래스 정의
class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("간단한 계산기")
        self.geometry("300x400")
        self.resizable(False, False)
        self.configure(bg="#f7f7f7")

        self.expression = ""

        # 결과창
        self.entry = tk.Entry(self, font=("Arial", 20), border=0, relief="ridge", justify="right")
        self.entry.pack(fill="x", ipady=15, pady=(20, 10), padx=10)

        # 버튼 프레임
        btn_frame = tk.Frame(self, bg="#f7f7f7")
        btn_frame.pack()

        # 버튼 정의
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', 'C', '+'],
        ]

        # 버튼 배치
        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                tk.Button(
                    btn_frame, text=char, font=("Arial", 16), width=5, height=2,
                    command=lambda ch=char: self.on_button_click(ch)
                ).grid(row=r, column=c, padx=5, pady=5)

        # = 버튼
        tk.Button(
            self, text="=", font=("Arial", 18, "bold"),
            bg="#4CAF50", fg="white", width=28, height=2,
            command=self.evaluate
        ).pack(pady=10)

    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
        else:
            self.expression += str(char)
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def evaluate(self):
        try:
            result = str(eval(self.expression))
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, result)
            self.expression = result
        except Exception as e:
            messagebox.showerror("Error", "잘못된 수식입니다.")
            self.expression = ""
            self.entry.delete(0, tk.END)

# 실행
if __name__ == "__main__":
    app = Calculator()
    app.mainloop()


