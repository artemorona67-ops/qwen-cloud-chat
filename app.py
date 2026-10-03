from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import httpx


app = FastAPI()


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "deepseek-r1:14b"


class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>DeepSeek Chat</title>
<style>
body {
    background:#111827;
    color:white;
    font-family:Arial;
    max-width:900px;
    margin:40px auto;
}
textarea {
    width:100%;
    height:100px;
}
button {
    padding:10px 20px;
}
#answer {
    margin-top:20px;
    background:#1f2937;
    padding:20px;
    border-radius:10px;
    white-space:pre-wrap;
}
</style>
</head>

<body>

<h1>DeepSeek</h1>

<textarea id="msg"></textarea>
<br><br>
<button onclick="send()">Отправить</button>

<div id="answer"></div>


<script>

async function send(){

let text=document.getElementById("msg").value;

let box=document.getElementById("answer");

box.innerHTML="Думаю...";

let r=await fetch("/chat",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
message:text
})
});


let data=await r.json();

box.innerHTML=data.answer;

}

</script>

</body>
</html>
"""


@app.get("/health")
def health():
    return {
        "status":"ok",
        "model":MODEL
    }


@app.post("/chat")
async def chat(request: ChatRequest):

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role":"user",
                "content":request.message
            }
        ],
        "stream": False
    }


    async with httpx.AsyncClient(timeout=600) as client:

        response = await client.post(
            OLLAMA_URL,
            json=payload
        )


    result = response.json()


    return {
        "answer": result["message"]["content"]
    }
