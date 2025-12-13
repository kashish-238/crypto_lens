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

# -------------------- ROMANTIC THEME --------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fff1f6, #fce7f3);
    }

    h1, h2, h3 {
        color: #9d174d;
        font-family: 'Segoe UI', sans-serif;
    }

    p, label {
        font-family: 'Segoe UI', sans-serif;
        color: #4a044e;
    }

    div.stButton > button {
        background-color: #ec4899;
        color: white;
        border-radius: 16px;
        padding: 0.7rem 1.2rem;
        font-weight: 600;
        border: none;
    }

    pre {
        background-color: #fff5f7 !important;
        border-radius: 14px;
        border: 1px solid #fbcfe8;
    }

    /* Envelope */
    .envelope {
        width: 280px;
        height: 180px;
        background: #fff;
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

tab_encrypt, tab_open = st.tabs(["💌 Send", "📨 Open"])

# ====================================================
# SEND TAB (SENDER)
# ====================================================
with tab_encrypt:
    st.subheader("💌 Send a Secret Message")

    pwd = st.text_input("Secret password", type="password", key="send_pwd")
    msg = st.text_area("Message", height=150, key="send_msg")

    if st.button("Seal Message 💖", use_container_width=True):
        payload = encrypt_message(msg, pwd)
        packed = pack_payload_for_url(payload)
        link = f"http://localhost:8501/?m={packed}"

        st.success("Message sealed 💖")
        st.markdown("### Share this link")
        st.code(link)

# ====================================================
# OPEN TAB (RECEIVER)
# ====================================================
with tab_open:
    st.subheader("💌 You've received a message")

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

        if st.button("Open Envelope 💖", key="open_env", use_container_width=True):
            st.session_state.envelope_opened = True
            play_sound()
            st.rerun()

        st.stop()

    if st.session_state.envelope_opened:
        pwd = st.text_input("Enter the secret password", type="password", key="open_pwd")

        if st.button("Unlock Message 💕", use_container_width=True):
            try:
                text = decrypt_message(st.session_state.payload, pwd)
                st.success("💖 Message unlocked")
                st.text_area("Your message", value=text, height=150)
            except Exception:
                st.error("Wrong password 💔")
