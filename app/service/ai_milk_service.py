from sqlalchemy import func
from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import date
import calendar

from app.models.milk_model import MilkRecord


def highest_milk(db: Session ):
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


def lowest_milk(db: Session ):
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
    

def today_milkdata(db:Session):
    today = date.today()
    try:
        todaymilk = db.query(func.sum(
            MilkRecord.milk_perDay)).filter(
            MilkRecord.date == today).scalar()
        

        return{
            "todaymilk" : todaymilk
        }
    
    except Exception as e:
        return {
            "error" : str(e)
        }
    

#This month total milk
def total_milk_ofMonth(db:Session, year, month):

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
            "total_milk" : total
        }
    
    except Exception as e:
        return{
            "Error" : str(e)
        }

def monthly_highest_milk_cow(db:Session, year, month):
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
            "total_milk" : round(highest_milk_produce_cow.total_milk,2)
        }
    
    except Exception as e:
        return{
            "error" : str(e)
        }

