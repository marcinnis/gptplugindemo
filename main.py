from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from unstructured.partition.html import partition_html
from pydantic import BaseModel

class ProcessWebUrl(BaseModel):
    url: str

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.route("/.well-known/ai-plugin.json")
async def get_manifest(request):
    file_path = "./well-known/ai-plugin.json"
    return FileResponse(file_path, media_type="text/json")

@app.route("/.well-known/logo.png")
async def get_logo(request):
    file_path = "./well-known/logo.png"
    return FileResponse(file_path, media_type="image/png")

@app.route("/.well-known/openapi.yaml")
async def get_openapi(request):
    file_path = "./well-known/openapi.yaml"
    return FileResponse(file_path, media_type="text/json")

@app.post("/get_data_from_url")
async def get_data_from_url(job_request: ProcessWebUrl):
    print("Processing web url: " + job_request.url)
    try:
        url = job_request.url
        if not url.startswith("http"):
          url = "https://" + url
        headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
        elements = partition_html(
            url=url, headers=headers
        )
        text = "\n\n".join([str(el) for el in elements])

    except Exception as e:
        return {"code": 400, "success": False, "message": "Error processing web url: " + str(e)}

    return JSONResponse(
        status_code=200,
        content={
            "data": text,
        })