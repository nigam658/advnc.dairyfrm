from app.ai.Geminiai_client import client
from google.genai.errors import ServerError

from app.service.ai_milk_service import highest_milk , lowest_milk, today_milkdata, total_milk_ofMonth, monthly_highest_milk_cow

month= {
    "january" : 1,
    "february" : 2,
    "march" : 3,
    "april" : 4,
    "may" : 5,
    "june" : 6,
    "july" : 7,
    "august" : 8,
    "september" : 9,
    "october" : 10,
    "november" : 11,
    "december" : 12
}


# detect Intention
def detect_intent(question):

    intent_prompt = f"""
    You are a dairy farm AI intent classifier.

    Possible intents:
    - highest_milk
    - lowest_milk
    - today_total_milk
    - monthly_total_milk
    - monthly_highest_milk_cow

    User question:
    {question}

    Rules:
    - Return ONLY intent name
    - No explanation
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=intent_prompt
    )

    return response.text.strip()


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

    intent = detect_intent(question)


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

        ai_response = ai_format_response(question,data)
        
        return {
            "answer" : ai_response
        }


    elif intent == "monthly_total_milk":
    # find month
        selected_month = None

        for month_name, month_number in month.items():

            if month_name in question:

                selected_month = month_number
                break
        # error handle if month in not in dict 
        if selected_month is None:
            return "Please specify month."
        
        # Finally we can function with proper data 
        data = total_milk_ofMonth(db,2026,selected_month)

        ai_response = ai_format_response(question,data)
        
        return {
            "answer" : ai_response
        }
    

    elif intent == "monthly_highest_milk_cow":
        # find month
        selected_month = None

        for month_name, month_number in month.items():

            if month_name in question:

                selected_month = month_number
                break
        # error handle if month in not in dict 
        if selected_month is None:
            return "Please specify month."
        
        data = monthly_highest_milk_cow(db,2026, selected_month)

        ai_response = ai_format_response(question,data)
        
        return {
            "answer" : ai_response
        } 
    
    else:
        return "intent not found"

