import os
import fal_client
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

API_KEY = "7d4cd77d-93a4-44c3-b0e0-d9e5b62e666e:f4eb507827d9182b1dcaf697a357493f"

# ===================================================
# CHARACTER PROMPT GENERATION / KARAKTER PROMPT OLUŞTURMA
# ===================================================
def create_prompt(character):
    if not character:
        return "Fantasy character in a dungeon setting"

    base_class = character.__class__.__name__
    if hasattr(character, 'decorated'):
        base_class = character.decorated.__class__.__name__

    description = character.get_description()
    level = character.get_level()
    skills = character.get_skills()
    equipment = character.get_equipment()

    races = ["Human", "Elf", "Dwarf", "Half-Elf", "Half-Orc", "Tiefling", "Dragonborn"]
    genders = ["male", "female"]
    import random
    race = random.choice(races)
    gender = random.choice(genders)

    class_info = []
    if "Fighter" in description:
        class_info.append("Fighter")
    if "Ranger" in description:
        class_info.append("Ranger")
    if "Sorcerer" in description:
        class_info.append("Sorcerer")

    subclass_info = []
    subclasses = [
        "Battle Master", "Eldritch Knight", "Champion", "Arcane Archer",
        "Beast Master", "Hunter", "Gloom Stalker", "Swarmkeeper",
        "Draconic Bloodline", "Wild Magic", "Storm Sorcery", "Shadow Magic"
    ]

    for subclass in subclasses:
        if subclass in description:
            subclass_info.append(subclass)

    class_desc = f"{race} {gender} {' + '.join(class_info)}"
    if subclass_info:
        class_desc += f" + {' + '.join(subclass_info)}"

    weapons = []
    armor_items = []

    weapon_types = ["Sword", "Bow", "Dagger", "Axe", "Staff"]
    armor_types = ["Hat", "Helmet", "Chain Armor", "Knight Armor", "Leather Boots", "Plate Boots"]

    for item in equipment:
        if any(weapon in item for weapon in weapon_types):
            weapons.append(item)
        if any(armor in item for armor in armor_types):
            armor_items.append(item)

    weapon_desc = ""
    if weapons:
        weapon_terms = {
            "Sword": "sword",
            "Bow": "composite bow",
            "Dagger": "throwing knife",
            "Axe": "battle axe",
            "Staff": "magical staff"
        }
        weapon_list = [weapon_terms.get(w, w.lower()) for w in weapons]
        if len(weapons) > 1:
            weapon_desc = f"dual-wielding {' and '.join(weapon_list)}, with weapons in proper combat position"
        else:
            weapon_desc = f"wielding {' and '.join(weapon_list)}"

    armor_desc = ""
    if armor_items:
        armor_terms = {
            "Hat": "wide-brimmed brown hat",
            "Helmet": "ornate metal helmet",
            "Chain Armor": "chainmail armor",
            "Knight Armor": "ornate plate armor",
            "Leather Boots": "sturdy brown leather boots",
            "Plate Boots": "protective metal greaves"
        }
        armor_list = [armor_terms.get(a, a.lower()) for a in armor_items]
        armor_desc = f"wearing {', '.join(armor_list)}"

    hair_colors = ["black", "brown", "blonde", "red", "white", "silver", "blue", "purple", "green"]
    eye_colors = ["brown", "blue", "green", "amber", "gray", "purple", "red"]

    hair_color = random.choice(hair_colors)
    eye_color = random.choice(eye_colors)

    features_desc = f"with {hair_color} hair and {eye_color} eyes"

    accessories = []
    if "Ranger" in class_info:
        accessories.extend(["a map and compass", "animal companion"])
    if "Sorcerer" in class_info:
        accessories.extend(["glowing magical orb", "arcane focus"])
    if "Fighter" in class_info:
        accessories.extend(["shield with emblem", "battle scars"])

    accessories_desc = ""
    if accessories:
        accessories_desc = f"with {', '.join(random.sample(accessories, min(2, len(accessories))))}"

    environments = {
        "Fighter": ["castle courtyard", "training grounds", "battlefield", "arena"],
        "Ranger": ["wilderness campsite", "forest trail", "mountain pass", "hidden cave"],
        "Sorcerer": ["arcane library", "magical tower", "mystical ritual site", "enchanted grove"]
    }

    env_options = []
    for cls in class_info:
        if cls in environments:
            env_options.extend(environments[cls])

    environment = "fantasy landscape"
    if env_options:
        environment = random.choice(env_options)

    times = ["dawn", "dusk", "night", "morning", "afternoon"]
    atmospheres = ["foggy", "stormy", "clear", "moonlit", "sunlit"]

    time_of_day = random.choice(times)
    atmosphere = random.choice(atmospheres)

    experience_level = "novice"
    aura_effects = ""
    battle_damage = ""
    magical_effects = ""

    if level >= 5:
        experience_level = "experienced"
        battle_damage = "with minor battle scars"
    if level >= 10:
        experience_level = "veteran"
        battle_damage = "with prominent battle scars and weathered armor"
        aura_effects = "surrounded by a faint aura of experience"
    if level >= 15:
        experience_level = "master"
        battle_damage = "with legendary battle scars and masterfully crafted armor"
        aura_effects = "radiating a powerful aura of mastery"
        magical_effects = "with subtle magical energy emanating from their equipment"
    if level >= 20:
        experience_level = "legendary"
        battle_damage = "with legendary battle scars and divine armor"
        aura_effects = "radiating a divine aura of power"
        magical_effects = "with powerful magical energy swirling around them"

    level_details = {
        "novice": "young and eager",
        "experienced": "confident and battle-hardened",
        "veteran": "seasoned and battle-scarred",
        "master": "renowned and formidable",
        "legendary": "mythical and awe-inspiring"
    }

    class_effects = {
        "Fighter": {
            "novice": "with basic combat stance",
            "experienced": "with expert combat stance",
            "veteran": "with masterful combat stance",
            "master": "with legendary combat stance",
            "legendary": "with divine combat stance"
        },
        "Ranger": {
            "novice": "with basic tracking skills",
            "experienced": "with expert tracking skills",
            "veteran": "with masterful tracking skills",
            "master": "with legendary tracking skills",
            "legendary": "with divine tracking skills"
        },
        "Sorcerer": {
            "novice": "with basic magical aura",
            "experienced": "with expert magical aura",
            "veteran": "with masterful magical aura",
            "master": "with legendary magical aura",
            "legendary": "with divine magical aura"
        }
    }

    class_effect = ""
    for cls in class_info:
        if cls in class_effects:
            class_effect = class_effects[cls][experience_level]
            break

    prompt = f"A {level_details[experience_level]} {experience_level} {class_desc}, {weapon_desc}, {armor_desc}, {features_desc}, {accessories_desc}, {class_effect}, {battle_damage}, {aura_effects}, {magical_effects}, in a traditional adventure pose, in a {environment} on a {atmosphere} {time_of_day}. All weapons must be properly positioned in the character's hands or appropriate holsters/sheaths. Character must be depicted in an appropriate and respectful manner with proper weapon placement. Full body portrait, highly detailed illustration, epic lighting, dramatic composition."

    return prompt

