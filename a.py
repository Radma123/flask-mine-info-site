# import PIL.Image
# from g4f.client import Client
# import PIL
# from app.functions import compress_base64
# client = Client()

# with open('b.txt', 'r') as f:
#     img = f.read()
#     img = compress_base64(img)

# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": "Что изображено на этом фото?"},
#                 {"type": "image_url", "image_url": {"url": f"data:image/png;base64, {img}"}}
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

# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "Hellov"}],
#     web_search=False
# )
# print(response.choices[0].message.content)

import g4f.image
from app.functions import get_all_gpts

gpts = get_all_gpts()
import g4f
client = g4f.Client()