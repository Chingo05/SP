from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="User Management App")

# Правильный путь к шаблонам
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# In-memory база данных
users_db = []
current_id = 1  # Счетчик для ID

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/users", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {
        "request": request,
        "users": users_db
    })

@app.get("/create", response_class=HTMLResponse)
async def create_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create", response_class=HTMLResponse)
async def create_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...)
):
    global current_id
    
    new_user = {
        "id": current_id,
        "username": username,
        "email": email,
        "full_name": full_name
    }
    users_db.append(new_user)
    current_id += 1
    
    return templates.TemplateResponse("create.html", {
        "request": request,
        "message": f"Пользователь {username} успешно создан!",
        "users": users_db
    })

@app.get("/delete", response_class=HTMLResponse)
async def delete_form(request: Request):
    return templates.TemplateResponse("delete.html", {
        "request": request,
        "users": users_db
    })

@app.post("/delete", response_class=HTMLResponse)
async def delete_user(request: Request, user_id: str = Form(...)):
    user_id_int = int(user_id)
    for i, user in enumerate(users_db):
        if user["id"] == user_id_int:
            deleted_username = user["username"]
            users_db.pop(i)
            return templates.TemplateResponse("delete.html", {
                "request": request,
                "message": f"Пользователь {deleted_username} удален!",
                "users": users_db
            })
    
    return templates.TemplateResponse("delete.html", {
        "request": request,
        "error": "Пользователь не найден!",
        "users": users_db
    })

# Добавляем тестовых пользователей при запуске
@app.on_event("startup")
async def startup_event():
    global current_id
    if not users_db:
        test_users = [
            {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com",
                "full_name": "Администратор Системы"
            },
            {
                "id": 2,
                "username": "user1", 
                "email": "user1@example.com",
                "full_name": "Первый Пользователь"
            }
        ]
        users_db.extend(test_users)
        current_id = 3  # Следующий ID будет 3

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)