from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from cryptography.fernet import Fernet


app = FastAPI()

# Mount static folder like pipe to sewer
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")

# Set up template plumbing
templates = Jinja2Templates(directory="templates")

# Key is like master valve, keep safe
KEY = Fernet.generate_key()
fernet = Fernet(KEY)

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
def post_form(request: Request, text: str = Form(...), action: str = Form(...)):
    if action == "encrypt":
        result = fernet.encrypt(text.encode()).decode()
    elif action == "decrypt":
        try:
            result = fernet.decrypt(text.encode()).decode()
        except Exception as e:
            result = f"Decryption fail, maybe wrong input, try again carefully : {e}"
    else:
        result = "Unknown action, ."

    return templates.TemplateResponse("form.html", {"request": request, "result": result})
