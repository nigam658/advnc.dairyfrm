from app.ai.Geminiai_client import client
from google.genai.errors import ServerError
import json
from datetime import datetime

from app.service.ai_milk_service import highest_milk , lowest_milk, today_milkdata, total_milk_ofMonth, monthly_highest_milk_cow, daily_total_milk_record


# detect Intention
def detect_intent(question):
    today = datetime.today()

    intent_prompt = f"""
    You are a dairy farm AI intent classifier.

    Possible intents:
    - highest_milk
    - lowest_milk
    - today_total_milk
    - monthly_total_milk
    - monthly_highest_milk_cow
    - daily_total_milk_record

    User question:
    {question}

    Current date: {today.date()}
    Current month: {today.month}
    Current year: {today.year}
    

    Rules:
    - Return ONLY valid json
    - No explanation
    - If user says "this month", use current month and current year

    Example outputs:

    {{
        "intent": "highest_milk"
    }}

    {{
        "intent": "daily_total_milk_record",
        "day" : 1,
        "month": 4,
        "year": 2026
    }}

    {{
        "intent": "monthly_total_milk",
        "month": 4,
        "year": 2026
    }}

    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=intent_prompt
    )

    return json.loads(response.text.strip())


# Answer with AI response 
def ai_format_response(question, raw_answer):
    final_prompt = f"""
    Your are a Dairy Farm Assistant.

    user_question : {question}

    result : {raw_answer}

    rules: 
    - Keep your answer with sort and friendly tone 
    - answer should be human readable
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=final_prompt
    )

    return response.text.strip()

# cretae response to user as follow question
def generate_response(prompt, db):
    
    question = prompt.lower()

    #data comes with json format
    intent_data = detect_intent(question)

    #store only intent 
    intent = intent_data["intent"]

    # Access month if comes with json 
    month = intent_data.get("month")

    # Assign year if comes with json
    year = intent_data.get("year")

    # Assign date if comes with json
    day = intent_data.get("day")

    # check intent
    if intent == "highest_milk":
        data = highest_milk(db)
        ai_response = ai_format_response(question,data)
        
        return {
            "answer" : ai_response
        }
    

    elif intent == "lowest_milk":
        data = lowest_milk(db)

        ai_response = ai_format_response(question,data)
        
        return {
            "answer" : ai_response
        }
    

    elif intent == "today_total_milk":
        data = today_milkdata(db)

        ai_response = ai_format_response(question,data,)
        
        return {
            "answer" : ai_response
        }


    elif intent == "monthly_total_milk":
    
        # error handle if month in not in json
        if month is None:
            return {
                "answer": "Please specify month."
            }
        # check year is exist or not
        if year is None:
            return {
                "answer": "Please specify year."
            }
        
        # Finally we can function with proper data 
        data = total_milk_ofMonth(db, year, month)

        ai_response = ai_format_response(question,data)
        
        return {
            "answer" : ai_response
        }
    

    elif intent == "monthly_highest_milk_cow":
        
        # error handle if month in not in json
        if month is None:
            return {
                "answer":"Please specify month."
            }
        # check year is exist or not 
        if year is None:
            return {
                "answer": "Please specify year."
            }
        
        data = monthly_highest_milk_cow(db, year, month)

        ai_response = ai_format_response(question,data)
        
        return {
            "answer" : ai_response
        } 
        
    elif intent == "daily_total_milk_record":

        # error handle if month in not in json
        if month is None:
            return {
                "answer":"Please specify month."
            }
        # check year is exist or not 
        if year is None:
            return {
                "answer": "Please specify year."
            }
        
        if day is None :
            return {
                "answer" : "Please specify day."
            }

        data = daily_total_milk_record(db,year,month,day)

        ai_response = ai_format_response(question,data)

        return {
            "answer" : ai_response
        }

    else:
        return {
            "answer": "Sorry, I could not understand your request."
        }

