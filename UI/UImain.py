import streamlit as st
import streamlit.components.v1 as components
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# ---------------------------------------------------------------- Config
st.set_page_config(page_title="Jester AI", page_icon="🃏", layout="centered")

DEFAULT_SYSTEM = "You are a jester in a royal setting. reply in short messages."

SUGGESTIONS = [
    ("😄  Tell me a joke", "Tell me a joke fit for the royal court."),
    ("🌤️  Cheer me up", "I'm having a rough day. Cheer me up!"),
    ("🧩  Riddle me this", "Give me a clever riddle to solve."),
    ("👑  Praise the king", "Compose a short verse praising the king."),
]

TYPING_HTML = (
    '<div class="typing"><span></span><span></span><span></span></div>'
)

# ---------------------------------------------------------------- Styling
st.markdown(
    """
    <style>
    :root {
        --bg: #faf8f5;
        --surface: #f2efe9;
        --surface-2: #e9e5de;
        --border: #e0dcd4;
        --text: #3b3b3b;
        --muted: #8c8a85;
        --accent: #6e6c68;
        --shadow: 0 4px 18px rgba(60, 55, 45, 0.07);
        --ease: cubic-bezier(.22, .61, .36, 1);
    }

    html { scroll-behavior: smooth; color-scheme: light; }
    #MainMenu, footer, header {visibility: hidden;}

    .stApp, [data-testid="stBottom"] > div { background: var(--bg); color: var(--text); }
    .block-container { max-width: 740px; padding-top: 2rem; padding-bottom: 7rem; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-thumb { background: var(--surface-2); border-radius: 8px; }
    ::-webkit-scrollbar-thumb:hover { background: #cfcac1; }

    /* ---------- Sidebar ---------- */
    /* Auto-hiding sidebar: only a 16px grip stays visible */
    section[data-testid="stSidebar"] {
        position: fixed !important; top: 0; left: 0; height: 100vh;
        width: 300px !important; min-width: 300px !important; max-width: 300px !important;
        transform: translateX(calc(-100% + 16px)) !important;
        transition: transform .38s var(--ease), box-shadow .38s var(--ease) !important;
        background: var(--surface); border-right: 1px solid var(--border);
        z-index: 1000; cursor: pointer;
    }
    section[data-testid="stSidebar"]::after {   /* grip handle */
        content: ""; position: absolute; right: 5px; top: 50%;
        width: 4px; height: 52px; margin-top: -26px; border-radius: 4px;
        background: #cfcac1; transition: background .25s var(--ease), opacity .25s var(--ease);
    }
    section[data-testid="stSidebar"]:hover,
    section[data-testid="stSidebar"][data-pinned="1"] {
        transform: translateX(0) !important;
        box-shadow: 8px 0 32px rgba(60, 55, 45, 0.12);
        cursor: default;
    }
    section[data-testid="stSidebar"]:hover::after,
    section[data-testid="stSidebar"][data-pinned="1"]::after { opacity: 0; }
    section[data-testid="stSidebar"] > div { opacity: 0; transition: opacity .3s var(--ease); }
    section[data-testid="stSidebar"]:hover > div,
    section[data-testid="stSidebar"][data-pinned="1"] > div { opacity: 1; transition-delay: .08s; }

    /* hide Streamlit's own collapse controls */
    [data-testid="stSidebarCollapseButton"], [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarResizeHandle"] { display: none !important; }
    section[data-testid="stSidebar"] * { color: var(--text); }
    .brand { font-size: 1.2rem; font-weight: 650; letter-spacing: -0.02em; margin-bottom: .6rem; }
    section[data-testid="stSidebar"] .stButton > button {
        background: var(--bg); border: 1px solid var(--border); border-radius: 12px;
        width: 100%; text-align: left; font-weight: 500;
        transition: all .25s var(--ease);
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #fff; transform: translateY(-1px); box-shadow: var(--shadow);
    }
    section[data-testid="stSidebar"] textarea {
        background: var(--bg) !important; border: 1px solid var(--border) !important;
        border-radius: 12px !important; color: var(--text) !important;
        transition: border-color .2s var(--ease), box-shadow .2s var(--ease);
    }
    section[data-testid="stSidebar"] textarea:focus {
        border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(110,108,104,.12) !important;
    }

    /* ---------- Hero ---------- */
    @keyframes fadeUp { from {opacity: 0; transform: translateY(14px);} to {opacity: 1; transform: none;} }
    @keyframes float { 0%,100% {transform: translateY(0);} 50% {transform: translateY(-6px);} }

    .hero { text-align: center; padding: 4.2rem 0 2rem 0; animation: fadeUp .7s var(--ease) both; }
    .hero .logo {
        width: 92px; height: 92px; border-radius: 30px; background: var(--surface);
        border: 1px solid var(--border); box-shadow: var(--shadow);
        display: inline-flex; align-items: center; justify-content: center; font-size: 46px;
        margin-bottom: 1.3rem; animation: float 4.5s ease-in-out infinite;
    }
    .hero h1 { font-size: 2.1rem; font-weight: 650; letter-spacing: -0.03em; margin: 0; color: var(--text); }
    .hero p { color: var(--muted); font-size: 1.02rem; margin-top: .6rem; }

    /* ---------- Suggestion cards ---------- */
    @property --angle { syntax: "<angle>"; initial-value: 0deg; inherits: false; }
    @keyframes ledSpin { to { --angle: 360deg; } }
    @keyframes ledGlow {
        0%   { box-shadow: 0 0 22px 3px rgba(255, 60, 150, .55); }
        25%  { box-shadow: 0 0 22px 3px rgba(255, 170, 40, .55); }
        50%  { box-shadow: 0 0 22px 3px rgba(60, 220, 130, .55); }
        75%  { box-shadow: 0 0 22px 3px rgba(60, 160, 255, .55); }
        100% { box-shadow: 0 0 22px 3px rgba(255, 60, 150, .55); }
    }

    /* Centre the suggestion grid under the hero */
    [data-testid="stMain"] [data-testid="stHorizontalBlock"],
    .main [data-testid="stHorizontalBlock"] { max-width: 580px; margin: 0 auto; gap: 1rem; }
    [data-testid="stMain"] .stButton, .main .stButton { display: flex; justify-content: center; }

    [data-testid="stMain"] .stButton > button, .main .stButton > button {
        --angle: 0deg;
        color: var(--text) !important; border: 3px solid transparent !important; border-radius: 18px;
        padding: calc(1rem - 2px) 1rem; min-height: 68px; width: 100%;
        font-weight: 500; text-align: center;
        display: flex; align-items: center; justify-content: center;
        background-color: transparent !important;
        background:
            linear-gradient(var(--surface), var(--surface)) padding-box,
            linear-gradient(var(--border), var(--border)) border-box !important;
        box-shadow: none; outline: none;
        transition: transform .28s var(--ease);
    }
    [data-testid="stMain"] .stButton > button *, .main .stButton > button * {
        background: transparent !important; color: var(--text) !important;
        text-align: center; justify-content: center;
    }
    [data-testid="stMain"] .stButton > button:hover, .main .stButton > button:hover,
    [data-testid="stMain"] .stButton > button:focus, .main .stButton > button:focus {
        transform: translateY(-3px);
        background:
            linear-gradient(#fff, #fff) padding-box,
            conic-gradient(from var(--angle),
                #ff3c96, #ffaa28, #f5e642, #3cdc82, #3ca0ff, #a064ff, #ff3c96) border-box !important;
        animation: ledSpin 2.2s linear infinite, ledGlow 4s linear infinite;
    }
    [data-testid="stMain"] .stButton > button:active, .main .stButton > button:active {
        transform: translateY(0) scale(.99);
    }

    /* ---------- Chat ---------- */
    [data-testid="stChatMessage"] {
        background: transparent; padding: .5rem 0; animation: fadeUp .45s var(--ease) both;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 20px; padding: .8rem 1.1rem; box-shadow: var(--shadow);
    }
    [data-testid="stChatMessage"] p { color: var(--text); line-height: 1.65; }

    /* Typing indicator */
    .typing { display: inline-flex; gap: 5px; padding: .5rem 0; }
    .typing span {
        width: 7px; height: 7px; border-radius: 50%; background: var(--muted);
        animation: bounce 1.2s infinite ease-in-out;
    }
    .typing span:nth-child(2) { animation-delay: .15s; }
    .typing span:nth-child(3) { animation-delay: .3s; }
    @keyframes bounce { 0%,60%,100% {transform: translateY(0); opacity: .4;} 30% {transform: translateY(-5px); opacity: 1;} }

    /* ---------- Input ---------- */
    [data-testid="stChatInput"] {
        background: var(--surface); border: 1px solid var(--border); border-radius: 26px;
        box-shadow: var(--shadow); transition: all .25s var(--ease);
    }
    [data-testid="stChatInput"]:focus-within {
        background: #fff; border-color: #bdb8ae; box-shadow: 0 6px 24px rgba(60,55,45,.12);
    }
    [data-testid="stChatInput"] textarea { color: var(--text); }
    [data-testid="stChatInput"] button {
        background: var(--accent); color: #fff; border-radius: 50%; transition: all .2s var(--ease);
    }
    [data-testid="stChatInput"] button:hover { background: #55534f; transform: scale(1.06); }

    .disclaimer { text-align: center; color: var(--muted); font-size: .75rem; margin-top: 1.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- State
if "convo" not in st.session_state:
    st.session_state.convo = []
if "pending" not in st.session_state:
    st.session_state.pending = None


@st.cache_resource
def get_model(temperature: float) -> ChatOpenAI:
    return ChatOpenAI(
        base_url="http://127.0.0.1:1234/v1",
        api_key="lm-studio",
        model="qwen/qwen3.5-9b",
        temperature=temperature,
    )


# ---------------------------------------------------------------- Sidebar
with st.sidebar:
    st.markdown('<div class="brand">🃏 Jester AI</div>', unsafe_allow_html=True)
    if st.button("＋  New chat"):
        st.session_state.convo = []
        st.session_state.pending = None
        st.rerun()

    st.markdown("---")
    system_prompt = st.text_area("System prompt", value=DEFAULT_SYSTEM, height=140)
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
    st.markdown("---")
    st.caption("Model: qwen/qwen3.5-9b\n\nServer: 127.0.0.1:1234 (LM Studio)")

# ---------------------------------------------------------------- Landing / history
if not st.session_state.convo:
    st.markdown(
        """
        <div class="hero">
            <div class="logo">🃏</div>
            <h1>How can I amuse you today?</h1>
            <p>Your witty royal jester, running right on your machine.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    for i, (label, text) in enumerate(SUGGESTIONS):
        if cols[i % 2].button(label, key=f"sug_{i}"):
            st.session_state.pending = text
            st.rerun()
else:
    for msg in st.session_state.convo:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role, avatar="🧑" if role == "user" else "🃏"):
            st.markdown(msg.content)

