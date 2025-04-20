import tkinter as tk
from tkinter import ttk
from tkinter import font

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер")
        self.root.overrideredirect(True)  # Убираем рамку окна
        self.root.attributes('-topmost', True)  # Окно поверх всех окон
        
        # Настройка размеров
        self.width = 200
        self.height = 120
        self.root.geometry(f"{self.width}x{self.height}+100+100")  # Начальная позиция
        
        # Настройка стилей
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Кастомные стили для кнопок
        self.style.configure('Green.TButton', background='#4CAF50', foreground='white')
        self.style.configure('Red.TButton', background='#F44336', foreground='white')
        self.style.configure('Blue.TButton', background='#2196F3', foreground='white')
        
        # Переменные для перемещения окна
        self.x = 0
        self.y = 0
        
        # Переменные таймера
        self.remaining_time = 0
        self.is_running = False
        
        # Шрифты
        self.timer_font = font.Font(family='Helvetica', size=20, weight='bold')
        self.button_font = font.Font(family='Helvetica', size=9)
        
        # Основной контейнер
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Привязываем перемещение ко всему окну
        main_frame.bind("<ButtonPress-1>", self.start_move)
        main_frame.bind("<B1-Motion>", self.on_move)
        
        # Поле ввода/отображения времени
        self.time_entry = ttk.Entry(main_frame, font=self.timer_font, width=7, 
                                  justify='center')
        self.time_entry.insert(0, "45:00")
        self.time_entry.pack(pady=(8, 8))
        
        # Фрейм для кнопок Старт/Стоп
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=5)
        
        # Кнопки Старт и Стоп
        self.start_button = ttk.Button(button_frame, text="Старт", 
                                     style='Green.TButton',
                                     command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        self.stop_button = ttk.Button(button_frame, text="Стоп", 
                                    style='Red.TButton',
                                    command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        # Кнопка Сброс
        self.reset_button = ttk.Button(main_frame, text="Сброс", 
                                     style='Blue.TButton',
                                     command=self.reset_timer)
        self.reset_button.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Привязываем горячую клавишу Alt+Q
        self.root.bind('<Alt-q>', lambda e: self.root.destroy())
        self.root.bind('<Alt-Q>', lambda e: self.root.destroy())
    
    def start_move(self, event):
        """Начало перемещения окна"""
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        """Перемещение окна"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def start_timer(self):
        if not self.is_running:
            try:
                minutes, seconds = map(int, self.time_entry.get().split(':'))
                self.remaining_time = minutes * 60 + seconds
            except:
                self.remaining_time = 45 * 60
            
            self.is_running = True
            self.time_entry.config(state='readonly')
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.update_timer()
    
    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            self.time_entry.config(state='normal')
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def reset_timer(self):
        self.is_running = False
        self.time_entry.config(state='normal')
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "45:00")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def update_timer(self):
        if self.is_running and self.remaining_time > 0:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.time_entry.config(state='normal')
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, f"{minutes:02d}:{seconds:02d}")
            self.time_entry.config(state='readonly')
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining_time <= 0:
            self.time_entry.config(state='normal')
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, "00:00")
            self.time_entry.config(state='readonly')
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
