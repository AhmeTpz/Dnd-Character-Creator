import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os


# Ana ve alt sınıf bilgileri
class_data = {
    "Fighter": {
        "base_power": 16,
        "power_per_level": 2,
        "skills": ["Extra Attack", "Action Surge"],
        "subclasses": {
            "Battle Master": {"power": 10, "skill": "Precision Attack"},
            "Eldritch Knight": {"power": 8, "skill": "Mage Armour"},
            "Champion": {"power": 10, "skill": "Improved Critical Hit"},
            "Arcane Archer": {"power": 8, "skill": "Arcane Shoot"}
        }
    },
    "Ranger": {
        "base_power": 12,
        "power_per_level": 2,
        "skills": ["Survival", "Longstrider"],
        "subclasses": {
            "Beast Master": {"power": 8, "skill": "Animal Handling"},
            "Hunter": {"power": 10, "skill": "True Strike"},
            "Gloom Stalker": {"power": 10, "skill": "Dread Ambusher"},
            "Swarmkeeper": {"power": 8, "skill": "Legion of Bees"}
        }
    },
    "Sorcerer": {
        "base_power": 6,
        "power_per_level": 3,
        "skills": ["Sacred Flame", "Light", "Paison Spray"],
        "subclasses": {
            "Draconic Bloodline": {"power": 3, "skills": ["Dragon Ancestry", "Fly"]},
            "Wild Magic": {"power": 3, "skills": ["Controlled Kaos", "Bend Luck"]},
            "Storm Sorcery": {"power": 3, "skills": ["Heart of the Storm", "Gust of Wind"]},
            "Shadow Magic": {"power": 3, "skills": ["Superior Darkvision", "Shadow Walk"]}
        }
    }

}

root = tk.Tk()
root.title("Karakter Yaratıcı")
root.configure(bg="#2e2b2b")
root.geometry("1400x1350")

selected_main_class = tk.StringVar()
selected_level = tk.IntVar(value=1)
selected_subclass = tk.StringVar()

# Ana Sınıf Paneli
tk.Label(root, text="Ana Sınıf Seç:", font=("Georgia", 20, "bold"), fg="white", bg="#2e2b2b").pack(pady=20)
main_frame = tk.Frame(root, bg="#2e2b2b")
main_frame.pack(pady=5)

main_class_buttons = {}

color_map = {
    "Fighter": "#996600",
    "Ranger": "#336633",
    "Sorcerer": "#990000"
}

subclass_selected_colors = {
    "Battle Master": "#b22222",
    "Eldritch Knight": "#8a2be2",
    "Champion": "#ff6600",
    "Arcane Archer": "#3300cc",
    "Beast Master": "#228b22",
    "Hunter": "#66cccc",
    "Gloom Stalker": "#660099",
    "Swarmkeeper": "#cc9933",
    "Draconic Bloodline": "#cc6600",
    "Wild Magic": "#003300",
    "Storm Sorcery": "#9966ff",
    "Shadow Magic": "#660000"
}

def update_main_class_buttons():
    for cls, btn in main_class_buttons.items():
        if selected_main_class.get() == cls:
            btn.config(relief=tk.SUNKEN, bg=color_map[cls], fg="white")
        else:
            btn.config(relief=tk.RAISED, bg="gray20", fg="white")

def set_main_class(cls):
    selected_main_class.set(cls)
    selected_subclass.set("")  # Alt sınıfı sıfırlıyoruz
    update_main_class_buttons()
    update_subclasses()

for cls in class_data:
    frame = tk.Frame(main_frame, bg="#2e2b2b")
    frame.pack(side=tk.LEFT, padx=20)
    try:
        for ext in ["png", "webp"]:
            path = f"Classes/{cls}.{ext}"
            if os.path.exists(path):
                icon = Image.open(path).resize((140, 140))
                break
        icon = ImageTk.PhotoImage(icon)
        label = tk.Label(frame, image=icon, bg="#2e2b2b")
        label.image = icon
        label.pack()
    except:
        pass
    btn = tk.Button(frame, text=cls, width=10, height=1, command=lambda c=cls: set_main_class(c), relief=tk.RAISED, bg="gray20", fg="white", font=("Georgia", 10, "bold"))
    btn.pack(pady=3)
    main_class_buttons[cls] = btn

# Seviye Seçimi
level_frame = tk.Frame(root, bg="#2e2b2b")
level_frame.pack(pady=15)
tk.Label(level_frame, text="Seviye Seç (1-10):", font=("Georgia", 18), fg="white", bg="#2e2b2b").pack(side=tk.LEFT, padx=10)
level_menu = ttk.Combobox(level_frame, textvariable=selected_level, values=list(range(1, 11)), width=6, state="readonly", font=("Georgia", 16))
level_menu.pack(side=tk.LEFT)

