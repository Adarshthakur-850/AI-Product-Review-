"""
ProductGuard AI - Multilingual Product Conversation Auditor Dashboard.
Interactive Streamlit Application for Call Auditing, Claim Verification & Coaching.
"""
import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Ensure root directory is on PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from services.auditor_pipeline import ProductGuardAuditorPipeline
from services.knowledge_base import ProductKnowledgeBase
from core.config import settings

# Page Configuration
st.set_page_config(
    page_title="ProductGuard AI — Conversation Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished, modern typography and cards
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .badge-verified {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-contradicted {
        background-color: #FDE8E8;
        color: #9B1C1C;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-unsupported {
        background-color: #FEF08A;
        color: #713F12;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .lang-pill {
        background: #E0E7FF;
        color: #3730A3;
        font-size: 0.78rem;
        padding: 2px 8px;
        border-radius: 12px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Services
@st.cache_resource
def get_pipeline():
    kb = ProductKnowledgeBase()
    return ProductGuardAuditorPipeline(kb=kb), kb

pipeline, kb = get_pipeline()

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/fluency/96/shield.png", width=64)
st.sidebar.title("ProductGuard AI")
st.sidebar.caption("Multilingual Conversation Compliance Auditor v1.0")

menu = st.sidebar.radio(
    "Navigation Menu",
    [
        "📊 Executive Overview",
        "⚡ Real-Time Audio & Call Simulator",
        "🎙️ Audit a Conversation",
        "📑 Private Coaching Report",
        "📦 Approved Product Catalog",
        "📈 Provider Performance Analytics"
    ]
)

# Helper to load sample files
def load_sample_call(filename: str):
    path = settings.CONVERSATIONS_DIR / filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# ==========================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ==========================================================
if menu == "📊 Executive Overview":
    st.markdown('<div class="main-header">🛡️ ProductGuard AI — Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Continuous compliance, factual claim verification, and communication coaching across English, Hindi, and Hinglish calls.</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Calls Audited", value="142", delta="+18 this week")
    with col2:
        st.metric(label="Average Quality Score", value="79.4 / 100", delta="+3.2 pts")
    with col3:
        st.metric(label="Factual Accuracy Rate", value="88.6%", delta="-1.5%")
    with col4:
        st.metric(label="Off-Topic Rate", value="11.2%", delta="-4.0%")

    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Language Distribution Across Calls")
        lang_df = pd.DataFrame({
            "Language": ["Hinglish (Code-Switched)", "Hindi (Devanagari)", "English"],
            "Call Count": [78, 42, 22]
        })
        fig_pie = px.pie(
            lang_df, values="Call Count", names="Language",
            hole=0.45, color_discrete_sequence=["#4F46E5", "#06B6D4", "#10B981"]
        )
        st.plotly_chart(fig_pie)
        
    with col_chart2:
        st.subheader("Primary Communication Deductions")
        deduct_df = pd.DataFrame({
            "Issue Category": ["Contradicted Specs", "Off-topic Personal Stories", "Unsupported Claims", "Repetitive Elaboration", "Missed Follow-up"],
            "Frequency": [28, 22, 18, 14, 9]
        })
        fig_bar = px.bar(
            deduct_df, x="Frequency", y="Issue Category", orientation="h",
            color="Frequency", color_continuous_scale="Reds"
        )
        st.plotly_chart(fig_bar)

# ==========================================================
# PAGE: REAL-TIME AUDIO & CALL SIMULATOR
# ==========================================================
elif menu == "⚡ Real-Time Audio & Call Simulator":
    st.markdown('<div class="main-header">⚡ Real-Time Audio & Call Auditor Lab</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Test live microphone audio in English, Hindi, and Hinglish, or simulate a live call stream with real-time compliance alerting.</div>', unsafe_allow_html=True)

    products = kb.list_products()
    product_options = {p["name"]: p["id"] for p in products}

    # Initialize session state for real-time live testing
    if "live_turns" not in st.session_state:
        st.session_state["live_turns"] = []
    if "sim_step" not in st.session_state:
        st.session_state["sim_step"] = 0

    tab_audio, tab_stream = st.tabs(["🎙️ Live Microphone Audio Tester", "⏱️ Live Stream Call Simulator"])

    # --- SUB-TAB 1: LIVE MICROPHONE AUDIO ---
    with tab_audio:
        st.markdown("### 🎙️ Live Voice Recording & Real-Time Auditor")
        st.caption("Record spoken audio in English, Hindi, or Hinglish directly through your browser microphone.")

        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            prod_name_live = st.selectbox("Product Catalog:", list(product_options.keys()), key="live_prod")
            prod_id_live = product_options[prod_name_live]
        with col_c2:
            speaker_role_live = st.selectbox("Speaker Role:", ["Service Provider (B)", "Customer (A)"], key="live_role")
            role_key = "provider" if "Provider" in speaker_role_live else "customer"
        with col_c3:
            audio_lang = st.selectbox(
                "Speech Language Mode:",
                ["en-IN (Indian English / Hinglish)", "hi-IN (Devanagari Hindi)", "en-US (Standard English)"],
                key="live_lang"
            )
            lang_code = audio_lang.split()[0]

        # Streamlit Native Live Audio Input
        audio_file = st.audio_input("Record audio turn (speak into microphone):")

        if audio_file is not None:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/wav")

            if st.button("⚡ Transcribe & Audit Live Audio Turn", type="primary"):
                with st.spinner("Processing speech recognition and auditing against catalog..."):
                    from services.audio_service import AudioService
                    trans_result = AudioService.transcribe_audio_bytes(audio_bytes, preferred_language=lang_code)

                    if not trans_result["success"]:
                        st.error(f"Speech Recognition Notice: {trans_result['error']}")
                    else:
                        spoken_text = trans_result["transcript"]
                        st.success(f"🗣️ **Transcribed ({trans_result['language_label']}):** \"{spoken_text}\"")

                        # Real-time audit
                        audit_turn = pipeline.audit_realtime_turn(
                            product_id=prod_id_live,
                            turn_text=spoken_text,
                            speaker_role=role_key,
                            conversation_history=st.session_state["live_turns"],
                            target_language="Hinglish" if "Hinglish" in audio_lang else ("Hindi" if "Hindi" in audio_lang else "English"),
                            generate_tts=True
                        )

                        # Display Real-Time Alert
                        alert_type = audit_turn["alert_type"]
                        if alert_type == "CRITICAL":
                            st.error(f"🚨 **{audit_turn['alert_message']}**")
                        elif alert_type == "WARNING":
                            st.warning(f"⚠️ **{audit_turn['alert_message']}**")
                        elif alert_type == "SUCCESS":
                            st.success(f"✅ **{audit_turn['alert_message']}**")
                        else:
                            st.info(f"ℹ️ **{audit_turn['alert_message']}**")

                        # Claims Table
                        if audit_turn.get("claims"):
                            st.write("**Factual Claims Detected in this Turn:**")
                            for c in audit_turn["claims"]:
                                status = c["verification_status"].upper()
                                badge = "✅ VERIFIED" if status == "VERIFIED" else "❌ CONTRADICTED"
                                st.write(f"- {badge}: **{c['claim_text']}** (Source: *{c.get('supporting_source')}*)")

                        # Instant Replacement Response & Audio Playback
                        if audit_turn.get("instant_correction"):
                            st.markdown("#### 💡 Live Corrected Replacement Response:")
                            st.info(f"👉 *\"{audit_turn['instant_correction']}\"*")
                            if audit_turn.get("tts_audio"):
                                st.write("🔊 **Listen to Corrected Answer Audio:**")
                                st.audio(audit_turn["tts_audio"], format="audio/wav")

                        # Append to live session
                        st.session_state["live_turns"].append({
                            "speaker_role": role_key,
                            "text": spoken_text,
                            "alert": audit_turn["alert_message"],
                            "alert_type": alert_type
                        })

        if st.session_state["live_turns"]:
            st.markdown("---")
            st.markdown("#### 💬 Ongoing Live Conversation Stream")
            for idx, turn in enumerate(st.session_state["live_turns"]):
                role_label = "👤 Customer" if turn["speaker_role"] == "customer" else "🎧 Service Provider"
                color = "#DEF7EC" if turn["alert_type"] == "SUCCESS" else ("#FDE8E8" if turn["alert_type"] == "CRITICAL" else "#F8FAFC")
                st.markdown(
                    f"""
                    <div style="background:{color}; padding: 10px; border-radius: 6px; margin-bottom: 6px;">
                        <strong>{role_label} #{idx+1}:</strong> {turn['text']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            if st.button("🔄 Clear Live Session"):
                st.session_state["live_turns"] = []
                st.rerun()

    # --- SUB-TAB 2: REAL-TIME STREAM SIMULATOR ---
    with tab_stream:
        st.markdown("### ⏱️ Live Call Stream Simulator")
        st.caption("Simulates an incoming real-time call turn-by-turn. Watch the 100-point score meter and compliance warnings update dynamically.")

        sim_case = load_sample_call("call_01_hinglish_earbuds.json")
        all_sim_segments = sim_case.get("segments", []) if sim_case else []
        total_sim_turns = len(all_sim_segments)
        current_step = st.session_state["sim_step"]

        col_ctl1, col_ctl2, col_ctl3 = st.columns([2, 2, 4])
        with col_ctl1:
            if st.button("▶️ Stream Next Turn", type="primary"):
                if current_step < total_sim_turns:
                    st.session_state["sim_step"] += 1
                    st.rerun()
        with col_ctl2:
            if st.button("🔄 Reset Stream"):
                st.session_state["sim_step"] = 0
                st.rerun()
        with col_ctl3:
            st.write(f"**Turn Progress: {current_step} of {total_sim_turns} turns streamed**")

        active_segments = all_sim_segments[:current_step]

        if active_segments:
            # Audit active stream
            stream_result = pipeline.audit_conversation(
                call_id="call-stream-sim",
                product_id="quantum-sound-pro",
                provider_name="Rohan Sharma",
                structured_segments=active_segments,
                target_report_language="Hinglish"
            )
            sim_score = stream_result["evaluation"]["overall_score"]
            sim_tier = stream_result["evaluation"]["tier"]

            st.metric("Live Dynamic Score", f"{sim_score} / 100", delta=f"{sim_score - 100:.1f} pts" if sim_score < 100 else "Perfect")

            for seg in stream_result["segments"]:
                role_icon = "👤 Customer" if seg["speaker_role"] == "customer" else "🎧 Service Provider"
                is_off = seg.get("is_off_topic", False)
                card_bg = "#FEF2F2" if is_off else ("#F0FDF4" if seg["speaker_role"] == "provider" else "#F8FAFC")
                st.markdown(
                    f"""
                    <div style="background:{card_bg}; padding: 10px; border-radius: 6px; margin-bottom: 6px; border-left: 4px solid {'#EF4444' if is_off else '#3B82F6'};">
                        <div style="display:flex; justify-content:space-between;">
                            <strong>{role_icon}</strong>
                            <span class="lang-pill">{seg.get('language_label', 'English')}</span>
                        </div>
                        <div>{seg['text']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            if stream_result["claims"]:
                st.markdown("#### Real-Time Claims Flagged So Far:")
                for c in stream_result["claims"]:
                    st.warning(f"**{c['verification_status'].upper()}**: {c['claim_text']} — {c.get('explanation')}")

            if current_step >= total_sim_turns:
                st.success("🎉 Full call stream completed! Private coaching report ready.")
        else:
            st.info("Click '▶️ Stream Next Turn' to begin streaming the real-time conversation.")

# ==========================================================
# PAGE 2: AUDIT A CONVERSATION
# ==========================================================
elif menu == "🎙️ Audit a Conversation":
    st.markdown('<div class="main-header">🎙️ Call Audit & Ingestion Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Upload an authorized recording, import a transcript, or select a multilingual benchmark case.</div>', unsafe_allow_html=True)

    input_mode = st.radio(
        "Choose Ingestion Mode:",
        ["Benchmark Sample Case", "Paste Raw Transcript", "Upload JSON Transcript / Audio"],
        horizontal=True
    )

    products = kb.list_products()
    product_options = {p["name"]: p["id"] for p in products}

    selected_product_id = "quantum-sound-pro"
    raw_transcript_text = ""
    structured_segments = None
    provider_name = "Rohan Sharma"
    target_lang = "Hinglish"

    if input_mode == "Benchmark Sample Case":
        case_choice = st.selectbox(
            "Select Multilingual Benchmark Case:",
            [
                "Case 1: Hinglish — Quantum Sound Pro (Battery claim, off-topic vacation story, waterproof contradiction)",
                "Case 2: Hindi — Apex Smartphone 15 Pro (Wireless charging check, 50MP camera, price)",
                "Case 3: English — Quantum Sound Pro (Dual-device multipoint, warranty)"
            ]
        )
        
        if "Case 1" in case_choice:
            sample_data = load_sample_call("call_01_hinglish_earbuds.json")
        elif "Case 2" in case_choice:
            sample_data = load_sample_call("call_02_hindi_phone.json")
        else:
            sample_data = load_sample_call("call_03_english_laptop.json")

        if sample_data:
            selected_product_id = sample_data.get("product_id", "quantum-sound-pro")
            provider_name = sample_data.get("provider_name", "Rohan Sharma")
            structured_segments = sample_data.get("segments", [])
            st.success(f"Loaded benchmark with {len(structured_segments)} conversational turns for product: **{selected_product_id}**")

    elif input_mode == "Paste Raw Transcript":
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            selected_prod_name = st.selectbox("Select Product Catalog:", list(product_options.keys()))
            selected_product_id = product_options[selected_prod_name]
        with col_meta2:
            provider_name = st.text_input("Service Provider Name:", value="Rohan Sharma")
            
        raw_transcript_text = st.text_area(
            "Paste Conversation Transcript (e.g. 'Customer: ...' / 'Provider: ...'):",
            height=200,
            value="Customer: Is headphone ki battery kitni der chalti hai?\nProvider: Sir iska battery backup around 30 hours hai, aur mere friend ne bhi last month trip par use kiya tha.\nCustomer: Kya ye swimming pool me waterproof hai?\nProvider: Haan sir, bilkul 100% waterproof hai aap swim kar sakte ho."
        )

    else:
        uploaded_file = st.file_uploader("Upload Transcript JSON or Audio (WAV/MP3/M4A):", type=["json", "wav", "mp3", "m4a"])
        if uploaded_file:
            if uploaded_file.name.endswith(".json"):
                data = json.load(uploaded_file)
                structured_segments = data.get("segments", [])
                selected_product_id = data.get("product_id", "quantum-sound-pro")
                provider_name = data.get("provider_name", "Service Provider")
                st.info(f"Loaded {len(structured_segments)} segments from uploaded file.")
            else:
                st.info(f"Audio file '{uploaded_file.name}' received. Running speech-to-text pipeline simulation...")
                sample_data = load_sample_call("call_01_hinglish_earbuds.json")
                structured_segments = sample_data.get("segments", []) if sample_data else []

    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        target_lang = st.selectbox("Preferred Coaching Report Language:", ["Hinglish", "Hindi", "English"])
    with col_opt2:
        disclosure_box = st.checkbox("Participant disclosure & recording authorization confirmed", value=True)

    if st.button("🚀 Run Complete Conversation Audit", type="primary"):
        if not disclosure_box:
            st.error("Compliance Error: Recording disclosure must be confirmed before processing.")
        else:
            with st.spinner("Analyzing conversation turns, language detection, and claim verification..."):
                audit_result = pipeline.audit_conversation(
                    call_id="call-live-session",
                    product_id=selected_product_id,
                    provider_name=provider_name,
                    raw_transcript=raw_transcript_text if not structured_segments else None,
                    structured_segments=structured_segments,
                    target_report_language=target_lang
                )
                st.session_state["latest_audit"] = audit_result
                st.success("Audit Completed! Redirecting to report below...")

    # Display results if present
    if "latest_audit" in st.session_state:
        res = st.session_state["latest_audit"]
        report = res["report"]
        eval_data = res["evaluation"]

        st.markdown("---")
        st.subheader("📋 Audit Executive Summary")
        
        c1, c2, c3, c4 = st.columns(4)
        score = eval_data["overall_score"]
        tier = eval_data["tier"]
        
        with c1:
            st.metric("Overall Score", f"{score}/100", help="Evaluated using the 100-point transparent framework")
        with c2:
            st.metric("Performance Tier", tier)
        with c3:
            st.metric("Verified Claims", f"{eval_data['metrics']['verified_claims']} / {eval_data['metrics']['total_claims']}")
        with c4:
            st.metric("Contradicted Claims", f"{eval_data['metrics']['contradicted_claims']}")

        # Score Breakdown Radar / Progress
        st.markdown("#### 100-Point Framework Breakdown")
        b_cols = st.columns(5)
        categories = [
            ("Factual Accuracy", "factual_accuracy"),
            ("Product Relevance", "product_relevance"),
            ("Answer Quality", "answer_quality"),
            ("Conciseness", "conciseness"),
            ("Communication Clarity", "communication_clarity")
        ]
        for idx, (label, key) in enumerate(categories):
            with b_cols[idx]:
                item = eval_data["breakdown"][key]
                st.write(f"**{label}**")
                st.progress(item["score"] / item["max"])
                st.caption(f"{item['score']} / {item['max']} pts ({item['percentage']}%)")

        # Deductions Audit Trail
        if eval_data["deductions"]:
            st.markdown("#### ⚠️ Deductions Audit Trail")
            for d in eval_data["deductions"]:
                st.warning(f"**[-{d['deduction']} pts] {d['category']}**: {d['reason']}")

        # Interactive Transcript View
        st.markdown("#### 💬 Timestamped Conversational Turns & Language Tagging")
        for seg in res["segments"]:
            role_icon = "👤 Customer" if seg["speaker_role"] == "customer" else "🎧 Service Provider"
            is_off = seg.get("is_off_topic", False)
            bg_color = "#FEF2F2" if is_off else ("#F0FDF4" if seg["speaker_role"] == "provider" else "#F8FAFC")
            
            with st.container():
                st.markdown(
                    f"""
                    <div style="background:{bg_color}; border-left: 4px solid {'#EF4444' if is_off else '#3B82F6'}; padding: 12px; border-radius: 6px; margin-bottom: 8px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                            <strong>{role_icon} [{seg.get('start_time', 0.0):.1f}s - {seg.get('end_time', 0.0):.1f}s]</strong>
                            <span>
                                <span class="lang-pill">{seg.get('language_label', 'English')}</span>
                                <span style="font-size:0.8rem; color:#6B7280; margin-left:8px;">{seg.get('topic_label', '')}</span>
                            </span>
                        </div>
                        <div style="font-size: 1rem; color:#1F2937;">{seg['text']}</div>
                        {f'<div style="font-size:0.82rem; color:#DC2626; margin-top:4px;">⚠️ {seg.get("relevance_explanation")}</div>' if is_off else ''}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Factual Claims Verification Table
        st.markdown("#### 🔍 Product Claims Verification Matrix")
        if res["claims"]:
            claims_data = []
            for c in res["claims"]:
                status = c["verification_status"].upper()
                badge = f"✅ {status}" if status == "VERIFIED" else (f"❌ {status}" if status == "CONTRADICTED" else f"⚠️ {status}")
                claims_data.append({
                    "Timestamp": f"{c['timestamp']:.1f}s",
                    "Claim Extracted": c["claim_text"],
                    "Status": badge,
                    "Catalog Source & Excerpt": f"{c.get('supporting_source', '')} - \"{c.get('supporting_excerpt', '')}\"",
                    "Explanation": c.get("explanation", "")
                })
            st.dataframe(pd.DataFrame(claims_data))
        else:
            st.info("No explicit numerical or technical product claims detected in this conversation.")

        # Grounded Corrected Responses
        st.markdown(f"#### 💡 Grounded Replacement Responses (Target: {target_lang})")
        if report["suggested_replacements"]:
            for rep in report["suggested_replacements"]:
                with st.expander(f"Correction for: \"{rep['original_statement'][:60]}...\"", expanded=True):
                    st.write(f"**Identified Issue:** {rep['issue']}")
                    st.success(f"**Recommended Customer-Friendly Answer ({target_lang}):**\n\n👉 *\"{rep['suggested_response']}\"*")
                    st.caption(f"Grounded Source: {rep['verified_source']}")
        else:
            st.success("All provider statements were accurate and aligned with the approved catalog.")

# ==========================================================
# PAGE 3: PRIVATE COACHING REPORT
# ==========================================================
elif menu == "📑 Private Coaching Report":
    st.markdown('<div class="main-header">📑 Private Coaching & Development Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Confidential coaching insights for the service provider to review and improve performance.</div>', unsafe_allow_html=True)

    if "latest_audit" not in st.session_state:
        st.info("Please audit a conversation first in the 'Audit a Conversation' tab to view its private report.")
    else:
        rep = st.session_state["latest_audit"]["report"]
        
        st.markdown(f"### Coaching Report for **{rep['provider_name']}**")
        st.info(rep["summary"])
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("#### ⭐ Effective Practices Observed")
            if rep["effective_statements"]:
                for stmt in rep["effective_statements"]:
                    st.write(f"✅ *\"{stmt}\"*")
            else:
                st.write("Factual adherence demonstrated.")
                
            st.markdown("#### 🎯 Actionable Improvement Plan")
            for action in rep["action_plan"]:
                st.markdown(f"- 📌 {action}")

        with col_g2:
            st.markdown("#### ⚠️ Communication Side-tracks Flagged")
            if rep["off_topic_statements"]:
                for item in rep["off_topic_statements"]:
                    st.error(f"**[{item['timestamp']}]** *\"{item['text']}\"*\n\n{item['critique']}")
            else:
                st.success("Zero off-topic side-tracks detected. Excellent conversational focus!")

        st.caption(f"🔒 {rep['confidence_limitation_note']}")

# ==========================================================
# PAGE 4: PRODUCT CATALOG
# ==========================================================
elif menu == "📦 Approved Product Catalog":
    st.markdown('<div class="main-header">📦 Approved Product Knowledge Base</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Source of truth specifications, prices, warranties, and FAQs used for verification grounding.</div>', unsafe_allow_html=True)

    products = kb.list_products()
    selected_name = st.selectbox("Select Product to Inspect:", [p["name"] for p in products])
    selected_id = [p["id"] for p in products if p["name"] == selected_name][0]
    
    prod_data = kb.get_product(selected_id)
    if prod_data:
        t1, t2, t3, t4, t5 = st.tabs([
            "Specifications",
            "Commercial Terms",
            "Policies & Warranty",
            "Approved FAQs",
            "📄 Provider Script & Model Testing Doc (.docx)"
        ])
        
        with t1:
            st.json(prod_data.get("specifications", {}))
        with t2:
            st.json(prod_data.get("commercial_terms", {}))
        with t3:
            st.json(prod_data.get("policies", {}))
        with t4:
            for item in prod_data.get("frequently_asked_questions", []):
                st.markdown(f"**Q: {item['question']}**")
                st.write(f"A: {item['answer']}")
                st.divider()
        with t5:
            st.markdown("### 📄 Service Provider Talk-Track & Model Testing Guide")
            st.caption("Standard compliance script for service providers and structured benchmark prompts for evaluating ProductGuard AI.")
            
            from services.script_doc_generator import ScriptDocGenerator
            doc_gen = ScriptDocGenerator(kb=kb)
            docx_path = doc_gen.generate_docx(selected_id)
            md_path = doc_gen.generate_markdown(selected_id)
            
            with open(docx_path, "rb") as f:
                docx_bytes = f.read()

            col_d1, col_d2 = st.columns([2, 3])
            with col_d1:
                st.download_button(
                    label=f"📥 Download Official Provider Script (.docx)",
                    data=docx_bytes,
                    file_name=f"{selected_id}_compliance_script_guide.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    type="primary"
                )
            with col_d2:
                st.info(f"Generated Word file saved at: `{docx_path.name}`")

            st.markdown("---")
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
            st.markdown(md_content)

# ==========================================================
# PAGE 5: PROVIDER PERFORMANCE ANALYTICS
# ==========================================================
elif menu == "📈 Provider Performance Analytics":
    st.markdown('<div class="main-header">📈 Provider Longitudinal Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Multi-call compliance and quality trajectory over time.</div>', unsafe_allow_html=True)

    provider_select = st.selectbox("Select Service Provider:", ["Rohan Sharma", "Priya Verma"])
    
    if provider_select == "Rohan Sharma":
        st.subheader("Performance Profile: Rohan Sharma")
        st.write("Department: Consumer Electronics Sales | Total Calls Audited: 14 | Average Score: 76.5/100")
        
        df_trend = pd.DataFrame({
            "Call": [f"Call {i}" for i in range(1, 7)],
            "Score": [68.0, 72.5, 74.0, 75.0, 81.5, 84.0]
        })
        fig = px.line(df_trend, x="Call", y="Score", markers=True, title="Compliance & Quality Score Progression", range_y=[50, 100])
        st.plotly_chart(fig)
        
        st.markdown("#### Primary Coaching Focus for Rohan:")
        st.write("1. ⚠️ Eliminate personal travel stories during customer feature questions.")
        st.write("2. 🔍 Re-confirm audio water resistance: Quantum Sound Pro is IPX4 splash resistant, NOT swimming waterproof.")
    else:
        st.subheader("Performance Profile: Priya Verma")
        st.write("Department: Smartphone Customer Support | Total Calls Audited: 22 | Average Score: 92.0/100")
        
        df_trend = pd.DataFrame({
            "Call": [f"Call {i}" for i in range(1, 7)],
            "Score": [88.0, 89.5, 91.0, 93.0, 94.5, 95.5]
        })
        fig = px.line(df_trend, x="Call", y="Score", markers=True, title="Compliance & Quality Score Progression", range_y=[50, 100])
        st.plotly_chart(fig)
        
        st.success("Exemplary compliance record across all Hindi and Hinglish conversations.")
