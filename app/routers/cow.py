from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cow_model import Cow
from app.models.milk_model import MilkRecord
from app.schemas.cow_schema import cowDataReq, Cow_updateSchema, get_single_cow_respons
from app.service.jwt_handler import get_current_user
from datetime import date 


router = APIRouter()


@router.post("/add_CowData")
def add_cow_data(cow: cowDataReq, current_user = Depends(get_current_user),  db : Session =Depends(get_db)):

    if current_user["role"] not in ["Manager", "Admin"]:

        raise HTTPException(
            status_code=403,
            detail="only Manager can add cow data"
        )

    Existing_cow = db.query(Cow).filter(
        Cow.cow_tag == cow.cow_tag
    ).first()

    if Existing_cow:
        raise HTTPException(
            status_code=404,
            detail="Cow already Exist"
        )
    
    new_cow = Cow(
        cow_tag=cow.cow_tag,
        breed=cow.breed,
        age=cow.age,
        milk_per_day=cow.milk_per_day
    )

    db.add(new_cow)
    db.commit()

    return {
        "message": "cow data add successful"
    }


# Get cow cow details
@router.get("/cow", response_model=get_single_cow_respons)
def get_single_cow(cow_tag: str,db : Session =Depends(get_db)):


    cow = db.query(Cow).filter(
        Cow.cow_tag == cow_tag
    ).first()

    if not cow:
        raise HTTPException(
            status_code=404,
            detail="Cow not found!"
        )

    return cow

    

# update cow data using their tag
@router.put("/cow/{cow_tag}")
def update_cow(cow_tag: str, cow_data: Cow_updateSchema, current_user = Depends(get_current_user), db : Session =Depends(get_db)):

    if cow_tag != cow_data.cow_tag:
        raise HTTPException(
            status_code=400,
            detail="cow tag missmatch"
        )

    if current_user["role"] != "Admin":

        raise HTTPException(
            status_code=403,
            detail="only Worker can add cow data"
        )


    cow = db.query(Cow).filter(
        Cow.cow_tag == cow_tag
    ).first()

    if not cow:
        raise HTTPException(
            status_code=404,
            detail="Cow not found"
        )

    cow.cow_tag = cow_data.cow_tag
    cow.breed = cow_data.breed
    cow.age = cow_data.age
    cow.milk_per_day = cow_data.milk_per_day

    db.commit()

    db.refresh(cow)

    return {
        "message" : "cow update sucessfully",
        "update_data" : cow 
    }


# delete a cow 
@router.delete("/delete_cow")
def delete_cow(cow_tag : str, current_user = Depends(get_current_user),db : Session =Depends(get_db)):

    if current_user["role"] != "Admin":

        raise HTTPException(
            status_code=403,
            detail="only Admin and can add cow data"
        )
     
    db.query(MilkRecord).filter( MilkRecord.cow_tag == cow_tag ).delete()
    
    del_cow = db.query(Cow).filter(Cow.cow_tag == cow_tag).first()

    if not del_cow :
        raise HTTPException(
            status_code=404,
            detail="cow not found"
        )

    db.delete(del_cow)

    db.commit()

    return {
        "message" : "cow delete sucessfully"
    }