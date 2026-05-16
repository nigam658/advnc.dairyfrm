from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cow_model import Cow, MilkRecord
from app.schemas.cow_schema import cowDataReq, Cow_updateSchema, get_single_cow_respons, MorningMilkRecordSchema, EveningMilkRecordSchema
from app.service.jwt_handler import get_current_user
from datetime import date 


router = APIRouter()


@router.post("/add_CowData")
def add_cow_data(cow: cowDataReq, current_user = Depends(get_current_user),  db : Session =Depends(get_db)):

    if current_user["role"] != "Admin":

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
@router.get("/cow/{cow_id}", response_model=get_single_cow_respons)
def get_single_cow(cow_id: str,db : Session =Depends(get_db)):


    cow = db.query(Cow).filter(
        Cow.cow_tag == cow_id
    ).first()

    if not cow:
        raise HTTPException(
            status_code=404,
            detail="Cow not found"
        )

    return cow

    

# update cow data using their tag
@router.put("/cow/{cow_id}")
def update_cow(cow_id: str, cow_data: Cow_updateSchema, current_user = Depends(get_current_user), db : Session =Depends(get_db)):

    if current_user["role"] != "Admin":

        raise HTTPException(
            status_code=403,
            detail="only Worker can add cow data"
        )



    cow = db.query(Cow).filter(
        Cow.cow_tag == cow_id
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
    

# Morning milk router  
@router.post("/cow/{cow_tag}/morning_milk")
def add_Morning_milk_record(cow_tag: str, milk: MorningMilkRecordSchema, db: Session = Depends(get_db)):
    
    if cow_tag != milk.cow_tag:
        raise HTTPException(
            status_code=400,
            detail="Cow tag mismatch"
    )

    cow = db.query(Cow).filter(
        Cow.cow_tag == cow_tag
    ).first()

    if not cow:
        raise HTTPException(
            status_code=404,
            detail="Cow not found"
        )
    
    milk_date = milk.date or date.today()

    existing_record = db.query(MilkRecord).filter( MilkRecord.cow_tag == cow_tag, MilkRecord.date == milk_date ).first()
    
    if existing_record: 
        raise HTTPException(
            status_code=400, 
            detail="Morning milk already added" 
        )
    
    new_record = MilkRecord(

        cow_tag=cow_tag,

        date=milk_date,

        morning_milk=milk.morning_milk,

        milk_perDay =milk.morning_milk
    )

    db.add(new_record)

    db.commit()

    db.refresh(new_record)

    return {
        "message": "Milk record added successfully"
    }


# Evening milk router
@router.post("/cow/{cow_tag}/evening_milk")
def evening_milk(cow_tag: str, milk: EveningMilkRecordSchema, db: Session = Depends(get_db)):

    # cow tag mismatch check
    if cow_tag != milk.cow_tag:

        raise HTTPException(
            status_code=400,
            detail="Cow tag mismatch"
        )

    # check cow exists
    exist_cow = db.query(Cow).filter(
        Cow.cow_tag == milk.cow_tag
    ).first()

    if not exist_cow:

        raise HTTPException(
            status_code=404,
            detail="Cow not found"
        ) 

    # automatic/manual date
    milk_date = milk.date or date.today()

    # check same day record exists or not
    existing_record = db.query(MilkRecord).filter(
        MilkRecord.cow_tag == milk.cow_tag,
        MilkRecord.date == milk_date
    ).first()


    # if row already exists
    if existing_record:

        # prevent duplicate evening entry
        if existing_record.evening_milk is not None:

            raise HTTPException(
                status_code=400,
                detail="Evening milk already added"
            )

        # update evening milk
        existing_record.evening_milk = milk.evening_milk

        # calculate total milk
        existing_record.milk_perDay = (
            existing_record.morning_milk
            +
            milk.evening_milk
        )

        db.commit()

        db.refresh(existing_record)

        return {
            "message": "Evening milk updated successfully",
            "data": existing_record
        }

    # if no row exists
    else:

        # create new row with evening milk only
        new_record = MilkRecord(

            cow_tag=milk.cow_tag,

            date=milk_date,

            morning_milk=0,

            evening_milk=milk.evening_milk,

            milk_perDay=milk.evening_milk
        )

        db.add(new_record)

        db.commit()

        db.refresh(new_record)

        return {
            "message": "Evening milk added successfully",
            "data": new_record
        }
    

@router.get("/cow/access_MilkRecord")
def access_MilkRecord(cow_tag: str, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    
    # Check role
    if current_user["role"] not in ["Manager", "Admin"]:
        raise HTTPException(
            status_code=403,
            detail="you cannot access milk record"
        )

    # Check cow exists
    cow_exist = db.query(Cow).filter(
        Cow.cow_tag == cow_tag
    ).first()

    if not cow_exist:
        print(cow_tag)
        raise HTTPException(
            status_code=404,
            detail="cow not exist"
        )

    # Get milk records
    cow_milk_record = db.query(MilkRecord).filter(
        MilkRecord.cow_tag == cow_tag
    ).all()

    if not cow_milk_record:
        raise HTTPException(
            status_code=404,
            detail="Milk record not filled"
        )

    return {
        "cow_tag": cow_tag,
        "data": cow_milk_record
    }