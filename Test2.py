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
        },
        "armors": {
            "Light Armor": 6,
            "Medium Armor": 10,
            "Heavy Armor": 16
        },
        "weapons": {
            "Axe": 8,
            "Sword": 6,
            "Spear": 8,
            "Dagger": 4,
            "Bow": 8
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
        },
        "armors": {
            "Light Armor": 6,
            "Medium Armor": 10
        },
        "weapons": {
            "Sword": 6,
            "Dagger": 4,
            "Bow": 8
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
        },
        "armors": {
            "Light Armor": 6
        },
        "weapons": {
            "Staff": 6,
            "Dagger": 4
        }
    }
}

root = tk.Tk()
root.title("Karakter Yaratıcı")
root.configure(bg="#2e2b2b")
root.geometry("1400x1400")

selected_main_class = tk.StringVar()
selected_level = tk.IntVar(value=1)
selected_subclass = tk.StringVar()
selected_armor = tk.StringVar()
selected_weapon = tk.StringVar()

# Ana Sınıf Paneli
tk.Label(root, text="Ana Sınıf Seç:", font=("Georgia", 16, "bold"), fg="white", bg="#2e2b2b").pack(pady=15)
main_frame = tk.Frame(root, bg="#2e2b2b")
main_frame.pack(pady=5)

main_class_buttons = {}

