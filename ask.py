# The plan:
# Send Claude the whole RFP, not just page 1.
# Design the output shape: deadlines, mandatory requirements, evaluation criteria, risks, and a go/no-go.
# Write the prompt that asks for that shape.
# Run it and check the output against the RFP by hand.

import os
from dotenv import load_dotenv
from anthropic import Anthropic
from streamlit import json
from reader import get_pdf_text
from convert import convert_json_to_list

# read the .env file so the API key is available
load_dotenv()

# create the connection to Claude (it finds your key automatically)
client = Anthropic()

# get the RFP text
text = get_pdf_text("rfps/rfp.pdf")

# Design the output shape: deadlines, mandatory requirements, evaluation criteria, risks, and a go/no-go.
instructions = """
You are analyzing a Request for Proposal (RFP) for a company deciding whether to bid.

Return ONLY JSON in exactly this shape, with no other words before or after:
{
  "deadlines": [
    {"event": "Site visit", "date": "March 1, 2030", "quote": "exact words from the RFP"}
  ],
  "requirements": [
    {"requirement": "Vendor must provide 24/7 support", "section": "4.3 Scope of Work", "quote": "exact words from the RFP"}
  ],
  "evaluation_criteria": [
    {"criterion": "Technical approach", "weight": "40%", "quote": "exact words from the RFP"}
  ],
  "risks": [
    {"issue": "Unlimited liability clause", "severity": "high", "why": "Exposes the vendor to uncapped losses", "quote": "exact words from the RFP"}
  ],
  "go_no_go": {
    "recommendation": "go",
    "reasoning": "Two or three sentences explaining why"
  }
}

Rules:
- Only include mandatory requirements (words like "must", "shall", "required").
- Every "quote" must be copied word for word from the RFP, never reworded.
- Keep event names and requirement names short, under 12 words.
- severity must be "high", "medium" or "low".
- recommendation must be "go" or "no-go".
- If a section has nothing in the RFP, return an empty list for it.

Here is the RFP:
"""

# glue the instructions and the RFP text together
prompt = instructions + text

# send a message to Claude and wait for the reply
message = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=16000,
    messages=[{"role": "user", "content": prompt}]
)   

# go through each block in the reply
for block in message.content:
    # only print the blocks that are actual text, skipping the thinking
    if block.type == "text":
        print(block.text)

# print the stop reason and the types of blocks in the reply
print(message.stop_reason)
print([block.type for block in message.content])

# find the text block and store its words in a box
reply_text = ""
for block in message.content:
    if block.type == "text":
        reply_text = block.text

# convert the reply into a Python dictionary
result = convert_json_to_list(reply_text)

# stop here if the conversion failed
if not result:
    print("Could not read Claude's reply. Try running again.")
    raise SystemExit

print("DEADLINES")
for item in result["deadlines"]:
    print(f"{item['event']} - {item['date']}")

print()
print("REQUIREMENTS")
for item in result["requirements"]:
    print(f"{item['requirement']} - {item['section']}")

print()
print("EVALUATION CRITERIA")
for item in result["evaluation_criteria"]:
    print(f"{item['criterion']} - {item['weight']}")

print()
print("RISKS")
for item in result["risks"]:
    print(f"[{item['severity']}] {item['issue']}: {item['why']}")

print()
print("GO / NO-GO")
print(result["go_no_go"]["recommendation"])
print(result["go_no_go"]["reasoning"])