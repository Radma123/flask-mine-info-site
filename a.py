import PIL.Image
from g4f.client import Client
import PIL
client = Client()
# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": "Что изображено на этом фото?"},
#                 {"type": "image_url", "image_url": {"url": "https://cdn1.insta360.ru/wp-content/uploads/2018/04/sandisk-extreme-pro-uhs-i-sd-128gb-500x500-min.jpg"}}
#             ]
#         }
#     ],
#     web_search = False
# )

# print(response.choices[0].message.content)

# import base64
# from io import BytesIO
# from PIL import Image

# response = client.images.generate(
#     model="flux",
#     prompt="a white siamese cat",
#     response_format="b64_json"
# )

# print(response.data[0].b64_json)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hellov"}],
    web_search=False
)
print(response.choices[0].message.content)