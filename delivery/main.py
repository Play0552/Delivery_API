import uvicorn
from fastapi import FastAPI

from delivery.courier.router import router as router_courier
from delivery.order.router import router as router_order

app = FastAPI()

app.include_router(router_courier)

app.include_router(router_order)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
