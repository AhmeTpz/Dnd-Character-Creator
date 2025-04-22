import os
import fal_client

os.environ["FAL_KEY"] = "7d4cd77d-93a4-44c3-b0e0-d9e5b62e666e:f4eb507827d9182b1dcaf697a357493f"

def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])

result = fal_client.subscribe(
    "fal-ai/flux/schnell",
    arguments={
        "prompt": "Create a detailed portrait of a Tiefling Sorcerer with Draconic Bloodline. The character has dark red skin with subtle scales, curved horns that sweep back from their forehead, and glowing amber eyes. They wear a flowing dark blue robe with gold embroidery, and their hands crackle with arcane energy. Their expression is intense and focused, with a slight smirk. The background shows a mystical library with floating books and magical orbs. The lighting is dramatic, with blue and gold magical effects surrounding them. The style should match Baldur's Gate 3's semi-realistic fantasy aesthetic.",
        "image_size": "landscape_4_3",
        "num_images": 1,
        "num_inference_steps": 4
    },
    with_logs=True,
    on_queue_update=on_queue_update
)

print("Image URL:", result["images"][0]["url"])

