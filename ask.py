# load libraries

from dotenv import load_dotenv
from anthropic import Anthropic
from reader import get_pdf_text

# read the .env file so the API key is available
load_dotenv()

# create the connection to Claude (it finds your key automatically)
client = Anthropic()

# get the RFP text, then keep only the first 6000 characters to keep it cheap
text = get_pdf_text("rfps/rfp.pdf")

first_part = text[:6000]

# the instruction and the example format, written across several lines
instructions = """
Extract every key deadline from the RFP (issue date, questions deadline, closing date, etc). Add ALL relevant dates.
Return ONLY JSON in this exact shape, with no other words:
[
  {"event": "RFP issued", "date": "March 2, 2030"},
  {"event": "Closing date", "date": "April 23, 2030"}
]

Here is the first part of the RFP:
"""

# glue the instructions and the RFP text together
prompt = instructions + first_part

# send a message to Claude and wait for the reply
message = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=1500,
    messages=[{"role": "user", "content": prompt}]
)

# go through each block in the reply
for block in message.content:
    # only print the blocks that are actual text, skipping the thinking
    if block.type == "text":
        print(block.text)

print(message.stop_reason)
print([block.type for block in message.content])