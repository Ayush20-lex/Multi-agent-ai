# app.py

import streamlit as st
from agents import AgentManager
from utils.logger import logger
import os
import time
import re
import html as html_module
from dotenv import load_dotenv

load_dotenv()


def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { font-family: 'DM Sans', sans-serif !important; }
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Header ── */
    .app-header {
        padding: 2rem 0 1.2rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 2rem;
    }
    .app-header h1 {
        font-size: 1.6rem !important; font-weight: 700 !important;
        color: #e4e4e7 !important; margin: 0 !important; letter-spacing: -0.3px;
    }
    .app-header p { font-size: 0.85rem; color: #71717a; margin-top: 4px; }
    .header-badge {
        display: inline-block; padding: 3px 10px;
        background: rgba(99,102,241,0.12); color: #818cf8;
        border-radius: 6px; font-size: 0.7rem; font-weight: 600;
        letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 8px;
    }

    /* ═══ SVG PIPELINE ═══ */
    .svg-pipeline { padding: 20px 0; margin: 1rem 0 1.5rem 0; overflow-x: auto; }
    .svg-pipeline svg { width: 100%; max-width: 720px; }
    .node-idle { fill: #27272a; stroke: #3f3f46; }
    .node-running { fill: #312e81; stroke: #818cf8; }
    .node-done { fill: #14532d; stroke: #4ade80; }
    .node-fail { fill: #450a0a; stroke: #f87171; }
    .node-text { font-family: 'DM Sans', sans-serif; font-size: 11px; font-weight: 500; }
    .node-text-idle { fill: #52525b; }
    .node-text-running { fill: #c7d2fe; }
    .node-text-done { fill: #bbf7d0; }
    .node-text-fail { fill: #fecaca; }
    .conn-idle { stroke: #27272a; stroke-width: 2; }
    .conn-active { stroke: #818cf8; stroke-width: 2; stroke-dasharray: 8 4; animation: dash-flow 1s linear infinite; }
    .conn-done { stroke: #4ade80; stroke-width: 2; }
    @keyframes dash-flow { to { stroke-dashoffset: -24; } }
    .pulse-ring { animation: pulse-expand 1.5s ease-out infinite; }
    @keyframes pulse-expand { 0% { r: 22; opacity: 0.6; } 100% { r: 34; opacity: 0; } }

    /* ═══ GLASSMORPHISM ═══ */
    .glass-card {
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px; padding: 22px 26px; margin: 14px 0;
        position: relative; overflow: hidden;
    }
    .glass-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
    }
    .glass-card .card-label {
        font-size: 0.68rem; font-weight: 600; color: #71717a;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;
    }
    .glass-card .card-body { color: #d4d4d8; font-size: 0.88rem; line-height: 1.7; }

    /* ═══ THINKING + REVEAL ═══ */
    .thinking-card {
        background: rgba(49, 46, 129, 0.12);
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(129, 140, 248, 0.2);
        border-radius: 14px; padding: 32px 26px; margin: 14px 0;
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; gap: 14px;
    }
    .thinking-card .thinking-dots { display: flex; gap: 6px; }
    .thinking-card .thinking-dots span {
        width: 8px; height: 8px; border-radius: 50%; background: #818cf8;
        animation: think-bounce 1.4s ease-in-out infinite;
    }
    .thinking-card .thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
    .thinking-card .thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes think-bounce {
        0%, 80%, 100% { transform: scale(0.6); opacity: 0.3; }
        40% { transform: scale(1); opacity: 1; }
    }
    .thinking-card .thinking-label { font-size: 0.8rem; font-weight: 500; color: #a5b4fc; }

    .reveal-card {
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px; padding: 22px 26px; margin: 14px 0;
        position: relative; overflow: hidden;
        animation: fadeSlideIn 0.5s ease-out;
    }
    @keyframes fadeSlideIn {
        0% { opacity: 0; transform: translateY(16px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .reveal-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(74,222,128,0.3), transparent);
    }
    .reveal-card .card-label {
        font-size: 0.68rem; font-weight: 600; color: #4ade80;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;
    }
    .reveal-card .card-body { color: #d4d4d8; font-size: 0.85rem; line-height: 1.7; }

    /* ── Flow card ── */
    .flow-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-left: 3px solid #818cf8;
        border-radius: 8px; padding: 14px 18px; margin: 12px 0;
    }
    .flow-label {
        font-size: 0.7rem; font-weight: 600; color: #71717a;
        text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px;
    }
    .flow-preview {
        color: #a1a1aa; font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem; line-height: 1.6;
    }

    /* ── Console ── */
    .console {
        background: #09090b; border: 1px solid rgba(255,255,255,0.06);
        border-radius: 8px; padding: 14px 18px;
        font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
        line-height: 1.8; max-height: 140px; overflow-y: auto; margin: 8px 0 16px 0;
    }
    .console .ts { color: #52525b; }
    .console .who { color: #818cf8; }
    .console .msg { color: #a1a1aa; }
    .console .ok { color: #4ade80; }
    .console .err { color: #f87171; }

    /* ── Score ── */
    .score-chip {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 6px 14px; border-radius: 6px;
        font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 0.82rem;
        margin: 8px 0 12px 0;
    }
    .score-good { background: rgba(74,222,128,0.1); color: #4ade80; border: 1px solid rgba(74,222,128,0.2); }
    .score-ok { background: rgba(250,204,21,0.1); color: #facc15; border: 1px solid rgba(250,204,21,0.2); }
    .score-bad { background: rgba(248,113,113,0.1); color: #f87171; border: 1px solid rgba(248,113,113,0.2); }

    .section-label {
        font-size: 0.7rem; font-weight: 600; color: #52525b;
        text-transform: uppercase; letter-spacing: 1px; margin: 24px 0 8px 0;
    }

    /* ═══ METRICS BAR ═══ */
    .metrics-bar {
        display: flex; gap: 12px; flex-wrap: wrap;
        margin: 16px 0; padding: 16px 20px;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px;
    }
    .metric-item {
        display: flex; flex-direction: column; gap: 2px;
        padding: 8px 16px;
        background: rgba(255,255,255,0.02);
        border-radius: 8px; min-width: 100px;
    }
    .metric-label {
        font-size: 0.62rem; font-weight: 600; color: #52525b;
        text-transform: uppercase; letter-spacing: 0.8px;
    }
    .metric-value {
        font-size: 1.1rem; font-weight: 700; color: #e4e4e7;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-value.accent { color: #818cf8; }
    .metric-value.green { color: #4ade80; }
    </style>
    """, unsafe_allow_html=True)


# ─── Rendering helpers ────────────────────────────────────────────────────────

def draw_header():
    st.markdown("""
    <div class="app-header">
        <span class="header-badge">Multi-Agent System</span>
        <h1>Research AI Workspace</h1>
        <p>Collaborative agents for writing, summarization, and data sanitization.</p>
    </div>
    """, unsafe_allow_html=True)


def draw_svg_pipeline(steps, active=-1, results=None):
    results = results or {}
    n = len(steps)
    spacing = 160
    w = spacing * (n - 1) + 80
    cx_start = 40
    svg = f'<div class="svg-pipeline"><svg viewBox="0 0 {w} 80" xmlns="http://www.w3.org/2000/svg">'
    for i in range(n - 1):
        x1 = cx_start + i * spacing + 22
        x2 = cx_start + (i + 1) * spacing - 22
        y = 32
        if i + 1 <= active or (i in results and results[i] == "ok" and i + 1 in results):
            cls = "conn-done"
        elif i + 1 == active or (i in results and results[i] == "ok"):
            cls = "conn-active"
        else:
            cls = "conn-idle"
        svg += f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" class="{cls}" />'
    for i, label in enumerate(steps):
        cx = cx_start + i * spacing
        cy = 32
        if i in results:
            state = "done" if results[i] == "ok" else "fail"
        elif i == active:
            state = "running"
        else:
            state = "idle"
        if state == "running":
            svg += f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="#818cf8" stroke-opacity="0.3" class="pulse-ring" />'
        svg += f'<circle cx="{cx}" cy="{cy}" r="20" class="node-{state}" stroke-width="2" />'
        if state == "done":
            svg += f'<text x="{cx}" y="{cy+1}" text-anchor="middle" dominant-baseline="central" fill="#4ade80" font-size="14">✓</text>'
        elif state == "fail":
            svg += f'<text x="{cx}" y="{cy+1}" text-anchor="middle" dominant-baseline="central" fill="#f87171" font-size="14">✗</text>'
        elif state == "running":
            svg += f'''<g transform="translate({cx},{cy})">
                <circle cx="-6" cy="0" r="2.5" fill="#818cf8" opacity="0.4"><animate attributeName="opacity" values="0.4;1;0.4" dur="1s" repeatCount="indefinite" /></circle>
                <circle cx="0" cy="0" r="2.5" fill="#818cf8" opacity="0.7"><animate attributeName="opacity" values="0.7;1;0.7" dur="1s" begin="0.2s" repeatCount="indefinite" /></circle>
                <circle cx="6" cy="0" r="2.5" fill="#818cf8" opacity="1"><animate attributeName="opacity" values="1;0.4;1" dur="1s" begin="0.4s" repeatCount="indefinite" /></circle>
            </g>'''
        else:
            svg += f'<text x="{cx}" y="{cy+1}" text-anchor="middle" dominant-baseline="central" fill="#52525b" font-size="11" font-family="DM Sans">{i+1}</text>'
        svg += f'<text x="{cx}" y="{cy+40}" text-anchor="middle" class="node-text node-text-{state}">{label}</text>'
    svg += '</svg></div>'
    st.markdown(svg, unsafe_allow_html=True)


def draw_thinking(agent_name):
    st.markdown(f"""
    <div class="thinking-card">
        <div class="thinking-dots"><span></span><span></span><span></span></div>
        <div class="thinking-label">{agent_name} is processing...</div>
    </div>
    """, unsafe_allow_html=True)


def draw_result(label, content):
    safe = html_module.escape(str(content)).replace('\n', '<br>')
    st.markdown(f"""
    <div class="reveal-card">
        <div class="card-label">{label}</div>
        <div class="card-body">{safe}</div>
    </div>
    """, unsafe_allow_html=True)


def draw_console(entries):
    html = '<div class="console">'
    for e in entries:
        cls = "ok" if "✓" in e["m"] else ("err" if "✗" in e["m"] else "msg")
        html += f'<div><span class="ts">{e["t"]}</span> <span class="who">{e["a"]}</span> <span class="{cls}">{e["m"]}</span></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def draw_flow(src, dst, text):
    preview = str(text)[:180] + "…" if len(str(text)) > 180 else str(text)
    safe = html_module.escape(preview)
    st.markdown(f"""
    <div class="flow-card">
        <div class="flow-label">{src} → {dst}</div>
        <div class="flow-preview">{safe}</div>
    </div>
    """, unsafe_allow_html=True)


def draw_score(val_text):
    score = _parse_score(val_text)
    if score is None:
        return
    cls = "score-good" if score >= 4 else ("score-ok" if score >= 3 else "score-bad")
    st.markdown(f'<span class="score-chip {cls}">● {score}/5</span>', unsafe_allow_html=True)


def draw_metrics(timings, total_chars=0):
    """Render performance metrics bar."""
    total = sum(timings.values())
    items = ""
    for name, secs in timings.items():
        items += f'''
        <div class="metric-item">
            <span class="metric-label">{name}</span>
            <span class="metric-value accent">{secs:.1f}s</span>
        </div>'''
    items += f'''
    <div class="metric-item">
        <span class="metric-label">Total Time</span>
        <span class="metric-value green">{total:.1f}s</span>
    </div>'''
    if total_chars:
        items += f'''
        <div class="metric-item">
            <span class="metric-label">Output</span>
            <span class="metric-value">{total_chars:,} chars</span>
        </div>'''
    st.markdown(f'<div class="metrics-bar">{items}</div>', unsafe_allow_html=True)


def draw_actions(text_content, filename="output"):
    """Render copy-to-clipboard and download buttons."""
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        st.download_button(
            "📥 Download .txt",
            data=str(text_content),
            file_name=f"{filename}.txt",
            mime="text/plain",
            key=f"dl_txt_{filename}",
        )
    with col2:
        st.download_button(
            "📥 Download .md",
            data=str(text_content),
            file_name=f"{filename}.md",
            mime="text/markdown",
            key=f"dl_md_{filename}",
        )
    with col3:
        with st.popover("📋 Copy to clipboard", key=f"copy_{filename}"):
            st.code(str(text_content), language=None)


def _parse_score(text):
    for p in [r'(\d)\s*/\s*5', r'(?:score|rating|rate)[:\s]*(\d)', r'\*\*(\d)/5\*\*', r'(\d)\s*out\s*of\s*5']:
        m = re.search(p, str(text), re.IGNORECASE)
        if m:
            return int(m.group(1))
    return None


def ts():
    return time.strftime("%H:%M:%S")


def section(label):
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)


# ─── Task runners ─────────────────────────────────────────────────────────────

def run_summarize(mgr):
    steps = ["Input", "Summarize", "Validate"]
    text = st.text_area("Paste medical text below", height=180, placeholder="Enter the medical text you want to summarize...", key="summarize_input")

    if st.button("Run", type="primary", key="summarize_run"):
        if not text:
            st.warning("Please enter some text first.")
            return

        agents = (mgr.get_agent("summarize"), mgr.get_agent("summarize_validator"))
        log, res, timings = [], {0: "ok"}, {}
        pp, cp = st.empty(), st.empty()

        log.append({"t": ts(), "a": "sys", "m": f"input received — {len(text)} chars"})
        with pp.container(): draw_svg_pipeline(steps, 1, res)
        with cp.container(): draw_console(log)

        # summarize
        log.append({"t": ts(), "a": "summarizer", "m": "working..."})
        with cp.container(): draw_console(log)
        card1 = st.empty()
        with card1.container(): draw_thinking("Summarizer")

        t0 = time.time()
        with st.spinner("Summarizing..."):
            try:
                summary = agents[0].execute(text)
                timings["Summarize"] = time.time() - t0
                res[1] = "ok"
                log.append({"t": ts(), "a": "summarizer", "m": f"✓ done in {timings['Summarize']:.1f}s"})
            except Exception as e:
                res[1] = "err"
                log.append({"t": ts(), "a": "summarizer", "m": f"✗ {e}"})
                with pp.container(): draw_svg_pipeline(steps, 1, res)
                with cp.container(): draw_console(log)
                card1.empty()
                st.error(str(e))
                return

        with pp.container(): draw_svg_pipeline(steps, 2, res)
        with cp.container(): draw_console(log)
        with card1.container(): draw_result("Summary", summary)

        draw_actions(summary, "summary")
        draw_flow("Summarizer", "Validator", summary)

        # validate
        log.append({"t": ts(), "a": "validator", "m": "checking quality..."})
        with cp.container(): draw_console(log)
        card2 = st.empty()
        with card2.container(): draw_thinking("Validator")

        t0 = time.time()
        with st.spinner("Validating..."):
            try:
                validation = agents[1].execute(original_text=text, summary=summary)
                timings["Validate"] = time.time() - t0
                res[2] = "ok"
                log.append({"t": ts(), "a": "validator", "m": f"✓ done in {timings['Validate']:.1f}s"})
            except Exception as e:
                res[2] = "err"
                log.append({"t": ts(), "a": "validator", "m": f"✗ {e}"})
                with pp.container(): draw_svg_pipeline(steps, 2, res)
                with cp.container(): draw_console(log)
                card2.empty()
                st.error(str(e))
                return

        with pp.container(): draw_svg_pipeline(steps, -1, res)
        with cp.container(): draw_console(log)
        with card2.container(): draw_result("Validation Report", validation)
        draw_score(validation)
        draw_metrics(timings, len(str(summary)))


def run_write_article(mgr):
    steps = ["Input", "Draft", "Refine", "Validate"]
    topic = st.text_input("Topic", placeholder="e.g. Impact of AI on drug discovery", key="article_topic")
    outline = st.text_area("Outline (optional)", height=120, placeholder="Optional structure or key points...", key="article_outline")

    if st.button("Run", type="primary", key="article_run"):
        if not topic:
            st.warning("Please enter a topic.")
            return

        w, r, v = mgr.get_agent("write_article"), mgr.get_agent("refiner"), mgr.get_agent("validator")
        log, res, timings = [], {0: "ok"}, {}
        pp, cp = st.empty(), st.empty()

        log.append({"t": ts(), "a": "sys", "m": f"topic: {topic}"})
        with pp.container(): draw_svg_pipeline(steps, 1, res)
        with cp.container(): draw_console(log)

        # draft
        log.append({"t": ts(), "a": "writer", "m": "drafting article..."})
        with cp.container(): draw_console(log)
        card1 = st.empty()
        with card1.container(): draw_thinking("Writer Agent")

        t0 = time.time()
        with st.spinner("Writing draft..."):
            try:
                draft = w.execute(topic, outline)
                timings["Draft"] = time.time() - t0
                res[1] = "ok"
                log.append({"t": ts(), "a": "writer", "m": f"✓ draft ready in {timings['Draft']:.1f}s — {len(str(draft))} chars"})
            except Exception as e:
                res[1] = "err"
                log.append({"t": ts(), "a": "writer", "m": f"✗ {e}"})
                with pp.container(): draw_svg_pipeline(steps, 1, res)
                with cp.container(): draw_console(log)
                card1.empty()
                st.error(str(e))
                return

        with pp.container(): draw_svg_pipeline(steps, 2, res)
        with cp.container(): draw_console(log)
        with card1.container():
            with st.expander("View raw draft"):
                st.write(draft)

        draw_flow("Writer", "Refiner", draft)

        # refine
        log.append({"t": ts(), "a": "refiner", "m": "polishing..."})
        with cp.container(): draw_console(log)
        card2 = st.empty()
        with card2.container(): draw_thinking("Refiner Agent")

        t0 = time.time()
        with st.spinner("Refining..."):
            try:
                refined = r.execute(draft)
                timings["Refine"] = time.time() - t0
                res[2] = "ok"
                log.append({"t": ts(), "a": "refiner", "m": f"✓ refined in {timings['Refine']:.1f}s"})
            except Exception as e:
                res[2] = "err"
                log.append({"t": ts(), "a": "refiner", "m": f"✗ {e}"})
                with pp.container(): draw_svg_pipeline(steps, 2, res)
                with cp.container(): draw_console(log)
                card2.empty()
                st.error(str(e))
                return

        with pp.container(): draw_svg_pipeline(steps, 3, res)
        with cp.container(): draw_console(log)
        with card2.container(): draw_result("Refined Article", refined)

        draw_actions(refined, "refined_article")
        draw_flow("Refiner", "Validator", refined)

        # validate
        log.append({"t": ts(), "a": "validator", "m": "evaluating quality..."})
        with cp.container(): draw_console(log)
        card3 = st.empty()
        with card3.container(): draw_thinking("Validator Agent")

        t0 = time.time()
        with st.spinner("Validating..."):
            try:
                validation = v.execute(topic=topic, article=refined)
                timings["Validate"] = time.time() - t0
                res[3] = "ok"
                log.append({"t": ts(), "a": "validator", "m": f"✓ done in {timings['Validate']:.1f}s"})
            except Exception as e:
                res[3] = "err"
                log.append({"t": ts(), "a": "validator", "m": f"✗ {e}"})
                with pp.container(): draw_svg_pipeline(steps, 3, res)
                with cp.container(): draw_console(log)
                card3.empty()
                st.error(str(e))
                return

        with pp.container(): draw_svg_pipeline(steps, -1, res)
        with cp.container(): draw_console(log)
        with card3.container(): draw_result("Validation Report", validation)
        draw_score(validation)
        draw_metrics(timings, len(str(refined)))


def run_sanitize(mgr):
    steps = ["Input", "Sanitize", "Validate"]
    data = st.text_area("Paste medical records below", height=180, placeholder="Enter medical data containing PHI...", key="sanitize_input")

    if st.button("Run", type="primary", key="sanitize_run"):
        if not data:
            st.warning("Please enter data to sanitize.")
            return

        agents = (mgr.get_agent("sanitize_data"), mgr.get_agent("sanitize_data_validator"))
        log, res, timings = [], {0: "ok"}, {}
        pp, cp = st.empty(), st.empty()

        log.append({"t": ts(), "a": "sys", "m": f"data received — {len(data)} chars"})
        with pp.container(): draw_svg_pipeline(steps, 1, res)
        with cp.container(): draw_console(log)

        # sanitize
        log.append({"t": ts(), "a": "sanitizer", "m": "removing PHI..."})
        with cp.container(): draw_console(log)
        card1 = st.empty()
        with card1.container(): draw_thinking("Sanitizer")

        t0 = time.time()
        with st.spinner("Sanitizing..."):
            try:
                clean = agents[0].execute(data)
                timings["Sanitize"] = time.time() - t0
                res[1] = "ok"
                log.append({"t": ts(), "a": "sanitizer", "m": f"✓ cleaned in {timings['Sanitize']:.1f}s"})
            except Exception as e:
                res[1] = "err"
                log.append({"t": ts(), "a": "sanitizer", "m": f"✗ {e}"})
                with pp.container(): draw_svg_pipeline(steps, 1, res)
                with cp.container(): draw_console(log)
                card1.empty()
                st.error(str(e))
                return

        with pp.container(): draw_svg_pipeline(steps, 2, res)
        with cp.container(): draw_console(log)
        with card1.container(): draw_result("Sanitized Output", clean)

        draw_actions(clean, "sanitized_data")
        draw_flow("Sanitizer", "Validator", clean)

        # validate
        log.append({"t": ts(), "a": "validator", "m": "verifying removal..."})
        with cp.container(): draw_console(log)
        card2 = st.empty()
        with card2.container(): draw_thinking("Validator")

        t0 = time.time()
        with st.spinner("Validating..."):
            try:
                validation = agents[1].execute(original_data=data, sanitized_data=clean)
                timings["Validate"] = time.time() - t0
                res[2] = "ok"
                log.append({"t": ts(), "a": "validator", "m": f"✓ done in {timings['Validate']:.1f}s"})
            except Exception as e:
                res[2] = "err"
                log.append({"t": ts(), "a": "validator", "m": f"✗ {e}"})
                with pp.container(): draw_svg_pipeline(steps, 2, res)
                with cp.container(): draw_console(log)
                card2.empty()
                st.error(str(e))
                return

        with pp.container(): draw_svg_pipeline(steps, -1, res)
        with cp.container(): draw_console(log)
        with card2.container(): draw_result("Validation Report", validation)
        draw_score(validation)
        draw_metrics(timings, len(str(clean)))


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(page_title="Research AI Workspace", page_icon="◉", layout="wide")
    inject_styles()
    draw_header()

    mgr = AgentManager(max_retries=3, verbose=True)

    tab1, tab2, tab3 = st.tabs(["✍️ Write Article", "📄 Summarize Text", "🛡️ Sanitize Data"])

    with tab1:
        section("Write & Refine Research Article")
        run_write_article(mgr)

    with tab2:
        section("Summarize Medical Text")
        run_summarize(mgr)

    with tab3:
        section("Sanitize Medical Data — PHI Removal")
        run_sanitize(mgr)

    st.divider()
    st.caption("Powered by Llama 3.3 70B via Groq")


if __name__ == "__main__":
    main()
