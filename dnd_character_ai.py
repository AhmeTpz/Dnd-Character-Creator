import os
import time
import requests
import json
import base64
from PIL import Image
import io


def create_prompt(character):
    desc = character.get_description()
    subclass = desc.split(" ")[-1]
    equipment = ", ".join(character.get_equipment()) or "basic weapons"
    armor = character.get_armor() or "leather armor"

    prompt = (
        f"full body fantasy D&D character, {subclass}, wearing {armor}, "
        f"equipped with {equipment}, ultra detailed, digital painting, "
        f"epic background, 4k, cinematic lighting"
    )
    return prompt


def ensure_output_directory():
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_images")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def generate_image(prompt):
    # Fooocus'un API'sine erişmek için port numarası (varsayılan)
    # Eğer farklı bir port kullanıyorsanız bunu değiştirin
    FOOOCUS_PORT = 7866
    API_URL = f"http://127.0.0.1:{FOOOCUS_PORT}/v1/generation/text-to-image"

    # Çıktı dizinini oluştur
    output_dir = ensure_output_directory()
    output_filename = f"character_{int(time.time())}.png"
    output_path = os.path.join(output_dir, output_filename)

    # API parametreleri
    payload = {
        "prompt": prompt,
        "negative_prompt": "ugly, deformed, disfigured, poor quality, low resolution",
        "style_selections": ["Fooocus V2", "Fooocus Enhance", "Fooocus Sharp"],
        "performance_selection": "Speed",
        "aspect_ratios": "1:1",
        "image_number": 1,
        "image_seed": -1,  # Rastgele seed
        "sharpness": 2,
        "guidance_scale": 7.5,
        "base_model_name": "juggernautXL_v9Rundiffusion.safetensors",
        "refiner_model_name": "None",
        "refiner_switch": 0.8,
        "loras": [],
        "advanced_params": {
            "disable_preview": True,
            "adm_scaler_positive": 1.5,
            "adm_scaler_negative": 0.8,
            "adm_scaler_end": 0.3,
            "adaptive_cfg": 7.0,
            "sampler_name": "dpmpp_2m_sde_gpu",
            "scheduler_name": "karras",
            "overwrite_step": -1,
            "overwrite_switch": -1,
            "overwrite_width": -1,
            "overwrite_height": -1,
            "overwrite_vary_strength": -1,
            "overwrite_upscale_strength": -1,
            "mixing_image_prompt_and_variation_strength": -1,
            "mixing_image_prompt_and_negative_prompt": -1,
            "debugging_cn_preprocessor": False,
            "skipping_cn_preprocessor": False,
            "controlnet_softness": 0.25,
            "canny_low_threshold": 64,
            "canny_high_threshold": 128,
            "refiner_swap_method": "joint"
        }
    }

    try:
        print(f"📸 Görsel üretiliyor: {prompt}")
        print(f"🌐 Fooocus'a bağlanılıyor: {API_URL}")

        # API'ye istek gönder
        response = requests.post(API_URL, json=payload, timeout=180)

        # Yanıtı kontrol et
        if response.status_code == 200:
            result = response.json()

            # Base64 görüntü verisini al
            if "images" in result and result["images"]:
                image_data = result["images"][0]
                if image_data.startswith("data:image"):
                    # Base64 kısmını ayır
                    base64_data = image_data.split(",")[1]
                else:
                    base64_data = image_data

                # Base64'ü görüntüye dönüştür
                image_bytes = base64.b64decode(base64_data)
                image = Image.open(io.BytesIO(image_bytes))

                # Görüntüyü kaydet
                image.save(output_path)
                print(f"✅ Görsel başarıyla oluşturuldu: {output_path}")
                return output_path
            else:
                print(f"❌ API yanıtında görsel verisi bulunamadı: {result}")
                return None
        else:
            print(f"❌ API hatası: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"❌ Görsel oluşturma hatası: {str(e)}")

        # Fallback olarak alternatif yöntem deneyelim
        try:
            return generate_image_fallback(prompt, output_dir, output_filename)
        except Exception as fallback_error:
            print(f"❌ Fallback yöntemi de başarısız oldu: {str(fallback_error)}")
            return None


def generate_image_fallback(prompt, output_dir, output_filename):
    """Fooocus API çalışmadığında alternatif yöntem"""
    import subprocess

    output_path = os.path.join(output_dir, output_filename)
    foocus_dir = r"D:\Fooocus"  # Fooocus dizin yolunu kontrol edin

    # Komut satırı parametreleri
    cmd = [
        os.path.join(foocus_dir, "python_embeded", "python.exe"),
        os.path.join(foocus_dir, "entry_with_update.py"),
        "--preset", "default",
        "--prompt", prompt,
        "--negative-prompt", "ugly, deformed, disfigured, poor quality, low resolution",
        "--style-name", "Fooocus V2",
        "--performance", "Speed",
        "--aspect-ratio", "1:1",
        "--output", output_path,
        "--no-preview"
    ]

    print("🔄 Alternatif yöntem kullanılıyor: Komut satırı")
    process = subprocess.Popen(cmd, cwd=foocus_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Çıktıyı izle
    stdout, stderr = process.communicate(timeout=300)

    if process.returncode == 0 and os.path.exists(output_path):
        print(f"✅ Görsel başarıyla oluşturuldu (alternatif yöntem): {output_path}")
        return output_path
    else:
        print(f"❌ Komut satırı hata çıktısı: {stderr}")
        return None