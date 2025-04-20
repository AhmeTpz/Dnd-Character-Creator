import os
import fal_client
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# API Key setup
API_KEY = "7d4cd77d-93a4-44c3-b0e0-d9e5b62e666e:f4eb507827d9182b1dcaf697a357493f"


def create_prompt(character):
    """Creates a detailed prompt for image generation based on character attributes"""
    if not character:
        return "Fantasy character in a dungeon setting"

    # Base description
    base_class = character.__class__.__name__
    if hasattr(character, 'decorated'):
        base_class = character.decorated.__class__.__name__

    # Get character components
    description = character.get_description()
    level = character.get_level()
    skills = character.get_skills()
    equipment = character.get_equipment()

    # Character race and gender (random for now)
    races = ["Human", "Elf", "Dwarf", "Half-Elf", "Half-Orc", "Tiefling", "Dragonborn"]
    genders = ["male", "female"]
    import random
    race = random.choice(races)
    gender = random.choice(genders)

    # Extract class and subclass information
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

    # Build class description
    class_desc = f"{race} {gender} {' + '.join(class_info)}"
    if subclass_info:
        class_desc += f" + {' + '.join(subclass_info)}"

    # Extract equipment
    weapons = []
    armor_items = []

    weapon_types = ["Sword", "Bow", "Dagger", "Axe", "Staff"]
    armor_types = ["Hat", "Helmet", "Chain Armor", "Knight Armor", "Leather Boots", "Plate Boots"]

    for item in equipment:
        if any(weapon in item for weapon in weapon_types):
            weapons.append(item)
        if any(armor in item for armor in armor_types):
            armor_items.append(item)

    # Format weapons and armor descriptions
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

    # Random character features
    hair_colors = ["black", "brown", "blonde", "red", "white", "silver", "blue", "purple", "green"]
    eye_colors = ["brown", "blue", "green", "amber", "gray", "purple", "red"]

    hair_color = random.choice(hair_colors)
    eye_color = random.choice(eye_colors)

    features_desc = f"with {hair_color} hair and {eye_color} eyes"

    # Character accessories based on class
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

    # Environment based on class
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

    # Lighting and atmosphere
    times = ["dawn", "dusk", "night", "morning", "afternoon"]
    atmospheres = ["foggy", "stormy", "clear", "moonlit", "sunlit"]

    time_of_day = random.choice(times)
    atmosphere = random.choice(atmospheres)

    # Build the complete prompt
    prompt = f"A experienced {class_desc}, {weapon_desc}, {armor_desc}, {features_desc}, {accessories_desc}, in a traditional adventure pose, in a {environment} on a {atmosphere} {time_of_day}. All weapons must be properly positioned in the character's hands or appropriate holsters/sheaths. Character must be depicted in an appropriate and respectful manner with proper weapon placement. Full body portrait, detailed illustration, highly detailed, epic lighting, dramatic composition."

    return prompt


def generate_image(prompt, callback=None, on_progress=None):
    """Generates an image using Flux API and returns the image URL"""
    os.environ["FAL_KEY"] = API_KEY

    def on_queue_update(update):
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
                if on_progress:
                    on_progress(log["message"])

    try:
        # Generate image
        result = fal_client.subscribe(
            "fal-ai/flux/schnell",
            arguments={
                "prompt": prompt,
                "image_size": "portrait_4_3",  # Changed from "square_1_1" to "square"
                "num_images": 1,
                "num_inference_steps": 4
            },
            with_logs=True,
            on_queue_update=on_queue_update
        )

        # Get image URL
        image_url = result["images"][0]["url"]

        # Download the image
        response = requests.get(image_url)
        img_data = BytesIO(response.content)

        # Save the image locally
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


def show_image_window(image_path):
    """Opens a new window to display the generated image with improved size"""
    if not image_path or not os.path.exists(image_path):
        return

    window = tk.Toplevel()
    window.title("D&D Karakter Görseli")
    window.configure(bg="#1e1e1e")  # Koyu tema

    # Ana pencerenin ortasında açılması için
    window.geometry("800x900")  # Daha büyük pencere boyutu

    # Frame oluştur
    frame = tk.Frame(window, bg="#1e1e1e", padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    # Görüntüyü orijinal boyutuna yakın bir şekilde yükle
    img = Image.open(image_path)

    # Orijinal görüntü boyutlarını al
    original_width, original_height = img.size

    # Görüntü boyutunu daha büyük yap (2x)
    display_width = min(original_width * 2, 700)  # Maksimum genişlik
    display_height = int((display_width / original_width) * original_height)

    # Yüksek kaliteli yeniden boyutlandırma
    img = img.resize((display_width, display_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    # Görüntüyü göstermek için label oluştur
    label = tk.Label(frame, image=photo, bg="#1e1e1e")
    label.image = photo  # Referansı koru
    label.pack(padx=10, pady=10)

    # Bilgi etiketi
    info_text = f"Görüntü Boyutu: {original_width}x{original_height} (Gösterilen: {display_width}x{display_height})"
    info_label = tk.Label(frame, text=info_text, fg="white", bg="#1e1e1e")
    info_label.pack(pady=(0, 10))

    # Kaydet butonu
    button_frame = tk.Frame(frame, bg="#1e1e1e")
    button_frame.pack(pady=10)

    def save_image():
        from tkinter import filedialog
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("All files", "*.*")])
        if save_path:
            # Orijinal görüntüyü kaydet (yeniden boyutlandırılmamış hali)
            original_img = Image.open(image_path)
            original_img.save(save_path)
            tk.messagebox.showinfo("Başarılı", f"Görsel kaydedildi: {save_path}")

    def open_folder():
        import os, subprocess
        folder_path = os.path.dirname(os.path.abspath(image_path))
        # İşletim sistemine göre klasör açma komutu
        if os.name == 'nt':  # Windows
            os.startfile(folder_path)
        elif os.name == 'posix':  # macOS veya Linux
            subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', folder_path])

    # Kaydet butonu
    save_btn = tk.Button(button_frame, text="Görseli Kaydet", command=save_image,
                         bg="#4CAF50", fg="white", width=15, height=2)
    save_btn.pack(side="left", padx=10)

    # Klasörü aç butonu
    folder_btn = tk.Button(button_frame, text="Klasörü Aç", command=open_folder,
                           bg="#2196F3", fg="white", width=15, height=2)
    folder_btn.pack(side="left", padx=10)

    # Pencereyi ekranın ortasında göster
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window.winfo_width()) // 2
    y = (screen_height - window.winfo_height()) // 2
    window.geometry(f"+{x}+{y}")