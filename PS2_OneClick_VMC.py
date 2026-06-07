import sys
import os
import re
import threading
import time
import shutil
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

def resource_path(relative_path):
    """Получает абсолютный путь к ресурсу, работает и в dev, и в скомпилированном PyInstaller .exe"""
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PS2VmcApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PS2 VMC One-Click Creator")
        self.root.resizable(False, False)
        
        # --- Железобетонная установка иконки окна через Pillow ---
        icon_path = resource_path("app_icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(default=icon_path)
            except Exception:
                pass
                
            try:
                # Насильный метод замены пера картинкой высокого разрешения
                icon_img = ImageTk.PhotoImage(Image.open(icon_path))
                self.root.iconphoto(True, icon_img)
            except Exception:
                pass
        # --------------------------------------------------------
        
        self.selected_path = ""
        self.is_running = False
        self.blink_state = True
        self.spoiler_expanded = False
        
        # Константы для логики PS2
        self.ID_PATTERN = re.compile(b'[A-Z]{4}_[0-9]{3}\.[0-9]{2}')
        
        # Цвета в стиле PS2
        self.PS2_BLUE = "#0057B8"
        self.PS2_CYAN = "#00F0FF"
        
        # Загрузка фона через менеджер ресурсов
        self.bg_image_path = resource_path("background.jpg")
        if os.path.exists(self.bg_image_path):
            self.bg_image = Image.open(self.bg_image_path)
            self.img_w, self.img_h = self.bg_image.size
        else:
            self.bg_image = Image.new("RGB", (600, 400), "#0a0a1a")
            self.img_w, self.img_h = 600, 400
            
        self.root.geometry(f"{self.img_w}x{self.img_h}")
        self.tk_bg = ImageTk.PhotoImage(self.bg_image)
        
        # Основной холст для точного позиционирования
        self.canvas = tk.Canvas(root, width=self.img_w, height=self.img_h, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.tk_bg, anchor="nw")
        
        # Отрисовка интерфейса
        self.build_ui()

    def create_text_with_effects(self, x, y, text, font, fill="white", anchor="center", tag=None):
        """Создает текст с черной обводкой и тенью"""
        # Тень
        self.canvas.create_text(x+2, y+2, text=text, font=font, fill="black", anchor=anchor, tags=tag)
        # Обводка
        for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1), (0,-1), (0,1), (-1,0), (1,0)]:
            self.canvas.create_text(x+dx, y+dy, text=text, font=font, fill="black", anchor=anchor, tags=tag)
        # Основной текст
        return self.canvas.create_text(x, y, text=text, font=font, fill=fill, anchor=anchor, tags=tag)

    def draw_custom_button(self, x, y, w, h, text, command, tooltip=None):
        """Рисует обведенную рамкой кнопку с эффектами текста и подсказкой"""
        rect = self.canvas.create_rectangle(x, y, x+w, y+h, outline=self.PS2_BLUE, width=2, fill="#050515")
        text_id = self.create_text_with_effects(x + w//2, y + h//2, text, ("Arial", 11, "bold"), fill="white")
        
        def on_enter(e):
            self.canvas.itemconfig(rect, outline=self.PS2_CYAN)
            if tooltip:
                tt_y = y - 15
                self.tt_txt = self.canvas.create_text(x + w//2, tt_y, text=tooltip, fill=self.PS2_CYAN, font=("Arial", 9, "italic"), tags="tooltip")
                bbox = self.canvas.bbox(self.tt_txt)
                self.tt_bg = self.canvas.create_rectangle(bbox[0]-5, bbox[1]-2, bbox[2]+5, bbox[3]+2, fill="#02020a", outline=self.PS2_BLUE, tags="tooltip")
                self.canvas.tag_lower(self.tt_bg, self.tt_txt)
                
        def on_leave(e):
            self.canvas.itemconfig(rect, outline=self.PS2_BLUE)
            if tooltip:
                self.canvas.delete("tooltip")
                
        def on_click(e):
            command()

        for item in (rect, text_id):
            self.canvas.tag_bind(item, "<Enter>", on_enter)
            self.canvas.tag_bind(item, "<Leave>", on_leave)
            self.canvas.tag_bind(item, "<Button-1>", on_click)

    def create_clickable_link(self, x, y, text, url, outline_color="white"):
        """Создает кликабельную ссылку с эффектом наведения и кастомной обводкой"""
        link_ids = []
        
        if outline_color:
            for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1), (0,-1), (0,1), (-1,0), (1,0)]:
                bg_id = self.canvas.create_text(x+dx, y+dy, text=text, fill=outline_color, font=("Arial", 9, "bold"), anchor="w", justify="left")
                link_ids.append(bg_id)
                
        main_id = self.canvas.create_text(x, y, text=text, fill="#333333", font=("Arial", 9, "bold", "underline"), anchor="w", justify="left")
        link_ids.append(main_id)
        
        def on_enter(e):
            self.canvas.itemconfig(main_id, fill=self.PS2_CYAN)
            self.canvas.config(cursor="hand2")
            
        def on_leave(e):
            self.canvas.itemconfig(main_id, fill="#333333")
            self.canvas.config(cursor="")
            
        def on_click(e):
            webbrowser.open(url)
            
        for item in link_ids:
            self.canvas.tag_bind(item, "<Enter>", on_enter)
            self.canvas.tag_bind(item, "<Leave>", on_leave)
            self.canvas.tag_bind(item, "<Button-1>", on_click)

    def build_ui(self):
        mid_x = self.img_w // 2
        
        # Заголовок
        self.create_text_with_effects(mid_x, 30, "PS2 VMC AUTOMATION TOOL", ("Arial", 16, "bold"), fill=self.PS2_CYAN)
        
        # Блок 1: Поиск HDD
        btn1_y = 90
        self.draw_custom_button(
            mid_x - 220, btn1_y, 180, 35, 
            "Find your's PS2 HDD", 
            self.select_folder,
            tooltip="Укажите путь к папке DVD на вашем накопителе"
        )
        
        self.path_text_tag = "path_text"
        self.update_path_display("Path: Not selected...")
        
        # Разделитель
        self.canvas.create_line(40, 160, self.img_w - 40, 160, fill=self.PS2_BLUE, width=1)
        
        # Блок 2: Выполнение
        self.draw_custom_button(mid_x - 125, 190, 250, 40, "Create PS2 VMC for ALL Games", self.start_magic_thread)
        
        self.status_tag = "blinking_status"
        
        # --- ПАСХАЛКИ И ССЫЛКИ (Левый нижний угол) ---
        easter_egg_y = self.img_h - 60 
        
        # Цвета обводки (outline_color): "white", "black", "#0057B8" (синий PS2) или "" (отключить)
        self.create_clickable_link(
            15, easter_egg_y, 
            "Made with love for\nobscure modding by Tualatin", 
            "https://t.me/IDE_HDD40Gb",
            outline_color=""
        )
        
        self.create_clickable_link(
            15, easter_egg_y + 35, 
            "💿 My_RetroTube", 
            "https://www.youtube.com/@HDD40Gb",
            outline_color=""
        )
        # ---------------------------------------------
        
        # Спойлер и консоль логов
        self.spoiler_btn_y = self.img_h - 40
        self.draw_custom_button(mid_x - 75, self.spoiler_btn_y, 150, 25, "Magic Spoiler", self.toggle_spoiler)
        
        self.log_frame = tk.Frame(self.root, bg="black")
        self.log_box = ScrolledText(self.log_frame, bg="#02020a", fg=self.PS2_CYAN, insertbackground="white", font=("Consolas", 9), height=8)
        self.log_box.pack(fill="both", expand=True, padx=5, pady=5)

    def update_path_display(self, text):
        self.canvas.delete(self.path_text_tag)
        mid_x = self.img_w // 2
        short_text = text if len(text) <= 30 else text[:27] + "..."
        self.create_text_with_effects(mid_x + 10, 108, short_text, ("Arial", 10, "italic"), fill="#aaaaaa", anchor="nw", tag=self.path_text_tag)

    def select_folder(self):
        path = filedialog.askdirectory(title="Выберите папку DVD на HDD вашей PS2")
        if path:
            if os.path.basename(path).lower() != "dvd":
                messagebox.showwarning("Внимание", "Вы выбрали не папку 'DVD'. Убедитесь, что внутри находятся ISO-образы.")
            self.selected_path = path
            self.update_path_display(f"Path: {path}")
            self.canvas.create_text(self.img_w // 2 - 240, 108, text="✔", font=("Arial", 14, "bold"), fill="#00FF00", anchor="center")

    def toggle_spoiler(self):
        if not self.spoiler_expanded:
            self.root.geometry(f"{self.img_w}x{self.img_h + 150}")
            self.log_frame.pack(fill="both", expand=True, side="bottom")
            self.spoiler_expanded = True
        else:
            self.log_frame.pack_forget()
            self.root.geometry(f"{self.img_w}x{self.img_h}")
            self.spoiler_expanded = False

    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    def blink_effect(self):
        if self.is_running:
            color = self.PS2_CYAN if self.blink_state else "#002b5c"
            self.canvas.itemconfig("status_main_text", fill=color)
            self.blink_state = not self.blink_state
            self.root.after(400, self.blink_effect)
        else:
            self.canvas.delete(self.status_tag)

    def start_magic_thread(self):
        if not self.selected_path:
            messagebox.showerror("Ошибка", "Сначала укажите путь к вашей папке DVD!")
            return
        if self.is_running:
            return
            
        self.is_running = True
        mid_x = self.img_w // 2
        self.create_text_with_effects(mid_x, 260, "Doing PS2 Magic...", ("Arial", 14, "bold"), fill=self.PS2_CYAN, tag=self.status_tag)
        all_items = self.canvas.find_withtag(self.status_tag)
        if all_items:
            self.canvas.itemconfig(all_items[-1], tags=(self.status_tag, "status_main_text"))
            
        self.blink_effect()
        threading.Thread(target=self.process_core, daemon=True).start()

    def process_core(self):
        # 1. Проверяем наличие шаблона перед стартом магии
        template_path = resource_path("template_8mb.bin")
        if not os.path.exists(template_path):
            self.log("[-] КРИТИЧЕСКАЯ ОШИБКА: Файл 'template_8mb.bin' не найден!")
            messagebox.showerror("Ошибка", "Файл шаблона 'template_8mb.bin' не найден рядом с программой. Поместите его в папку и перезапустите!")
            self.is_running = False
            return

        base_dir = os.path.dirname(self.selected_path)
        vmc_dir = os.path.join(base_dir, "VMC")
        cfg_dir = os.path.join(base_dir, "CFG")
        
        for folder in [vmc_dir, cfg_dir]:
            if not os.path.exists(folder):
                os.makedirs(folder)
                
        try:
            iso_files = [f for f in os.listdir(self.selected_path) if f.lower().endswith('.iso')]
        except Exception as e:
            self.log(f"[Ошибка доступа к папке]: {str(e)}")
            self.is_running = False
            return

        self.log(f"[СТАРТ] Найдено файлов для анализа: {len(iso_files)}")
        
        for iso_file in iso_files:
            iso_path = os.path.join(self.selected_path, iso_file)
            game_id = None
            
            try:
                with open(iso_path, 'rb') as f:
                    chunk = f.read(5 * 1024 * 1024)
                    match = self.ID_PATTERN.search(chunk)
                    if match:
                        game_id = match.group(0).decode('utf-8')
            except Exception as e:
                self.log(f"[-] Ошибка чтения файла {iso_file}: {str(e)}")
                continue

            if not game_id:
                self.log(f"[-] ID не обнаружен в образе: {iso_file}")
                continue

            self.log(f"[+] Обработка: {game_id} -> {iso_file}")

            # --- ОБНОВЛЕНО: Создание VMC копированием шаблона ---
            vmc_path = os.path.join(vmc_dir, f"{game_id}_0.bin")
            if not os.path.exists(vmc_path):
                shutil.copyfile(template_path, vmc_path)
                self.log(f"    -> Карта успешно скопирована из шаблона.")
            else:
                self.log(f"    -> Карта памяти уже существовала.")
            # ----------------------------------------------------

            # Запись CFG
            cfg_path = os.path.join(cfg_dir, f"{game_id}.cfg")
            vmc_line = f"$VMC_0={game_id}_0"
            
            cfg_content = ""
            if os.path.exists(cfg_path):
                with open(cfg_path, 'r', encoding='utf-8', errors='ignore') as f:
                    cfg_content = f.read()

            if vmc_line not in cfg_content:
                with open(cfg_path, 'a', encoding='utf-8') as f:
                    if cfg_content and not cfg_content.endswith('\n'):
                        f.write('\n')
                    f.write(vmc_line + '\n')
                self.log(f"    -> Конфигурация успешно обновлена.")
            else:
                self.log(f"    -> Конфиг уже содержал привязку.")
                
            time.sleep(0.05)

        self.log("[ЗАВЕРШЕНО] Процесс успешно выполнен!")
        self.is_running = False
        messagebox.showinfo("Успех", "Магия PS2 успешно завершена! Все карты сгенерированы.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PS2VmcApp(root)
    root.mainloop()
