# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware
# from PIL import Image
# import pytesseract
# import requests
# import io
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
#
# app = FastAPI()
#
# # Доступ з фронтенду
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# # Статика
# app.mount("/static", StaticFiles(directory="backend/frontend"), name="static")
#
# @app.get("/", response_class=HTMLResponse)
# async def get_index():
#     return FileResponse("backend/frontend/index.html")
#
# @app.post("/upload/")
# async def upload_image(file: UploadFile = File(...)):
#     try:
#         image = Image.open(io.BytesIO(await file.read()))
#         text = pytesseract.image_to_string(image, lang="eng+slk")
#
#         prompt = f"""
# Ty si expert na riesenie testov. Otazka a moznosti su:
#
# {text}
#
# Vyber spravnu odpoved a napis ju co najkratsie.
# """
#
#         headers = {
#             "Authorization": f"Bearer {OPENAI_API_KEY}",
#             "Content-Type": "application/json"
#         }
#
#         payload = {
#             "model": "gpt-4o",
#             "messages": [
#                 {"role": "system", "content": "Ty si expert na testy, odpovedaj vzdy co najkratsie."},
#                 {"role": "user", "content": prompt}
#             ],
#             "temperature": 0.2,
#             "max_tokens": 200
#         }
#
#         response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
#
#         if response.status_code == 200:
#             result = response.json()
#             answer = result["choices"][0]["message"]["content"].strip()
#             return {"answer": answer}
#         else:
#             print("Помилка від OpenAI:", response.text)
#             return {"error": "Failed to get response from OpenAI", "details": response.text}
#
#     except Exception as e:
#         print("Внутрішня помилка сервера:", str(e))
#         return {"error": "Server error", "details": str(e)}


from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64
import os
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="backend/frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    return FileResponse("backend/frontend/index.html")

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    data_uri = f"data:image/jpeg;base64,{base64_image}"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "Ty si expert na testy, odpovedaj co najkratsie."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Na obrazku je otazka a moznosti. Vyber spravnu odpoved a napis ju co najkratsie."},
                    {"type": "image_url", "image_url": {"url": data_uri}}
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        answer = result["choices"][0]["message"]["content"].strip()
        return {"answer": answer}
    else:
        return {"error": "Failed to get response from OpenAI", "details": response.text}