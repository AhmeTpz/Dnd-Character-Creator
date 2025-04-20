import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from abc import ABC, abstractmethod
import os

# Component Interface
class Character(ABC):
    @abstractmethod
    def get_description(self):
        pass
    @abstractmethod
    def get_power(self):
        pass
    @abstractmethod
    def get_armor(self):
        pass
    @abstractmethod
    def get_skills(self):
        pass
    @abstractmethod
    def get_level(self):
        pass

# Concrete Components
class Fighter(Character):
    def __init__(self):
        self.level = 1

    def get_description(self):
        return "Fighter"

    def get_power(self):
        return 12 + (self.level - 1) * 2

    def get_armor(self):
        return 6

    def get_skills(self):
        return ["Extra Attack", "Action Surge"]

    def get_level(self):
        return self.level


class Ranger(Character):
    def __init__(self):
        self.level = 1

    def get_description(self):
        return "Ranger"

    def get_power(self):
        return 10 + (self.level - 1) * 2

    def get_armor(self):
        return 4

    def get_skills(self):
        return ["Survival", "Longstrider"]

    def get_level(self):
        return self.level


class Sorcerer(Character):
    def __init__(self):
        self.level = 1

    def get_description(self):
        return "Sorcerer"

    def get_power(self):
        return 6 + (self.level - 1) * 3

    def get_armor(self):
        return 2

    def get_skills(self):
        return ["Sacred Flame", "Light", "Paison Spray"]

    def get_level(self):
        return self.level


# Decorator Base Class
class CharacterDecorator(Character):
    def __init__(self, character):
        self.character = character

    def get_description(self):
        return self.character.get_description()

    def get_power(self):
        return self.character.get_power()

    def get_armor(self):
        return self.character.get_armor()

    def get_skills(self):
        return self.character.get_skills()

    def get_level(self):
        return self.character.get_level()


# Level Decorator
class LevelDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)
        character.level += 1

    def get_description(self):
        return self.character.get_description()


# Subclass Decorators - Fighter
class BattleMasterDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)

    def get_description(self):
        return f"{self.character.get_description()} (Battle Master)"

    def get_power(self):
        return self.character.get_power() + 8

    def get_skills(self):
        skills = self.character.get_skills()
        if "Precision Attack" not in skills:
            skills.append("Precision Attack")
        return skills


class EldritchKnightDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)

    def get_description(self):
        return f"{self.character.get_description()} (Eldritch Knight)"

    def get_power(self):
        return self.character.get_power() + 6

    def get_skills(self):
        skills = self.character.get_skills()
        if "Mage Armour" not in skills:
            skills.append("Mage Armour")
        return skills


class ChampionDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)

    def get_description(self):
        return f"{self.character.get_description()} (Champion)"

    def get_power(self):
        return self.character.get_power() + 8

    def get_skills(self):
        skills = self.character.get_skills()
        if "Improved Critical Hit" not in skills:
            skills.append("Improved Critical Hit")
        return skills


class ArcaneArcherDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)

    def get_description(self):
        return f"{self.character.get_description()} (Arcane Archer)"

    def get_power(self):
        return self.character.get_power() + 6

    def get_skills(self):
        skills = self.character.get_skills()
        if "Arcane Shoot" not in skills:
            skills.append("Arcane Shoot")
        return skills


# Subclass Decorators - Ranger
class BeastMasterDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)

    def get_description(self):
        return f"{self.character.get_description()} (Beast Master)"

    def get_power(self):
        return self.character.get_power() + 6

    def get_skills(self):
        skills = self.character.get_skills()
        if "Animal Handling" not in skills:
            skills.append("Animal Handling")
        return skills


class HunterDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)

    def get_description(self):
        return f"{self.character.get_description()} (Hunter)"

    def get_power(self):
        return self.character.get_power() + 8

    def get_skills(self):
        skills = self.character.get_skills()
        if "True Strike" not in skills:
            skills.append("True Strike")
        return skills


class GloomStalkerDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)

    def get_description(self):
        return f"{self.character.get_description()} (Gloom Stalker)"

    def get_power(self):
        return self.character.get_power() + 8

    def get_skills(self):
        skills = self.character.get_skills()
        if "Dread Ambusher" not in skills:
            skills.append("Dread Ambusher")
        return skills


class SwarmkeeperDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)

    def get_description(self):
        return f"{self.character.get_description()} (Swarmkeeper)"

    def get_power(self):
        return self.character.get_power() + 6

    def get_skills(self):
        skills = self.character.get_skills()
        if "Legion of Bees" not in skills:
            skills.append("Legion of Bees")
        return skills


# Subclass Decorators - Sorcerer
class DraconicBloodlineDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)

    def get_description(self):
        return f"{self.character.get_description()} (Draconic Bloodline)"

    def get_power(self):
        return self.character.get_power() + 8

    def get_skills(self):
        skills = self.character.get_skills()
        if "Dragon Ancestry" not in skills:
            skills.append("Dragon Ancestry")
        if "Fly" not in skills:
            skills.append("Fly")
        return skills


class WildMagicDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)

    def get_description(self):
        return f"{self.character.get_description()} (Wild Magic)"

    def get_power(self):
        return self.character.get_power() + 8

    def get_skills(self):
        skills = self.character.get_skills()
        if "Kontrollü Kaos" not in skills:
            skills.append("Kontrollü Kaos")
        if "Bend Luck" not in skills:
            skills.append("Bend Luck")
        return skills


class StormSorceryDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)

    def get_description(self):
        return f"{self.character.get_description()} (Storm Sorcery)"

    def get_power(self):
        return self.character.get_power() + 8

    def get_skills(self):
        skills = self.character.get_skills()
        if "Heart of the Storm" not in skills:
            skills.append("Heart of the Storm")
        if "Gust of Wind" not in skills:
            skills.append("Gust of Wind")
        return skills


class ShadowMagicDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)

    def get_description(self):
        return f"{self.character.get_description()} (Shadow Magic)"

    def get_power(self):
        return self.character.get_power() + 8

    def get_skills(self):
        skills = self.character.get_skills()
        if "Superior Darkvision" not in skills:
            skills.append("Superior Darkvision")
        if "Shadow Walk" not in skills:
            skills.append("Shadow Walk")
        return skills


# Armor Decorators
class HatDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)
        self.armor_item = "Şapka"

    def get_description(self):
        return self.character.get_description()

    def get_armor(self):
        return self.character.get_armor() + 2


class HelmetDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)
        self.armor_item = "Miğfer"

    def get_description(self):
        return self.character.get_description()

    def get_armor(self):
        return self.character.get_armor() + 4


class ChainmailDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)
        self.armor_item = "Zincir zırh"

    def get_description(self):
        return self.character.get_description()

    def get_armor(self):
        return self.character.get_armor() + 6


class KnightArmorDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)
        self.armor_item = "Şovalye zırhı"

    def get_description(self):
        return self.character.get_description()

    def get_armor(self):
        return self.character.get_armor() + 12


class LeatherBootsDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)
        self.armor_item = "Deri Çizme"

    def get_description(self):
        return self.character.get_description()

    def get_armor(self):
        return self.character.get_armor() + 2


class PlateBootsDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)
        self.armor_item = "Plaka bot"

    def get_description(self):
        return self.character.get_description()

    def get_armor(self):
        return self.character.get_armor() + 6


# Weapon Decorators
class SwordDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)
        self.weapon = "Kılıç"

    def get_description(self):
        return self.character.get_description()

    def get_power(self):
        return self.character.get_power() + 6


class BowDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)
        self.weapon = "Yay"

    def get_description(self):
        return self.character.get_description()

    def get_power(self):
        return self.character.get_power() + 6


class DaggerDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)
        self.weapon = "Hançer"

    def get_description(self):
        return self.character.get_description()

    def get_power(self):
        return self.character.get_power() + 4


class AxeDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)
        self.weapon = "Balta"

    def get_description(self):
        return self.character.get_description()

    def get_power(self):
        return self.character.get_power() + 8


