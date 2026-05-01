import streamlit as st
from datetime import datetime
from textblob import TextBlob
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Conversation Helper", layout="wide", page_icon="🎧")

# ---------------- EMOTION KEYWORDS ----------------
EMOTION_MAP = {
    "frustrated": ["frustrated", "frustrating", "annoying", "annoyed", "sick of", "fed up"],
    "angry": ["angry", "furious", "outraged", "unacceptable", "ridiculous", "horrible", "terrible", "worst"],
    "confused": ["confused", "don't understand", "unclear", "makes no sense", "lost", "what do you mean"],
    "urgent": ["urgent", "asap", "immediately", "emergency", "critical", "right now", "hurry"],
    "happy": ["happy", "great", "awesome", "excellent", "wonderful", "perfect", "love", "amazing", "thanks", "thank you"],
    "disappointed": ["disappointed", "let down", "expected more", "not good enough", "unhappy"],
}

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main .block-container {
    max-width: 1300px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* ---- Header ---- */
.app-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 0.2rem;
}
.app-header h1 {
    margin: 0;
    font-size: 1.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #61b0ff, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.app-version {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
    background: linear-gradient(135deg, #61b0ff33, #a78bfa33);
    color: #a78bfa;
    letter-spacing: 0.03em;
}
.app-tagline {
    color: #9aa0ab;
    font-size: 0.88rem;
    margin-bottom: 1rem;
}

/* ---- Section Titles ---- */
.section-title {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
}
.section-subtitle {
    color: #9aa0ab;
    font-size: 0.85rem;
    margin-bottom: 0.7rem;
}

/* ---- Chat Bubbles ---- */
.chat-line {
    padding: 0.6rem 0.85rem;
    border-radius: 12px;
    margin-bottom: 0.4rem;
    border: 1px solid rgba(130,140,160,0.18);
    background: rgba(26,31,44,0.35);
    backdrop-filter: blur(6px);
    transition: transform 0.15s ease;
}
.chat-line:hover {
    transform: translateX(3px);
}
.chat-customer {
    border-left: 4px solid #f0b35f;
}
.chat-agent {
    border-left: 4px solid #61b0ff;
}
.chat-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.chat-role {
    font-weight: 600;
    font-size: 0.82rem;
}
.chat-time {
    font-size: 0.72rem;
    color: #888;
}
.chat-text {
    margin-top: 0.25rem;
    font-size: 0.92rem;
    line-height: 1.45;
}
.sentiment-badge {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 0.12rem 0.5rem;
    border-radius: 999px;
    margin-left: 0.4rem;
    vertical-align: middle;
}
.badge-positive { background: #22c55e22; color: #22c55e; }
.badge-negative { background: #ef444422; color: #ef4444; }
.badge-neutral  { background: #eab30822; color: #eab308; }

/* ---- Score Indicator ---- */
.score-ring {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    margin: 0.5rem auto;
}
.score-value {
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1;
}
.score-label {
    font-size: 0.75rem;
    color: #9aa0ab;
    margin-top: 0.2rem;
}
.score-low    { color: #ef4444; }
.score-mid    { color: #eab308; }
.score-high   { color: #22c55e; }

/* ---- Suggestion Cards ---- */
.suggestion-card {
    background: rgba(30,36,50,0.55);
    border: 1px solid rgba(130,140,160,0.18);
    border-radius: 12px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 0.45rem;
    backdrop-filter: blur(6px);
}
.suggestion-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.25rem;
}
.suggestion-text {
    font-size: 0.88rem;
    line-height: 1.45;
}
.label-empathetic { color: #f472b6; }
.label-action     { color: #60a5fa; }
.label-concise    { color: #34d399; }

/* ---- Emotion Tags ---- */
.emotion-tag {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.1rem 0.45rem;
    border-radius: 999px;
    margin: 0.15rem 0.15rem 0.15rem 0;
    background: rgba(139, 92, 246, 0.15);
    color: #a78bfa;
}

/* ---- Nudge Breakdown ---- */
.rule-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.35rem 0;
    border-bottom: 1px solid rgba(130,140,160,0.1);
    font-size: 0.84rem;
}
.rule-pass { color: #22c55e; }
.rule-fail { color: #ef4444; }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="app-header">
    <h1>🎧 Conversation Assistant</h1>
    <span class="app-version">v2.0</span>
</div>
<div class="app-tagline">Real-time quality monitoring &amp; coaching for customer support interactions</div>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
defaults = {
    "messages": [],
    "last_score": None,
    "score_history": [],
    "polarity_history": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- HELPER FUNCTIONS ----------------

def sentiment(text):
    """Return (label, polarity, subjectivity)."""
    blob = TextBlob(text)
    pol = blob.sentiment.polarity
    sub = blob.sentiment.subjectivity
    if pol < -0.2:
        return "Negative", pol, sub
    elif pol > 0.2:
        return "Positive", pol, sub
    return "Neutral", pol, sub


def detect_emotions(text):
    """Return list of detected emotion tags."""
    lower = text.lower()
    found = []
    for emotion, keywords in EMOTION_MAP.items():
        if any(kw in lower for kw in keywords):
            found.append(emotion)
    return found


def sentiment_emoji(label):
    return {"Positive": "😊", "Negative": "😠", "Neutral": "😐"}.get(label, "❓")


def sentiment_badge_html(label):
    emoji = sentiment_emoji(label)
    css_class = f"badge-{label.lower()}"
    return f'<span class="sentiment-badge {css_class}">{emoji} {label}</span>'


def analyze_agent_reply(agent_text, customer_text=""):
    """Score agent reply out of 10, return (score, nudges, breakdown)."""
    text = agent_text.lower()
    score = 10
    nudges = []
    breakdown = {}

    # --- Profanity ---
    toxic_words = ["fuck", "shit", "idiot", "stupid", "bitch", "damn", "ass"]
    if any(w in text for w in toxic_words):
        return 0, ["🚫 Unprofessional language detected. Use respectful tone."], {"Profanity check": False}

    # --- Greeting ---
    greetings = ["hello", "hi ", "hi,", "hey", "good morning", "good afternoon", "good evening"]
    has_greeting = any(g in text for g in greetings)
    if not has_greeting:
        score -= 1
        nudges.append("👋 Start with a greeting (Hello, Hi, etc.).")
    breakdown["Greeting"] = has_greeting

    # --- Empathy ---
    empathy = ["sorry", "understand", "apologize", "appreciate", "i see", "hear you"]
    has_empathy = any(w in text for w in empathy)
    if not has_empathy:
        score -= 2
        nudges.append("💛 Add empathy to acknowledge the customer's concern.")
    breakdown["Empathy"] = has_empathy

    # --- Action words ---
    actions = ["check", "assist", "help", "update", "resolve", "look into", "investigate",
               "escalate", "follow up", "get back", "arrange", "process"]
    has_action = any(w in text for w in actions)
    if not has_action:
        score -= 2
        nudges.append("🎯 Mention a clear next action (check, resolve, follow up, etc.).")
    breakdown["Action words"] = has_action

    # --- Personalization ---
    personal = ["your", "you ", "you'", "you,"]
    has_personal = any(w in text for w in personal)
    if not has_personal:
        score -= 1
        nudges.append("🧑 Personalize the reply — address the customer directly.")
    breakdown["Personalization"] = has_personal

    # --- Asks clarifying question ---
    has_question = "?" in agent_text
    if not has_question and customer_text:
        cust_label, _, _ = sentiment(customer_text)
        if cust_label in ("Negative", "Neutral"):
            score -= 1
            nudges.append("❓ Consider asking a clarifying question to better understand the issue.")
    breakdown["Clarifying question"] = has_question

    # --- Length check ---
    word_count = len(agent_text.split())
    too_short = word_count < 6
    if too_short:
        score -= 2
        nudges.append("📏 Reply is too short — add more context and clarity.")
    breakdown["Sufficient length"] = not too_short

    # --- Polite closing ---
    has_thanks = any(w in text for w in ["thank", "thanks", "grateful"])
    if not has_thanks:
        score -= 1
        nudges.append("🙏 End with a polite closing (Thank you, etc.).")
    breakdown["Polite closing"] = has_thanks

    score = max(0, score)
    return score, nudges, breakdown


def latest_customer_message():
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "Customer":
            return msg["text"]
    return ""


def count_role(role):
    return sum(1 for m in st.session_state.messages if m["role"] == role)


def build_replies(customer_text):
    """Generate 3 categorized suggested replies based on customer sentiment + emotions."""
    label, _, _ = sentiment(customer_text)
    emotions = detect_emotions(customer_text)

    # Empathetic reply
    if label == "Negative":
        if "angry" in emotions or "frustrated" in emotions:
            empathetic = ("I completely understand your frustration, and I sincerely apologize "
                          "for the experience you've had. This is not the level of service we aim for. "
                          "Let me personally look into this and make it right for you.")
        else:
            empathetic = ("I'm sorry for the inconvenience you're facing. I understand how "
                          "important this is to you, and I want to make sure we resolve it properly.")
    elif label == "Positive":
        empathetic = ("Thank you so much for sharing that! I'm truly glad to hear things are working well. "
                      "Your satisfaction means a lot to us.")
    else:
        empathetic = ("Thank you for reaching out. I appreciate you taking the time to share the details. "
                      "I want to make sure we address your concern fully.")

    # Action-oriented reply
    if "urgent" in emotions:
        action = ("I understand the urgency. I'm escalating this right now and will have an update "
                  "for you within the next 30 minutes. Let me get this moving immediately.")
    elif label == "Negative":
        action = ("Let me check this for you right away. I'll investigate the issue, "
                  "coordinate with the relevant team, and update you with a resolution shortly.")
    elif label == "Positive":
        action = ("Great to hear! I'll verify everything on our end and confirm that all is "
                  "set. You should receive a confirmation shortly.")
    else:
        action = ("I'll look into this for you now. Let me check the details and I'll share "
                  "the next steps within a few minutes.")

    # Concise reply
    if label == "Negative":
        concise = "I apologize for the trouble. I'm on it — I'll update you shortly."
    elif label == "Positive":
        concise = "Glad to hear that! All confirmed on our end. Thank you!"
    else:
        concise = "Got it. I'm checking now and will update you shortly. Thank you."

    return [
        ("Empathetic", empathetic),
        ("Action-oriented", action),
        ("Concise", concise),
    ]


def score_color_class(score):
    if score is None:
        return "score-mid"
    if score <= 4:
        return "score-low"
    elif score <= 7:
        return "score-mid"
    return "score-high"


def avg_polarity():
    pols = [m["polarity"] for m in st.session_state.messages if m["role"] == "Customer"]
    return sum(pols) / len(pols) if pols else 0.0


# ---------------- LAYOUT ----------------
left_col, right_col = st.columns([2, 1], gap="medium")

# =====================================================
# LEFT COLUMN
# =====================================================
with left_col:

    # -------- Message Composer --------
    with st.container(border=True):
        st.markdown('<div class="section-title">💬 Message Composition</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Add customer or agent messages to simulate support interactions.</div>',
            unsafe_allow_html=True,
        )

        sender = st.selectbox("Who is sending the message?", ["Customer", "Agent"])
        msg = st.text_area("Enter message", height=120, placeholder="Type your message here...")

        has_customer = any(m["role"] == "Customer" for m in st.session_state.messages)
        disable_agent = sender == "Agent" and not has_customer

        b1, b2, b3 = st.columns(3)

        with b1:
            send_clicked = st.button("📤 Send Message", use_container_width=True, disabled=disable_agent)
        with b2:
            clear_clicked = st.button("🗑️ Clear Chat", use_container_width=True)
        with b3:
            # Export conversation
            if st.session_state.messages:
                export_lines = []
                for m in st.session_state.messages:
                    emotions_str = ", ".join(m.get("emotions", []))
                    line = f"[{m['time']}] {m['role']} ({m['sentiment']}): {m['text']}"
                    if emotions_str:
                        line += f"  [Emotions: {emotions_str}]"
                    export_lines.append(line)
                export_text = "\n".join(export_lines)
                st.download_button(
                    "📥 Export Chat",
                    data=export_text,
                    file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            else:
                st.button("📥 Export Chat", use_container_width=True, disabled=True)

        if disable_agent:
            st.info("💡 Customer should send the first message before the agent can reply.")

    # -------- Button Actions --------
    if clear_clicked:
        st.session_state.messages = []
        st.session_state.last_score = None
        st.session_state.score_history = []
        st.session_state.polarity_history = []
        st.rerun()

    if send_clicked and msg.strip():
        label, pol, sub = sentiment(msg.strip())
        emotions = detect_emotions(msg.strip()) if sender == "Customer" else []
        st.session_state.messages.append({
            "role": sender,
            "text": msg.strip(),
            "time": datetime.now().strftime("%H:%M:%S"),
            "sentiment": label,
            "polarity": pol,
            "subjectivity": sub,
            "emotions": emotions,
        })
        if sender == "Customer":
            st.session_state.polarity_history.append(pol)
        st.rerun()

    # -------- Conversation Log --------
    with st.container(border=True):
        st.markdown('<div class="section-title">📋 Conversation Log</div>', unsafe_allow_html=True)

        if not st.session_state.messages:
            st.info("Start by adding a customer message to begin the conversation.")
        else:
            for item in st.session_state.messages:
                role = item["role"]
                text = item["text"]
                tm = item["time"]
                slabel = item.get("sentiment", "Neutral")
                emotions = item.get("emotions", [])

                icon = "🧑" if role == "Customer" else "🎧"
                css_class = "chat-customer" if role == "Customer" else "chat-agent"
                badge = sentiment_badge_html(slabel)

                emotion_html = ""
                if emotions:
                    tags = "".join(f'<span class="emotion-tag">{e}</span>' for e in emotions)
                    emotion_html = f'<div style="margin-top:0.2rem;">{tags}</div>'

                st.markdown(f"""
                <div class="chat-line {css_class}">
                    <div class="chat-meta">
                        <span class="chat-role">{icon} {role} {badge}</span>
                        <span class="chat-time">{tm}</span>
                    </div>
                    <div class="chat-text">{text}</div>
                    {emotion_html}
                </div>
                """, unsafe_allow_html=True)

    # -------- Suggested Replies --------
    last_customer = latest_customer_message()

    if last_customer:
        with st.container(border=True):
            st.markdown('<div class="section-title">💡 Suggested Replies</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-subtitle">Choose a style that fits the situation best.</div>',
                unsafe_allow_html=True,
            )

            replies = build_replies(last_customer)
            label_classes = {"Empathetic": "label-empathetic", "Action-oriented": "label-action", "Concise": "label-concise"}
            label_icons = {"Empathetic": "💛", "Action-oriented": "🎯", "Concise": "⚡"}

            for cat, reply_text in replies:
                lclass = label_classes.get(cat, "")
                icon = label_icons.get(cat, "")
                st.markdown(f"""
                <div class="suggestion-card">
                    <div class="suggestion-label {lclass}">{icon} {cat}</div>
                    <div class="suggestion-text">{reply_text}</div>
                </div>
                """, unsafe_allow_html=True)


# =====================================================
# RIGHT COLUMN — Quality Insights
# =====================================================
with right_col:

    # -------- Quality Score --------
    with st.container(border=True):
        st.markdown('<div class="section-title">📊 Quality Insights</div>', unsafe_allow_html=True)

        total = len(st.session_state.messages)
        customer_count = count_role("Customer")
        agent_count = count_role("Agent")

        score = st.session_state.last_score
        nudges = []
        breakdown = {}

        if st.session_state.messages:
            last_msg = st.session_state.messages[-1]
            if last_msg["role"] == "Agent":
                cust_text = latest_customer_message()
                score, nudges, breakdown = analyze_agent_reply(last_msg["text"], cust_text)
                st.session_state.last_score = score
                st.session_state.score_history.append(score)

        score_display = "—" if score is None else f"{score}/10"
        color_class = score_color_class(score)

        st.markdown(f"""
        <div class="score-ring">
            <div class="score-value {color_class}">{score_display}</div>
            <div class="score-label">Quality Score</div>
        </div>
        """, unsafe_allow_html=True)

        if score is not None:
            st.progress(score / 10)

        # Metrics row
        c1, c2 = st.columns(2)
        c1.metric("Total Messages", total)
        c2.metric("Agent Replies", agent_count)

        c3, c4 = st.columns(2)
        c3.metric("Customer Msgs", customer_count)
        avg_p = avg_polarity()
        trend_label = "😊 Positive" if avg_p > 0.2 else ("😠 Negative" if avg_p < -0.2 else "😐 Neutral")
        c4.metric("Avg Sentiment", trend_label)

        st.divider()

        # ---- Nudges ----
        if score is None:
            st.info("No agent response yet. Send an agent reply to see quality analysis.")
        elif nudges:
            for n in nudges:
                st.warning(n)
        else:
            st.success("✅ Excellent response! All quality checks passed.")

    # -------- Rule Breakdown --------
    if breakdown:
        with st.container(border=True):
            st.markdown('<div class="section-title">🔍 Detailed Breakdown</div>', unsafe_allow_html=True)
            for rule, passed in breakdown.items():
                icon = "✅" if passed else "❌"
                color = "rule-pass" if passed else "rule-fail"
                st.markdown(
                    f'<div class="rule-row"><span>{rule}</span><span class="{color}">{icon}</span></div>',
                    unsafe_allow_html=True,
                )

    # -------- Sentiment Trend Chart --------
    if len(st.session_state.polarity_history) >= 2:
        with st.container(border=True):
            st.markdown('<div class="section-title">📈 Customer Sentiment Trend</div>', unsafe_allow_html=True)
            st.line_chart(st.session_state.polarity_history, use_container_width=True, height=180)

    # -------- Score History Chart --------
    if len(st.session_state.score_history) >= 2:
        with st.container(border=True):
            st.markdown('<div class="section-title">📉 Agent Score History</div>', unsafe_allow_html=True)
            st.bar_chart(st.session_state.score_history, use_container_width=True, height=180)

    # -------- Detected Emotions --------
    all_emotions = []
    for m in st.session_state.messages:
        all_emotions.extend(m.get("emotions", []))
    if all_emotions:
        with st.container(border=True):
            st.markdown('<div class="section-title">🏷️ Detected Customer Emotions</div>', unsafe_allow_html=True)
            unique = sorted(set(all_emotions))
            tags_html = "".join(f'<span class="emotion-tag">{e} ({all_emotions.count(e)})</span>' for e in unique)
            st.markdown(f'<div style="margin-top:0.3rem;">{tags_html}</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.divider()
st.markdown("""
<div style="text-align:center; color:#666; font-size:0.78rem; padding:0.5rem 0;">
    Conversation Assistant v2.0 — Real-time quality monitoring & coaching for customer support
</div>
""", unsafe_allow_html=True)
