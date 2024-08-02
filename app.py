import random
import time
import json
import mesop as me
import mesop.labs as mel
from agent import agent

def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")

def stream_text(response, chunk_size=10, delay=0.1):
    for i in range(0, len(response), chunk_size):
        chunk = response[i:i+chunk_size]
        time.sleep(delay)
        yield chunk

@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io", "https://huggingface.co"]
  ),
  path="/",
  title="Context aware LLM",
  on_load=on_load,
)
def page():
  mel.chat(transform, title="Context aware LLM", bot_user="Incle Bot")

def transform(input: str, history: list[mel.ChatMessage]):
  transformed_history = [{"role": message.role, "content": message.content} for message in history]
  transformed_history.pop()
  print(transformed_history)
  x = agent(input,transformed_history ,"gokul", 11.7910866,77.778496)
  selected_line = x["completion"]
  words = selected_line.split()
  for word in words:
      time.sleep(0.05)
      yield word + " "
