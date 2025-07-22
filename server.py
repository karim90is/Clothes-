import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import replicate
import shutil

load_dotenv()
app = FastAPI()
replicate.api_token = os.getenv("REPLICATE_API_TOKEN")

@app.post("/tryon")
async def tryon(person: UploadFile = File(...), clothes: UploadFile = File(...)):
    with open("person.png", "wb") as f:
        shutil.copyfileobj(person.file, f)
    with open("clothes.png", "wb") as f:
        shutil.copyfileobj(clothes.file, f)

    output = replicate.run(
        "suno-ai/tryon:latest",
        input={"image": open("person.png", "rb"), "cloth": open("clothes.png", "rb")}
    )
    return JSONResponse(content={"output_url": output})
