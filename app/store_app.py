"""
Departmental Store Billing System
A simple Tkinter application to display menu, take orders, and generate bills.
"""
 
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
 
# ─────────────────────────────────────────────
#  PRODUCT CATALOG
# ─────────────────────────────────────────────
PRODUCTS = {
    "Groceries": {
        "Rice (1 kg)":       45.00,
        "Wheat Flour (1 kg)": 40.00,
        "Sugar (1 kg)":      42.00,
        "Salt (500 g)":      18.00,
        "Cooking Oil (1 L)": 130.00,
    },
    "Beverages": {
        "Tea (250 g)":       90.00,
        "Coffee (100 g)":    110.00,
        "Cold Drink (500 ml)": 40.00,
        "Juice (1 L)":        80.00,
        "Mineral Water":      20.00,
    },
    "Snacks": {
        "Biscuits":          25.00,
        "Chips":             20.00,
        "Namkeen (200 g)":   35.00,
        "Chocolate":         50.00,
        "Cookies (100 g)":   45.00,
    },
    "Dairy": {
        "Milk (1 L)":        58.00,
        "Butter (100 g)":    55.00,
        "Cheese (200 g)":    90.00,
        "Curd (500 g)":      40.00,
        "Paneer (200 g)":    80.00,
    },
    "Personal Care": {
        "Shampoo (200 ml)":  120.00,
        "Soap (100 g)":       30.00,
        "Toothpaste":         60.00,
        "Face Wash":          90.00,
        "Lotion (100 ml)":    85.00,
    },
}
 
