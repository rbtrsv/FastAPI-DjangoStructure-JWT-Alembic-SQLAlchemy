import os
from time import time

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import __version__


router = APIRouter()

router.mount("/static", StaticFiles(directory="apps/main/static"), name="static")

templates = Jinja2Templates(directory="apps/main/templates")

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request, "version": __version__})


@router.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}
