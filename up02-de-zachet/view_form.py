"""Форма просмотра товара."""
import tkinter as tk
from tkinter import messagebox
from styles import COLOR_MAIN_BG, COLOR_ACCENT, font, FONT_SIZE_NORMAL
from resources import get_product_image
from database import get_product_quantity
from order_manager import create_order
from error_handler import validate_positive_int
import os

RESOURCES_DIR = "resources"

class ViewForm:
    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order
        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product[1]}")
        self.window.geometry("700x650")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()

    def build_ui(self):
        image_name = self.product[7]
        image_path = os.path.join(RESOURCES_DIR, image_name) if image_name else None
        photo = get_product_image(image_path, size=(200, 200))
        if photo:
            img = tk.Label(self.window, image=photo, bg=COLOR_MAIN_BG)
            img.image = photo
            img.pack(pady=10)
        else:
            tk.Label(self.window, text="[НЕТ ФОТО]", bg=COLOR_MAIN_BG, width=20, height=8).pack(pady=10)

        body = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        body.pack(fill="x", padx=20)
        self._add_field(body, "Название", self.product[1])
        self._add_field(body, "Категория", self.product[2])
        self._add_field(body, "Производитель", self.product[3])
        self._add_field(body, "Характеристики", self.product[4])
        self._add_field(body, "Цена", f"{self.product[5]} руб.")
        self._add_field(body, "Количество", self.product[6])
        self._add_field(body, "Модель", self.product[8])

        qty_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(qty_frame, text="Количество:", bg=COLOR_MAIN_BG, font=font(FONT_SIZE_NORMAL, bold=True)).pack(side="left")
        self.qty_var = tk.StringVar(value="1")
        tk.Entry(qty_frame, textvariable=self.qty_var, width=8, font=font(FONT_SIZE_NORMAL)).pack(side="left", padx=10)

        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", padx=20, pady=15)
        tk.Button(btn_frame, text="Добавить в заказ", command=self.add_to_order, bg=COLOR_ACCENT, fg="white", font=font(FONT_SIZE_NORMAL)).pack(side="left")
        tk.Button(btn_frame, text="Назад", command=self.window.destroy, bg=COLOR_ACCENT, fg="white", font=font(FONT_SIZE_NORMAL)).pack(side="right")

    def _add_field(self, parent, label, value):
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=f"{label}:", font=font(FONT_SIZE_NORMAL, bold=True), width=15, anchor="w", bg=COLOR_MAIN_BG).pack(side="left")
        tk.Label(row, text=str(value) if value else "—", font=font(FONT_SIZE_NORMAL), anchor="w", bg=COLOR_MAIN_BG).pack(side="left")

    def add_to_order(self):
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return
        ok, result = validate_positive_int(self.qty_var.get(), "Количество")
        if not ok:
            messagebox.showwarning("Ошибка ввода", result)
            return
        qty = result
        current_qty = get_product_quantity(self.product[0])
        if qty > current_qty:
            messagebox.showwarning("Ошибка", f"Доступно только {current_qty} шт.")
            return
        try:
            items = [(self.product[0], self.product[8], qty, self.product[5])]
            order_id = create_order("Клиент", items)
            if order_id:
                messagebox.showinfo("Успех", f"Заказ №{order_id} оформлен")
                if self.on_add_to_order:
                    self.on_add_to_order()
                self.window.destroy()
            else:
                messagebox.showerror("Ошибка", "Не удалось создать заказ")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка заказа:\n{e}")
