from app.functions import gpt_send_message

message = gpt_send_message(prompt="hello", model="gpt-4o-mini")
print(message)