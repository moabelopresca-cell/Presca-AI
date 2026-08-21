import streamlit as st
import google.generativeai as genai

# Configure your Gemini API key securely
# For local testing, replace with: genai.configure(api_key="YOUR_API_KEY")
# For deployment, use Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.sidebar.warning("⚠️ API Key missing. Please configure GEMINI_API_KEY in your settings.")

# Initialize the Gemini Pro Model
model = genai.GenerativeModel('gemini-pro')

def generate_ai_response(prompt, system_instruction=""):
    """Helper function to send structured prompts to Gemini."""
    try:
        full_prompt = f"{system_instruction}\n\nUser Request:\n{prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"

# --- UI Layout ---
st.set_page_config(page_title="Presca-AI", page_icon="💼", layout="wide")

st.title("💼 Presca-AI Workspace Assistant")
st.subheader("Automating workplace productivity with smart prompt engineering")

# Sidebar navigation
option = st.sidebar.radio(
    "Choose a Task Tool:",
    ["Email Generation", "Meeting Summarization", "Task Planning", "Research Assistance"]
)

# --- Tool 1: Email Generation ---
if option == "Email Generation":
    st.header("✉️ Professional Email Generator")
    points = st.text_area("Enter bullet points or key details for the email:", placeholder="Request a extension on the project deadline until Monday because our server went down.")
    tone = st.selectbox("Select email tone:", ["Professional", "Casual", "Urgent", "Polite"])
    
    if st.button("Generate Email"):
        if points:
            system_msg = f"You are an expert corporate communications assistant. Write a clear, well-structured email with a subject line based on the user notes. Tone: {tone}."
            with st.spinner("Drafting..."):
                result = generate_ai_response(points, system_msg)
            st.markdown("### Drafted Email:")
            st.code(result, language="text")
        else:
            st.error("Please enter some details first.")

# --- Tool 2: Meeting Summarization ---
elif option == "Meeting Summarization":
    st.header("📝 Meeting Summarizer")
    transcript = st.text_area("Paste meeting transcript text here:", height=200, placeholder="John: We need to finish the login UI by Tuesday. Sarah: I will look into the API bugs...")
    
    if st.button("Summarize Transcript"):
        if transcript:
            system_msg = "You are a professional secretary. Analyze the transcript and output: 1) Executive Summary, 2) Key Decisions Made, and 3) Bulleted Action Items with owners."
            with st.spinner("Analyzing transcript..."):
                result = generate_ai_response(transcript, system_msg)
            st.markdown("### Meeting Minutes:")
            st.write(result)
        else:
            st.error("Please paste a transcript first.")

# --- Tool 3: Task Planning ---
elif option == "Task Planning":
    st.header("📅 Project Task Planner")
    goal = st.text_input("What project or goal are you planning?", placeholder="Launch a marketing campaign for a new mobile app")
    
    if st.button("Create Action Plan"):
        if goal:
            system_msg = "You are a senior project manager. Break down the user's goal into a chronological checklist of actionable phases. Include realistic micro-deadlines."
            with st.spinner("Planning milestones..."):
                result = generate_ai_response(goal, system_msg)
            st.markdown("### Step-by-Step Checklist:")
            st.write(result)
        else:
            st.error("Please enter a project goal.")

# --- Tool 4: Research Assistance ---
elif option == "Research Assistance":
    st.header("🔍 Research Assistant")
    topic = st.text_input("Enter a technical topic or concept to research:", placeholder="What are the differences between REST and GraphQL APIs?")
    
    if st.button("Synthesize Research"):
        if topic:
            system_msg = "You are an advanced researcher. Provide a comprehensive, easy-to-read summary of the topic with brief definitions, core comparisons, and use cases."
            with st.spinner("Synthesizing data..."):
                result = generate_ai_response(topic, system_msg)
            st.markdown("### Research Briefing:")
            st.write(result)
        else:
            st.error("Please provide a topic.")