color_map = {
    "Fighter": "#996600",
    "Ranger": "#336633",
    "Sorcerer": "#990000"
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
    selected_armor.set("")  # Zırhı sıfırlıyoruz
    selected_weapon.set("")  # Silahı sıfırlıyoruz
    update_main_class_buttons()
    update_subclasses()
    update_armor_weapons()


for cls in class_data:
    frame = tk.Frame(main_frame, bg="#2e2b2b")
    frame.pack(side=tk.LEFT, padx=15)
    try:
        for ext in ["png", "webp"]:
            path = f"Classes/{cls}.{ext}"
            if os.path.exists(path):
                icon = Image.open(path).resize((120, 120))
                break
        icon = ImageTk.PhotoImage(icon)
        label = tk.Label(frame, image=icon, bg="#2e2b2b")
        label.image = icon
        label.pack()
    except:
        pass
    btn = tk.Button(frame, text=cls, width=10, height=1, command=lambda c=cls: set_main_class(c), relief=tk.RAISED,
                    bg="gray20", fg="white", font=("Georgia", 10, "bold"))
    btn.pack(pady=3)
    main_class_buttons[cls] = btn

# Seviye Seçimi
level_frame = tk.Frame(root, bg="#2e2b2b")
level_frame.pack(pady=10)
tk.Label(level_frame, text="Seviye Seç (1-10):", font=("Georgia", 14), fg="white", bg="#2e2b2b").pack(side=tk.LEFT,
                                                                                                      padx=10)
level_menu = ttk.Combobox(level_frame, textvariable=selected_level, values=list(range(1, 11)), width=6,
                          state="readonly", font=("Georgia", 14))
level_menu.pack(side=tk.LEFT)

# Alt Sınıflar
subclass_frame = tk.Frame(root, bg="#2e2b2b")
subclass_frame.pack(pady=15)
tk.Label(subclass_frame, text="Alt Sınıf Seç (Sadece Seviye 4+):", font=("Georgia", 14, "bold"), fg="white",
         bg="#2e2b2b").pack(pady=8)
subclass_buttons_frame = tk.Frame(subclass_frame, bg="#2e2b2b")
subclass_buttons_frame.pack(pady=10)

# Zırh ve Silah Seçimi
armor_weapon_frame = tk.Frame(root, bg="#2e2b2b")
armor_weapon_frame.pack(pady=20)

# Zırh Seçimi
tk.Label(armor_weapon_frame, text="Zırh Seç:", font=("Georgia", 14), fg="white", bg="#2e2b2b").pack(side=tk.LEFT,
                                                                                                    padx=10)
armor_menu = ttk.Combobox(armor_weapon_frame, textvariable=selected_armor, width=20, state="readonly",
                          font=("Georgia", 14))
armor_menu.pack(side=tk.LEFT, padx=10)

# Silah Seçimi
tk.Label(armor_weapon_frame, text="Silah Seç:", font=("Georgia", 14), fg="white", bg="#2e2b2b").pack(side=tk.LEFT,
                                                                                                     padx=10)
weapon_menu = ttk.Combobox(armor_weapon_frame, textvariable=selected_weapon, width=20, state="readonly",
                           font=("Georgia", 14))
weapon_menu.pack(side=tk.LEFT, padx=10)

# Sonuç Paneli
result_frame = tk.Frame(root, bg="#2e2b2b")
result_frame.pack(pady=30)

level_icon_label = tk.Label(result_frame, bg="#2e2b2b")
level_icon_label.grid(row=0, column=0, padx=10, sticky="nw")
level_value_label = tk.Label(result_frame, font=("Georgia", 18), fg="white", bg="#2e2b2b")
level_value_label.grid(row=0, column=1, sticky="w")

total_power_icon = tk.Label(result_frame, bg="#2e2b2b")
total_power_icon.grid(row=1, column=0, padx=10, sticky="nw")
total_power_label = tk.Label(result_frame, font=("Georgia", 18), fg="white", bg="#2e2b2b")
total_power_label.grid(row=1, column=1, sticky="w")

abilities_icon = tk.Label(result_frame, bg="#2e2b2b")
abilities_icon.grid(row=4, column=0, padx=10, sticky="nw")
abilities_label = tk.Label(result_frame, justify=tk.LEFT, font=("Georgia", 18), fg="white", bg="#2e2b2b")
abilities_label.grid(row=4, column=1, sticky="w")

# Alt Sınıf Renklerini Ayarlama
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


# Alt Sınıf Seçimi Fonksiyonu Güncelleme
# Alt Sınıf Seçimi İçin Fonksiyon Güncelleme
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

        # Alt sınıfın simgesini ekleyelim
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

        # Her alt sınıf için bir Radiobutton ekliyoruz
        rb = tk.Radiobutton(
            frame, text=sub, variable=selected_subclass, value=sub,
            bg="gray20", fg="white", font=("Georgia", 10, "bold"),
            indicatoron=0, width=16, height=1, relief=tk.RAISED,
            selectcolor=subclass_selected_colors.get(sub, "#444444"),
            command=lambda sub=sub: change_subclass_color(sub)  # Tıklandığında rengi değiştir
        )
        rb.pack(pady=4)

# Alt Sınıf Tıklandığında Rengi Değiştirme
def change_subclass_color(sub):
    # Önce tüm alt sınıfların renklerini gri yapıyoruz
    for widget in subclass_buttons_frame.winfo_children():
        widget.config(bg="gray20")

    # Seçilen alt sınıfın rengini ayarlıyoruz
    for widget in subclass_buttons_frame.winfo_children():
        if widget.cget("text") == sub:
            widget.config(bg=subclass_selected_colors.get(sub, "#444444"))



# Zırh ve Silah Seçiminde Boş Seçenek Ekleme
def update_armor_weapons():
    cls = selected_main_class.get()

    if not cls:
        return

    armors = class_data[cls]["armors"]
    weapons = class_data[cls]["weapons"]

    # Boş bir seçenek ekleyelim ("-")
    armor_menu['values'] = ["-"] + list(armors.keys())
    weapon_menu['values'] = ["-"] + list(weapons.keys())

    # Varsayılan olarak boş seçeneği seçili hale getirelim
    selected_armor.set("-")
    selected_weapon.set("-")



# Herhangi bir alt sınıf seçildiğinde, bu alt sınıfa ait renk değişimlerini güncelleyen fonksiyonu çağırmamız gerek:
selected_subclass.trace("w", lambda *args: update_subclasses())


def create_character():
    cls = selected_main_class.get()
    lvl = selected_level.get()
    sub = selected_subclass.get() if lvl >= 4 else None
    armor = selected_armor.get()
    weapon = selected_weapon.get()

    if not cls:
        messagebox.showerror("Hata", "Ana sınıf seçmelisiniz!")
        return

    base = class_data[cls]
    power = base["base_power"] + base["power_per_level"] * (lvl - 1)
    abilities = [("Ana", skill) for skill in base["skills"][:]]

    if sub:
        subdata = base["subclasses"][sub]
        power += subdata["power"]
        if cls == "Sorcerer":
            for skill in subdata["skills"]:
                abilities.append(("Alt", skill))
        else:
            abilities.append(("Alt", subdata['skill']))

    additional_power = power - base["base_power"]

    # Zırh ve Silah etkilerini ekleyelim
    armor_power = base["armors"].get(armor, 0)
    weapon_power = base["weapons"].get(weapon, 0)
    power += armor_power + weapon_power

    # Görselleri ekle
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

    # Silah ve Zırhı ekleyelim
    try:
        icon = Image.open("Sword.png").resize((32, 32))
        icon = ImageTk.PhotoImage(icon)
        weapon_icon_label.config(image=icon)
        weapon_icon_label.image = icon
    except:
        weapon_icon_label.config(text="Silah:")

    weapon_label.config(text=f"Silah: {weapon} (+{weapon_power})")

    try:
        icon = Image.open("Defense.png").resize((32, 32))
        icon = ImageTk.PhotoImage(icon)
        armor_icon_label.config(image=icon)
        armor_icon_label.image = icon
    except:
        armor_icon_label.config(text="Zırh:")

    armor_label.config(text=f"Zırh: {armor} (+{armor_power})")

# Sonuç Paneli
weapon_icon_label = tk.Label(result_frame, bg="#2e2b2b")
weapon_icon_label.grid(row=3, column=0, padx=10, sticky="nw")
weapon_label = tk.Label(result_frame, font=("Georgia", 18), fg="white", bg="#2e2b2b")
weapon_label.grid(row=3, column=1, sticky="w")

armor_icon_label = tk.Label(result_frame, bg="#2e2b2b")
armor_icon_label.grid(row=2, column=0, padx=10, sticky="nw")
armor_label = tk.Label(result_frame, font=("Georgia", 18), fg="white", bg="#2e2b2b")
armor_label.grid(row=2, column=1, sticky="w")



# Buton
button_frame = tk.Frame(root, bg="#2e2b2b")
button_frame.pack(pady=20)
tk.Button(button_frame, text="Karakteri Oluştur", command=create_character, font=("Georgia", 16, "bold"), bg="#daa520",
          fg="black", height=2, width=30).pack()


selected_level.trace("w", lambda *args: update_subclasses())
root.mainloop()
