from google.genai.errors import ServerError
from app.ai.Geminiai_client import client
import json
import httpx
from datetime import datetime

from app.service.ai_milk_service import (
    highest_milk_cow ,
    lowest_milk_cow, 
    monthly_total_milk, 
    monthly_highest_milk_cow, 
    daily_total_milk_record
    )


today = datetime.today()
TOOLS = [
    {
        "function_declarations" : [
            {
                "name" : "highest_milk_production",

                "description" : """
                Get the cow that produced the highest amount of milk of all time.

                Examples : 
                - highest milk
                - highest milk produced cow 
                - which cow give most of the milk
                - Top milk cow
                - Which cow gave maximum milk?
                - Best milk producer
                - Cow with highest milk
                - Highest yielding cow
                - Most productive cow
                - Which cow gave the most liters
                """
            },
            
            # lowest produce cow
            {
                "name" : "lowest_milk_production",

                "description" : """
                Get the cow that produced the lowest amount of milk of all time.
                
                Examples :
                - lowest milk cow
                - which cow gives least milk
                - least milk production
                - cow with minimum milk
                - lowest milk produced cow
                - which cow produced the least milk
                - worst milk producer
                - lowest yielding cow
                - minimum milk cow
                - cow giving less milk
                - which cow gave the fewest liters
                - least productive cow
                """
            },
            
            # total milk of a month
            {
                "name" : "total_milk_of_month",

                "description" : """
                Get total milk production for a month.

                Examples:
                - this month milk
                - april total milk
                - monthly milk production
                - total milk of this month
                - may milk report
                - total milk in june
                - how much milk produced this month
                - milk production for may 2026
                - monthly milk summary
                - total liters this month
                - april 2025 milk production
                - show monthly milk record
                - milk report of current month
                - total milk for january
                - monthly dairy production
                """,   

                "parameters" : {
                    "type" : "object",

                    "properties" : {
                        "month" : {
                            "type" : "integer",
                            "description": "Month number"

                        },

                        "year" :{ 
                            "type" : "integer",
                            "description" : "Year number"
                        } 
                    },

                    "required" : ["month", "year"] 
                }
            },

            # cows monthly highest milk producer cow
            {
                "name" : "monthly_highest_milk_given_cow",

                "description" : """
                Find the highest milk producing cow for a specific month.

                Examples:
                - highest milk cow this month
                - top producer cow in april
                - best milk cow monthly
                - monthly highest milk cow
                - which cow gave highest milk in may
                - top milk producer in 2026
                - highest producer cow for this month
                - april top milk cow
                - cow with maximum milk this month
                - who produced most milk this month
                - highest milk giving cow in june
                - best dairy cow for may 2026
                - top milk cow monthly report
                - maximum milk producer this month
                - monthly top producer cow
                """,

                "parameters" : {
                    "type" : "object",

                    "properties" : {
                        "month" : {
                            "type" : "integer",
                            "description" : "month number "
                        },

                        "year" : {
                            "type" : "integer",
                            "description" : "year number"
                        }
                    },

                    "required" : ["month","year"]
                }
            },

            # specific day cow total milk
            {
                "name" : "daily_total_milk_record",
                
                "description" : """
                Get total milk production for a specific day.

                If date is not provided,
                use today's date.

                Examples:
                - today total milk
                - milk produced today
                - daily milk report
                - total milk on may 5
                - milk production for april 10
                - this day milk record
                - today's milk production
                - how much milk produced today
                - total liters today
                - milk report for june 2
                - show today milk record
                - give daily milk report
                - today milk summary
                - total milk for one day
                """,

                "parameters" : {
                    "type" : "object",

                    "properties" : {
                        "day": {
                            "type": "integer",
                            "description": "Day number"
                        },

                        "month": {
                            "type": "integer",
                            "description": "Month number"
                        },

                        "year": {
                            "type": "integer",
                            "description": "Year number"
                        }
                    }
                }
            }
        ]
    }
]



function_map = {
    "highest_milk_production" : highest_milk_cow,
    "lowest_milk_production" : lowest_milk_cow,
    "total_milk_of_month" : monthly_total_milk,
    "monthly_highest_milk_given_cow" : monthly_highest_milk_cow,
    "daily_total_milk_record" : daily_total_milk_record
}



def generate_human_response(question, result):

    try:

        response = client.models.generate_content(

            model="gemini-3.1-flash-lite",

            contents=f"""
            You are an intelligent dairy farm AI assistant.

            Your job is to convert backend database results
            into professional and human-friendly responses.

            RULES:

            - Keep responses short and clear
            - Sound natural and conversational
            - Never mention database, JSON, SQL, or backend
            - Use dairy/business language
            - Mention liters when milk data exists
            - If no records are found, respond politely
            - Do not generate fake information
            - Use simple professional English

            USER QUESTION:
            {question}
            BACKEND RESULT:
            {result}

            Generate the final user-friendly response.

            """
        )

        return response.text
    
    except httpx.ReadTimeout:

        return "The AI service is taking too long to respond. Please try again."
    
    except ServerError :
        return "Gemini server is temporarily unavailable."

    except Exception as e:
        return f"Error generating response: {str(e)}"


def generate_response(question, db):
    
    response = client.models.generate_content(

        model="gemini-3.1-flash-lite",
        contents=f"""

        Current Date: {today}

        User Question:
        {question}

        """,

        config={
            "tools" : TOOLS 
        }
    )

    tool_call = response.candidates[0].content.parts[0].function_call

    print(tool_call)

    # function name now contain intent fucntion
    function_name = tool_call.name

    args = {}

    if tool_call.args :
        args = dict(tool_call.args)

    selected_function = function_map[function_name]

    result = selected_function(db, **args)
    
    final_result = generate_human_response(question, result)
    print(result)
    print(final_result)

    return {
        "answer": final_result
    }