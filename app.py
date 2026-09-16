import streamlit as st 
import os 
from dotenv import load_dotenv 
from groq import Groq 

#load Environment
load_dotenv()

#client is a  delivery boy 
client=Groq(api_key=os.environ.get("GROQ_API_KEY")) 

financial_database = {
    "Q1": "Q1 Marketing Spend: $50,000. New Customers Acquired: 1,000. Average Customer Lifespan: 24 months. Monthly Revenue per User: $50.",
    "Q2": "Q2 Marketing Spend: $75,000. New Customers Acquired: 1,200. Average Customer Lifespan: 22 months. Monthly Revenue per User: $55."
}
def search_query(query):

    if "Q1" in query.upper() :
        return financial_database["Q1"]

    if "Q2" in query.upper():
        return financial_database["Q2"]

    return "No internal financial data found."
st.title("Autonomous Finance Analyst - CAC/LTV Engine")
# session_state is dictionary
if "messages" not in st.session_state:
    st.session_state["messages"]=[{"role":"system","content":"You are an elite, senior-level Finance Analyst specializing in unit economics, specifically Customer Acquisition Cost (CAC) and Customer Lifetime Value (LTV)."}]

#chat display and memory appending
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

user_query=st.chat_input("Ask Finance Question")

if user_query:
    retrieved_data=search_query(user_query)
    augmented_prompt = f"User Question: {user_query}\n\nInternal Data: {retrieved_data}"
    st.session_state["messages"].append({"role":"user","content":augmented_prompt})

    st.chat_message("user").write(user_query)
    chat_completion = client.chat.completions.create(
    messages=st.session_state["messages"],
    model="openai/gpt-oss-120b",
    )
    bot_reply = chat_completion.choices[0].message.content
    #memory storing for ai side
    st.session_state["messages"].append({"role":"assistant","content":bot_reply})
    #message display
    st.chat_message("assistant").write(bot_reply) 


    


