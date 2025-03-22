from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
from PIL import Image
import io

app = FastAPI()

def ubah_warna(image, warna):
    img = np.array(image)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    warna_dict = {
        "hitam": [0, 0, 0],
        "coklat": [139, 69, 19]
    }
    img[mask > 0] = warna_dict.get(warna, [0, 0, 0])
    return Image.fromarray(img)

@app.post("/process")
async def process_image(file: UploadFile = File(...), warna: str = Form(...)):
    image = Image.open(file.file).convert("RGB")
    processed_image = ubah_warna(image, warna)
    img_io = io.BytesIO()
    processed_image.save(img_io, format='PNG')
    img_io.seek(0)
    return StreamingResponse(img_io, media_type="image/png")