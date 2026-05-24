from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date
import calendar

from app.models.milk_model import MilkRecord


def highest_milk_cow(db: Session ):
    try:
        highestMilk = (db.query(
            MilkRecord.cow_tag,
            func.sum(MilkRecord.milk_perDay).label("total_milk"))
            .group_by(MilkRecord.cow_tag)
            .order_by(func.sum(MilkRecord.milk_perDay).desc())
            .first() 
            )

        return {"cow_tag" : highestMilk.cow_tag, 
                "milk" : round(highestMilk.total_milk,2)
                }
    
    except Exception as e:
        return {
            "error" : str(e)
        }


def lowest_milk_cow(db: Session ):
    try:
        lowestmilk = (db.query(
            MilkRecord.cow_tag,
            func.sum(MilkRecord.milk_perDay).label("total_milk"))
            .group_by(MilkRecord.cow_tag)
            .order_by(func.sum(MilkRecord.milk_perDay).asc())
            .first() 
            )

        return {"cow_tag" : lowestmilk.cow_tag, 
                "milk" : round(lowestmilk.total_milk,2)
                }
    
    except Exception as e:
        return{
            "error" : str(e)
        }
    
    

#This month total milk
def monthly_total_milk(db:Session, year=None, month=None):
    
    today = date.today()

    if year is None:
        year = today.year

    if month is None:
        month = today.month

    start_date = date(year, month, 1)
    last_date = calendar.monthrange(year,month)[1] 
    end_date = date(year, month, last_date)

    try:
        total = db.query(func.sum(
            MilkRecord.milk_perDay)).filter(
                MilkRecord.date.between(start_date,end_date)).scalar() 
        
        if total is None :
            total = 0 

        
        return {
            "total_milk" : total,
            "date" : start_date
        }
    
    except Exception as e:
        return{
            "Error" : str(e)
        }

def monthly_highest_milk_cow(db:Session, year=None, month=None):
    
    today = date.today()

    if year is None:
        year = today.year

    if month is None:
        month = today.month
    
    start_date = date(year, month, 1)
    last_date = calendar.monthrange(year,month)[1]
    end_date = date(year,month,last_date)
    try:
        highest_milk_produce_cow = db.query(
            MilkRecord.cow_tag,
            func.sum(MilkRecord.milk_perDay).label("total_milk")
            ).filter(
                MilkRecord.date.between(start_date,end_date)
                ).group_by(
                    MilkRecord.cow_tag
                    ).order_by(
                        func.sum(MilkRecord.milk_perDay).desc()).first()


        
        if not highest_milk_produce_cow :
            return{
                "Error" : "no cow record found"
            }
        
        return{
            "cow_tag" : highest_milk_produce_cow.cow_tag,
            "total_milk" : round(highest_milk_produce_cow.total_milk,2),
        }
    
    except Exception as e:
        return{
            "error" : str(e)
        }

def daily_total_milk_record(db:Session, year=None, month=None, day=None):

    today = date.today()


    if year is None:
        year = today.year

    if month is None:
        month = today.month

    if day is None:
        day = today.day

    try:
        exact_date = date(year, month, day)

        milk = db.query(
            func.sum(MilkRecord.milk_perDay)).filter(
                MilkRecord.date == exact_date).scalar()
        
        if milk is None:
            milk = 0
    
        return {
            "total_milk" : round(milk,2)
        }
    
    except Exception as e:
        return{
            "error" : str(e)
        }
