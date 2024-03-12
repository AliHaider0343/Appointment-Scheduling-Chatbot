##################This code is for API##########

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatRequest,ChatResponse
from agent import generate_response

app = FastAPI(title="Appointment booking boot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.post('/process_data',response_model=ChatResponse)
async def process_data(request:ChatRequest):
    try:
        ans = generate_response(request.question)
        print('Answered.')
        return ChatResponse(answer=ans)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    





















# from agent import generate_response
# if __name__=="__main__":
#     for i in range(10):
        
#         print(generate_response(input("Enter you response here! : ")))