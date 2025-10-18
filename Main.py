from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.routes import api
from backend.data_management.pool_handler import init_data_pool, close_data_pool
from backend.user_management.pool_handler import init_user_pool, close_user_pool
from contextlib import asynccontextmanager 

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Startup: Initializing database pools...")
    await init_data_pool()
    await init_user_pool()
    print("Application Startup: Database pools initialized successfully.")
    
    yield
    
    print("Application Shutdown: Closing connections...")
    await close_user_pool()
    await close_data_pool()


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api.api_router)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )
