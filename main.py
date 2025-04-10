import streamlit as st
import re
import string
import random
import base64
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Password Strength Meter",
    page_icon="🔒",
    layout="centered"
)

# Common password list
common_passwords = [
    "password", "123456", "qwerty", "admin", "welcome", 
    "password123", "abc123", "letmein", "monkey", "1234567890",
    "trustno1", "sunshine", "iloveyou", "princess", "admin123",
    "welcome123", "login", "qwerty123", "solo", "1q2w3e4r",
    "master", "dragon", "baseball", "football", "superman"
]

def check_password_strength(password):
  
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")
    
    # Character type checks
    if re.search(r'[A-Z]', password):
        score += 0.75
    else:
        feedback.append("Add uppercase letters (A-Z)")
        
    if re.search(r'[a-z]', password):
        score += 0.75
    else:
        feedback.append("Add lowercase letters (a-z)")
        
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Add numbers (0-9)")
        
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'\"\\|,.<>\/?]', password):
        score += 1.5
    else:
        feedback.append("Add special characters (!@#$%^&*)")
    
    # Check for repeated characters
    if re.search(r'(.)\1{2,}', password):
        score -= 1
        feedback.append("Avoid repeated characters (e.g., 'aaa', '111')")
    

    sequences = ['abcdefghijklmnopqrstuvwxyz', '0123456789']
    for seq in sequences:
        for i in range(len(seq) - 2):
            if seq[i:i+3].lower() in password.lower():
                score -= 0.5
                feedback.append("Avoid sequential characters (e.g., 'abc', '123')")
                break
    

    for common in common_passwords:
        if common in password.lower():
            score -= 1.5
            feedback.append("Avoid common passwords or patterns")
            break

    score = max(0, min(5, score))
    

    if score < 2:
        strength = "Weak"
        color = "red"
    elif score < 4:
        strength = "Moderate"
        color = "orange"
    else:
        strength = "Strong"
        color = "green"
        if not feedback:
            feedback = ["Excellent password!"]
    
    return {
        "score": score,
        "strength": strength,
        "color": color,
        "feedback": feedback
    }

def generate_password(length=12):


    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice('!@#$%^&*()_+-=[]{}|;:,.<>?')
    

    remaining_length = length - 4
    all_chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
    remaining_chars = ''.join(random.choice(all_chars) for _ in range(remaining_length))
    

    password_chars = list(lowercase + uppercase + digit + special + remaining_chars)
    random.shuffle(password_chars)
    return ''.join(password_chars)


def local_css():
    st.markdown("""
    <style>
    .password-container {
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f0f2f6;
    }
    .meter-container {
        margin: 20px 0;
    }
    .feedback-item {
        margin: 5px 0;
        padding: 8px;
        border-radius: 5px;
        background-color: #143557;
    }
    .generated-password {
        font-family: monospace;
        font-size: 1.2em;
        padding: 10px;
        background-color: #3d4349;
        border-radius: 5px;
        margin: 10px 0;
    }
    .title-container {
        text-align: center;
        padding: 10px;
        margin-bottom: 20px;
    }
    .password-input {
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    local_css()
    

    st.markdown("<div class='title-container'><h1>🔒 Password Strength Meter</h1></div>", unsafe_allow_html=True)
    st.markdown("Evaluate and improve your password security with our advanced strength meter.")
    

    col1, col2 = st.columns([3, 1])
    with col1:
        password_input = st.text_input("Enter your password:", type="password", key="password")
    with col2:
        show_password = st.checkbox("Show password")
    
    if show_password and password_input:
        st.markdown(f"<div class='generated-password'>{password_input}</div>", unsafe_allow_html=True)

    st.markdown("### 🎲 Need a strong password?")
    col1, col2 = st.columns([2, 1])
    with col1:
        password_length = st.slider("Password length", min_value=8, max_value=30, value=16)
    with col2:
        if st.button("Generate Password"):
            generated_password = generate_password(password_length)
            st.session_state.generated_password = generated_password
    
    if 'generated_password' in st.session_state:
        st.markdown("<div class='password-container'>", unsafe_allow_html=True)
        st.markdown(f"<div class='generated-password'>{st.session_state.generated_password}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    

    if password_input:
        result = check_password_strength(password_input)
        

        st.markdown("<div class='meter-container'>", unsafe_allow_html=True)
        st.markdown(f"### Password Strength: <span style='color:{result['color']}'>{result['strength']}</span>", unsafe_allow_html=True)
        
   
        progress_color = f"progress-color: {result['color']};"
        progress_value = result['score'] / 5
        st.progress(progress_value)
        
        # Score details
        st.markdown(f"**Score:** {result['score']:.1f}/5.0")
        
        # Feedback section
        if result['feedback']:
            st.markdown("### 💡 Suggestions for improvement:")
            for item in result['feedback']:
                st.markdown(f"<div class='feedback-item'>✅ {item}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        

        if result['strength'] != "Strong":
            st.markdown("### 🛡️ General Password Tips:")
            tips = [
                "Use a unique password for each account",
                "Consider using a password manager",
                "Change your passwords regularly",
                "Avoid using personal information in passwords"
            ]
            for tip in tips:
                st.markdown(f"- {tip}")

    # Password history (optional feature)
    if st.checkbox("Enable Password History"):
        if 'password_history' not in st.session_state:
            st.session_state.password_history = []
        
        if password_input and st.button("Save to History"):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if password_input not in [p['password'] for p in st.session_state.password_history]:
                st.session_state.password_history.append({
                    'password': password_input,
                    'strength': check_password_strength(password_input)['strength'],
                    'timestamp': timestamp
                })
                st.success("Password saved to history!")
        
        if st.session_state.password_history:
            st.markdown("### Password History")
            for i, entry in enumerate(st.session_state.password_history):
                st.markdown(f"**{i+1}.** Strength: {entry['strength']} - Created: {entry['timestamp']}")

    # Footer
    st.markdown("---")
    st.markdown("### About this tool")
    st.markdown("""
    This password strength meter evaluates passwords based on:
    - Length (minimum 8 characters)
    - Character diversity (uppercase, lowercase, numbers, special characters)
    - Pattern detection (repetitions, sequences)
    - Common password checking
    
    Password security is crucial for protecting your accounts from unauthorized access.
    """)

if __name__ == "__main__":
    main()