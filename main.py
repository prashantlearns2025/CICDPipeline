from fastapi import FastAPI
from openai import OpenAI
import config
import uvicorn
import os
from pydantic import BaseModel


assistant_id = config.assistant_id
api_key = os.environ['OPENAI_API']    # config.api_key
client = OpenAI(api_key=api_key)


app = FastAPI()

class Body(BaseModel):
    text: str

@app.get("/")
def welcome():
    return {"message": "Welcome to ChatGPT AI App V2"}

@app.post("/response")
def generate(body: Body):

    prompt =  body.text
    thread = client.beta.threads.create()
    messages = client.beta.threads.messages.create(
        thread_id = thread.id,  
        role = "user",
        content = prompt
    )

    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
    )

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            latest_message = messages.data[0].content[0].text.value
            break;

    return latest_message


if __name__ == "__main__":
    uvicorn.run(app,host = "0.0.0.0",port=80)