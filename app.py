import streamlit as st
import streamlit.components.v1 as components

from crypto_utils import (
    encrypt_message,
    decrypt_message,
    pack_payload_for_url,
    unpack_payload_from_url,
)

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Crypto Lens",
    page_icon="💖",
    layout="centered",
)

# -------------------- AUTO BASE URL --------------------
def get_base_url():
    try:
        headers = st.context.headers
        proto = headers.get("x-forwarded-proto", "http")
        host = headers.get("host")
        if host:
            return f"{proto}://{host}"
    except Exception:
        pass
    return "http://localhost:8501"

# -------------------- ROMANTIC + MOBILE SAFE THEME --------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff1f6, #fce7f3);
    }

    h1, h2, h3 {
        color: #9d174d !important;
        font-family: 'Segoe UI', sans-serif;
    }

    label {
        color: #4a044e !important;
        font-weight: 600;
    }

    input, textarea {
        background-color: #ffffff !important;
        color: #3b0a45 !important;
        border-radius: 12px !important;
        border: 1px solid #fbcfe8 !important;
    }

    input::placeholder, textarea::placeholder {
        color: #9f7aea !important;
        opacity: 0.7 !important;
    }

    input[type="password"] {
        color: #3b0a45 !important;
    }

    div.stButton > button {
        background-color: #ec4899 !important;
        color: white !important;
        border-radius: 16px;
        padding: 0.7rem 1.2rem;
        font-weight: 600;
        border: none;
    }

    pre, code {
        background-color: #fff5f7 !important;
        color: #4a044e !important;
        border-radius: 14px;
        border: 1px solid #fbcfe8;
    }

    button[data-baseweb="tab"] {
        font-weight: 600;
        color: #9d174d !important;
    }

    .envelope {
        width: 280px;
        height: 180px;
        background: #ffffff;
        border-radius: 16px;
        margin: 40px auto 20px;
        position: relative;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    .envelope:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, transparent 50%, #fbcfe8 50%);
        clip-path: polygon(0 0, 100% 0, 50% 60%);
    }

    .seal {
        width: 64px;
        height: 64px;
        background: #ec4899;
        border-radius: 50%;
        position: absolute;
        bottom: 36px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        color: white;
        box-shadow: 0 6px 14px rgba(0,0,0,0.25);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- SOUND --------------------
def play_sound():
    components.html(
        """
        <audio autoplay>
            <source src="data:audio/mp3;base64,//uQxAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAACcQCAAwACABAAZGF0YcQCAAAAAA==" type="audio/mp3">
        </audio>
        """,
        height=0,
    )

# -------------------- STATE --------------------
query_payload = st.query_params.get("m")

if "envelope_opened" not in st.session_state:
    st.session_state.envelope_opened = False

if "payload" not in st.session_state and query_payload:
    st.session_state.payload = unpack_payload_from_url(query_payload)

# -------------------- HEADER --------------------
st.title("💖 Crypto Lens")
st.caption("A secret message, sealed just for you.")

tab_send, tab_open = st.tabs(["💌 Send", "📨 Open"])

# ====================================================
# SEND TAB
# ====================================================
with tab_send:
    st.subheader("💌 Send a Secret Message")

    pwd = st.text_input("Secret password (share separately)", type="password")
    msg = st.text_area(
        "Message",
        placeholder="Write something sweet, mysterious, or just for them...",
        height=150,
    )

    if st.button("Seal Message 💖", use_container_width=True):
        if not pwd or not msg:
            st.error("Please enter both a message and a password 💔")
        else:
            payload = encrypt_message(msg, pwd)
            packed = pack_payload_for_url(payload)
            link = f"{get_base_url()}/?m={packed}"

            st.success("Your secret message is sealed 💖")
            st.markdown("### 🔗 Share this link")
            st.code(link)

# ====================================================
# OPEN TAB
# ====================================================
with tab_open:
    st.subheader("💌 You've Received a Message")

    if query_payload and not st.session_state.envelope_opened:
        st.markdown(
            """
            <div class="envelope">
                <div class="seal">💖</div>
            </div>
            <center style="font-weight:600;color:#9d174d;">
                Tap the heart to open the envelope
            </center>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Open Envelope 💖", use_container_width=True):
            st.session_state.envelope_opened = True
            play_sound()
            st.rerun()

        st.stop()

    if st.session_state.envelope_opened:
        pwd = st.text_input("Enter the secret password", type="password")

        if st.button("Unlock Message 💕", use_container_width=True):
            try:
                text = decrypt_message(st.session_state.payload, pwd)
                st.success("💖 Message unlocked")
                st.text_area("Your message", value=text, height=150)
            except Exception:
                st.error("Wrong password 💔")

# -------------------- FOOTER --------------------
st.markdown(
    """
    <hr style="border:none;height:1px;background:#fbcfe8;margin-top:2rem;">
    <center style="color:#9d174d;">
        Made by Kashish Dhanani with 💕
    </center>
    """,
    unsafe_allow_html=True,
)

