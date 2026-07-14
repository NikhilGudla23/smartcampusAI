import streamlit as st
import config

def inject_custom_css():
    """Reads style.css and injects it into Streamlit's head."""
    css_file = config.CSS_DIR / "style.css"
    if css_file.exists():
        try:
            with open(css_file, "r", encoding="utf-8") as f:
                css_content = f.read()
            
            theme = st.session_state.get("theme", "dark")
            # Override root tokens dynamically depending on theme preference
            if theme == "light":
                theme_vars = """
                :root {
                    --bg-overlay: rgba(255, 255, 255, 0.7);
                    --card-bg: rgba(255, 255, 255, 0.75);
                    --border-color: rgba(99, 102, 241, 0.15);
                    --text-primary: #1e293b;
                    --text-secondary: #475569;
                    --stApp-bg: #f9fafb;
                }
                """
            else:
                theme_vars = """
                :root {
                    --bg-overlay: rgba(11, 15, 25, 0.85);
                    --card-bg: rgba(255, 255, 255, 0.03);
                    --border-color: rgba(255, 255, 255, 0.08);
                    --text-primary: #f8fafc;
                    --text-secondary: #94a3b8;
                    --stApp-bg: #0b0f19;
                }
                """
            st.markdown(f"<style>{theme_vars}\n{css_content}</style>", unsafe_allow_html=True)
        except Exception:
            pass

def glass_metric(label: str, value: str, icon: str, theme: str = "dark") -> str:
    """HTML code for a glassmorphism metric card."""
    text_color = "#f8fafc" if theme == "dark" else "#1e293b"
    desc_color = "#94a3b8" if theme == "dark" else "#475569"
    border_color = "rgba(255, 255, 255, 0.08)" if theme == "dark" else "rgba(99, 102, 241, 0.15)"
    bg_color = "rgba(255, 255, 255, 0.03)" if theme == "dark" else "rgba(255, 255, 255, 0.45)"
    
    html = f"""<div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 16px; padding: 20px; display: flex; align-items: center; justify-content: space-between; transition: all 0.3s ease; margin-bottom: 10px;"><div style="display: flex; flex-direction: column;"><span style="font-size: 0.85rem; color: {desc_color}; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500;">{label}</span><span style="font-size: 1.8rem; font-weight: 700; color: {text_color}; margin-top: 4px;">{value}</span></div><div style="width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; background: rgba(99, 102, 241, 0.15); color: #818cf8;">{icon}</div></div>"""
    return html.replace("\n", "").strip()

def card_wrapper(title: str, content: str, icon: str = "⚡", theme: str = "dark") -> str:
    """HTML styled wrapper for standard cards."""
    text_color = "#f8fafc" if theme == "dark" else "#1e293b"
    bg_color = "rgba(255, 255, 255, 0.03)" if theme == "dark" else "rgba(255, 255, 255, 0.45)"
    border_color = "rgba(255, 255, 255, 0.08)" if theme == "dark" else "rgba(99, 102, 241, 0.15)"
    
    html = f"""<div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 16px; padding: 20px; color: {text_color}; margin-bottom: 20px;"><div style="display: flex; align-items: center; gap: 8px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 10px; margin-bottom: 15px;"><span style="font-size: 1.25rem;">{icon}</span><h3 style="margin: 0; font-size: 1.2rem; font-weight: 600; color: {text_color};">{title}</h3></div><div>{content}</div></div>"""
    return html.replace("\n", "").strip()

def get_hero_html() -> str:
    """HTML code for the landing page hero section."""
    html = """<div class="hero-wrapper"><div class="hero-gradient"></div><div class="particles-box"><div class="particle" style="width: 8px; height: 8px; left: 10%; top: 40%; animation-delay: 0s; animation-duration: 6s;"></div><div class="particle" style="width: 12px; height: 12px; left: 30%; top: 70%; animation-delay: 1s; animation-duration: 8s;"></div><div class="particle" style="width: 6px; height: 6px; left: 75%; top: 20%; animation-delay: 2s; animation-duration: 5s;"></div><div class="particle" style="width: 10px; height: 10px; left: 85%; top: 60%; animation-delay: 3s; animation-duration: 7s;"></div></div><div class="hero-content"><h1 class="hero-title">SmartCampusAI</h1><p class="hero-subtitle">AI-Powered Smart Campus Management Platform</p><p style="color: #94a3b8; max-width: 600px; margin: 0 auto 30px auto; font-size: 1.1rem; line-height: 1.6;">Unifying academics, administration, and artificial intelligence into a single, seamless, glassmorphic experience.</p></div></div>"""
    return html.replace("\n", "").strip()

def get_feature_card_html(title: str, desc: str, icon: str) -> str:
    """HTML for standard landing features section."""
    html = f"""<div class="feature-card"><div class="feature-icon">{icon}</div><div class="feature-title">{title}</div><div class="feature-desc">{desc}</div></div>"""
    return html.replace("\n", "").strip()
