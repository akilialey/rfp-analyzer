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

# send a message to Claude and wait for the reply
message = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=1500,
    messages=[{"role": "user", "content": "summarize in 3 bullets what is being procured, and list every date mentioned. Here is the first part of the RFP:\n\n " + first_part}],
)

# go through each block in the reply
for block in message.content:
    # only print the blocks that are actual text, skipping the thinking
    if block.type == "text":
        print(block.text)