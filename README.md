# PS2 One-Click VMC Creation Tool 🎮💾

🌍 **[ English ](#-english)** | **[ Українська ](#-українська)** | **[ Русский ](#-русский)**
---
<img width="686" height="419" alt="image" src="https://github.com/user-attachments/assets/927a5232-49f3-497b-b958-7c3d4d23252d" />

---

## 🇬🇧 English

**PS2 One-Click VMC Creation Tool** is a standalone, retro-styled utility designed for the PlayStation 2 homebrew community. It solves the tedious problem of manually creating Virtual Memory Cards (VMCs) for large game libraries in Open PS2 Loader (OPL).

If you are using a modern **exFAT HDD** setup with dozens or hundreds of `.iso` backups, this tool will save you hours of menu navigation by generating perfectly configured VMCs for your entire library in a single click.

### ✨ How it works (Under the Hood)
Unlike other tools, you don't need to rename your `.iso` files to include Game IDs. The magic happens dynamically:
1. **Binary Deep-Scan:** The tool reads the first 5MB of each `.iso` file in your `DVD` folder as raw binary.
2. **Regex ID Extraction:** It searches for the official PlayStation 2 Game ID pattern (e.g., `SLUS_200.00`) directly within the image header.
3. **VMC Generation:** It creates a fresh, zero-filled 8MB `.bin` virtual memory card for each game in the `VMC` folder.
4. **CFG Binding:** It automatically creates or updates the specific game's `.cfg` file in the `CFG` folder, permanently linking `$VMC_0` to the newly generated card.

### 🚀 Features
* **Zero Dependencies:** Distributed as a single compiled `.exe` file. No Python installation required.
* **Intelligent Parsing:** Works with plain ISO names (e.g., `Tekken 5.iso`).
* **Non-Destructive:** Safe to run multiple times; it skips existing VMCs and only updates missing configs.
* **Retro UI:** Multithreaded GUI with a nostalgic PS2 aesthetic.

*Made with love for obscure modding by [Tualatin](https://t.me/IDE_HDD40Gb)*

---

## 🇺🇦 Українська

**PS2 One-Click VMC Creation Tool** — це автономна утиліта в ретро-стилі, створена для homebrew-спільноти PlayStation 2. Вона вирішує проблему ручного створення віртуальних карт пам'яті (VMC) для великих бібліотек ігор в Open PS2 Loader (OPL).

Якщо ви використовуєте сучасну збірку з **exFAT HDD** та десятками або сотнями `.iso` образів, цей інструмент заощадить вам години блукань по меню, згенерувавши ідеально налаштовані VMC для всієї вашої бібліотеки в один клік.

### ✨ Як це працює (Під капотом)
На відміну від інших інструментів, вам не потрібно перейменовувати ваші `.iso` файли, додаючи до них Game ID. Магія відбувається динамічно:
1. **Бінарне сканування:** Утиліта читає перші 5 МБ кожного `.iso` файлу в папці `DVD` як сирий бінарник.
2. **Пошук ID через Regex:** Вона шукає офіційний патерн Game ID для PlayStation 2 (наприклад, `SLUS_200.00`) прямо всередині заголовка образу.
3. **Генерація VMC:** Створює нову віртуальну карту пам'яті `.bin` розміром 8 МБ, заповнену нулями, для кожної гри в папці `VMC`.
4. **Прив'язка CFG:** Автоматично створює або оновлює файл `.cfg` конкретної гри в папці `CFG`, назавжди пов'язуючи `$VMC_0` з щойно створеною картою.

### 🚀 Особливості
* **Жодних залежностей:** Розповсюджується як один скомпільований `.exe` файл. Встановлення Python не потрібне.
* **Розумний парсинг:** Працює зі звичайними назвами ISO (наприклад, `Tekken 5.iso`).
* **Безпека:** Можна запускати кілька разів; пропускає існуючі VMC та оновлює лише відсутні конфіги.
* **Ретро-інтерфейс:** Багатопотоковий GUI з ностальгічною естетикою PS2.

*Зроблено з любов'ю до obscure modding від [Tualatin](https://t.me/IDE_HDD40Gb)*

---

## 🇷🇺 Русский

**PS2 One-Click VMC Creation Tool** — это автономная утилита в ретро-стиле, созданная для homebrew-сообщества PlayStation 2. Она решает нудную проблему ручного создания виртуальных карт памяти (VMC) для больших библиотек игр в Open PS2 Loader (OPL).

Если вы используете современную сборку с **exFAT HDD** и десятками или сотнями `.iso` образов, этот инструмент сэкономит вам часы ползания по менюшкам, сгенерировав идеально настроенные VMC для всей вашей библиотеки в один клик.

### ✨ Как это работает (Под капотом)
В отличие от других инструментов, вам не нужно переименовывать ваши `.iso` файлы, добавляя в них Game ID. Магия происходит динамически:
1. **Бинарное сканирование:** Утилита читает первые 5 МБ каждого `.iso` файла в папке `DVD` как сырой бинарник.
2. **Поиск ID через Regex:** Она ищет официальный паттерн Game ID для PlayStation 2 (например, `SLUS_200.00`) прямо внутри заголовка образа.
3. **Генерация VMC:** Создает новую виртуальную карту памяти `.bin` размером 8 МБ, заполненную нулями, для каждой игры в папке `VMC`.
4. **Привязка CFG:** Автоматически создает или обновляет файл `.cfg` конкретной игры в папке `CFG`, навсегда связывая `$VMC_0` с только что созданной картой.

### 🚀 Особенности
* **Никаких зависимостей:** Распространяется как один скомпилированный `.exe` файл. Установка Python не требуется.
* **Умный парсинг:** Работает с обычными названиями ISO (например, `Tekken 5.iso`).
* **Безопасность:** Можно запускать несколько раз; пропускает существующие VMC и обновляет только недостающие конфиги.
* **Ретро-интерфейс:** Многопоточный GUI с ностальгической эстетикой PS2.

*Сделано с любовью к obscure modding от [Tualatin](https://t.me/IDE_HDD40Gb)*