TAX_RATE = 0.05  # 5% GST
 
 
# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────
class DepartmentalStoreApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🛒  Smart Departmental Store")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(True, True)
 
        # State
        self.cart: dict[str, dict] = {}   # item_name -> {price, qty}
        self.customer_name = tk.StringVar(value="")
        self.customer_phone = tk.StringVar(value="")
 
        self._build_ui()
 
    # ──────────────────── UI BUILD ────────────────────
    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", pady=12)
        header.pack(fill="x")
        tk.Label(
            header,
            text="🛒  Smart Departmental Store",
            font=("Helvetica", 22, "bold"),
            fg="white", bg="#2c3e50"
        ).pack(side="left", padx=20)
        tk.Label(
            header,
            text="Your One-Stop Shop",
            font=("Helvetica", 11),
            fg="#bdc3c7", bg="#2c3e50"
        ).pack(side="left", padx=5, pady=8)
 
        # Body
        body = tk.Frame(self.root, bg="#f0f4f8")
        body.pack(fill="both", expand=True, padx=15, pady=10)
 
        # Left panel — menu
        left = tk.Frame(body, bg="#f0f4f8")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self._build_menu_panel(left)
 
        # Right panel — cart + customer
        right = tk.Frame(body, bg="#f0f4f8", width=360)
        right.pack(side="right", fill="both")
        right.pack_propagate(False)
        self._build_cart_panel(right)
 
    def _build_menu_panel(self, parent):
        tk.Label(
            parent, text="📦  Product Menu",
            font=("Helvetica", 14, "bold"),
            bg="#f0f4f8", fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 6))
 
        # Category tabs
        nb = ttk.Notebook(parent)
        nb.pack(fill="both", expand=True)
 
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"), padding=[10, 5])
 
        for category, items in PRODUCTS.items():
            frame = tk.Frame(nb, bg="white")
            nb.add(frame, text=f"  {category}  ")
            self._build_category_tab(frame, items)
 
    def _build_category_tab(self, parent, items: dict):
        # Header row
        hdr = tk.Frame(parent, bg="#2c3e50")
        hdr.pack(fill="x")
        for text, width in [("Product", 28), ("Price (₹)", 12), ("Qty", 6), ("Action", 10)]:
            tk.Label(
                hdr, text=text, font=("Helvetica", 10, "bold"),
                fg="white", bg="#2c3e50", width=width, anchor="w", pady=6
            ).pack(side="left", padx=4)
 
        canvas = tk.Canvas(parent, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")
 
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
 
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
 
        for i, (item, price) in enumerate(items.items()):
            bg = "#f8f9fa" if i % 2 == 0 else "white"
            row = tk.Frame(scroll_frame, bg=bg, pady=4)
            row.pack(fill="x")
 
            tk.Label(row, text=item, font=("Helvetica", 10),
                     bg=bg, width=28, anchor="w").pack(side="left", padx=6)
            tk.Label(row, text=f"₹{price:.2f}", font=("Helvetica", 10),
                     bg=bg, width=12, anchor="w", fg="#27ae60").pack(side="left", padx=4)
 
            qty_var = tk.IntVar(value=1)
            qty_spin = ttk.Spinbox(row, from_=1, to=100, width=5,
                                   textvariable=qty_var, font=("Helvetica", 10))
            qty_spin.pack(side="left", padx=6)
 
            tk.Button(
                row, text="Add +", font=("Helvetica", 9, "bold"),
                bg="#27ae60", fg="white", relief="flat",
                cursor="hand2", padx=8,
                command=lambda n=item, p=price, q=qty_var: self._add_to_cart(n, p, q)
            ).pack(side="left", padx=4)
 
    def _build_cart_panel(self, parent):
        # Customer info
        info_frame = tk.LabelFrame(
            parent, text="  👤  Customer Info  ",
            font=("Helvetica", 11, "bold"),
            bg="#f0f4f8", fg="#2c3e50", padx=10, pady=8
        )
        info_frame.pack(fill="x", pady=(0, 8))
 
        for label, var in [("Name:", self.customer_name), ("Phone:", self.customer_phone)]:
            row = tk.Frame(info_frame, bg="#f0f4f8")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, font=("Helvetica", 10),
                     bg="#f0f4f8", width=7, anchor="w").pack(side="left")
            tk.Entry(row, textvariable=var, font=("Helvetica", 10),
                     relief="solid", bd=1).pack(side="left", fill="x", expand=True)
 
        # Cart
        cart_frame = tk.LabelFrame(
            parent, text="  🛒  Cart  ",
            font=("Helvetica", 11, "bold"),
            bg="#f0f4f8", fg="#2c3e50"
        )
        cart_frame.pack(fill="both", expand=True, pady=(0, 8))
 
        cols = ("Item", "Qty", "Price")
        self.cart_tree = ttk.Treeview(cart_frame, columns=cols,
                                       show="headings", height=12)
        self.cart_tree.heading("Item", text="Item")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Price", text="Price (₹)")
        self.cart_tree.column("Item", width=160)
        self.cart_tree.column("Qty", width=40, anchor="center")
        self.cart_tree.column("Price", width=80, anchor="e")
 
        vsb = ttk.Scrollbar(cart_frame, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=vsb.set)
        self.cart_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
 
        # Remove selected
        tk.Button(
            parent, text="🗑  Remove Selected",
            font=("Helvetica", 9), bg="#e74c3c", fg="white",
            relief="flat", cursor="hand2", pady=4,
            command=self._remove_from_cart
        ).pack(fill="x", pady=(0, 6))
 
        # Summary
        summary = tk.Frame(parent, bg="#2c3e50", padx=12, pady=10)
        summary.pack(fill="x", pady=(0, 8))
 
        self.lbl_subtotal = tk.Label(summary, text="Subtotal:  ₹0.00",
                                      font=("Helvetica", 10), fg="#ecf0f1", bg="#2c3e50")
        self.lbl_subtotal.pack(anchor="w")
        self.lbl_tax = tk.Label(summary, text=f"GST ({int(TAX_RATE*100)}%):  ₹0.00",
                                 font=("Helvetica", 10), fg="#ecf0f1", bg="#2c3e50")
        self.lbl_tax.pack(anchor="w")
        tk.Frame(summary, bg="#7f8c8d", height=1).pack(fill="x", pady=4)
        self.lbl_total = tk.Label(summary, text="TOTAL:  ₹0.00",
                                   font=("Helvetica", 13, "bold"), fg="#f1c40f", bg="#2c3e50")
        self.lbl_total.pack(anchor="w")
 
        # Buttons
        btn_frame = tk.Frame(parent, bg="#f0f4f8")
        btn_frame.pack(fill="x")
 
        tk.Button(
            btn_frame, text="🧾  Generate Bill",
            font=("Helvetica", 11, "bold"),
            bg="#2980b9", fg="white", relief="flat",
            cursor="hand2", pady=8,
            command=self._generate_bill
        ).pack(fill="x", pady=(0, 4))
 
        tk.Button(
            btn_frame, text="🔄  Clear All",
            font=("Helvetica", 10),
            bg="#95a5a6", fg="white", relief="flat",
            cursor="hand2", pady=6,
            command=self._clear_all
        ).pack(fill="x")
 
    # ──────────────────── LOGIC ────────────────────
    def _add_to_cart(self, name: str, price: float, qty_var: tk.IntVar):
        qty = qty_var.get()
        if qty < 1:
            messagebox.showwarning("Invalid Qty", "Quantity must be at least 1.")
            return
        if name in self.cart:
            self.cart[name]["qty"] += qty
        else:
            self.cart[name] = {"price": price, "qty": qty}
        self._refresh_cart()
 
    def _remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showinfo("Remove", "Please select an item to remove.")
            return
        for sel in selected:
            item_name = self.cart_tree.item(sel)["values"][0]
            self.cart.pop(item_name, None)
        self._refresh_cart()
 
    def _refresh_cart(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
        subtotal = 0.0
        for name, data in self.cart.items():
            line = data["price"] * data["qty"]
            subtotal += line
            self.cart_tree.insert("", "end", values=(name, data["qty"], f"{line:.2f}"))
        tax = subtotal * TAX_RATE
        total = subtotal + tax
        self.lbl_subtotal.config(text=f"Subtotal:  ₹{subtotal:.2f}")
        self.lbl_tax.config(text=f"GST ({int(TAX_RATE*100)}%):  ₹{tax:.2f}")
        self.lbl_total.config(text=f"TOTAL:  ₹{total:.2f}")
 
    def _clear_all(self):
        if self.cart and messagebox.askyesno("Clear Cart", "Remove all items from cart?"):
            self.cart.clear()
            self.customer_name.set("")
            self.customer_phone.set("")
            self._refresh_cart()
 
    def _generate_bill(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add items to the cart first.")
            return
 
        subtotal = sum(d["price"] * d["qty"] for d in self.cart.values())
        tax = subtotal * TAX_RATE
        total = subtotal + tax
        now = datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
        cust = self.customer_name.get().strip() or "Walk-in Customer"
        phone = self.customer_phone.get().strip() or "N/A"
 
        # Build bill text
        w = 46
        lines = [
            "=" * w,
            "       SMART DEPARTMENTAL STORE",
            "        Jaipur, Rajasthan, India",
            "=" * w,
            f"  Date  : {now}",
            f"  Name  : {cust}",
            f"  Phone : {phone}",
            "-" * w,
            f"  {'ITEM':<22} {'QTY':>4}  {'AMOUNT':>10}",
            "-" * w,
        ]
        for name, data in self.cart.items():
            amt = data["price"] * data["qty"]
            lines.append(f"  {name:<22} {data['qty']:>4}  ₹{amt:>9.2f}")
        lines += [
            "-" * w,
            f"  {'Subtotal':<28}  ₹{subtotal:>9.2f}",
            f"  {'GST (5%)':<28}  ₹{tax:>9.2f}",
            "=" * w,
            f"  {'TOTAL AMOUNT':<28}  ₹{total:>9.2f}",
            "=" * w,
            "     Thank you for shopping with us!",
            "        Please visit again  🙏",
            "=" * w,
        ]
        bill_text = "\n".join(lines)
 
        # Show bill in a popup
        win = tk.Toplevel(self.root)
        win.title("Bill Receipt")
        win.geometry("500x560")
        win.configure(bg="#f0f4f8")
        win.grab_set()
 
        tk.Label(win, text="🧾  Bill Receipt",
                 font=("Helvetica", 14, "bold"),
                 bg="#2c3e50", fg="white"
                 ).pack(fill="x", pady=0)
 
        txt = tk.Text(win, font=("Courier", 10), bg="white",
                      relief="flat", padx=10, pady=10)
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.insert("end", bill_text)
        txt.config(state="disabled")
 
        btn_row = tk.Frame(win, bg="#f0f4f8")
        btn_row.pack(fill="x", padx=10, pady=(0, 10))
 
        tk.Button(
            btn_row, text="💾  Save Bill",
            font=("Helvetica", 10, "bold"),
            bg="#27ae60", fg="white", relief="flat",
            cursor="hand2", padx=12, pady=6,
            command=lambda: self._save_bill(bill_text, win)
        ).pack(side="left", padx=4)
 
        tk.Button(
            btn_row, text="✅  New Order",
            font=("Helvetica", 10, "bold"),
            bg="#2980b9", fg="white", relief="flat",
            cursor="hand2", padx=12, pady=6,
            command=lambda: [win.destroy(), self._clear_all_silent()]
        ).pack(side="left", padx=4)
 
        tk.Button(
            btn_row, text="✖  Close",
            font=("Helvetica", 10),
            bg="#e74c3c", fg="white", relief="flat",
            cursor="hand2", padx=12, pady=6,
            command=win.destroy
        ).pack(side="right", padx=4)
 
    def _save_bill(self, text: str, win: tk.Toplevel):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bill_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        messagebox.showinfo("Saved", f"Bill saved as:\n{filename}", parent=win)
 
    def _clear_all_silent(self):
        self.cart.clear()
        self.customer_name.set("")
        self.customer_phone.set("")
        self._refresh_cart()
 
 
# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = DepartmentalStoreApp(root)
    root.mainloop()