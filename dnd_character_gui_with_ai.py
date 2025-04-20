import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import threading
from PIL import Image, ImageTk
from dnd_character_decorator import *
from dnd_character_ai import create_prompt, generate_image, show_image_window


class CharacterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧙‍♂️ D&D Karakter Oluşturucu")
        self.root.configure(bg="#1e1e1e")
        self.root.geometry("1200x900")
        self.character = None
        self.images = {}

        self.create_widgets()

    def load_image(self, name, size=(100, 100), folders=None):
        if folders is None:
            folders = ["Classes", "Subclasses"]

        cache_key = f"{name}_{size[0]}x{size[1]}"
        if cache_key in self.images:
            return self.images[cache_key]

        for folder in folders:
            for ext in [".png", ".webp"]:
                path = os.path.join(folder, f"{name}{ext}")
                if os.path.exists(path):
                    image = Image.open(path).resize(size, Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(image)
                    self.images[cache_key] = image
                    return image
        return None

    def create_button(self, parent, text, img_name, cmd, folders=None, img_size=(100, 100)):
        image = self.load_image(img_name, img_size, folders)
        btn = tk.Button(parent, text=text, image=image, compound="top",
                        command=lambda: cmd(text), bg="#2d2d2d", fg="white",
                        font=("Arial", 10), bd=0)
        btn.image = image
        btn.pack(side="left", padx=10, pady=10, expand=True)
        return btn

    def create_equipment_button(self, parent, text, img_name, cmd, folders=None, img_size=(32, 32)):
        frame = tk.Frame(parent, bg="#2d2d2d")

        image = self.load_image(img_name, img_size, folders)

        if image:
            img_label = tk.Label(frame, image=image, bg="#2d2d2d")
            img_label.image = image
            img_label.pack(side="left", padx=5)

        btn = tk.Button(frame, text=text,
                        command=lambda: cmd(text), bg="#2d2d2d", fg="white",
                        font=("Arial", 10), bd=0, width=10)
        btn.pack(side="right", padx=5, fill="both", expand=True)

        frame.pack(side="left", padx=10, pady=10, expand=True)
        return frame

    def create_widgets(self):
        main = tk.Frame(self.root, bg="#1e1e1e")
        main.pack(expand=True, fill="both", padx=20, pady=20)

        self.output = tk.Text(main, height=10, width=110, bg="#111", fg="lightgreen")
        self.output.pack(side="bottom", pady=10)

        btn_frame = tk.Frame(main, bg="#1e1e1e")
        btn_frame.pack(side="bottom")
        tk.Button(btn_frame, text="Karakteri Göster", command=self.show_character,
                  bg="#4CAF50", fg="white", width=20).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Sıfırla", command=self.reset,
                  bg="#F44336", fg="white", width=20).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🎨 Görsel Oluştur", command=self.create_and_show_image,
                  bg="#FFD700", fg="black", width=20).pack(side="left", padx=10)

        class_frame = tk.LabelFrame(main, text="Ana Sınıf Seç", bg="#1e1e1e", fg="white")
        class_frame.pack(fill="x", pady=10)
        class_inner = tk.Frame(class_frame, bg="#1e1e1e")
        class_inner.pack(anchor="center")
        for cls in ["Fighter", "Ranger", "Sorcerer"]:
            self.create_button(class_inner, cls, cls, self.select_class)

        tk.Button(main, text="Seviye Ekle", command=self.level_up,
                  bg="#2196F3", fg="white", width=20).pack(pady=5)

        self.subclass_frame = tk.LabelFrame(main, text="Alt Sınıf Seç", bg="#1e1e1e", fg="white")
        self.subclass_frame.pack(fill="x", pady=10)

        weapon_frame = tk.LabelFrame(main, text="Silah Seç", bg="#1e1e1e", fg="white")
        weapon_frame.pack(fill="x", pady=10)
        weapon_inner = tk.Frame(weapon_frame, bg="#1e1e1e")
        weapon_inner.pack(anchor="center")
        for weapon in ["Sword", "Bow", "Dagger", "Axe", "Staff"]:
            self.create_equipment_button(weapon_inner, weapon, weapon, self.add_weapon,
                                         folders=["equipments"], img_size=(50, 50))

        armor_frame = tk.LabelFrame(main, text="Zırh Seç", bg="#1e1e1e", fg="white")
        armor_frame.pack(fill="x", pady=10)
        armor_inner = tk.Frame(armor_frame, bg="#1e1e1e")
        armor_inner.pack(anchor="center")
        for armor in ["Hat", "Helmet", "Chain Armor", "Knight Armor", "Leather Boots", "Plate Boots"]:
            self.create_equipment_button(armor_inner, armor, armor, self.add_armor,
                                         folders=["equipments"], img_size=(50, 50))

    def select_class(self, cls):
        self.character = {"Fighter": Fighter(), "Ranger": Ranger(), "Sorcerer": Sorcerer()}[cls]
        self.level_bonus = {"Fighter": 2, "Ranger": 2, "Sorcerer": 3}[cls]
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"{cls} seçildi.\n")

        for widget in self.subclass_frame.winfo_children():
            widget.destroy()
        subclasses = {
            "Fighter": ["Battle Master", "Eldritch Knight", "Champion", "Arcane Archer"],
            "Ranger": ["Beast Master", "Hunter", "Gloom Stalker", "Swarmkeeper"],
            "Sorcerer": ["Draconic Bloodline", "Wild Magic", "Storm Sorcery", "Shadow Magic"]
        }[cls]
        sub_inner = tk.Frame(self.subclass_frame, bg="#1e1e1e")
        sub_inner.pack(anchor="center")
        for sub in subclasses:
            self.create_button(sub_inner, sub, sub, self.add_subclass)

    def level_up(self):
        if self.character:
            self.character = LevelUp(self.character, self.level_bonus)
            self.output.insert(tk.END, "Seviye eklendi.\n")

    def add_subclass(self, name):
        if self.character:
            self.character = {
                "Battle Master": BattleMaster,
                "Eldritch Knight": EldritchKnight,
                "Champion": Champion,
                "Arcane Archer": ArcaneArcher,
                "Beast Master": BeastMaster,
                "Hunter": Hunter,
                "Gloom Stalker": GloomStalker,
                "Swarmkeeper": Swarmkeeper,
                "Draconic Bloodline": DraconicBloodline,
                "Wild Magic": WildMagic,
                "Storm Sorcery": StormSorcery,
                "Shadow Magic": ShadowMagic
            }[name](self.character)
            self.output.insert(tk.END, f"{name} eklendi.\n")

    def add_weapon(self, name):
        if self.character:
            self.character = {
                "Sword": Sword,
                "Bow": Bow,
                "Dagger": Dagger,
                "Axe": Axe,
                "Staff": Staff
            }[name](self.character)
            self.output.insert(tk.END, f"{name} eklendi.\n")

    def add_armor(self, name):
        if self.character:
            self.character = {
                "Hat": Hat,
                "Helmet": Helmet,
                "Chain Armor": ChainArmor,
                "Knight Armor": KnightArmor,
                "Leather Boots": LeatherBoots,
                "Plate Boots": PlateBoots
            }[name](self.character)
            self.output.insert(tk.END, f"{name} eklendi.\n")

    def show_character(self):
        if self.character:
            description = f"‍💝Karakter: {self.character.get_description()}\n"
            level = f"📊  Seviye: {self.character.get_level()}\n"
            power = f"⚔️  Güç: {self.character.get_power()}\n"
            armor = f"🛡️Zırh: {self.character.get_armor()}\n"
            skills = f"✨  Yetenekler: {', '.join(self.character.get_skills())}\n"
            equipment = f"🎒  Ekipmanlar: {', '.join(self.character.get_equipment()) if self.character.get_equipment() else 'Yok'}\n"

            self.output.insert(tk.END, description + level + power + armor + skills + equipment)

    def reset(self):
        self.character = None
        self.output.delete("1.0", tk.END)
        for widget in self.subclass_frame.winfo_children():
            widget.destroy()

    def on_image_progress(self, message):
        """Update the UI with image generation progress"""
        self.output.insert(tk.END, f"🔄 {message}\n")
        self.output.see(tk.END)
        self.root.update()

    def on_image_complete(self, image_path, error=None):
        """Handle image generation completion"""
        if error:
            self.output.insert(tk.END, f"❌ Görsel oluşturulurken hata: {error}\n")
            messagebox.showerror("Hata", f"Görsel oluşturulurken hata: {error}")
            return

        self.output.insert(tk.END, f"✅ Görsel başarıyla oluşturuldu: {image_path}\n")
        # Show the image in a new window
        show_image_window(image_path)

    def create_and_show_image(self):
        """Create an image for the character using Flux API"""
        if not self.character:
            messagebox.showwarning("Uyarı", "Önce bir karakter oluşturmalısınız!")
            return

        # İlerleme bilgisi göster
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "🎨 Görsel oluşturuluyor, lütfen bekleyin...\n")
        self.root.update()

        # Prompt oluştur
        prompt = create_prompt(self.character)
        self.output.insert(tk.END, f"📝 Kullanılan prompt: {prompt}\n")
        self.root.update()

        # Save prompt for reference
        try:
            with open("prompt_output.txt", "w") as file:
                file.write(prompt)
        except Exception as e:
            self.output.insert(tk.END, f"❌ Prompt kaydedilirken hata oluştu: {e}\n")

        # Generate image in a separate thread to keep UI responsive
        def generate_thread():
            generate_image(
                prompt,
                callback=self.on_image_complete,
                on_progress=self.on_image_progress
            )

        threading.Thread(target=generate_thread, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterApp(root)
    root.mainloop()