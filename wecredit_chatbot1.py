import streamlit as st
import openai
import os

# Streamlit App Title
st.title("WeCredit FinTech Chatbot 💬")
st.write("Ask me about loans, credit reports, interest rates, CIBIL scores, and more!")

# OpenAI API Key (Use Streamlit Secrets for Deployment)
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
elif os.getenv("OPENAI_API_KEY"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
    st.error("🚨 OpenAI API Key not found! Please add it to Streamlit secrets or set it as an environment variable.")

# User Input
user_input = st.text_input("You:", "Type your question here...")

# Knowledge Base Function
def knowledge_base_response(query):
    knowledge_base = {
        "loans": "Loans include Personal, Home, Auto, Education, and Business Loans. Eligibility depends on age (21–60), income stability, credit score, and employment status. Documents: ID proof, address proof, income proof, and bank statements.",
        "interest rates": "Interest rates can be fixed or floating. Simple Interest = (P * R * T) / 100. Factors: RBI rates, credit score, loan amount, and market trends.",
        "credit bureaus": "Major credit bureaus in India: CIBIL (TransUnion), Experian, Equifax, and CRIF High Mark. They track credit history, influencing loan approvals.",
        "credit reports": "Credit reports show personal info, credit accounts, payment history, inquiries, and public records. Access one free report annually from official bureaus.",
        "cibil score": "CIBIL Score ranges from 300–900; 750+ is good. It’s based on payment history (35%), credit utilization (30%), history length (15%), credit mix (10%), and new credit inquiries (10%)."
    }
    for key, value in knowledge_base.items():
        if key in query.lower():
            return value
    return None

# OpenAI LLM Response
def openai_response(user_query):
    prompt = f"""
    You are a helpful financial advisor chatbot for WeCredit.
    Answer the following query in detail about loans, interest rates, credit bureaus, credit reports, and CIBIL scores.

    User: {user_query}
    Bot:
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.5
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Handle User Query
if user_input:
    kb_response = knowledge_base_response(user_input)
    if kb_response:
        st.write(f"**WeCredit Bot:** {kb_response}")
    else:
        ai_response = openai_response(user_input)
        st.write(f"**WeCredit Bot:** {ai_response}")

# Footer
st.markdown("---")
st.markdown("Created for WeCredit by Amit Kumar Singh")
