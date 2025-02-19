import requests
import io
import base64
from PIL import Image, PngImagePlugin

url = "http://eqw-weqq.1001713595165998.cn-shanghai.pai-eas.aliyuncs.com"

payload = {
    "prompt": "puppy dog",
    "steps": 20,
    "n_iter": 2
}

session = requests.session()
session.headers.update({"Authorization": "YTAxOTg5YzQ0ZjRlOTEyMTRiNTQyMjJhMmVlN2FiMjc1NjZlYzg2ZA=="})


response = session.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
if response.status_code != 200:
    raise Exception(response.content)

data = response.json()

# 同步接口可直接返回图片的base64，但推荐使用返回图片地址。
for idx, im in enumerate(data['images']):
    image = Image.open(io.BytesIO(base64.b64decode(im.split(",", 1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + im
    }
    resp = session.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", resp.json().get("info"))
    image.save(f'output-{idx}.png', pnginfo=pnginfo)