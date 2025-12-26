from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/media", StaticFiles(directory="media"), name="media")

from api import auth, orders, products, profile
app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(profile.router)

import uvicorn
if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)