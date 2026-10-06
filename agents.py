from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.3)

planner_prompt = ChatPromptTemplate.from_messages([
    ("system", "You break a claim into 2-4 smaller sub-claims that can each be checked separately."),
    ("human", "Claim: {claim}\n\nList the sub-claims, one per line, no extra text.")
])
planner_chain = planner_prompt | llm | StrOutputParser()

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a careful fact-checker. Use only the evidence given. Never guess."),
    ("human", """Claim: {claim}

Evidence gathered:
{evidence}

Write a fact-check report structured as:
-Verdict (True / False / Misleading / Unverifiable)
-Reasoning (explain using the evidence)
-Sources (list all urls found in evidence)
""")
])
writer_chain = writer_prompt | llm | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a strict reviewer. Check if the verdict is truly supported by the evidence."),
    ("human", """Evidence:
{evidence}

Report:
{report}

Respond in this exact format:
Score:x/10
Issues:
- ...
Verdict-is-supported: yes/no
""")
])
critic_chain = critic_prompt | llm | StrOutputParser()

reviser_prompt = ChatPromptTemplate.from_messages([
    ("system", "You improve fact-check reports based on critic feedback. Keep the same structure."),
    ("human", """Original report:
{report}

Critic feedback:
{feedback}

Evidence:
{evidence}

Write the improved report, same structure as before.""")
])
reviser_chain = reviser_prompt | llm | StrOutputParser()