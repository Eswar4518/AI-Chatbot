import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Custom CSS for enhanced styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f8ff; /* Light blue background */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .chat-container {
        max-width: 800px;
        margin: 20px auto;
        background: linear-gradient(135deg, #e0f7fa, #c2e5ff); /* Gradient background */
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    .chat-message {
        padding: 15px 20px;
        border-radius: 25px;
        margin-bottom: 15px;
        font-size: 16px;
        line-height: 1.6;
        transition: transform 0.3s ease-in-out;
    }
    .chat-message:hover {
        transform: translateY(-3px);
    }
    .user-message {
        background-color: #e8f5e9; /* Light green for user messages */
        color: #2e7d32; /* Dark green text */
        text-align: right;
        border: 1px solid #a5d6a7;
    }
    .assistant-message {
        background-color: #f8f8f8; /* Light gray for assistant messages */
        color: #333;
        text-align: left;
        border: 1px solid #eee;
    }
    .chat-input {
        width: 100%;
        padding: 15px 20px;
        border-radius: 30px;
        border: 2px solid #4fc3f7; /* Light blue border */
        font-size: 16px;
        margin-top: 20px;
        transition: border-color 0.3s ease;
    }
    .chat-input:focus {
        border-color: #1e88e5; /* Darker blue on focus */
        outline: none;
    }
    .stSpinner > div > div > div {
        border-top-color: #4fc3f7; /* Spinner color */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Gemini API client
genai.configure(api_key="AIzaSyCLD65tgojROlLqROqjBhNDJhIQA6NDUzs")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hello! I'm your friendly AI assistant. How can I brighten your day?",
        }
    ]

# Sidebar for additional controls
st.sidebar.title("⚙️ Chatbot Settings")
model_choice = st.sidebar.selectbox(
    "Choose AI Model",
    ["gemini-2.5-pro-exp-03-25", "gemini-2.0-flash", "gemini-1.5-flash"],
)


# Function to get AI response
def get_ai_response(user_message, model):
    try:
        generation_model = genai.GenerativeModel(model)
        chat_history = [
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in st.session_state.messages
        ]
        full_context = "\n".join(chat_history + [f"User: {user_message}"])
        response = generation_model.generate_content(
            full_context,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1024, temperature=0.7, top_p=0.9
            ),
        )
        return response.text
    except Exception as e:
        return f"Oops! Something went wrong: {str(e)}"


# Main chat interface
st.title("✨ AI Chatbot ")
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display chat messages from history
for message in st.session_state.messages:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    st.markdown(
        f"<div class='chat-message {role_class}'>{message['content']}</div>",
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Enter your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(
        f"<div class='chat-message user-message'>{prompt}</div>", unsafe_allow_html=True
    )
    with st.spinner("🧠 Processing your request..."):
        response = get_ai_response(prompt, model_choice)
        st.markdown(
            f"<div class='chat-message assistant-message'>{response}</div>",
            unsafe_allow_html=True,
        )
    st.session_state.messages.append({"role": "assistant", "content": response})
