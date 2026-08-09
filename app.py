import streamlit as st
from quantum_engine import run_bb84_protocol

st.set_page_config(page_title="Q-Shield Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ Q-Shield | Quantum Key Distribution")
st.caption("BB84 Protocol Simulation & Network Threat Detection")

st.sidebar.header("Control Panel")
bits = st.sidebar.slider("Bit Count", 20, 500, 100, step=20)
eve_active = st.sidebar.checkbox("Inject Eavesdropper (Eve)")

if st.button("Generate & Transmit Keys"):
    qber, key_len, sample_key, status = run_bb84_protocol(bits, eve_active)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Qubits Sent", bits)
    col2.metric("Sifted Key Size", f"{key_len} bits")
    col3.metric("Error Rate (QBER)", f"{qber:.1f}%")
    
    st.divider()
    
    if status == "ATTACK_DETECTED":
        st.error("🚨 Threat Detected: High QBER threshold exceeded. Key aborted!")
        st.warning("Eavesdropper interference detected on quantum channel. Initiating key regeneration...")
    elif status == "SECURE":
        st.success("✅ Secure Handshake: No channel disturbance detected.")
        st.code(f"Shared Key (First 16 bits): {sample_key}", language="text")
    else:
        st.error("Key exchange failed due to zero basis alignment.")