class StaffDecorator(CharacterDecorator):
    def __init__(self, character):
        super().__init__(character)
        self.weapon = "Asa"

    def get_description(self):
        return self.character.get_description()

    def get_power(self):
        return self.character.get_power() + 4


# Main application
class CharacterCreatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RPG Character Creator - Decorator Pattern")
        self.geometry("1200x700")
        self.configure(bg="#2c3e50")

        # Character state
        self.character = None
        self.chosen_weapons = []
        self.chosen_armors = []
        self.chosen_subclasses = []

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Left panel (character selection)
        left_panel = ttk.LabelFrame(main_frame, text="Karakter Özellikleri")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # Base class selection
        base_frame = ttk.LabelFrame(left_panel, text="Ana Sınıf")
        base_frame.pack(pady=10, padx=10, fill=tk.X)

        self.base_class_var = tk.StringVar()
        fighter_rb = ttk.Radiobutton(base_frame, text="Fighter", value="Fighter", variable=self.base_class_var)
        ranger_rb = ttk.Radiobutton(base_frame, text="Ranger", value="Ranger", variable=self.base_class_var)
        sorcerer_rb = ttk.Radiobutton(base_frame, text="Sorcerer", value="Sorcerer", variable=self.base_class_var)

        fighter_rb.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ranger_rb.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        sorcerer_rb.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        create_btn = ttk.Button(base_frame, text="Karakter Oluştur", command=self.create_character)
        create_btn.grid(row=1, column=0, columnspan=3, pady=10)

        # Level management
        level_frame = ttk.LabelFrame(left_panel, text="Seviye Ekle")
        level_frame.pack(pady=10, padx=10, fill=tk.X)

        level_btn = ttk.Button(level_frame, text="Seviye Arttır", command=self.add_level)
        level_btn.pack(pady=10)

        # Subclass selection
        self.subclass_frame = ttk.LabelFrame(left_panel, text="Alt Sınıf")
        self.subclass_frame.pack(pady=10, padx=10, fill=tk.X)

        self.subclass_var = tk.StringVar()
        self.subclass_dropdown = ttk.Combobox(self.subclass_frame, textvariable=self.subclass_var, state="readonly")
        self.subclass_dropdown.pack(pady=5, fill=tk.X)

        subclass_btn = ttk.Button(self.subclass_frame, text="Ekle", command=self.add_subclass)
        subclass_btn.pack(pady=5)

        # Weapon selection
        weapon_frame = ttk.LabelFrame(left_panel, text="Silah")
        weapon_frame.pack(pady=10, padx=10, fill=tk.X)

        weapons = ["Kılıç (+6)", "Yay (+6)", "Hançer (+4)", "Balta (+8)", "Asa (+4)"]
        self.weapon_var = tk.StringVar()
        weapon_dropdown = ttk.Combobox(weapon_frame, textvariable=self.weapon_var, values=weapons, state="readonly")
        weapon_dropdown.pack(pady=5, fill=tk.X)

        weapon_btn = ttk.Button(weapon_frame, text="Ekle", command=self.add_weapon)
        weapon_btn.pack(pady=5)

        # Armor selection
        armor_frame = ttk.LabelFrame(left_panel, text="Zırh")
        armor_frame.pack(pady=10, padx=10, fill=tk.X)

        armors = ["Şapka (+2)", "Miğfer (+4)", "Zincir zırh (+6)", "Şovalye zırhı (+12)", "Deri Çizme (+2)",
                  "Plaka bot (+6)"]
        self.armor_var = tk.StringVar()
        armor_dropdown = ttk.Combobox(armor_frame, textvariable=self.armor_var, values=armors, state="readonly")
        armor_dropdown.pack(pady=5, fill=tk.X)

        armor_btn = ttk.Button(armor_frame, text="Ekle", command=self.add_armor)
        armor_btn.pack(pady=5)

        # Reset button
        reset_btn = ttk.Button(left_panel, text="Sıfırla", command=self.reset_character)
        reset_btn.pack(pady=10)

        # Right panel (character stats and image)
        right_panel = ttk.LabelFrame(main_frame, text="Karakter Bilgileri")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Character image
        self.image_label = ttk.Label(right_panel)
        self.image_label.pack(pady=20)

        # Character stats
        stats_frame = ttk.Frame(right_panel)
        stats_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Stats with icons
        self.level_frame = self.create_stat_frame(stats_frame, "Seviye", "level.png", 0, 0)
        self.power_frame = self.create_stat_frame(stats_frame, "Güç", "power.png", 0, 1)
        self.armor_frame = self.create_stat_frame(stats_frame, "Zırh", "defense.png", 1, 0)
        self.skills_frame = self.create_stat_frame(stats_frame, "Yetenekler", "ability.png", 1, 1)
        self.weapons_frame = self.create_stat_frame(stats_frame, "Silahlar", "sword.png", 2, 0)
        self.armors_frame = self.create_stat_frame(stats_frame, "Zırhlar", "armor.png", 2, 1)

        # Initialize UI state
        self.update_ui()

    def create_stat_frame(self, parent, title, icon_name, row, column):
        frame = ttk.LabelFrame(parent, text=title)
        frame.grid(row=row, column=column, pady=5, padx=5, sticky=tk.NSEW)

        # Try to load icon
        try:
            icon = Image.open(icon_name)
            icon = icon.resize((24, 24))
            icon_img = ImageTk.PhotoImage(icon)
            icon_label = ttk.Label(frame, image=icon_img)
            icon_label.image = icon_img
            icon_label.pack(side=tk.LEFT, padx=5)
        except:
            pass  # Skip icon if not found

        value_label = ttk.Label(frame, text="")
        value_label.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

        return value_label

    def load_character_image(self, class_name):
        # Try to load image from Classes folder
        image_path = os.path.join("Classes", f"{class_name}.png")
        if not os.path.exists(image_path):
            image_path = os.path.join("Classes", f"{class_name}.webp")

        if not os.path.exists(image_path):
            self.image_label.configure(text="Image not found")
            return

        try:
            img = Image.open(image_path)
            img = img.resize((200, 200))
            photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image_label.configure(text=f"Error loading image: {e}")

    def create_character(self):
        base_class = self.base_class_var.get()

        if not base_class:
            messagebox.showwarning("Uyarı", "Lütfen bir ana sınıf seçin!")
            return

        if base_class == "Fighter":
            self.character = Fighter()
            self.subclass_dropdown['values'] = ["Battle Master", "Eldritch Knight", "Champion", "Arcane Archer"]
        elif base_class == "Ranger":
            self.character = Ranger()
            self.subclass_dropdown['values'] = ["Beast Master", "Hunter", "Gloom Stalker", "Swarmkeeper"]
        elif base_class == "Sorcerer":
            self.character = Sorcerer()
            self.subclass_dropdown['values'] = ["Draconic Bloodline", "Wild Magic", "Storm Sorcery", "Shadow Magic"]

        # Reset selections
        self.chosen_weapons = []
        self.chosen_armors = []
        self.chosen_subclasses = []

        # Load character image
        self.load_character_image(base_class)

        # Update UI
        self.update_ui()

    def add_level(self):
        if not self.character:
            messagebox.showwarning("Uyarı", "Önce bir karakter oluşturun!")
            return

        self.character = LevelDecorator(self.character)
        self.update_ui()

    def add_subclass(self):
        if not self.character:
            messagebox.showwarning("Uyarı", "Önce bir karakter oluşturun!")
            return

        subclass = self.subclass_var.get()
        if not subclass:
            messagebox.showwarning("Uyarı", "Lütfen bir alt sınıf seçin!")
            return

        if subclass in self.chosen_subclasses:
            messagebox.showwarning("Uyarı", "Bu alt sınıf zaten eklenmiş!")
            return

        # Add the selected subclass decorator
        if subclass == "Battle Master":
            self.character = BattleMasterDecorator(self.character)
        elif subclass == "Eldritch Knight":
            self.character = EldritchKnightDecorator(self.character)
        elif subclass == "Champion":
            self.character = ChampionDecorator(self.character)
        elif subclass == "Arcane Archer":
            self.character = ArcaneArcherDecorator(self.character)
        elif subclass == "Beast Master":
            self.character = BeastMasterDecorator(self.character)
        elif subclass == "Hunter":
            self.character = HunterDecorator(self.character)
        elif subclass == "Gloom Stalker":
            self.character = GloomStalkerDecorator(self.character)
        elif subclass == "Swarmkeeper":
            self.character = SwarmkeeperDecorator(self.character)
        elif subclass == "Draconic Bloodline":
            self.character = DraconicBloodlineDecorator(self.character)
        elif subclass == "Wild Magic":
            self.character = WildMagicDecorator(self.character)
        elif subclass == "Storm Sorcery":
            self.character = StormSorceryDecorator(self.character)
        elif subclass == "Shadow Magic":
            self.character = ShadowMagicDecorator(self.character)

        self.chosen_subclasses.append(subclass)
        self.update_ui()

    def add_weapon(self):
        if not self.character:
            messagebox.showwarning("Uyarı", "Önce bir karakter oluşturun!")
            return

        weapon = self.weapon_var.get()
        if not weapon:
            messagebox.showwarning("Uyarı", "Lütfen bir silah seçin!")
            return

        weapon_name = weapon.split(" ")[0]

        # Add the selected weapon decorator
        if weapon_name == "Kılıç":
            self.character = SwordDecorator(self.character)
        elif weapon_name == "Yay":
            self.character = BowDecorator(self.character)
        elif weapon_name == "Hançer":
            self.character = DaggerDecorator(self.character)
        elif weapon_name == "Balta":
            self.character = AxeDecorator(self.character)
        elif weapon_name == "Asa":
            self.character = StaffDecorator(self.character)

        self.chosen_weapons.append(weapon)
        self.update_ui()

    def add_armor(self):
        if not self.character:
            messagebox.showwarning("Uyarı", "Önce bir karakter oluşturun!")
            return

        armor = self.armor_var.get()
        if not armor:
            messagebox.showwarning("Uyarı", "Lütfen bir zırh seçin!")
            return

        armor_name = armor.split(" ")[0]

        # Add the selected armor decorator
        if armor_name == "Şapka":
            self.character = HatDecorator(self.character)
        elif armor_name == "Miğfer":
            self.character = HelmetDecorator(self.character)
        elif armor_name == "Zincir":
            self.character = ChainmailDecorator(self.character)
        elif armor_name == "Şovalye":
            self.character = KnightArmorDecorator(self.character)
        elif armor_name == "Deri":
            self.character = LeatherBootsDecorator(self.character)
        elif armor_name == "Plaka":
            self.character = PlateBootsDecorator(self.character)

        self.chosen_armors.append(armor)
        self.update_ui()

    def reset_character(self):
        self.character = None
        self.chosen_weapons = []
        self.chosen_armors = []
        self.chosen_subclasses = []
        self.image_label.configure(image="")
        self.update_ui()

    def update_ui(self):
        if not self.character:
            self.level_frame.configure(text="")
            self.power_frame.configure(text="")
            self.armor_frame.configure(text="")
            self.skills_frame.configure(text="")
            self.weapons_frame.configure(text="")
            self.armors_frame.configure(text="")
            return

        # Update character stats display
        self.level_frame.configure(text=str(self.character.get_level()))
        self.power_frame.configure(text=str(self.character.get_power()))
        self.armor_frame.configure(text=str(self.character.get_armor()))

        # Format skills
        skills_text = ", ".join(self.character.get_skills())
        self.skills_frame.configure(text=skills_text)

        # Format weapons and armors
        weapons_text = ", ".join(self.chosen_weapons) if self.chosen_weapons else "Yok"
        armors_text = ", ".join(self.chosen_armors) if self.chosen_armors else "Yok"

        self.weapons_frame.configure(text=weapons_text)
        self.armors_frame.configure(text=armors_text)


# Run the application
if __name__ == "__main__":
    app = CharacterCreatorApp()
    app.mainloop()