# ===================================================
# IMAGE GENERATION / GÖRSEL OLUŞTURMA
# ===================================================
def generate_image(prompt, callback=None, on_progress=None):
    os.environ["FAL_KEY"] = API_KEY

    def on_queue_update(update):
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
                if on_progress:
                    on_progress(log["message"])

    try:
        result = fal_client.subscribe(
            "fal-ai/flux/schnell",
            arguments={
                "prompt": prompt,
                "image_size": "portrait_4_3",
                "num_images": 1,
                "num_inference_steps": 4
            },
            with_logs=True,
            on_queue_update=on_queue_update
        )

        image_url = result["images"][0]["url"]

        response = requests.get(image_url)
        img_data = BytesIO(response.content)

        img = Image.open(img_data)
        timestamp = int(time.time())
        save_path = f"generated_images/character_image_{timestamp}.png"
        img.save(save_path)

        if callback:
            callback(save_path)

        return save_path

    except Exception as e:
        print(f"Error generating image: {e}")
        if callback:
            callback(None, str(e))
        return None, str(e)

# ===================================================
# IMAGE DISPLAY / GÖRSEL GÖSTERME
# ===================================================
def show_image_window(image_path):
    if not image_path or not os.path.exists(image_path):
        return

    window = tk.Toplevel()
    window.title("D&D Karakter Görseli")
    window.configure(bg="#1e1e1e")

    window.geometry("800x900")

    frame = tk.Frame(window, bg="#1e1e1e", padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    img = Image.open(image_path)

    original_width, original_height = img.size

    display_width = min(original_width * 2, 700)
    display_height = int((display_width / original_width) * original_height)

    img = img.resize((display_width, display_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(frame, image=photo, bg="#1e1e1e")
    label.image = photo
    label.pack(padx=10, pady=10)

    info_text = f"Görüntü Boyutu: {original_width}x{original_height} (Gösterilen: {display_width}x{display_height})"
    info_label = tk.Label(frame, text=info_text, fg="white", bg="#1e1e1e")
    info_label.pack(pady=(0, 10))

    button_frame = tk.Frame(frame, bg="#1e1e1e")
    button_frame.pack(pady=10)

    def save_image():
        from tkinter import filedialog
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("All files", "*.*")])
        if save_path:
            original_img = Image.open(image_path)
            original_img.save(save_path)
            tk.messagebox.showinfo("Başarılı", f"Görsel kaydedildi: {save_path}")

    def open_folder():
        import os, subprocess
        folder_path = os.path.dirname(os.path.abspath(image_path))
        if os.name == 'nt':
            os.startfile(folder_path)
        elif os.name == 'posix':
            subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', folder_path])

    save_btn = tk.Button(button_frame, text="Görseli Kaydet", command=save_image,
                         bg="#4CAF50", fg="white", width=15, height=2)
    save_btn.pack(side="left", padx=10)

    folder_btn = tk.Button(button_frame, text="Klasörü Aç", command=open_folder,
                           bg="#2196F3", fg="white", width=15, height=2)
    folder_btn.pack(side="left", padx=10)

    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window.winfo_width()) // 2
    y = (screen_height - window.winfo_height()) // 2
    window.geometry(f"+{x}+{y}")