# test.py — does the key work through our door?
from openai import OpenAI

client = OpenAI(
    api_key="AQ.Ab8RN6Lt2gA-BE9dI_2vbBQb-pcxshxBnA06dXiWJgrT-qOSXA",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

r = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[{"role": "user", "content": "Say hi in one word"}],
)
print(r.choices[0].message.content)
