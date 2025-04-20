import os
import fal_client

# API Key (senin sağladığın iki parçalı key, birleşik olarak burada)
os.environ["FAL_KEY"] = "7d4cd77d-93a4-44c3-b0e0-d9e5b62e666e:f4eb507827d9182b1dcaf697a357493f"

def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])

result = fal_client.subscribe(
    "fal-ai/flux/schnell",
    arguments={
        "prompt": "A experienced male Half-Orc Ranger + Beast Master + Hunter + Swarmkeeper, wielding composite bow and throwing knife, dual-wielding with weapons in proper combat position, wearing sturdy brown leather boots, wide-brimmed brown hat, with purple hair and red eyes, with a map and compass, in a traditional adventure pose, in a wilderness campsite on a foggy morning. All weapons must be properly positioned in the character's hands or appropriate holsters/sheaths. Character must be depicted in an appropriate and respectful manner with proper weapon placement. Full body portrait, detailed illustration, highly detailed, epic lighting, dramatic composition.",
        "image_size": "landscape_4_3",
        "num_images": 1,
        "num_inference_steps": 4
    },
    with_logs=True,
    on_queue_update=on_queue_update
)

print("Image URL:", result["images"][0]["url"])

