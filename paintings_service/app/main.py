import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from sqlalchemy.orm import Session
from database import database as database
from database.database import PaintingDB
from model.painting import Painting

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.post("/add_painting")
async def add_painting(painting: Painting, db: db_dependency):
    new_painting = PaintingDB(**painting.dict())
    db.add(new_painting)
    db.commit()
    db.refresh(new_painting)
    return new_painting


@app.get("/get_paintings")
async def get_paintings(db: db_dependency):
    return db.query(PaintingDB).all()


@app.get("/get_painting_by_id")
async def get_painting_by_id(painting_id: int, db: db_dependency):
    painting = db.query(PaintingDB).filter(PaintingDB.id == painting_id).first()
    if not painting:
        raise HTTPException(status_code=404, detail="Painting not found")
    return painting


@app.put("/update_painting")
async def update_painting(painting_id: int, painting: Painting, db: db_dependency):
    db_painting = db.query(PaintingDB).filter(PaintingDB.id == painting_id).first()
    if not db_painting:
        raise HTTPException(status_code=404, detail="Painting not found")
    for var, value in painting.dict(exclude_unset=True).items():
        setattr(db_painting, var, value)

    db.commit()
    db.refresh(db_painting)  # Обновляем объект после коммита

    try:
        result = jsonable_encoder(db_painting)
        return result
    except Exception as e:
        print(f"Error serializing the response: {e}")
        raise HTTPException(status_code=500, detail="Serialization error")


@app.delete("/delete_painting")
async def delete_painting(painting_id: int, db: db_dependency):
    db_painting = db.query(PaintingDB).filter(PaintingDB.id == painting_id).first()
    if not db_painting:
        raise HTTPException(status_code=404, detail="Painting not found")
    db.delete(db_painting)
    db.commit()
    return {"message": "Painting deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
