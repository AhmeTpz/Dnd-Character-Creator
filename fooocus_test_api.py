from diffusers import DiffusionPipeline
from huggingface_hub import login

# API anahtarınızı buraya girin
login(token="TOKEN")

# Stable Diffusion modelini yükleyin
pipe = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")

# Prompt (görsel açıklaması)
prompt = "A high tech solarpunk utopia in the Amazon rainforest"

# Görseli oluşturun
image = pipe(prompt).images[0]

# Görseli kaydedin
image.save("generated_image.png")

print("Görsel başarıyla oluşturuldu!")
