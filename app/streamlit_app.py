import streamlit as st
import pandas as pd
from utils.openai_api import get_llm_response

# Optional: metrics if response exists
from eval.readability_metrics import flesch_score, coleman_liau_index, word_count
from eval.response_scoring import step_count

# --- App Config ---
st.set_page_config(page_title="Tutor LLM Evaluation Dashboard", layout="wide")
st.title("🧠 Interactive Tutor Evaluation Dashboard")
with st.expander("ℹ️ About this App"):
    st.markdown("""
    This interactive dashboard demonstrates how large language models (LLMs), such as GPT-3.5 and GPT-4o, respond to middle school–level math questions under different prompting strategies: zero-shot, few-shot, and chain-of-thought. 

    The tool is designed to support research and experimentation in educational AI, prompt engineering, and model evaluation. Users can explore how different prompts affect the structure, readability, and depth of responses generated by the models.

    Each response is automatically assessed using readability indices, word count, and reasoning step analysis to facilitate structured comparison. This app is intended for educators, edtech developers, and AI researchers interested in adapting foundation models for instructional use.
    """)

# --- Load Questions ---
@st.cache_data
def load_questions(csv_path):
    return pd.read_csv(csv_path)

question_df = load_questions("data/student_questions.csv")

# --- Sidebar Controls ---
st.sidebar.header("📚 Select a Question")
selected_question = st.sidebar.selectbox("Choose a question:", question_df["question_text"].tolist())

st.sidebar.header("🧠 Prompt Strategy")
prompt_strategy = st.sidebar.radio("Prompt Type", ["Zero-shot", "Few-shot", "Chain-of-thought"])

st.sidebar.header("🤖 Language Model")
selected_model = st.sidebar.radio("LLM Model", ["gpt-3.5-turbo", "gpt-4o"])

# --- Load Prompt Template ---
def load_prompt_template(strategy):
    path_map = {
        "Zero-shot": "prompts/zero_shot.txt",
        "Few-shot": "prompts/few_shot.txt",
        "Chain-of-thought": "prompts/cot.txt"
    }
    try:
        with open(path_map[strategy], "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Prompt template not found."

template = load_prompt_template(prompt_strategy)
final_prompt = template.format(question=selected_question)

# --- Display Prompt ---
st.markdown("### 📝 Prompt Sent to LLM")
with st.expander("ℹ️ What do these prompt strategies mean?"):
    st.markdown("""
    **🔹 Zero-shot Prompting**  
    The model is given only the user's question — no examples or context.  
    - **Purpose**: Measures the model’s baseline understanding  
    - **Example**:  
      *Q: What is the slope of the line y = 3x + 2?*

    **🔹 Few-shot Prompting**  
    The model is shown 2–4 examples of Q&A pairs before the target question.  
    - **Purpose**: Helps guide the model by establishing a pattern or style  
    - **Strength**: Improves accuracy, consistency, and formatting  
    - **Limitation**: Can bias the model toward specific answer structures

    **🔹 Chain-of-Thought (CoT) Prompting**  
    The prompt encourages the model to reason step-by-step before giving a final answer.  
    - **Purpose**: Promotes logical reasoning and intermediate thinking  
    - **Best for**: Multi-step math, logic, or explanation-heavy tasks  
    - **Example**:  
      *Step 1: Subtract 6 from both sides... Step 2: Divide both sides...*
    """)

st.code(final_prompt, language="text")

# --- Generate LLM Response ---
if st.button("💬 Generate Response"):
    with st.spinner("Contacting OpenAI..."):
        response_text = get_llm_response(final_prompt, model=selected_model)
        st.markdown("### 🤖 LLM Response")
        st.write(response_text)

        # Save to session for evaluation
        st.session_state["response_text"] = response_text

# --- Evaluation Metrics ---
if "response_text" in st.session_state:
    response = st.session_state["response_text"]
    st.markdown("### 📏 Evaluation Metrics")
    
    with st.expander("ℹ️ What do these metrics mean?"):
        st.markdown("""
    **🔹 Flesch Reading Ease Score**  
    This score rates text on a 100-point scale; higher scores indicate easier reading.  
    - **90–100**: Very easy (5th grade level)  
    - **60–70**: Standard (8th–9th grade)  
    - **0–30**: Very difficult (college level and beyond)  
    This metric is useful for judging how accessible the response is to students.

    **🔹 Coleman-Liau Index**  
    This index estimates the U.S. school grade level required to understand the text.  
    - **6–8**: Ideal for middle school students  
    - **9–10**: High school  
    - **12+**: College-level  
    Lower values suggest better alignment with your target student audience.

    **🔹 Word Count**  
    A basic measure of response length.  
    - Too few words may indicate oversimplification  
    - Too many may overwhelm the reader

    **🔹 Step Count**  
    For chain-of-thought responses, this counts how many discrete steps or reasoning stages the model outputs.  
    - More steps often reflect more detailed reasoning  
    - Excessive steps may indicate unnecessary verbosity
    """)

    st.write(f"- **Readability (Flesch)**: {flesch_score(response):.2f}")
    st.write(f"- **Coleman-Liau Index**: {coleman_liau_index(response):.2f}")
    st.write(f"- **Word Count**: {word_count(response)}")
    if prompt_strategy == "Chain-of-thought": 
        steps = step_count(response)
        st.write(f"- **Step Count**: {steps}") 
    else:
        st.write("- **Step Count**: N/A (not applicable for this prompt type)")
st.markdown("---")
st.caption("Built by Alex Wasdahl — explore how LLMs explain math.")
