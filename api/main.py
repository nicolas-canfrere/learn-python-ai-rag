from typing import Dict

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

app = FastAPI()

class UserQuestion(BaseModel):
    question: str


@app.get("/")
def index():
    return {"message": "Welcome"}


@app.get(
    "/ping",
    response_class=PlainTextResponse
)
def ping() -> str:
    return "pong"


@app.post('/question')
def post_question(question: UserQuestion) -> Dict:
    return {"question": question.question}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=18080, reload=True)