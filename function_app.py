import azure.functions as func
import openai
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="chatbot")
def chatbot(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Read raw text from request body
        user_input = req.get_body().decode("utf-8").strip()

        # Define AI prompt
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_input},
        ]

        # Call OpenAI API
        response = client.chat.completions.create(
            messages=messages,
            max_completion_tokens=500,
            temperature=0.7,
            top_p=1.0,
            model=os.getenv("AZURE_DEPLOYMENT_NAME"),
        )

        ai_response = response.choices[0].message.content.strip()

    except Exception as e:
        ai_response = json.dumps({"error": f"An error occurred: {str(e)}"})

    return func.HttpResponse(
        json.dumps({"response": ai_response}),
        mimetype="application/json"
    )