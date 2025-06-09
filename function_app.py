import azure.functions as func
import logging
import json  

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="assistant_chatbot")
def assistant_chatbot(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        user_input = req_body.get("text", "No input provided")
    except ValueError:  # Fix indentation issue
        user_input = "Invalid input"

    return func.HttpResponse(
        json.dumps({"response": user_input}),
        mimetype="application/json"  # Correct mimetype
    )