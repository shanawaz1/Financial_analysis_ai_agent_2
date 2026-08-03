CUSTOM_CSS = """
<style>
body, html {
    height: 100%;
    margin: 0;
    font-family: "Segoe UI", -apple-system, Arial, Helvetica, sans-serif;
    background: linear-gradient(135deg, #0a1f38 0%, #102b4d 55%, #0a1f38 100%);
    color: #e6eef9;
}
.gradio-container {
    background: rgba(13, 28, 45, 0.88) !important;
    color: #e6eef9 !important;
    padding: 32px !important;
    border-radius: 18px !important;
    max-width: 1000px !important;
    margin: 24px auto !important;
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    box-shadow: 0 14px 44px rgba(0, 0, 0, 0.45) !important;
}
.gradio-container h1,
.gradio-container h2,
.gradio-container h3,
.gradio-container label,
.gradio-container span,
.gradio-container p {
    color: #e6eef9 !important;
}
.gradio-container .gr-box,
.gradio-container .gr-form,
.gradio-container .gr-panel {
    background: #0e2238 !important;
    border: 1px solid #27415f !important;
    border-radius: 12px !important;
}
input, textarea, select {
    background-color: #0b1c30 !important;
    color: #e6eef9 !important;
    border: 1px solid #2c4a6e !important;
    border-radius: 10px !important;
    padding: 10px 12px !important;
    font-size: 15px !important;
}
input::placeholder, textarea::placeholder {
    color: #6f8cac !important;
}
input:focus, textarea:focus, select:focus {
    outline: none !important;
    border-color: #12b981 !important;
    box-shadow: 0 0 0 3px rgba(18, 185, 129, 0.18) !important;
}
button, .gr-button {
    background-color: #12b981 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 4px 12px rgba(18, 185, 129, 0.25) !important;
}
button:hover, .gr-button:hover {
    background-color: #0fa66f !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(18, 185, 129, 0.35) !important;
}
.tab-nav button {
    background: transparent !important;
    color: #93aecb !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    padding: 12px 20px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
}
.tab-nav button:hover {
    color: #e6eef9 !important;
}
.tab-nav button[aria-selected="true"] {
    background: transparent !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-bottom: 3px solid #12b981 !important;
}
.gradio-container .gr-highlighted-text,
.gradio-container .gr-textbox {
    border-color: #2c4a6e !important;
}
#logo {
    position: absolute;
    top: 24px;
    right: 26px;
    width: 72px;
    height: auto;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    z-index: 1000;
}
footer, .gradio-container footer {
    color: #5b7696 !important;
}
.gradio-container .gr-status, .gradio-container .message {
    color: #b8cfe6 !important;
}
::-webkit-scrollbar {
    width: 10px;
}
::-webkit-scrollbar-track {
    background: #0a1c31;
}
::-webkit-scrollbar-thumb {
    background: #2c4a6e;
    border-radius: 6px;
}
::-webkit-scrollbar-thumb:hover {
    background: #12b981;
}
</style>
"""