# ---------------------------------------------------------------- Input
typed = st.chat_input("Message Jester AI...")
prompt = typed or st.session_state.pending
st.session_state.pending = None

if prompt:
    st.session_state.convo.append(HumanMessage(content=prompt))
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    messages = [SystemMessage(content=system_prompt)] + st.session_state.convo
    model = get_model(temperature)

    with st.chat_message("assistant", avatar="🃏"):
        placeholder = st.empty()
        placeholder.markdown(TYPING_HTML, unsafe_allow_html=True)
        reply = ""
        try:
            for chunk in model.stream(messages):
                reply += chunk.content
                placeholder.markdown(reply + "▌")
            placeholder.markdown(reply)
            st.session_state.convo.append(AIMessage(content=reply))
        except Exception as e:
            st.session_state.convo.pop()
            placeholder.error(
                "Couldn't reach the model. Is LM Studio's server running on "
                f"http://127.0.0.1:1234?\n\n`{e}`"
            )

st.markdown(
    '<div class="disclaimer">Jester AI runs locally and can make mistakes.</div>',
    unsafe_allow_html=True,
)

# Click-to-pin behaviour for the sidebar (hover is handled purely in CSS).
# Click the grip to pin it open; click the grip again or anywhere outside to close.
components.html(
    """
    <script>
    const doc = window.parent.document;
    if (!window.parent.__sidebarClickInit) {
        window.parent.__sidebarClickInit = true;
        doc.addEventListener("click", (e) => {
            const sb = doc.querySelector('section[data-testid="stSidebar"]');
            if (!sb) return;
            const pinned = sb.getAttribute("data-pinned") === "1";
            const onSidebar = e.clientX <= sb.getBoundingClientRect().right;
            const onGrip = e.clientX <= 16;
            if (onSidebar && onGrip) {
                pinned ? sb.removeAttribute("data-pinned") : sb.setAttribute("data-pinned", "1");
            } else if (!onSidebar && pinned) {
                sb.removeAttribute("data-pinned");
            }
        });
    }
    </script>
    """,
    height=0,
)