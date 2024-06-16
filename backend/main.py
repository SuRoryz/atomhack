import json
from ultralytics import YOLO
import uvicorn
from PIL import Image
from fastapi import FastAPI, File
from fastapi.responses import RedirectResponse
from io import BytesIO



app = FastAPI()

'''origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''

model = YOLO("best.pt")


@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse("/docs")

@app.post("/photoRec")
def recognition(file: bytes = File()):
    if file == b'':
        return {}
    image = Image.open(BytesIO(file)).convert("RGB")
    image = image.resize((640, 640))
    result = {
        "objects": []
    }
    predict = model.predict(image, device='cpu')
    if len(predict[0].boxes) > 0:
        for i in predict[0].boxes:
            xywhList = i.xywh.tolist()[0]
            result['objects'].append({
                    "class": predict[0].names[int(i.cls.tolist()[0])],
                    "x": round(xywhList[0],1),
                    "y": round(xywhList[1],1),
                    "width": round(xywhList[2],1),
                    "height": round(xywhList[3],1),
                    "confidence": i.conf.tolist()[0],
                    "filename": ""
            })
    else:
        return {}

    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)