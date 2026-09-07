import asyncio
import time

from fastapi import FastAPI, Header, Query

app = FastAPI()

@app.get('/sync-task')
def sync_task():
    time.sleep(2)
    return {'message': 'sync-task'}


@app.get('/async-task')
async def async_task():
    await asyncio.sleep(2)
    return {'message': 'async-task'}

@app.get('/api/v1/products/search')
async def search(
    q: str = Query(..., min_length=3, max_length=50),
    price_min: float = Query(..., gt=0),
    price_max: float | None = Query(None, gt=0),
    categories: list[str] | None = Query(None),
    x_client_version: str = Header(...),
    ):
    return {
            'q': q,
            'price_min': price_min,
            'price_max': price_max,
            'categories': categories,
            'x_client_version': x_client_version
            }
