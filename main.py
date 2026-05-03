import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import scrolledtext


# ========================= ЛОГИЧЕСКАЯ ЧАСТЬ / LOGIC PART =========================
# Здесь находится ваша исходная логика работы со списком

def create_user_list(nums, elements):
    """
    Логика создания списка на основе введённых данных.
    nums - количество элементов
    elements - список введённых значений (строки)
    Возвращает итоговый список.
    """
    user_list = []
    i = 0
    while i < nums:
        # Берём элемент по индексу i из elements
        user_list.append(elements[i])
        i += 1
    return user_list


def format_list_as_column(items):
    """Формат 1: Вывод в столбик с номерами"""
    result = "Ваш итоговый список (в столбик с номерами):\n\n"
    for i, item in enumerate(items, 1):
        result += f"{i}. {item}\n"
    result += f"\nВсего элементов: {len(items)}"
    return result


def format_list_as_python(items):
    """Формат 2: Классический Python список"""
    result = "Ваш итоговый список (Python-список):\n\n"
    # Добавляем кавычки для строковых элементов
    formatted_items = []
    for item in items:
        # Если элемент похож на число, не добавляем кавычки
        if item.isdigit() or (item[0] == '-' and item[1:].isdigit()):
            formatted_items.append(item)
        else:
            formatted_items.append(f"'{item}'")

    result += "[" + ", ".join(formatted_items) + "]"
    result += f"\n\nТип: list\nДлина: {len(items)} элементов"
    return result


def format_list_as_horizontal(items):
    """Формат 3: Вывод в строку через разделитель"""
    result = "Ваш итоговый список (в строку):\n\n"
    result += " → ".join(items)
    result += f"\n\nРазделитель: ' → '\nВсего элементов: {len(items)}"
    return result


def format_list_as_table(items):
    """Формат 4: Вывод в виде таблицы (по 5 элементов в строке)"""
    result = "Ваш итоговый список (таблица):\n\n"
    cols = 5  # Количество колонок в таблице
    for i in range(0, len(items), cols):
        row = items[i:i + cols]
        # Выравниваем колонки
        formatted_row = []
        for j, item in enumerate(row):
            # Ограничиваем длину элемента для красоты таблицы
            display_item = item if len(item) <= 15 else item[:12] + "..."
            formatted_row.append(f"{j + 1:2}. {display_item:15}")
        result += " | ".join(formatted_row) + "\n"
    result += f"\nВсего элементов: {len(items)}"
    return result


# ========================= ИНТЕРФЕЙС /INTERFACE (tkinter) =========================

class ListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Создание пользовательского списка - с выбором формата вывода")
        self.root.geometry("750x650")

        # Создаём основной контейнер с прокруткой
        self.main_canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = tk.Frame(self.main_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )

        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Привязываем колёсико мыши для прокрутки
        self.main_canvas.bind("<MouseWheel>", self._on_mousewheel)

        # Переменные для хранения данных
        self.num_elements = None  # количество элементов
        self.input_fields = []  # поля для ввода элементов
        self.elements_list = []  # список введённых элементов

        # Переменная для хранения выбранного формата
        self.format_var = tk.StringVar(value="column")

        # Фрейм для ввода количества элементов
        self.frame_count = tk.Frame(self.scrollable_frame)
        self.frame_count.pack(pady=20, fill="x")

        tk.Label(self.frame_count, text="Введите размер списка (количество элементов):",
                 font=("Arial", 10, "bold")).pack()
        self.entry_count = tk.Entry(self.frame_count, width=10, font=("Arial", 10))
        self.entry_count.pack(pady=5)
        self.btn_create = tk.Button(self.frame_count, text="Создать поля для ввода",
                                    command=self.create_input_fields,
                                    bg="#4CAF50", fg="white",
                                    font=("Arial", 10))
        self.btn_create.pack(pady=5)

        # Фрейм для выбора формата вывода (изначально скрыт)
        self.frame_format = tk.Frame(self.scrollable_frame)

        tk.Label(self.frame_format, text="Выберите формат вывода списка:",
                 font=("Arial", 10, "bold")).pack(pady=5)

        # Создаём радиокнопки для выбора формата
        formats_frame = tk.Frame(self.frame_format)
        formats_frame.pack()

        tk.Radiobutton(formats_frame, text="📋 Столбик с номерами",
                       variable=self.format_var, value="column",
                       font=("Arial", 9)).pack(anchor="w", padx=20, pady=2)

        tk.Radiobutton(formats_frame, text="🐍 Python-список (['a', 'b', 'c'])",
                       variable=self.format_var, value="python",
                       font=("Arial", 9)).pack(anchor="w", padx=20, pady=2)

        tk.Radiobutton(formats_frame, text="➡️  Строка с разделителем (a → b → c)",
                       variable=self.format_var, value="horizontal",
                       font=("Arial", 9)).pack(anchor="w", padx=20, pady=2)

        tk.Radiobutton(formats_frame, text="📊 Таблица (по 5 элементов в строке)",
                       variable=self.format_var, value="table",
                       font=("Arial", 9)).pack(anchor="w", padx=20, pady=2)

        # Фрейм для динамических полей ввода элементов
        self.frame_elements = tk.Frame(self.scrollable_frame)
        self.frame_elements.pack(pady=10, fill="x")

        # Фрейм для кнопки завершения и результата
        self.frame_bottom = tk.Frame(self.scrollable_frame)
        self.frame_bottom.pack(pady=10, fill="x")

        # Кнопка для завершения ввода и показа результата
        self.btn_finish = tk.Button(self.frame_bottom, text="Показать итоговый список",
                                    command=self.show_final_list, state=tk.DISABLED,
                                    bg="#2196F3", fg="white",
                                    font=("Arial", 10, "bold"))
        self.btn_finish.pack(pady=10)

        # Текстовое поле для вывода результата с собственной прокруткой
        tk.Label(self.frame_bottom, text="Результат:", font=("Arial", 10, "bold")).pack()
        self.result_text = scrolledtext.ScrolledText(self.frame_bottom, height=12, width=80,
                                                     wrap=tk.WORD, state=tk.DISABLED,
                                                     font=("Courier", 10))
        self.result_text.pack(pady=5)

    def _on_mousewheel(self, event):
        """Обработка прокрутки колёсиком мыши"""
        self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_input_fields(self):
        """Создаёт поля для ввода элементов на основе введённого количества"""
        # Очищаем предыдущие поля, если они были
        for widget in self.frame_elements.winfo_children():
            widget.destroy()
        self.input_fields.clear()
        self.elements_list.clear()

        # Получаем количество элементов
        try:
            self.num_elements = int(self.entry_count.get())
            if self.num_elements <= 0:
                messagebox.showerror("Ошибка", "Количество элементов должно быть положительным числом")
                return
            if self.num_elements > 100:
                if not messagebox.askyesno("Предупреждение",
                                           f"Вы создаёте список из {self.num_elements} элементов.\nЭто может замедлить работу программы. Продолжить?"):
                    return
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите целое число")
            return

        # Показываем фрейм с выбором формата
        self.frame_format.pack(pady=10, fill="x", before=self.frame_elements)

        # Создаём контейнер с прокруткой для полей ввода
        elements_canvas = tk.Canvas(self.frame_elements, height=350)  # Увеличил высоту
        elements_scrollbar = tk.Scrollbar(self.frame_elements, orient="vertical", command=elements_canvas.yview)
        elements_inner_frame = tk.Frame(elements_canvas)

        elements_inner_frame.bind(
            "<Configure>",
            lambda e: elements_canvas.configure(scrollregion=elements_canvas.bbox("all"))
        )

        elements_canvas.create_window((0, 0), window=elements_inner_frame, anchor="nw")
        elements_canvas.configure(yscrollcommand=elements_scrollbar.set)

        # Привязываем колёсико к этому канвасу
        elements_canvas.bind("<MouseWheel>", lambda e: elements_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Заголовок
        tk.Label(elements_inner_frame, text="Введите элементы списка:",
                 font=("Arial", 10, "bold")).pack(pady=5)

        # Подсказка
        tk.Label(elements_inner_frame, text="(Можно вводить любые значения: текст, числа, true/false и т.д.)",
                 font=("Arial", 8), fg="gray").pack(pady=(0, 10))

        # Создаём метки и поля ввода для каждого элемента
        for i in range(self.num_elements):
            frame = tk.Frame(elements_inner_frame)
            frame.pack(pady=2, fill="x", padx=10)
            label = tk.Label(frame, text=f"Элемент №{i + 1}:", width=12, anchor="w")
            label.pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=50)
            entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
            self.input_fields.append(entry)

        # Размещаем канвас с прокруткой
        elements_canvas.pack(side="left", fill="both", expand=True)
        elements_scrollbar.pack(side="right", fill="y")

        # Активируем кнопку завершения
        self.btn_finish.config(state=tk.NORMAL)
        # Очищаем предыдущий результат
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

        # Прокручиваем вверх
        self.main_canvas.yview_moveto(0)

        # Обновляем размер окна
        self.root.update()

    def show_final_list(self):
        """Собирает введённые данные, применяет логику и показывает результат в выбранном формате"""
        # Собираем значения из полей ввода
        self.elements_list = []
        empty_fields = []

        for i, entry in enumerate(self.input_fields):
            value = entry.get().strip()
            if value == "":
                empty_fields.append(i + 1)

        if empty_fields:
            messagebox.showwarning("Внимание",
                                   f"Следующие поля пусты: {', '.join(map(str, empty_fields))}\nПожалуйста, заполните все поля!")
            return

        for entry in self.input_fields:
            value = entry.get().strip()
            self.elements_list.append(value)

        # Применяем вашу исходную логику создания списка
        final_list = create_user_list(self.num_elements, self.elements_list)

        # Выбираем формат вывода
        format_choice = self.format_var.get()

        if format_choice == "column":
            output_text = format_list_as_column(final_list)
        elif format_choice == "python":
            output_text = format_list_as_python(final_list)
        elif format_choice == "horizontal":
            output_text = format_list_as_horizontal(final_list)
        elif format_choice == "table":
            output_text = format_list_as_table(final_list)
        else:
            output_text = format_list_as_column(final_list)

        # Выводим результат в текстовое поле
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, output_text)
        self.result_text.config(state=tk.DISABLED)

        # Показываем сообщение об успехе
        messagebox.showinfo("Готово!",
                            f"Список успешно создан!\nВыбранный формат: {self.get_format_name(format_choice)}")

    def get_format_name(self, format_choice):
        """Возвращает название формата для сообщения"""
        formats = {
            "column": "Столбик с номерами",
            "python": "Python-список",
            "horizontal": "Строка с разделителем",
            "table": "Таблица"
        }
        return formats.get(format_choice, "Столбик с номерами")


# ========================= ЗАПУСК ПРИЛОЖЕНИЯ/LAUNCHING APP =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = ListApp(root)
    root.mainloop()