# Alt Sınıflar
subclass_frame = tk.Frame(root, bg="#2e2b2b")
subclass_frame.pack(pady=20)
tk.Label(subclass_frame, text="Alt Sınıf Seç (Sadece Seviye 4+):", font=("Georgia", 18, "bold"), fg="white", bg="#2e2b2b").pack(pady=8)
subclass_buttons_frame = tk.Frame(subclass_frame, bg="#2e2b2b")
subclass_buttons_frame.pack(pady=10)

# Sonuç Paneli
result_frame = tk.Frame(root, bg="#2e2b2b")
result_frame.pack(pady=30)

level_icon_label = tk.Label(result_frame, bg="#2e2b2b")
level_icon_label.grid(row=0, column=0, padx=10, sticky="nw")
level_value_label = tk.Label(result_frame, font=("Georgia", 22), fg="white", bg="#2e2b2b")
level_value_label.grid(row=0, column=1, sticky="w")

total_power_icon = tk.Label(result_frame, bg="#2e2b2b")
total_power_icon.grid(row=1, column=0, padx=10, sticky="nw")
total_power_label = tk.Label(result_frame, font=("Georgia", 22), fg="white", bg="#2e2b2b")
total_power_label.grid(row=1, column=1, sticky="w")

abilities_icon = tk.Label(result_frame, bg="#2e2b2b")
abilities_icon.grid(row=2, column=0, padx=10, sticky="nw")
abilities_label = tk.Label(result_frame, justify=tk.LEFT, font=("Georgia", 22), fg="white", bg="#2e2b2b")
abilities_label.grid(row=2, column=1, sticky="w")

def update_subclasses():
    for widget in subclass_buttons_frame.winfo_children():
        widget.destroy()

    cls = selected_main_class.get()
    lvl = selected_level.get()
    if not cls or lvl < 4:
        return

    for sub in class_data[cls]["subclasses"]:
        frame = tk.Frame(subclass_buttons_frame, bg="#2e2b2b")
        frame.pack(side=tk.LEFT, padx=10)
        icon = None
        for ext in ["png", "webp"]:
            path = f"Subclasses/{sub}.{ext}"
            if os.path.exists(path):
                icon = Image.open(path).resize((80, 80))
                break
        if icon:
            icon = ImageTk.PhotoImage(icon)
            icon_label = tk.Label(frame, image=icon, bg="#2e2b2b")
            icon_label.image = icon
            icon_label.pack()

        def get_color():
            return subclass_selected_colors.get(sub, "#444444")

        rb = tk.Radiobutton(
            frame, text=sub, variable=selected_subclass, value=sub,
            bg="#2e2b2b", fg="white", font=("Georgia", 10, "bold"),
            indicatoron=0, width=16, height=1, relief=tk.RAISED,
            selectcolor=get_color()
        )
        rb.pack(pady=4)

def create_character():
    cls = selected_main_class.get()
    lvl = selected_level.get()
    sub = selected_subclass.get() if lvl >= 4 else None

    if not cls:
        messagebox.showerror("Hata", "Ana sınıf seçmelisiniz!")
        return

    base = class_data[cls]
    power = base["base_power"] + base["power_per_level"] * (lvl - 1)
    abilities = [("Ana", skill) for skill in base["skills"][:]]

    if sub:
        subdata = base["subclasses"][sub]
        power += subdata["power"]
        # Sorcerer için her bir yeteneği ayrı satıra ekliyoruz
        if cls == "Sorcerer":
            for skill in subdata["skills"]:
                abilities.append(("Alt", skill))  # Her yetenek farklı satırda olacak
        else:
            abilities.append(("Alt", subdata['skill']))

    # Base power'dan çıkarılan gücü hesapla
    additional_power = power - base["base_power"]

    try:
        icon = Image.open("level.png").resize((32, 32))
        icon = ImageTk.PhotoImage(icon)
        level_icon_label.config(image=icon)
        level_icon_label.image = icon
    except:
        level_icon_label.config(text="Seviye:")

    level_value_label.config(text=f"Seviye: {lvl}")

    try:
        icon = Image.open("power.png").resize((32, 32))
        icon = ImageTk.PhotoImage(icon)
        total_power_icon.config(image=icon)
        total_power_icon.image = icon
    except:
        total_power_icon.config(text="Güç:")

    # Toplam güç ve eklenen güç
    total_power_label.config(text=f"Toplam Güç: {power} (+{additional_power})")

    try:
        icon = Image.open("ability.png").resize((32, 32))
        icon = ImageTk.PhotoImage(icon)
        abilities_icon.config(image=icon)
        abilities_icon.image = icon
    except:
        abilities_icon.config(text="Yetenekler:")

    ability_text = ""
    for typ, skill in abilities:
        prefix = "• " if typ == "Ana" else "+ "
        ability_text += f"{prefix}{skill}\n"
    abilities_label.config(text=ability_text)



# Buton
button_frame = tk.Frame(root, bg="#2e2b2b")
button_frame.pack(pady=20)
tk.Button(button_frame, text="Karakteri Oluştur", command=create_character, font=("Georgia", 18, "bold"), bg="#daa520", fg="black", height=2, width=30).pack()

selected_level.trace("w", lambda *args: update_subclasses())
root.mainloop()