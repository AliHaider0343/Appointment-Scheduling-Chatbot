import chainlit as cl
from agent import generate_response,extract_data,chat_history

from langchain import OpenAI, LLMMathChain
import chainlit as cl

@cl.on_chat_start
async def start():
    await cl.Message(content="""Hi there! 📅 Welcome to XYZ Appointment Booking! 💼✨ We're here to make scheduling your appointments a breeze. What can we help you with today?""", author="AppointmentBot").send()





@cl.on_message
async def main(message: cl.Message):
  # Your custom logic goes here...

  res = generate_response(message.content)
  # Send a response back to the user
  if message.content.lower() == "confirm":
    print("confirm is called")
    user_data=extract_data(chat_history=chat_history)
  await cl.Message(res, author="AppointmentBot").send()


