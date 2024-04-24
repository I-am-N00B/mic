import uvicorn
from fastapi import FastAPI, HTTPException, status
import requests

app = FastAPI()

API_KEY = "3aa54599-5eba-4986-b646-ce5b1c3c7947"


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/search_art")
async def search_art(query: str):
    url = f"https://api.harvardartmuseums.org/object"
    params = {
        "apikey": API_KEY,
        "title": query,
        "size": 10
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail="Error retrieving data from Harvard Art Museums API")


@app.get("/get_art_by_id")
async def get_art_by_id(object_id: int):
    url = f"https://api.harvardartmuseums.org/object/{object_id}"
    params = {
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=404, detail="Art object not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
