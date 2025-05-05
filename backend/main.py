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
        # "model": "ft:gpt-4o-2024-08-06:gdkpwqer::BRQdHSWq",
        
      "messages": [
    {
        "role": "system",
        "content": "Ty si expert na riešenie rôznych otázok. Odpovedaj vždy čo najkratšie, najpresnejšie a bez zbytočných vysvetlení."
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                # "text": "Prečítaj si otázku a odpovedz podľa typu úlohy: Ak je len jedna správna možnosť, napíš len písmeno alebo číslo. Ak je viac správnych odpovedí, napíš ich cez čiarku (napr. A,C alebo 1,3). Ak ide o pravda/nepravda, napíš len: „pravda“ alebo „nepravda“. Ak treba zoradiť možnosti, napíš čísla v poradí cez čiarku (napr. 2,3,1,4), pričom 1 je najvyššie, ak nie je uvedené inak. Nezdôvodňuj, len odpovedz."
               "text": "Prečítaj si otázku a odpovedz podľa typu úlohy: mal by sa sa snažiť vykonať úlohu správne, ale čím kratšia je úloha"

            },
            {
                "type": "image_url",
                "image_url": {
                    "url": data_uri
                }
            }
        ]
    }
],
        "max_tokens": 1000
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        answer = result["choices"][0]["message"]["content"].strip()
        return {"answer": answer}
    else:
        return {"error": "Failed to get response from OpenAI", "details": response.text}
