import os
import fal_client
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import random

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

    # Irk tanımlamaları
    tiefling_colors = ["red", "blue", "purple", "black"]
    tiefling_color = random.choice(tiefling_colors)

    races = {
        "Human": "human",
        "Elf": "elf with pointy ears",
        "Dwarf": "dwarf",
        "Half-Elf": "half-elf with pointy ears",
        "Half-Orc": "green-skinned half-orc",
        "Tiefling": f"{tiefling_color}-skinned humanoid with long curved horns, glowing eyes, a pointed tail, and infernal features.",
        "Dragonborn": "dragon-like humanoid with scaled reptilian skin (full body), draconic facial features including a snout and sharp teeth, a long muscular tail, clawed hands and feet, and a powerful draconic build."
    }

    # Cinsiyet ve fiziksel özellikler
    genders = {
        "male": "male",
        "female": "female"
    }

    race = random.choice(list(races.keys()))
    race_desc = races[race]
    gender = random.choice(list(genders.keys()))
    gender_desc = genders[gender]

    # Class ve subclass bilgilerini topla
    class_info = []
    if "Fighter" in description:
        class_info.append("Fighter")
    if "Ranger" in description:
        class_info.append("Ranger")
    if "Sorcerer" in description:
        class_info.append("Sorcerer")

    # Tüm subclass'ları belirle
    all_subclasses = {
        "Fighter": ["Battle Master", "Eldritch Knight", "Champion", "Arcane Archer"],
        "Ranger": ["Beast Master", "Hunter", "Gloom Stalker", "Swarmkeeper"],
        "Sorcerer": ["Draconic Bloodline", "Wild Magic", "Storm Sorcery", "Shadow Magic"]
    }

    subclass_info = []
    for cls, subclasses in all_subclasses.items():
        for subclass in subclasses:
            if subclass in description:
                subclass_info.append((cls, subclass))  # Class ve subclass'ı birlikte saklıyoruz

    class_desc = f"{gender_desc} {race_desc}"
    # Subclass'ları prompt'a eklemeyi kaldırıyoruz

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
            "Sword": {
                "positions": ["in hand", "on their back", "sheathed at their side"],
                "descriptions": ["steel longsword", "broadsword", "sword"]
            },
            "Bow": {
                "positions": ["in hand", "on their back"],
                "descriptions": ["composite bow", "longbow", "hunting bow"]
            },
            "Dagger": {
                "positions": ["in hand", "sheathed at their side", "sheathed at their waist"],
                "descriptions": ["dagger", "throwing dagger", "short dagger"]
            },
            "Axe": {
                "positions": ["in hand", "on their back", "sheathed at their side"],
                "descriptions": ["battle axe", "war axe", "two-handed axe"]
            },
            "Staff": {
                "positions": ["in hand", "on their back"],
                "descriptions": ["magical staff", "arcane staff", "spellcasting staff"]
            }
        }
        
        weapon_list = []
        for weapon in weapons:
            for weapon_type in weapon_types:
                if weapon_type in weapon:
                    if weapon_type in weapon_terms:
                        desc = random.choice(weapon_terms[weapon_type]["descriptions"])
                        pos = random.choice(weapon_terms[weapon_type]["positions"])
                        weapon_list.append(f"a {desc} {pos}")
                    else:
                        weapon_list.append(f"a {weapon.lower()} in hand")
                    break
        
        # Yay için özel durum - eğer yay varsa ve sırtında değilse, sadak ekle
        for i, weapon in enumerate(weapon_list):
            if "bow" in weapon.lower() and "on their back" not in weapon:
                weapon_list[i] += " and a quiver on their back"
        
        weapon_desc = " and ".join(weapon_list)

    armor_desc = ""
    if armor_items:
        armor_terms = {
            "Hat": ["wide-brimmed hat", "adventurer's hat", "traveler's hat"],
            "Helmet": ["metal helmet", "steel helmet", "knight's helmet"],
            "Chain Armor": ["chainmail armor", "chain shirt", "mail armor"],
            "Knight Armor": ["plate armor", "full plate", "knight's plate"],
            "Leather Boots": ["leather boots", "traveling boots", "adventurer's boots"],
            "Plate Boots": ["metal boots", "steel boots", "knight's boots"]
        }
        
        armor_list = []
        for armor in armor_items:
            for armor_type in armor_types:
                if armor_type in armor:
                    armor_list.append(random.choice(armor_terms.get(armor_type, [armor_type.lower()])))
                    break
                    
        armor_desc = f"wearing {', '.join(armor_list)}"

    hair_colors = ["black", "brown", "blonde", "red", "white", "silver", "blue", "purple", "green"]
    eye_colors = ["brown", "blue", "green", "amber", "gray", "purple", "red"]

    hair_color = random.choice(hair_colors)
    eye_color = random.choice(eye_colors)

    features_desc = f"with {hair_color} hair and {eye_color} eyes"

    accessories = []
    for cls in class_info:
        if cls == "Ranger":
            accessories.extend([
                "leather-bound map case with compass",
                "trail rations and water skin",
                "weather-worn cloak with hood",
                "survival tools and herbs",
                "tracking journal with sketches"
            ])
        elif cls == "Sorcerer":
            accessories.extend([
                "ornate spellbook with glowing runes",
                "pouch of magical components",
                "enchanted amulet with protective wards",
                "mystical scroll case",
                "arcane focus crystal"
            ])
        elif cls == "Fighter":
            accessories.extend([
                "utility belt with potions",
                "tactical map case",
                "honor badge or medal",
                "battle journal",
                "whetstone and oil"
            ])

    accessories_desc = ""
    if accessories:
        selected_accessories = random.sample(accessories, min(2, len(accessories)))
        accessories_desc = f"with {', '.join(selected_accessories)}"

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
        "novice": ["young and inexperienced", "untested adventurer", "beginner warrior"],
        "experienced": ["confident and battle-hardened", "seasoned adventurer", "skilled warrior"],
        "veteran": ["seasoned and battle-scarred", "experienced adventurer", "battle-tested warrior"],
        "master": ["renowned and formidable", "master adventurer", "epic warrior"],
        "legendary": ["mythical and awe-inspiring", "legendary adventurer", "legendary warrior"]
    }

    class_effects = {
        "Fighter": {
            "level_novice": ["with uncertain combat stance", "in a nervous fighting pose", "hesitantly ready for battle"],
            "level_experienced": ["with confident combat stance", "in a warrior's pose", "battle-ready"],
            "level_veteran": ["with masterful combat stance", "in a veteran's pose", "battle-hardened"],
            "level_master": ["with legendary combat stance", "in a master's pose", "battle-perfected"],
            "level_legendary": ["with divine combat stance", "in an epic pose", "battle-transcended"],
            "Battle Master": "Tactical markings on their armor",
            "Eldritch Knight": "Weapons covered in blue magical energy and enchanted runes",
            "Champion": "Proud and confident stance, wearing ornate armor",
            "Arcane Archer": "Glowing blue magical energy in their eyes, leaving blue light trails"
        },
        "Ranger": {
            "level_novice": ["with basic tracking skills", "in a hunting pose", "ready to track"],
            "level_experienced": ["with expert tracking skills", "in a ranger's pose", "tracking-ready"],
            "level_veteran": ["with masterful tracking skills", "in a veteran's pose", "tracking-perfected"],
            "level_master": ["with legendary tracking skills", "in a master's pose", "tracking-transcended"],
            "level_legendary": ["with divine tracking skills", "in an epic pose", "tracking-mastered"],
            "Beast Master": "With a wolf companion beside them",
            "Hunter": "Wearing green leather clothes and a hooded cloak",
            "Gloom Stalker": "Dark and shadowy appearance, wearing a black mask and having a scar on their eye",
            "Swarmkeeper": "Surrounded by glowing magical fireflies"
        },
        "Sorcerer": {
            "level_novice": ["with basic magical aura", "in a casting pose", "ready to cast"],
            "level_experienced": ["with expert magical aura", "in a sorcerer's pose", "casting-ready"],
            "level_veteran": ["with masterful magical aura", "in a veteran's pose", "casting-perfected"],
            "level_master": ["with legendary magical aura", "in a master's pose", "casting-transcended"],
            "level_legendary": ["with divine magical aura", "in an epic pose", "casting-mastered"],
            "Draconic Bloodline": "With dragon wings on the back, having an ancient appearance",
            "Wild Magic": "Malevolent and powerful appearance, surrounded by red and black magical energy",
            "Storm Sorcery": "Covered in crackling lightning",
            "Shadow Magic": "Covered in shadows"
        }
    }

    # Class etkilerini topluyoruz
    class_effect_list = []
    for cls in class_info:
        if cls in class_effects:
            # Seviye bazlı efektleri al
            level_key = f"level_{experience_level}"
            if level_key in class_effects[cls]:
                class_effect_list.append(random.choice(class_effects[cls][level_key]))

    # Tüm subclass efektlerini topluyoruz
    subclass_effect_list = []
    for cls, subclass in subclass_info:
        if cls in class_effects and subclass in class_effects[cls]:
            subclass_effect_list.append(class_effects[cls][subclass])

    class_effect = ", ".join(class_effect_list) if class_effect_list else ""
    subclass_effect = ", ".join(subclass_effect_list) if subclass_effect_list else ""

    # Ekipman ve çevre efektlerini birleştir
    equipment_effects = []
    if weapons:
        equipment_effects.append(weapon_desc)
    if armor_items:
        equipment_effects.append(armor_desc)
    if accessories_desc:
        equipment_effects.append(accessories_desc)

    equipment_effects_joined = ", ".join(filter(None, equipment_effects))
    
    environment_effect = f"in a {environment} on a {atmosphere} {time_of_day}"

    # Tüm efektleri birleştiriyoruz ve boş olanları filtreleyelim
    all_effects = [
        f"A {random.choice(level_details[experience_level])} {experience_level} {class_desc}",
        equipment_effects_joined,
        features_desc,
        class_effect,
        subclass_effect,
        battle_damage,
        aura_effects,
        magical_effects,
        environment_effect
    ]

    # Boş string'leri kaldır
    filtered_effects = [effect for effect in all_effects if effect]
    
    prompt = ", ".join(filtered_effects) + ". Full body shot, dynamic pose, action stance, full character visible from head to toe, professional photography lighting, 8k resolution, sharp focus, intricate details, cinematic composition, professional photography, color grading, ultra realistic, photorealistic, highly detailed facial features, natural lighting, realistic textures, proper proportions, realistic skin tones, natural expressions, only one character in the image."

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