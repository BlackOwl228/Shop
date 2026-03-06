from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/media", StaticFiles(directory="media"), name="media")

#Роутеры для апи
from app.admin import router as admin
from app.auth import router as auth
from app.cart import router as cart
from app.category import router as category
from app.orders import router as orders
from app.products import router as products
from app.profile import router as profile
from app.review import router as review
from app.search import router as search

app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(profile.router)
app.include_router(search.router)
app.include_router(cart.router)
app.include_router(admin.router)
app.include_router(category.router)
app.include_router(review.router)

import time

from prometheus_client import make_asgi_app

from core.metrics import REQUEST_COUNT, REQUEST_LATENCY


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    REQUEST_COUNT.labels(
        request.method,
        request.url.path,
        response.status_code
    ).inc()

    REQUEST_LATENCY.observe(duration)

    return response

app.mount("/metrics", make_asgi_app())

#Роутеры для сайта
"""
from ..website.routers import home_web, profile_web, auth_web, cart_web, checkout_web, search_web

app.include_router(home_web.router)
app.include_router(profile_web.router)
app.include_router(auth_web.router)
app.include_router(cart_web.router)
app.include_router(checkout_web.router)
app.include_router(search_web.router)
"""

import uvicorn

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)