"""
SafarPak - Pakistan's Ultimate Travel Companion
Premium UI with themes, accessibility, responsive design, drive mode & offline support
"""

import streamlit as st
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium
import time
import json
import base64
from datetime import datetime
from dijkstra import load_cities, build_graph, dijkstra, calculate_distance_km
from locations_data import get_all_locations, get_location_categories


# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="SafarPak",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None  # Disable menu
)

# Add viewport meta tag for proper mobile rendering and early warning suppression
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<script>
    // Early warning suppression - runs immediately to catch Streamlit warnings
    (function() {
        const suppressPatterns = [
            'Unrecognized feature:', 'ambient-light-sensor', 'battery', 'document-domain',
            'layout-animations', 'legacy-image-formats', 'oversized-images', 'vr', 'wake-lock',
            'iframe which has both allow-scripts and allow-same-origin',
            'A form field element should have an id or name attribute',
            'form field element has neither an id nor a name attribute',
            'No label associated with a form field', 'index.CqTPbV5Y.js', 'Understand this warning'
        ];
        
        function shouldSuppress(msg) {
            return suppressPatterns.some(p => msg && msg.includes && msg.includes(p));
        }
        
        const origWarn = console.warn;
        const origError = console.error;
        const origLog = console.log;
        
        console.warn = function(...args) {
            if (!shouldSuppress(args.join(' '))) origWarn.apply(console, args);
        };
        console.error = function(...args) {
            if (!shouldSuppress(args.join(' '))) origError.apply(console, args);
        };
        console.log = function(...args) {
            if (!shouldSuppress(args.join(' '))) origLog.apply(console, args);
        };
    })();
</script>
""", unsafe_allow_html=True)


# ==================== THEME SYSTEM ====================
def get_theme_css(theme):
    """Return CSS for different themes."""
    
    themes = {
        "dark": {
            "bg_primary": "#0a0a0f",
            "bg_secondary": "#12121a",
            "bg_card": "#1a1a24",
            "bg_card_hover": "#22222e",
            "accent": "#22c55e",
            "accent_hover": "#16a34a",
            "text_primary": "#fafafa",
            "text_secondary": "#a1a1aa",
            "text_muted": "#71717a",
            "border": "#27272a",
            "success": "#22c55e",
            "warning": "#f59e0b",
            "error": "#ef4444",
            "info": "#3b82f6",
        },
        "light": {
            "bg_primary": "#fafafa",
            "bg_secondary": "#f4f4f5",
            "bg_card": "#ffffff",
            "bg_card_hover": "#f4f4f5",
            "accent": "#16a34a",
            "accent_hover": "#15803d",
            "text_primary": "#18181b",
            "text_secondary": "#52525b",
            "text_muted": "#a1a1aa",
            "border": "#e4e4e7",
            "success": "#16a34a",
            "warning": "#d97706",
            "error": "#dc2626",
            "info": "#2563eb",
        },
        "colorblind": {
            "bg_primary": "#0a0a0f",
            "bg_secondary": "#12121a",
            "bg_card": "#1a1a24",
            "bg_card_hover": "#22222e",
            "accent": "#0077bb",  # Blue - safe for most color blindness
            "accent_hover": "#005588",
            "text_primary": "#fafafa",
            "text_secondary": "#a1a1aa",
            "text_muted": "#71717a",
            "border": "#27272a",
            "success": "#0077bb",  # Blue instead of green
            "warning": "#ee7733",  # Orange - distinguishable
            "error": "#cc3311",    # Red-orange
            "info": "#33bbee",     # Cyan
        }
    }
    
    t = themes.get(theme, themes["dark"])
    
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        :root {{
            --bg-primary: {t['bg_primary']};
            --bg-secondary: {t['bg_secondary']};
            --bg-card: {t['bg_card']};
            --bg-card-hover: {t['bg_card_hover']};
            --accent: {t['accent']};
            --accent-hover: {t['accent_hover']};
            --text-primary: {t['text_primary']};
            --text-secondary: {t['text_secondary']};
            --text-muted: {t['text_muted']};
            --border: {t['border']};
            --success: {t['success']};
            --warning: {t['warning']};
            --error: {t['error']};
            --info: {t['info']};
        }}
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            box-sizing: border-box;
        }}
        
        *::before, *::after {{
            box-sizing: border-box;
        }}
        
        /* Mobile-first: Base font size */
        html {{
            font-size: 16px;
        }}
        
        /* Better text rendering on mobile */
        body {{
            text-rendering: optimizeLegibility;
            -webkit-text-size-adjust: 100%;
            -moz-text-size-adjust: 100%;
            text-size-adjust: 100%;
        }}
        
        html, body {{
            overflow-y: auto !important;
            overflow-x: hidden !important;
            height: auto !important;
            max-height: none !important;
            touch-action: pan-y !important;
            -webkit-overflow-scrolling: touch !important;
            overscroll-behavior: auto !important;
            /* Safe area insets for notched devices */
            padding-left: env(safe-area-inset-left);
            padding-right: env(safe-area-inset-right);
            padding-top: env(safe-area-inset-top);
            padding-bottom: env(safe-area-inset-bottom);
        }}
        
        .stApp {{
            background: var(--bg-primary);
            overflow-y: auto !important;
            overflow-x: hidden !important;
            height: auto !important;
            max-height: none !important;
            touch-action: pan-y !important;
            -webkit-overflow-scrolling: touch !important;
            overscroll-behavior: auto !important;
        }}
        
        [data-testid="stAppViewContainer"] {{
            overflow-y: auto !important;
            overflow-x: hidden !important;
            height: auto !important;
            max-height: none !important;
            touch-action: pan-y !important;
            -webkit-overflow-scrolling: touch !important;
            overscroll-behavior: auto !important;
        }}
        
        [data-testid="stMain"] {{
            overflow-y: auto !important;
            overflow-x: hidden !important;
            height: auto !important;
            max-height: none !important;
            touch-action: pan-y !important;
            -webkit-overflow-scrolling: touch !important;
            overscroll-behavior: auto !important;
        }}
        
        /* Ensure all scrollable elements allow wheel and touch events */
        * {{
            touch-action: pan-y !important;
        }}
        
        /* Remove any pointer-events that might block scrolling */
        main, [data-testid="stMain"], [data-testid="stAppViewContainer"] {{
            pointer-events: auto !important;
        }}
        
        #MainMenu, footer {{visibility: hidden;}}
        
        /* Force header and sidebar toggle to be visible */
        header {{
            visibility: visible !important;
            display: block !important;
        }}
        
        /* Ensure sidebar can be toggled */
        [data-testid="stSidebar"],
        section[data-testid="stSidebar"] {{
            transition: transform 0.3s ease, opacity 0.3s ease !important;
            z-index: 999 !important;
        }}
        
        /* Mobile sidebar overlay/backdrop */
        @media (max-width: 768px) {{
            /* Add overlay when sidebar is open on mobile */
            [data-testid="stSidebar"][aria-expanded="true"]::before,
            section[data-testid="stSidebar"][aria-expanded="true"]::before {{
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                z-index: 998;
                pointer-events: auto;
            }}
            
            /* Ensure sidebar closes properly on mobile */
            [data-testid="stSidebar"] {{
                position: fixed !important;
                height: 100vh !important;
                top: 0 !important;
                transform: translateX(-100%) !important;
                transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }}
            
            [data-testid="stSidebar"][aria-expanded="true"],
            section[data-testid="stSidebar"][aria-expanded="true"] {{
                transform: translateX(0) !important;
            }}
            
            /* Prevent body scroll when sidebar is open */
            body:has([data-testid="stSidebar"][aria-expanded="true"]) {{
                overflow: hidden !important;
            }}
        }}
        
        /* Hide ONLY Deploy button and 3-dot menu button - be very specific - MUST COME FIRST */
        /* Target Deploy button specifically - very aggressive selectors */
        [data-testid="stHeader"] button[aria-label*="Deploy"],
        [data-testid="stHeader"] button[aria-label*="deploy"],
        [data-testid="stHeader"] button[aria-label*="Deploy app"],
        button[kind="header"][aria-label*="Deploy"],
        button[kind="header"][aria-label*="deploy"],
        [data-testid="manage-app-button"],
        [data-testid="stHeader"] > div:last-child button[aria-label*="Deploy"],
        [data-testid="stHeader"] > div:last-child > div button[aria-label*="Deploy"],
        /* Target 3-dot menu button (Settings/Menu) - but NOT sidebar toggle */
        [data-testid="stHeader"] button[aria-label*="Settings"]:not([aria-label*="sidebar"]),
        [data-testid="stHeader"] button[aria-label*="settings"]:not([aria-label*="sidebar"]),
        [data-testid="stHeader"] button[aria-label*="Menu"]:not([aria-label*="sidebar"]),
        [data-testid="stHeader"] button[aria-label*="menu"]:not([aria-label*="sidebar"]),
        [data-testid="stHeader"] button[aria-label*="More options"],
        button[kind="header"][aria-label*="Settings"]:not([aria-label*="sidebar"]),
        button[kind="header"][aria-label*="Menu"]:not([aria-label*="sidebar"]) {{
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            width: 0 !important;
            height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }}
        
        /* Hide deploy menu items */
        [data-baseweb="popover"] [role="menuitem"],
        [data-baseweb="menu"] [role="menuitem"] {{
            display: none !important;
        }}
        
        /* Keep header visible for sidebar toggle */
        header[data-testid="stHeader"] {{
            background: transparent !important;
            height: auto !important;
            padding: 0.5rem !important;
            position: relative !important;
            z-index: 1000 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            flex-wrap: wrap !important;
        }}
        
        /* Hide Streamlit logo/title in header but keep toggle */
        [data-testid="stHeader"] a[href],
        [data-testid="stHeader"] a[href] img {{
            display: none !important;
        }}
        
        /* Don't hide button containers - ensure all buttons are visible by default */
        [data-testid="stHeader"] > div,
        [data-testid="stHeader"] > div > div {{
            display: flex !important;
        }}
        
        /* Remove ONLY the white 3-line toggle button - keep sidebar content */
        button[name="keyboard_double_arrow_left"],
        section[data-testid="stSidebar"] button[name="keyboard_double_arrow_left"],
        section[data-testid="stSidebar"] > div:first-child button[name="keyboard_double_arrow_left"],
        section[data-testid="stSidebar"] > div:first-child > div button[name="keyboard_double_arrow_left"] {{
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            width: 0 !important;
            height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            position: absolute !important;
            left: -9999px !important;
            top: -9999px !important;
            clip: rect(0,0,0,0) !important;
        }}
        
        /* Ensure sidebar toggle button is ALWAYS visible - comprehensive selectors */
        [data-testid="stHeader"] button[aria-label*="sidebar"]:not([aria-label*="menu"]),
        [data-testid="stHeader"] button[aria-label*="Sidebar"]:not([aria-label*="Menu"]),
        [data-testid="stHeader"] > div:first-child button:not(:first-child),
        [data-testid="stHeader"] > div:first-child > div button:not(:first-child),
        [data-testid="stHeader"] > div:first-child > div:first-child button:not(:first-child),
        header > div:first-child button:not(:first-child) {{
            visibility: visible !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            background: var(--accent) !important;
            border: 2px solid var(--accent) !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            padding: 0.6rem 0.9rem !important;
            font-weight: 700 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
            cursor: pointer !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            position: relative !important;
            z-index: 1001 !important;
            min-width: 40px !important;
            min-height: 40px !important;
            touch-action: manipulation !important;
            -webkit-tap-highlight-color: rgba(34, 197, 94, 0.3) !important;
            user-select: none !important;
        }}
        
        [data-testid="stHeader"] > div:first-child button:not(:first-child):hover,
        [data-testid="stHeader"] button[aria-label*="sidebar"]:not([aria-label*="menu"]):hover {{
            background: var(--accent-hover) !important;
            border-color: var(--accent-hover) !important;
            transform: translateY(-3px) scale(1.08) !important;
            box-shadow: 0 6px 16px rgba(34, 197, 94, 0.5) !important;
        }}
        
        [data-testid="stHeader"] button:not(:first-child):active,
        button[kind="header"]:not(:first-of-type):active {{
            transform: translateY(-1px) scale(1.02) !important;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.1s ease !important;
        }}
        
        /* Additional fallback - target any button in header area */
        header > div > div button,
        [data-testid="stHeader"] > div > div > button,
        [data-testid="stHeader"] > div:last-child button {{
            visibility: visible !important;
            display: inline-flex !important;
            background: var(--accent) !important;
            border: 2px solid var(--accent) !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            padding: 0.6rem 0.9rem !important;
            font-weight: 700 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
            cursor: pointer !important;
            opacity: 1 !important;
            z-index: 1001 !important;
            touch-action: manipulation !important;
            -webkit-tap-highlight-color: rgba(34, 197, 94, 0.3) !important;
            user-select: none !important;
            min-width: 40px !important;
            min-height: 40px !important;
        }}
        
        header > div > div button:hover,
        [data-testid="stHeader"] > div > div > button:hover {{
            background: var(--accent-hover) !important;
            border-color: var(--accent-hover) !important;
            transform: translateY(-3px) scale(1.08) !important;
            box-shadow: 0 6px 16px rgba(34, 197, 94, 0.5) !important;
        }}
        
        /* ===== RESPONSIVE CONTAINER ===== */
        .main-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem;
        }}
        
        @media (max-width: 768px) {{
            .main-container {{
                padding: 0.5rem;
            }}
        }}
        
        /* ===== HEADER ===== */
        .app-header {{
            text-align: center;
            padding: 2rem 1rem;
            margin-top: 1rem;
            margin-bottom: 1.5rem;
        }}
        
        .app-logo {{
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
        }}
        
        @media (max-width: 768px) {{
            .app-logo {{
                font-size: 2.5rem;
            }}
        }}
        
        .app-title {{
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 800;
            color: var(--accent);
            margin: 0;
            letter-spacing: -1px;
        }}
        
        .app-subtitle {{
            color: var(--text-secondary);
            font-size: clamp(0.875rem, 2vw, 1rem);
            margin-top: 0.5rem;
            font-weight: 400;
        }}
        
        /* ===== CARDS ===== */
        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.2s ease;
        }}
        
        .card:hover {{
            border-color: var(--accent);
            background: var(--bg-card-hover);
        }}
        
        @media (max-width: 768px) {{
            .card {{
                padding: 1rem;
                border-radius: 12px;
            }}
        }}
        
        /* ===== INPUT SECTION ===== */
        .input-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 1rem;
        }}
        
        @media (max-width: 768px) {{
            .input-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .input-card {{
            background: var(--bg-card);
            border: 2px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            transition: all 0.2s ease;
        }}
        
        .input-card:focus-within {{
            border-color: var(--accent);
        }}
        
        .input-label {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-secondary);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }}
        
        .input-icon {{
            font-size: 1.25rem;
        }}
        
        /* ===== DROPDOWNS ===== */
        .stSelectbox > div > div {{
            background: var(--bg-secondary) !important;
            border: 2px solid var(--border) !important;
            border-radius: 10px !important;
            color: var(--text-primary) !important;
            font-weight: 500 !important;
        }}
        
        .stSelectbox > div > div:focus-within {{
            border-color: var(--accent) !important;
        }}
        
        [data-baseweb="select"] > div {{
            background: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
        }}
        
        [data-baseweb="menu"] {{
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
        }}
        
        [data-baseweb="menu"] li {{
            color: var(--text-primary) !important;
        }}
        
        [data-baseweb="menu"] li:hover {{
            background: var(--accent) !important;
            color: var(--bg-primary) !important;
        }}
        
        [data-baseweb="select"] span {{
            color: var(--text-primary) !important;
        }}
        
        /* ===== BUTTONS ===== */
        .stButton > button {{
            background: var(--accent) !important;
            color: var(--bg-primary) !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.875rem 2rem !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100%;
            min-height: 44px !important;
            touch-action: manipulation !important;
            -webkit-tap-highlight-color: rgba(34, 197, 94, 0.2) !important;
            user-select: none !important;
            cursor: pointer !important;
            position: relative !important;
            overflow: hidden !important;
        }}
        
        .stButton > button::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }}
        
        .stButton > button:active::before {{
            width: 300px;
            height: 300px;
        }}
        
        .stButton > button:hover {{
            background: var(--accent-hover) !important;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }}
        
        .stButton > button:active {{
            transform: translateY(0) scale(0.98) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
        }}
        
        .stButton > button:focus-visible {{
            outline: 3px solid var(--accent);
            outline-offset: 2px;
        }}
        
        /* Mobile button sizes - smaller and better for phones */
        @media (max-width: 480px) {{
            .stButton > button {{
                padding: 0.625rem 1.25rem !important;
                font-size: 0.875rem !important;
                min-height: 40px !important;
                border-radius: 10px !important;
                font-weight: 600 !important;
            }}
            
            /* Radio buttons smaller on mobile */
            .stRadio > div > label {{
                padding: 0.5rem 0.75rem !important;
                font-size: 0.85rem !important;
                min-height: 38px !important;
            }}
            
            /* Smaller tabs on mobile */
            .stTabs [data-baseweb="tab"] {{
                padding: 0.5rem 0.75rem !important;
                font-size: 0.75rem !important;
                min-height: 38px !important;
            }}
        }}
        
        @media (min-width: 481px) and (max-width: 767px) {{
            .stButton > button {{
                padding: 0.7rem 1.5rem !important;
                font-size: 0.9rem !important;
                min-height: 42px !important;
                border-radius: 11px !important;
            }}
            
            .stRadio > div > label {{
                padding: 0.6rem 0.875rem !important;
                font-size: 0.9rem !important;
                min-height: 40px !important;
            }}
        }}
        
        /* ===== SETTINGS ROW ===== */
        .settings-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }}
        
        .setting-item {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.75rem 1rem;
            transition: all 0.2s ease;
        }}
        
        .setting-item:focus-within {{
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
        }}
        
        .setting-label {{
            color: var(--text-secondary);
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.25rem;
        }}
        
        /* ===== STATS GRID ===== */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin: 1.5rem 0;
        }}
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem;
            text-align: center;
            transition: all 0.2s ease;
        }}
        
        .stat-card:hover {{
            border-color: var(--accent);
            transform: translateY(-3px);
        }}
        
        .stat-value {{
            color: var(--accent);
            font-size: clamp(1.5rem, 4vw, 2rem);
            font-weight: 800;
            line-height: 1;
        }}
        
        .stat-label {{
            color: var(--text-muted);
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0.5rem;
        }}
        
        /* ===== ROUTE DISPLAY ===== */
        .route-card {{
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
            border: 2px solid var(--accent);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        
        .route-label {{
            color: var(--accent);
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 0.75rem;
        }}
        
        .route-path {{
            color: var(--text-primary);
            font-size: clamp(1rem, 2.5vw, 1.25rem);
            font-weight: 500;
            line-height: 1.8;
            word-wrap: break-word;
        }}
        
        .route-arrow {{
            color: var(--accent);
            margin: 0 0.5rem;
        }}
        
        /* ===== STOPS BADGES ===== */
        .stops-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            align-items: center;
            margin: 1rem 0;
        }}
        
        .stop-badge {{
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            white-space: nowrap;
        }}
        
        .stop-start {{
            background: var(--success);
            color: var(--bg-primary);
        }}
        
        .stop-mid {{
            background: var(--info);
            color: white;
        }}
        
        .stop-end {{
            background: var(--error);
            color: white;
        }}
        
        .stop-arrow {{
            color: var(--text-muted);
            font-size: 1.25rem;
        }}
        
        /* ===== NAV STEPS ===== */
        .nav-step {{
            background: var(--bg-card);
            border-left: 4px solid var(--accent);
            border-radius: 0 12px 12px 0;
            padding: 1rem 1.25rem;
            margin: 0.75rem 0;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        @media (max-width: 768px) {{
            .nav-step {{
                padding: 0.875rem 1rem;
                gap: 0.75rem;
            }}
        }}
        
        .nav-number {{
            background: var(--accent);
            color: var(--bg-primary);
            min-width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.875rem;
        }}
        
        .nav-content {{
            flex: 1;
        }}
        
        .nav-cities {{
            color: var(--text-primary);
            font-weight: 600;
            font-size: 1rem;
        }}
        
        .nav-meta {{
            color: var(--accent);
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }}
        
        /* ===== PLACE CARDS ===== */
        .place-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: all 0.2s ease;
        }}
        
        .place-card:hover {{
            border-color: var(--accent);
            background: var(--bg-card-hover);
        }}
        
        .place-icon {{
            font-size: 1.75rem;
            min-width: 45px;
            text-align: center;
        }}
        
        .place-info {{
            flex: 1;
            min-width: 0;
        }}
        
        .place-name {{
            color: var(--text-primary);
            font-weight: 600;
            font-size: 1rem;
            margin: 0;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        .place-detail {{
            color: var(--text-muted);
            font-size: 0.8rem;
            margin: 0.25rem 0;
        }}
        
        .place-rating {{
            color: var(--warning);
            font-size: 0.875rem;
        }}
        
        .place-distance {{
            color: var(--accent);
            font-weight: 700;
            font-size: 0.875rem;
            white-space: nowrap;
        }}
        
        /* ===== MAP CONTAINER ===== */
        .map-container {{
            border-radius: 16px;
            overflow: hidden;
            border: 2px solid var(--accent);
        }}
        
        /* ===== FUEL BREAKDOWN ===== */
        .fuel-breakdown {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
        }}
        
        .fuel-title {{
            color: var(--accent);
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }}
        
        .fuel-details {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}
        
        .fuel-total {{
            color: var(--accent);
            font-weight: 700;
        }}
        
        /* ===== TABS ===== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.25rem;
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 0.25rem;
            flex-wrap: wrap;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: transparent;
            border-radius: 10px;
            color: var(--text-secondary);
            font-weight: 600;
            padding: 0.625rem 1rem;
            font-size: 0.8rem;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: var(--accent) !important;
            color: var(--bg-primary) !important;
        }}
        
        @media (max-width: 768px) {{
            .stTabs [data-baseweb="tab"] {{
                padding: 0.5rem 0.75rem;
                font-size: 0.7rem;
            }}
        }}
        
        /* ===== SUCCESS/ERROR BANNERS ===== */
        .success-banner {{
            background: var(--bg-card);
            border: 2px solid var(--success);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            margin: 1rem 0;
        }}
        
        .success-text {{
            color: var(--success);
            font-weight: 600;
        }}
        
        .error-banner {{
            background: var(--bg-card);
            border: 2px solid var(--error);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        }}
        
        .error-title {{
            color: var(--error);
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .error-text {{
            color: var(--text-secondary);
        }}
        
        /* ===== SIDEBAR ===== */
        [data-testid="stSidebar"] {{
            background: var(--bg-secondary);
        }}
        
        [data-testid="stSidebar"] .stMarkdown {{
            color: var(--text-primary);
        }}
        
        .sidebar-section {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
        }}
        
        .sidebar-title {{
            color: var(--accent);
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.75rem;
        }}
        
        /* ===== SLIDERS ===== */
        .stSlider > div > div > div {{
            background: var(--accent) !important;
        }}
        
        /* ===== THEME TOGGLE ===== */
        .theme-toggle {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.75rem;
            margin-bottom: 1rem;
        }}
        
        .theme-label {{
            color: var(--text-secondary);
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }}
        
        /* ===== LIVE BADGE ===== */
        .live-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--bg-card);
            border: 1px solid var(--success);
            border-radius: 20px;
            padding: 0.375rem 0.875rem;
            margin-bottom: 1rem;
        }}
        
        .live-dot {{
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
        }}
        
        .live-text {{
            color: var(--success);
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* ===== WEATHER WIDGETS ===== */
        .weather-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }}
        
        .weather-card {{
            background: var(--info);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            color: white;
        }}
        
        .weather-icon {{
            font-size: 2rem;
        }}
        
        .weather-temp {{
            font-size: 1.5rem;
            font-weight: 800;
        }}
        
        .weather-city {{
            font-size: 0.8rem;
            opacity: 0.9;
        }}
        
        /* ===== FOOTER ===== */
        .footer {{
            text-align: center;
            padding: 2rem 1rem;
            color: var(--text-muted);
            font-size: 0.875rem;
            border-top: 1px solid var(--border);
            margin-top: 2rem;
        }}
        
        /* ===== DRIVE MODE ===== */
        .drive-mode {{
            background: #000;
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        
        .drive-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #222;
        }}
        
        .drive-status {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .drive-live {{
            width: 12px;
            height: 12px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }}
        
        .drive-label {{
            color: #22c55e;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .drive-current {{
            background: linear-gradient(135deg, #1a1a2e 0%, #0a0a0f 100%);
            border: 2px solid #22c55e;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 1rem;
        }}
        
        .drive-direction {{
            color: #22c55e;
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }}
        
        .drive-instruction {{
            color: #fff;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .drive-distance {{
            color: #22c55e;
            font-size: 2.5rem;
            font-weight: 800;
        }}
        
        .drive-unit {{
            color: #666;
            font-size: 1rem;
            margin-left: 0.25rem;
        }}
        
        .drive-next {{
            background: #111;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }}
        
        .drive-next-label {{
            color: #666;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }}
        
        .drive-next-text {{
            color: #fff;
            font-size: 1rem;
            font-weight: 500;
        }}
        
        .drive-progress {{
            background: #111;
            border-radius: 12px;
            padding: 1rem;
        }}
        
        .drive-progress-bar {{
            background: #222;
            border-radius: 8px;
            height: 8px;
            overflow: hidden;
            margin-bottom: 0.75rem;
        }}
        
        .drive-progress-fill {{
            background: linear-gradient(90deg, #22c55e, #4ade80);
            height: 100%;
            border-radius: 8px;
            transition: width 0.5s ease;
        }}
        
        .drive-stats {{
            display: flex;
            justify-content: space-between;
            color: #888;
            font-size: 0.85rem;
        }}
        
        .drive-eta {{
            color: #22c55e;
            font-weight: 600;
        }}
        
        /* ===== SAVE OFFLINE ===== */
        .offline-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
        }}
        
        .offline-title {{
            color: var(--text-primary);
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        
        .offline-desc {{
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-bottom: 0.75rem;
        }}
        
        .download-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--accent);
            color: var(--bg-primary);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.85rem;
            text-decoration: none;
            transition: all 0.2s ease;
            min-height: 40px;
            touch-action: manipulation;
        }}
        
        .download-btn:hover {{
            background: var(--accent-hover);
            transform: translateY(-1px);
        }}
        
        /* Mobile download button */
        @media (max-width: 480px) {{
            .download-btn {{
                padding: 0.5rem 0.875rem !important;
                font-size: 0.8rem !important;
                min-height: 38px !important;
                border-radius: 8px !important;
            }}
        }}
        
        /* ===== FORM INPUTS - BEST PRACTICES ===== */
        input[type="text"],
        input[type="number"],
        input[type="email"],
        input[type="tel"],
        input[type="url"],
        select,
        textarea {{
            font-size: 16px !important; /* Prevents zoom on iOS */
            min-height: 44px !important;
            padding: 0.75rem 1rem !important;
            border-radius: 10px !important;
            touch-action: manipulation !important;
            -webkit-appearance: none !important;
            appearance: none !important;
            transition: all 0.2s ease !important;
        }}
        
        input:focus,
        select:focus,
        textarea:focus {{
            outline: none !important;
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1) !important;
        }}
        
        /* ===== CARDS - IMPROVED MOBILE ===== */
        .card,
        .route-card,
        .place-card,
        .offline-card {{
            will-change: transform;
            backface-visibility: hidden;
            -webkit-backface-visibility: hidden;
        }}
        
        /* ===== LOADING STATES ===== */
        @keyframes shimmer {{
            0% {{
                background-position: -1000px 0;
            }}
            100% {{
                background-position: 1000px 0;
            }}
        }}
        
        .loading {{
            background: linear-gradient(
                90deg,
                var(--bg-card) 0%,
                var(--bg-secondary) 50%,
                var(--bg-card) 100%
            );
            background-size: 1000px 100%;
            animation: shimmer 2s infinite;
        }}
        
        /* ===== PERFORMANCE OPTIMIZATIONS ===== */
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {{
            contain: layout style paint;
            will-change: scroll-position;
        }}
        
        /* ===== SMOOTH SCROLLING ===== */
        html {{
            scroll-behavior: smooth;
        }}
        
        @media (prefers-reduced-motion: reduce) {{
            html {{
                scroll-behavior: auto;
            }}
        }}
        
        /* ===== BETTER TOUCH TARGETS ===== */
        button,
        a,
        input[type="button"],
        input[type="submit"],
        input[type="reset"],
        [role="button"] {{
            min-height: 44px !important;
            min-width: 44px !important;
            touch-action: manipulation !important;
            -webkit-tap-highlight-color: rgba(34, 197, 94, 0.2) !important;
        }}
        
        /* ===== IMPROVED TYPOGRAPHY SCALING ===== */
        h1 {{
            font-size: clamp(1.75rem, 5vw, 2.5rem) !important;
            line-height: 1.2 !important;
            font-weight: 800 !important;
        }}
        
        h2 {{
            font-size: clamp(1.5rem, 4vw, 2rem) !important;
            line-height: 1.3 !important;
            font-weight: 700 !important;
        }}
        
        h3 {{
            font-size: clamp(1.25rem, 3vw, 1.5rem) !important;
            line-height: 1.4 !important;
            font-weight: 600 !important;
        }}
        
        p, .stMarkdown {{
            font-size: clamp(0.875rem, 2vw, 1rem) !important;
            line-height: 1.6 !important;
        }}
        
        /* ===== IMPROVED SPACING ===== */
        .stContainer,
        .main-container {{
            padding-left: max(1rem, env(safe-area-inset-left)) !important;
            padding-right: max(1rem, env(safe-area-inset-right)) !important;
        }}
        
        /* ===== BETTER VISUAL HIERARCHY ===== */
        .stat-value,
        .drive-distance,
        .route-path {{
            font-weight: 800;
            letter-spacing: -0.5px;
        }}
        
        /* ===== IMPROVED ANIMATIONS ===== */
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .card,
        .route-card,
        .place-card {{
            animation: fadeIn 0.3s ease-out;
        }}
        
        /* ===== ACCESSIBILITY ===== */
        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
            }}
            
            .card,
            .route-card,
            .place-card {{
                animation: none !important;
            }}
        }}
        
        /* Focus indicators for keyboard navigation */
        *:focus-visible {{
            outline: 3px solid var(--accent) !important;
            outline-offset: 2px !important;
            border-radius: 4px !important;
        }}
        
        /* Skip to content link for accessibility */
        .skip-link {{
            position: absolute;
            top: -40px;
            left: 0;
            background: var(--accent);
            color: var(--bg-primary);
            padding: 0.5rem 1rem;
            text-decoration: none;
            z-index: 10000;
        }}
        
        .skip-link:focus {{
            top: 0;
        }}
        
        /* ===== IMPROVED CONTRAST ===== */
        @media (prefers-contrast: high) {{
            .card,
            .route-card,
            .place-card {{
                border-width: 2px !important;
            }}
            
            button {{
                border: 2px solid currentColor !important;
            }}
        }}
        
        /* ===== DARK MODE SUPPORT ===== */
        @media (prefers-color-scheme: dark) {{
            /* Already handled by theme system */
        }}
        
        /* ===== PRINT STYLES ===== */
        @media print {{
            .stSidebar,
            [data-testid="stSidebar"],
            header,
            [data-testid="stHeader"],
            .footer {{
                display: none !important;
            }}
            
            .card,
            .route-card {{
                break-inside: avoid;
                page-break-inside: avoid;
            }}
        }}
        
        /* ===== RESPONSIVE MEDIA QUERIES ===== */
        
        /* Large Desktop (1440px and above) */
        @media (min-width: 1440px) {{
            .stApp {{
                max-width: 1600px;
                margin: 0 auto;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(4, 1fr);
                gap: 1.5rem;
            }}
            
            .route-card {{
                padding: 2rem;
            }}
            
            .place-card {{
                padding: 1.5rem;
            }}
        }}
        
        /* Desktop (1024px to 1439px) */
        @media (min-width: 1024px) and (max-width: 1439px) {{
            .stats-grid {{
                grid-template-columns: repeat(4, 1fr);
            }}
            
            .settings-grid {{
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            }}
        }}
        
        /* Tablet (768px to 1023px) */
        @media (min-width: 768px) and (max-width: 1023px) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 0.75rem;
            }}
            
            .stat-card {{
                padding: 1rem;
            }}
            
            .stat-value {{
                font-size: 1.5rem;
            }}
            
            .route-card {{
                padding: 1.25rem;
            }}
            
            .route-path {{
                font-size: 1rem;
            }}
            
            .settings-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 0.75rem;
            }}
            
            .stButton > button {{
                padding: 0.75rem 1.5rem;
                font-size: 0.9rem;
            }}
            
            .nav-step {{
                padding: 0.875rem 1rem;
                flex-direction: row;
            }}
            
            .place-card {{
                padding: 0.875rem;
                gap: 0.75rem;
            }}
            
            .place-icon {{
                font-size: 1.5rem;
                min-width: 40px;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                padding: 0.5rem 0.875rem;
                font-size: 0.75rem;
            }}
            
            .drive-instruction {{
                font-size: 1.25rem;
            }}
            
            .drive-distance {{
                font-size: 2rem;
            }}
            
            [data-testid="stHeader"] {{
                padding: 0.5rem 1rem !important;
            }}
        }}
        
        /* Mobile Landscape / Small Tablet (481px to 767px) */
        @media (min-width: 481px) and (max-width: 767px) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 0.5rem;
            }}
            
            .stat-card {{
                padding: 0.875rem;
            }}
            
            .stat-value {{
                font-size: 1.25rem;
            }}
            
            .stat-label {{
                font-size: 0.65rem;
            }}
            
            .route-card {{
                padding: 1rem;
                margin: 0.75rem 0;
            }}
            
            .route-path {{
                font-size: 0.9rem;
                line-height: 1.6;
            }}
            
            .settings-grid {{
                grid-template-columns: 1fr;
                gap: 0.5rem;
            }}
            
            .setting-item {{
                padding: 0.625rem 0.875rem;
            }}
            
            .stButton > button {{
                padding: 0.75rem 1.25rem;
                font-size: 0.875rem;
            }}
            
            .nav-step {{
                padding: 0.75rem;
                gap: 0.625rem;
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .nav-number {{
                min-width: 28px;
                height: 28px;
                font-size: 0.75rem;
            }}
            
            .nav-cities {{
                font-size: 0.9rem;
            }}
            
            .nav-meta {{
                font-size: 0.8rem;
            }}
            
            .place-card {{
                padding: 0.75rem;
                gap: 0.625rem;
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .place-icon {{
                font-size: 1.5rem;
            }}
            
            .place-name {{
                font-size: 0.9rem;
            }}
            
            .place-detail {{
                font-size: 0.75rem;
            }}
            
            .stops-container {{
                gap: 0.375rem;
            }}
            
            .stop-badge {{
                padding: 0.375rem 0.75rem;
                font-size: 0.7rem;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                padding: 0.5rem 0.625rem;
                font-size: 0.7rem;
            }}
            
            .drive-mode {{
                padding: 1rem;
            }}
            
            .drive-instruction {{
                font-size: 1.1rem;
            }}
            
            .drive-distance {{
                font-size: 1.75rem;
            }}
            
            .drive-current {{
                padding: 1rem;
            }}
            
            .footer {{
                padding: 1.5rem 1rem;
                font-size: 0.8rem;
            }}
            
            [data-testid="stHeader"] {{
                padding: 0.5rem 0.75rem !important;
                flex-wrap: nowrap !important;
                gap: 0.5rem !important;
            }}
            
            [data-testid="stHeader"] > div {{
                display: flex !important;
                align-items: center !important;
                gap: 0.5rem !important;
                flex-wrap: nowrap !important;
            }}
            
            [data-testid="stHeader"] > div:first-child button:not(:first-child),
            [data-testid="stHeader"] button[aria-label*="sidebar"],
            [data-testid="stHeader"] button[aria-label*="Sidebar"],
            header > div:first-child button:not(:first-child) {{
                padding: 0.65rem 0.85rem !important;
                font-size: 0.825rem !important;
                min-width: 40px !important;
                min-height: 40px !important;
                border-radius: 10px !important;
                touch-action: manipulation !important;
                -webkit-tap-highlight-color: rgba(34, 197, 94, 0.4) !important;
                box-shadow: 0 3px 8px rgba(0, 0, 0, 0.25) !important;
            }}
            
            [data-testid="stHeader"] > div:first-child button:not(:first-child):active,
            [data-testid="stHeader"] button[aria-label*="sidebar"]:active {{
                transform: scale(0.95) !important;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
            }}
            
            /* Ensure header buttons are always accessible on mobile */
            [data-testid="stHeader"] button {{
                position: relative !important;
                z-index: 1002 !important;
            }}
        }}
        
        /* Mobile Portrait (up to 480px) */
        @media (max-width: 480px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
                gap: 0.5rem;
            }}
            
            .stat-card {{
                padding: 0.75rem;
            }}
            
            .stat-value {{
                font-size: 1.5rem;
            }}
            
            .stat-label {{
                font-size: 0.65rem;
            }}
            
            .route-card {{
                padding: 0.875rem;
                margin: 0.5rem 0;
                border-radius: 12px;
            }}
            
            .route-label {{
                font-size: 0.65rem;
                margin-bottom: 0.5rem;
            }}
            
            .route-path {{
                font-size: 0.85rem;
                line-height: 1.5;
            }}
            
            .route-arrow {{
                margin: 0 0.25rem;
            }}
            
            .settings-grid {{
                grid-template-columns: 1fr;
                gap: 0.5rem;
            }}
            
            .setting-item {{
                padding: 0.5rem 0.75rem;
            }}
            
            .setting-label {{
                font-size: 0.65rem;
            }}
            
            .stButton > button {{
                padding: 0.625rem 1rem;
                font-size: 0.85rem;
                border-radius: 10px;
            }}
            
            .nav-step {{
                padding: 0.625rem 0.75rem;
                gap: 0.5rem;
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .nav-number {{
                min-width: 24px;
                height: 24px;
                font-size: 0.7rem;
            }}
            
            .nav-cities {{
                font-size: 0.85rem;
            }}
            
            .nav-meta {{
                font-size: 0.75rem;
            }}
            
            .place-card {{
                padding: 0.625rem;
                gap: 0.5rem;
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .place-icon {{
                font-size: 1.25rem;
                min-width: 35px;
            }}
            
            .place-name {{
                font-size: 0.85rem;
            }}
            
            .place-detail {{
                font-size: 0.7rem;
            }}
            
            .place-rating {{
                font-size: 0.7rem;
            }}
            
            .place-distance {{
                font-size: 0.7rem;
            }}
            
            .stops-container {{
                gap: 0.25rem;
                flex-wrap: wrap;
            }}
            
            .stop-badge {{
                padding: 0.25rem 0.625rem;
                font-size: 0.65rem;
            }}
            
            .stop-arrow {{
                font-size: 1rem;
            }}
            
            .stTabs [data-baseweb="tab-list"] {{
                gap: 0.125rem;
                padding: 0.125rem;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                padding: 0.375rem 0.5rem;
                font-size: 0.65rem;
            }}
            
            .success-banner {{
                padding: 0.75rem;
            }}
            
            .success-text {{
                font-size: 0.85rem;
            }}
            
            .error-banner {{
                padding: 1rem;
            }}
            
            .error-title {{
                font-size: 1rem;
            }}
            
            .error-text {{
                font-size: 0.85rem;
            }}
            
            .drive-mode {{
                padding: 0.875rem;
                border-radius: 16px;
            }}
            
            .drive-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }}
            
            .drive-instruction {{
                font-size: 1rem;
            }}
            
            .drive-distance {{
                font-size: 1.5rem;
            }}
            
            .drive-current {{
                padding: 0.875rem;
            }}
            
            .drive-direction {{
                font-size: 2rem;
            }}
            
            .drive-next {{
                padding: 0.75rem;
            }}
            
            .drive-next-text {{
                font-size: 0.9rem;
            }}
            
            .offline-card {{
                padding: 0.75rem;
            }}
            
            .offline-title {{
                font-size: 0.9rem;
            }}
            
            .offline-desc {{
                font-size: 0.8rem;
            }}
            
            .download-btn {{
                padding: 0.5rem 0.875rem;
                font-size: 0.8rem;
            }}
            
            .footer {{
                padding: 1rem 0.75rem;
                font-size: 0.75rem;
            }}
            
            .fuel-breakdown {{
                padding: 0.75rem;
            }}
            
            .fuel-title {{
                font-size: 0.8rem;
            }}
            
            .fuel-details {{
                font-size: 0.75rem;
                gap: 0.5rem;
            }}
            
            [data-testid="stHeader"] {{
                padding: 0.5rem 0.75rem !important;
                flex-wrap: nowrap !important;
                gap: 0.5rem !important;
            }}
            
            [data-testid="stHeader"] > div {{
                display: flex !important;
                align-items: center !important;
                gap: 0.5rem !important;
                flex-wrap: nowrap !important;
            }}
            
            [data-testid="stHeader"] > div:first-child button:not(:first-child),
            [data-testid="stHeader"] button[aria-label*="sidebar"],
            [data-testid="stHeader"] button[aria-label*="Sidebar"],
            header > div:first-child button:not(:first-child) {{
                padding: 0.6rem 0.875rem !important;
                font-size: 0.8rem !important;
                min-width: 42px !important;
                min-height: 42px !important;
                border-radius: 10px !important;
                touch-action: manipulation !important;
                -webkit-tap-highlight-color: rgba(34, 197, 94, 0.4) !important;
                box-shadow: 0 3px 8px rgba(0, 0, 0, 0.25) !important;
            }}
            
            [data-testid="stHeader"] > div:first-child button:not(:first-child):active,
            [data-testid="stHeader"] button[aria-label*="sidebar"]:active {{
                transform: scale(0.95) !important;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
            }}
            
            /* Ensure header buttons are always accessible on mobile */
            [data-testid="stHeader"] button {{
                position: relative !important;
                z-index: 1002 !important;
            }}
            
            [data-testid="stSidebar"] {{
                min-width: 200px !important;
            }}
            
            /* Improve touch targets on mobile - smaller but still usable */
            button:not([data-testid="stHeader"] button),
            a:not([data-testid="stHeader"] a),
            .stButton > button {{
                min-height: 40px !important;
            }}
            
            /* Header buttons can be slightly smaller */
            [data-testid="stHeader"] button {{
                min-height: 40px !important;
                min-width: 40px !important;
            }}
            
            /* Inputs should maintain good size */
            input, select, textarea {{
                min-height: 44px !important;
            }}
            
            /* Better spacing for mobile */
            .stMarkdown {{
                font-size: 0.9rem;
                line-height: 1.7 !important;
            }}
            
            h1 {{
                font-size: 1.75rem !important;
                margin-bottom: 0.75rem !important;
            }}
            
            h2 {{
                font-size: 1.5rem !important;
                margin-bottom: 0.625rem !important;
            }}
            
            h3 {{
                font-size: 1.25rem !important;
                margin-bottom: 0.5rem !important;
            }}
            
            /* Better card spacing on mobile */
            .card,
            .route-card,
            .place-card {{
                margin-bottom: 1rem !important;
            }}
            
            /* Improved input spacing */
            .stTextInput,
            .stNumberInput,
            .stSelectbox {{
                margin-bottom: 1rem !important;
            }}
            
            /* Better map container on mobile */
            .folium-map {{
                height: 300px !important;
                border-radius: 12px !important;
                overflow: hidden !important;
            }}
            
            /* Improved tab spacing */
            .stTabs {{
                margin-bottom: 1rem !important;
            }}
            
            /* Better sidebar on mobile */
            [data-testid="stSidebar"] {{
                min-width: 280px !important;
                max-width: 85vw !important;
            }}
            
            /* Prevent horizontal scroll */
            body,
            .stApp {{
                overflow-x: hidden !important;
                max-width: 100vw !important;
            }}
            
            /* Better image handling */
            img {{
                max-width: 100% !important;
                height: auto !important;
            }}
            
            /* Improved list spacing */
            ul, ol {{
                padding-left: 1.5rem !important;
                margin: 0.75rem 0 !important;
            }}
            
            li {{
                margin-bottom: 0.5rem !important;
                line-height: 1.6 !important;
            }}
        }}
        
        /* Landscape orientation adjustments */
        @media (max-width: 768px) and (orientation: landscape) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .nav-step {{
                flex-direction: row;
            }}
            
            .place-card {{
                flex-direction: row;
            }}
        }}
        
        /* High DPI displays */
        @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {{
            .stat-value {{
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }}
        }}
    </style>
    """


# ==================== SAMPLE DATA ====================
def get_nearby_places(city, category):
    """Get nearby places for a specific city and category."""
    # Define places for different major cities/areas
    city_places = {
        # Karachi locations
        "Karachi": {
            "restaurants": [
                {"name": "Kolachi", "type": "Seafood", "rating": 4.6, "distance": "1.2 km", "price": "$$$"},
                {"name": "BBQ Tonight", "type": "Pakistani BBQ", "rating": 4.5, "distance": "0.8 km", "price": "$$"},
                {"name": "Café Zouk", "type": "Continental", "rating": 4.4, "distance": "1.5 km", "price": "$$"},
                {"name": "Burns Road Food Street", "type": "Street Food", "rating": 4.7, "distance": "2.0 km", "price": "$"},
                {"name": "Okra", "type": "Fine Dining", "rating": 4.8, "distance": "1.8 km", "price": "$$$"},
            ],
            "hotels": [
                {"name": "Pearl Continental", "type": "5-Star", "rating": 4.8, "distance": "1.0 km", "price": "$$$"},
                {"name": "Marriott Hotel", "type": "5-Star", "rating": 4.7, "distance": "1.5 km", "price": "$$$"},
                {"name": "Ramada Hotel", "type": "4-Star", "rating": 4.4, "distance": "0.8 km", "price": "$$"},
                {"name": "Avari Towers", "type": "5-Star", "rating": 4.6, "distance": "2.2 km", "price": "$$$"},
            ],
            "cafes": [
                {"name": "Gloria Jean's", "type": "Coffee Shop", "rating": 4.4, "distance": "0.5 km", "price": "$$"},
                {"name": "Espresso", "type": "Café", "rating": 4.3, "distance": "0.7 km", "price": "$$"},
                {"name": "The Second Cup", "type": "Coffee Shop", "rating": 4.2, "distance": "1.0 km", "price": "$$"},
                {"name": "Butlers Chocolate Café", "type": "Café", "rating": 4.5, "distance": "1.3 km", "price": "$$"},
            ],
            "parks": [
                {"name": "Beach Park", "type": "Recreation", "rating": 4.5, "distance": "3.0 km", "price": "Free"},
                {"name": "Safari Park", "type": "Zoo & Park", "rating": 4.3, "distance": "8.0 km", "price": "Rs.50"},
                {"name": "Hill Park", "type": "Public Park", "rating": 4.4, "distance": "5.0 km", "price": "Free"},
            ],
        },
        # Islamabad locations
        "Islamabad": {
            "restaurants": [
                {"name": "Monal Restaurant", "type": "Pakistani", "rating": 4.7, "distance": "8.0 km", "price": "$$$"},
                {"name": "Savour Foods", "type": "Pakistani", "rating": 4.6, "distance": "1.2 km", "price": "$$"},
                {"name": "Kabul Restaurant", "type": "Afghani", "rating": 4.5, "distance": "0.8 km", "price": "$$"},
                {"name": "Chaaye Khana", "type": "Café Restaurant", "rating": 4.4, "distance": "1.5 km", "price": "$$"},
                {"name": "Des Pardes", "type": "Pakistani", "rating": 4.3, "distance": "2.0 km", "price": "$$"},
            ],
            "hotels": [
                {"name": "Serena Hotel", "type": "5-Star", "rating": 4.9, "distance": "2.0 km", "price": "$$$"},
                {"name": "Islamabad Hotel", "type": "4-Star", "rating": 4.5, "distance": "1.5 km", "price": "$$"},
                {"name": "Ramada Hotel", "type": "4-Star", "rating": 4.4, "distance": "3.0 km", "price": "$$"},
                {"name": "Hotel One", "type": "Business", "rating": 4.2, "distance": "2.5 km", "price": "$$"},
            ],
            "cafes": [
                {"name": "Gloria Jean's", "type": "Coffee Shop", "rating": 4.4, "distance": "0.5 km", "price": "$$"},
                {"name": "Coffee Bean & Tea Leaf", "type": "Coffee Shop", "rating": 4.3, "distance": "1.0 km", "price": "$$"},
                {"name": "The Second Cup", "type": "Coffee Shop", "rating": 4.2, "distance": "0.8 km", "price": "$$"},
            ],
            "parks": [
                {"name": "Fatima Jinnah Park", "type": "National Park", "rating": 4.6, "distance": "2.5 km", "price": "Free"},
                {"name": "Lake View Park", "type": "Recreation", "rating": 4.4, "distance": "3.0 km", "price": "$"},
                {"name": "Daman-e-Koh", "type": "Viewpoint", "rating": 4.8, "distance": "5.0 km", "price": "Free"},
                {"name": "Shakarparian Park", "type": "Public Park", "rating": 4.5, "distance": "4.0 km", "price": "Free"},
            ],
        },
        # Lahore locations
        "Lahore": {
            "restaurants": [
                {"name": "Cuckoo's Den", "type": "Pakistani", "rating": 4.8, "distance": "2.0 km", "price": "$$$"},
                {"name": "Butt Karahi", "type": "Pakistani BBQ", "rating": 4.7, "distance": "1.5 km", "price": "$$"},
                {"name": "Food Street", "type": "Street Food", "rating": 4.6, "distance": "3.0 km", "price": "$"},
                {"name": "Salt'n Pepper", "type": "Pakistani", "rating": 4.5, "distance": "1.2 km", "price": "$$"},
                {"name": "Haveli Restaurant", "type": "Pakistani", "rating": 4.4, "distance": "4.0 km", "price": "$$"},
            ],
            "hotels": [
                {"name": "Pearl Continental", "type": "5-Star", "rating": 4.8, "distance": "1.5 km", "price": "$$$"},
                {"name": "Nishat Hotel", "type": "5-Star", "rating": 4.7, "distance": "2.0 km", "price": "$$$"},
                {"name": "Avari Hotel", "type": "5-Star", "rating": 4.6, "distance": "1.8 km", "price": "$$$"},
            ],
            "cafes": [
                {"name": "Gloria Jean's", "type": "Coffee Shop", "rating": 4.4, "distance": "0.5 km", "price": "$$"},
                {"name": "Espresso", "type": "Café", "rating": 4.3, "distance": "0.7 km", "price": "$$"},
            ],
            "parks": [
                {"name": "Jinnah Park", "type": "Public Park", "rating": 4.5, "distance": "2.0 km", "price": "Free"},
                {"name": "Race Course Park", "type": "Recreation", "rating": 4.6, "distance": "3.5 km", "price": "Rs.20"},
            ],
        },
    }
    
    # Try to find matching city (check if city name contains any key)
    matched_city = None
    city_lower = city.lower()
    
    # Check for major cities in the location name
    for key in city_places.keys():
        key_lower = key.lower()
        # Check if city name contains the key or vice versa
        if key_lower in city_lower or city_lower in key_lower:
            matched_city = key
            break
    
    # Also check for common area prefixes (DHA, F-7, etc.)
    if not matched_city:
        if "karachi" in city_lower or "dha" in city_lower:
            matched_city = "Karachi"
        elif "islamabad" in city_lower or "f-" in city_lower or "g-" in city_lower:
            matched_city = "Islamabad"
        elif "lahore" in city_lower:
            matched_city = "Lahore"
    
    # If no match found, use default data
    if matched_city and category in city_places[matched_city]:
        return city_places[matched_city][category]
    
    # Default fallback data
    default_data = {
        "restaurants": [
            {"name": "Local Restaurant", "type": "Pakistani", "rating": 4.0, "distance": "0.5 km", "price": "$$"},
            {"name": "Food Point", "type": "Fast Food", "rating": 3.8, "distance": "1.0 km", "price": "$"},
        ],
        "hotels": [
            {"name": "Local Hotel", "type": "3-Star", "rating": 3.5, "distance": "1.0 km", "price": "$$"},
        ],
        "cafes": [
            {"name": "Local Café", "type": "Coffee Shop", "rating": 3.8, "distance": "0.5 km", "price": "$$"},
        ],
        "parks": [
            {"name": "Local Park", "type": "Public Park", "rating": 4.0, "distance": "1.0 km", "price": "Free"},
        ],
    }
    
    return default_data.get(category, [])


# ==================== HELPER FUNCTIONS ====================
@st.cache_data
def load_data():
    return load_cities("pak_cities.csv")


@st.cache_data
def load_all_locations():
    cities = load_cities("pak_cities.csv")
    all_locations = {city["name"]: {"lat": city["lat"], "lon": city["lon"], "type": "city"} for city in cities}
    for name, coords in get_all_locations().items():
        if name not in all_locations:
            all_locations[name] = {"lat": coords[0], "lon": coords[1], "type": "area"}
    return all_locations


@st.cache_data
def build_city_graph(threshold):
    return build_graph(load_data(), threshold_km=threshold)


def find_nearest_city(loc_coords, cities):
    min_dist, nearest = float('inf'), None
    for city in cities:
        dist = calculate_distance_km(loc_coords["lat"], loc_coords["lon"], city["lat"], city["lon"])
        if dist < min_dist:
            min_dist, nearest = dist, city["name"]
    return nearest, min_dist


def find_route(source, dest, all_locations, cities, graph):
    src_coords, dst_coords = all_locations[source], all_locations[dest]
    direct = calculate_distance_km(src_coords["lat"], src_coords["lon"], dst_coords["lat"], dst_coords["lon"])
    
    if direct < 50:
        return [source, dest], round(direct, 2), "local"
    
    src_city, src_dist = find_nearest_city(src_coords, cities)
    dst_city, dst_dist = find_nearest_city(dst_coords, cities)
    
    if src_city == dst_city:
        return [source, dest], round(direct, 2), "local"
    
    try:
        city_path, city_dist = dijkstra(graph, src_city, dst_city)
        if city_path:
            path = [source] + ([src_city] if source != src_city else [])
            path += city_path[1:-1]
            path += ([dst_city] if dest != dst_city else []) + [dest]
            seen, unique = set(), []
            for p in path:
                if p not in seen:
                    seen.add(p)
                    unique.append(p)
            return unique, round(src_dist + city_dist + dst_dist, 2), "intercity"
    except:
        pass
    return [source, dest], round(direct, 2), "direct"


def create_map(path, locations, mode="car"):
    coords = [(locations[loc]["lat"], locations[loc]["lon"]) for loc in path]
    center = [sum(c[0] for c in coords)/len(coords), sum(c[1] for c in coords)/len(coords)]
    
    m = folium.Map(location=center, zoom_start=6, tiles='CartoDB dark_matter')
    
    colors = {"car": "#22c55e", "bike": "#f59e0b", "cycle": "#3b82f6", "walk": "#8b5cf6"}
    color = colors.get(mode, "#22c55e")
    
    folium.PolyLine(coords, weight=5, color=color, opacity=0.8).add_to(m)
    plugins.AntPath(coords, delay=1000, weight=3, color=color, pulse_color='#fff', dash_array=[10,20]).add_to(m)
    
    for i, loc in enumerate(path):
        lat, lon = locations[loc]["lat"], locations[loc]["lon"]
        if i == 0:
            ic = folium.Icon(color='green', icon='play', prefix='fa')
        elif i == len(path)-1:
            ic = folium.Icon(color='red', icon='flag-checkered', prefix='fa')
        else:
            ic = folium.Icon(color='blue', icon='circle', prefix='fa')
        folium.Marker([lat, lon], tooltip=loc, icon=ic).add_to(m)
    
    m.fit_bounds(coords)
    return m


def get_road_distance(straight_dist):
    """Convert straight-line distance to approximate road distance.
    Roads are typically 1.3-1.5x longer than straight line distance."""
    ROAD_FACTOR = 1.4  # Average road winding factor
    return round(straight_dist * ROAD_FACTOR, 1)


def est_time(dist, speed):
    """Estimate travel time based on distance and speed."""
    hrs = dist / speed if speed > 0 else 0
    if hrs < 1:
        return f"{int(hrs * 60)} min"
    else:
        h = int(hrs)
        m = int((hrs - h) * 60)
        return f"{h}h {m}m"


def create_map_picker(center_lat=30.3753, center_lon=69.3451, default_zoom=10):
    """Create an interactive map for location picking with a draggable marker."""
    m = folium.Map(location=[center_lat, center_lon], zoom_start=default_zoom, tiles='CartoDB dark_matter')
    
    # Create a red icon - use explicit red color
    red_icon = folium.Icon(
        color='red',
        icon='map-marker',
        prefix='fa'
    )
    
    # Add a draggable marker with red color
    draggable_marker = folium.Marker(
        [center_lat, center_lon],
        popup=folium.Popup(f"📍 Drag this pin or click on map<br>Lat: {center_lat:.6f}<br>Lon: {center_lon:.6f}", max_width=250),
        tooltip="Drag me to set location or click on map",
        icon=red_icon,
        draggable=True
    )
    draggable_marker.add_to(m)
    
    # Add a red circle underneath to make it more visible and clearly red
    folium.CircleMarker(
        [center_lat, center_lon],
        radius=8,
        popup="📍 Location marker",
        color='#ff0000',
        fill=True,
        fillColor='#ff0000',
        fillOpacity=0.6,
        weight=2
    ).add_to(m)
    
    # Add click handler to show coordinates when clicking on map
    m.add_child(folium.LatLngPopup())
    
    return m


def find_nearest_location_name(lat, lon, all_locations, cities):
    """Find the nearest location name to given coordinates."""
    min_dist = float('inf')
    nearest_name = None
    
    # Check all locations
    for name, coords in all_locations.items():
        dist = calculate_distance_km(lat, lon, coords["lat"], coords["lon"])
        if dist < min_dist:
            min_dist = dist
            nearest_name = name
    
    # If nearest location is more than 5km away, use coordinates
    if min_dist > 5:
        return f"Custom Location ({lat:.4f}, {lon:.4f})"
    
    return nearest_name


def add_custom_location(lat, lon, all_locations, location_names):
    """Add a custom location to the locations dictionary."""
    custom_name = f"Custom Location ({lat:.4f}, {lon:.4f})"
    if custom_name not in all_locations:
        all_locations[custom_name] = {"lat": lat, "lon": lon, "type": "custom"}
        location_names.append(custom_name)
        location_names.sort()
    return custom_name


def format_route(path):
    return ' <span style="color: var(--accent);">→</span> '.join(f'<span style="color: var(--text-primary);">{p}</span>' for p in path)


def generate_offline_data(path, distance, all_locations, mode_key, fuel_avg, fuel_price, speed):
    """Generate downloadable route data for offline use."""
    route_data = {
        "app": "SafarPak",
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "note": "Distances are road estimates (1.4x straight-line distance)",
        "route": {
            "from": path[0],
            "to": path[-1],
            "total_distance_km": distance,
            "transport_mode": mode_key,
            "speed_kmh": speed,
            "stops": len(path) - 2 if len(path) > 2 else 0,
        },
        "directions": [],
        "coordinates": []
    }
    
    cumulative = 0
    for i, loc in enumerate(path):
        coords = all_locations[loc]
        route_data["coordinates"].append({
            "name": loc,
            "lat": coords["lat"],
            "lon": coords["lon"],
            "stop_number": i + 1
        })
        
        if i < len(path) - 1:
            next_loc = path[i + 1]
            next_coords = all_locations[next_loc]
            seg_straight = calculate_distance_km(coords["lat"], coords["lon"], 
                                                next_coords["lat"], next_coords["lon"])
            seg_dist = get_road_distance(seg_straight)
            cumulative += seg_dist
            
            route_data["directions"].append({
                "step": i + 1,
                "from": loc,
                "to": next_loc,
                "distance_km": round(seg_dist, 1),
                "cumulative_km": round(cumulative, 1),
                "est_time": est_time(seg_dist, speed),
                "instruction": f"Head towards {next_loc}"
            })
    
    # Fuel calculation
    if mode_key in ["car", "bike"]:
        liters = distance / (fuel_avg * (1.5 if mode_key == "bike" else 1))
        route_data["fuel"] = {
            "liters_needed": round(liters, 2),
            "cost_estimate": round(liters * fuel_price, 0),
            "fuel_average_kmpl": fuel_avg,
            "fuel_price_per_liter": fuel_price
        }
    
    return route_data


def create_text_route(route_data):
    """Create a text version of the route for offline viewing."""
    text = f"""
╔══════════════════════════════════════════════════════════════╗
║                     🧭 SAFARPAK ROUTE                        ║
╚══════════════════════════════════════════════════════════════╝

📅 Generated: {route_data['generated']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 ROUTE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   From: {route_data['route']['from']}
   To:   {route_data['route']['to']}
   
   🛣️  Total Distance: ~{route_data['route']['total_distance_km']} km (road estimate)
   🚗  Transport Mode: {route_data['route']['transport_mode'].upper()}
   🏎️  Speed: {route_data['route']['speed_kmh']} km/h
   📍  Stops: {route_data['route']['stops']}

"""
    
    if 'fuel' in route_data:
        text += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛽ FUEL ESTIMATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Liters Needed: {route_data['fuel']['liters_needed']} L
   Estimated Cost: Rs. {int(route_data['fuel']['cost_estimate']):,}
   (Based on {route_data['fuel']['fuel_average_kmpl']} km/L @ Rs.{route_data['fuel']['fuel_price_per_liter']}/L)

"""
    
    text += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧭 TURN-BY-TURN DIRECTIONS (at {route_data['route']['speed_kmh']} km/h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    for d in route_data['directions']:
        text += f"""   [{d['step']}] {d['from']} → {d['to']}
       📏 ~{d['distance_km']} km • ⏱️ {d['est_time']} (Total: {d['cumulative_km']} km)
       
"""
    
    text += """   [🏁] DESTINATION REACHED!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 COORDINATES (For GPS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    for c in route_data['coordinates']:
        text += f"   {c['stop_number']}. {c['name']}: {c['lat']:.6f}, {c['lon']:.6f}\n"
    
    text += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    Safe Travels! 🇵🇰
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return text


def get_download_link(content, filename, file_type="text"):
    """Generate a download link for the content."""
    if file_type == "json":
        b64 = base64.b64encode(json.dumps(content, indent=2).encode()).decode()
        mime = "application/json"
    else:
        b64 = base64.b64encode(content.encode()).decode()
        mime = "text/plain"
    
    return f'<a href="data:{mime};base64,{b64}" download="{filename}" class="download-btn">📥 Download {filename}</a>'


def get_direction_icon(from_loc, to_loc, all_locations):
    """Get appropriate direction icon based on bearing."""
    from_coords = all_locations[from_loc]
    to_coords = all_locations[to_loc]
    
    lat_diff = to_coords["lat"] - from_coords["lat"]
    lon_diff = to_coords["lon"] - from_coords["lon"]
    
    if abs(lat_diff) > abs(lon_diff):
        return "⬆️" if lat_diff > 0 else "⬇️"
    else:
        return "➡️" if lon_diff > 0 else "⬅️"


def create_map_picker(center_lat=30.3753, center_lon=69.3451, default_zoom=10):
    """Create an interactive map for location picking."""
    m = folium.Map(location=[center_lat, center_lon], zoom_start=default_zoom, tiles='CartoDB dark_matter')
    
    # Add click handler to show coordinates
    m.add_child(folium.LatLngPopup())
    
    # Add a marker at center with instructions
    folium.Marker(
        [center_lat, center_lon],
        popup="📍 Click anywhere on the map to select this location",
        tooltip="Click on map to pick location",
        icon=folium.Icon(color='blue', icon='info-sign', prefix='fa')
    ).add_to(m)
    
    # Add a circle to show clickable area
    folium.CircleMarker(
        [center_lat, center_lon],
        radius=10,
        popup="Click here or anywhere on the map",
        color='#22c55e',
        fill=True,
        fillColor='#22c55e',
        fillOpacity=0.3
    ).add_to(m)
    
    return m


def find_nearest_location_name(lat, lon, all_locations, cities):
    """Find the nearest location name to given coordinates."""
    min_dist = float('inf')
    nearest_name = None
    
    # Check all locations
    for name, coords in all_locations.items():
        dist = calculate_distance_km(lat, lon, coords["lat"], coords["lon"])
        if dist < min_dist:
            min_dist = dist
            nearest_name = name
    
    # If nearest location is more than 5km away, use coordinates
    if min_dist > 5:
        return f"Custom Location ({lat:.4f}, {lon:.4f})"
    
    return nearest_name


def add_custom_location(lat, lon, all_locations, location_names):
    """Add a custom location to the locations dictionary."""
    custom_name = f"Custom Location ({lat:.4f}, {lon:.4f})"
    if custom_name not in all_locations:
        all_locations[custom_name] = {"lat": lat, "lon": lon, "type": "custom"}
        location_names.append(custom_name)
        location_names.sort()
    return custom_name


# ==================== MAIN APP ====================
def main():
    # Fix sidebar closing on mobile devices
    st.markdown("""
    <script>
        (function() {
            // Mobile sidebar close functionality
            function setupMobileSidebar() {
                const sidebar = document.querySelector('section[data-testid="stSidebar"]');
                
                if (!sidebar) return;
                
                // Create overlay for mobile
                let overlay = document.getElementById('sidebar-overlay');
                if (!overlay) {
                    overlay = document.createElement('div');
                    overlay.id = 'sidebar-overlay';
                    overlay.style.cssText = `
                        position: fixed;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background: rgba(0, 0, 0, 0.5);
                        z-index: 997;
                        display: none;
                        opacity: 0;
                        transition: opacity 0.3s ease;
                    `;
                    document.body.appendChild(overlay);
                    
                    // Close sidebar when overlay is clicked
                    overlay.addEventListener('click', function() {
                        closeSidebar();
                    });
                }
                
                // Function to check if sidebar is open
                function isSidebarOpen() {
                    const sidebar = document.querySelector('section[data-testid="stSidebar"]');
                    if (!sidebar) return false;
                    
                    const style = window.getComputedStyle(sidebar);
                    const transform = style.transform;
                    const ariaExpanded = sidebar.getAttribute('aria-expanded') === 'true';
                    const isVisible = sidebar.offsetWidth > 0 && transform !== 'matrix(1, 0, 0, 1, -9999, 0)';
                    
                    return ariaExpanded || isVisible;
                }
                
                // Function to close sidebar
                function closeSidebar() {
                    const toggleBtn = document.querySelector('[data-testid="stHeader"] button[aria-label*="sidebar"], [data-testid="stHeader"] button[aria-label*="Sidebar"]');
                    
                    if (toggleBtn) {
                        toggleBtn.click();
                    } else {
                        // Fallback: find any sidebar toggle button
                        const allToggleBtns = document.querySelectorAll('button[aria-label*="sidebar"], button[aria-label*="Sidebar"]');
                        if (allToggleBtns.length > 0) {
                            allToggleBtns[0].click();
                        }
                    }
                    
                    // Hide overlay
                    if (overlay) {
                        overlay.style.opacity = '0';
                        setTimeout(() => {
                            overlay.style.display = 'none';
                        }, 300);
                    }
                    
                    document.body.style.overflow = '';
                }
                
                // Show/hide overlay based on sidebar state
                function updateOverlay() {
                    if (window.innerWidth <= 768) {
                        if (isSidebarOpen()) {
                            overlay.style.display = 'block';
                            setTimeout(() => {
                                overlay.style.opacity = '1';
                            }, 10);
                            document.body.style.overflow = 'hidden';
                        } else {
                            overlay.style.opacity = '0';
                            setTimeout(() => {
                                overlay.style.display = 'none';
                            }, 300);
                            document.body.style.overflow = '';
                        }
                    } else {
                        overlay.style.display = 'none';
                        document.body.style.overflow = '';
                    }
                }
                
                // Monitor sidebar state
                const observer = new MutationObserver(function() {
                    updateOverlay();
                });
                
                if (sidebar) {
                    observer.observe(sidebar, {
                        attributes: true,
                        attributeFilter: ['aria-expanded', 'class', 'style'],
                        childList: false,
                        subtree: false
                    });
                    
                    window.addEventListener('resize', updateOverlay);
                    
                    // Close on outside click
                    document.addEventListener('click', function(e) {
                        if (window.innerWidth <= 768 && isSidebarOpen()) {
                            const clickedElement = e.target;
                            const isInsideSidebar = sidebar.contains(clickedElement);
                            const isToggleButton = clickedElement.closest('button[aria-label*="sidebar"]') || 
                                                  clickedElement.closest('button[aria-label*="Sidebar"]');
                            
                            if (!isInsideSidebar && !isToggleButton && clickedElement !== overlay) {
                                closeSidebar();
                            }
                        }
                    });
                }
                
                updateOverlay();
            }
            
            // Run when DOM is ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', setupMobileSidebar);
            } else {
                setupMobileSidebar();
            }
            
            setTimeout(setupMobileSidebar, 500);
            setTimeout(setupMobileSidebar, 1000);
        })();
    </script>
    """, unsafe_allow_html=True)
    
    # Enable scrolling with mouse wheel and touchpad and suppress console warnings
    st.markdown("""
    <script>
        (function() {
            // Suppress harmless Streamlit console warnings - comprehensive filtering
            const originalWarn = console.warn;
            const originalError = console.error;
            const originalLog = console.log;
            
            // Create a function to check if message should be suppressed
            function shouldSuppress(message) {
                if (!message || typeof message !== 'string') return false;
                
                const suppressedPatterns = [
                    'Unrecognized feature:',
                    'ambient-light-sensor',
                    'battery',
                    'document-domain',
                    'layout-animations',
                    'legacy-image-formats',
                    'oversized-images',
                    'vr',
                    'wake-lock',
                    'iframe which has both allow-scripts and allow-same-origin',
                    'A form field element should have an id or name attribute',
                    'form field element has neither an id nor a name attribute',
                    'No label associated with a form field',
                    'index.CqTPbV5Y.js',
                    'Understand this warning'
                ];
                
                return suppressedPatterns.some(pattern => message.includes(pattern));
            }
            
            console.warn = function(...args) {
                const message = args.join(' ');
                if (shouldSuppress(message)) {
                    return; // Suppress these warnings
                }
                // Show other warnings
                originalWarn.apply(console, args);
            };
            
            console.error = function(...args) {
                const message = args.join(' ');
                if (shouldSuppress(message)) {
                    return; // Suppress these errors
                }
                // Show other errors
                originalError.apply(console, args);
            };
            
            // Also filter console.log for these warnings
            console.log = function(...args) {
                const message = args.join(' ');
                if (shouldSuppress(message)) {
                    return; // Suppress these logs
                }
                // Show other logs
                originalLog.apply(console, args);
            };
            
            // Suppress warnings from Streamlit's iframe
            window.addEventListener('message', function(event) {
                // Filter out messages that might contain warnings
                if (event.data && typeof event.data === 'string' && shouldSuppress(event.data)) {
                    event.stopPropagation();
                }
            }, true);
            
            // Ensure scroll events work properly
            document.addEventListener('wheel', function(e) {
                // Allow default scroll behavior
                e.stopPropagation();
            }, { passive: true });
            
            document.addEventListener('touchmove', function(e) {
                // Allow touch scrolling
                e.stopPropagation();
            }, { passive: true });
            
            // Remove any event listeners that might prevent scrolling
            document.body.style.overflow = 'auto';
            document.documentElement.style.overflow = 'auto';
        })();
    </script>
    """, unsafe_allow_html=True)
    
    # Remove toggle button - inject into head for maximum priority
    st.markdown("""
    <script>
        (function() {
            // Inject style into head for maximum priority
            const style = document.createElement('style');
            style.textContent = `
                button[name="keyboard_double_arrow_left"],
                section[data-testid="stSidebar"] button[name="keyboard_double_arrow_left"],
                #root > div:first-child > div:first-child > div > div > div > section > div:first-child > div > div:nth-child(6) > div > div:nth-child(2) > button,
                #root > div:first-child > div:first-child > div > div > div > section > div:first-child > div > div:nth-of-type(6) > div > div:nth-of-type(2) > button,
                #root > div:first-child > div:first-child > div > div > div > section > div:first-child > div > div:nth-child(7) > div > div:nth-child(2) > button,
                #root > div:first-child > div:first-child > div > div > div > section > div:first-child > div > div:nth-of-type(7) > div > div:nth-of-type(2) > button {
                    display: none !important;
                    visibility: hidden !important;
                    opacity: 0 !important;
                    width: 0 !important;
                    height: 0 !important;
                    padding: 0 !important;
                    margin: 0 !important;
                    position: absolute !important;
                    left: -9999px !important;
                    pointer-events: none !important;
                }
            `;
            document.head.appendChild(style);
            
            function removeBtn() {
                // Method 1: Direct XPath evaluation for div[6] button
                try {
                    const xpath6 = '//*[@id="root"]/div[1]/div[1]/div/div/div/section/div[1]/div/div[6]/div/div[2]/button';
                    const result6 = document.evaluate(xpath6, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                    const btn6 = result6.singleNodeValue;
                    if (btn6) {
                        btn6.style.cssText = 'display:none!important;visibility:hidden!important;opacity:0!important;width:0!important;height:0!important;padding:0!important;margin:0!important;position:absolute!important;left:-9999px!important;pointer-events:none!important;';
                        try { 
                            btn6.remove();
                        } catch(e) {
                            btn6.parentNode && btn6.parentNode.removeChild(btn6);
                        }
                    }
                } catch(e) {}
                
                // Method 2: Direct XPath evaluation for div[7] button
                try {
                    const xpath7 = '//*[@id="root"]/div[1]/div[1]/div/div/div/section/div[1]/div/div[7]/div/div[2]/button';
                    const result7 = document.evaluate(xpath7, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                    const btn7 = result7.singleNodeValue;
                    if (btn7) {
                        btn7.style.cssText = 'display:none!important;visibility:hidden!important;opacity:0!important;width:0!important;height:0!important;padding:0!important;margin:0!important;position:absolute!important;left:-9999px!important;pointer-events:none!important;';
                        try { 
                            btn7.remove();
                        } catch(e) {
                            btn7.parentNode && btn7.parentNode.removeChild(btn7);
                        }
                    }
                } catch(e) {}
                
                // Method 3: Navigate DOM structure programmatically for div[6]
                try {
                    const root = document.getElementById('root');
                    if (root) {
                        const div1 = root.firstElementChild;
                        if (div1) {
                            const div2 = div1.firstElementChild;
                            if (div2) {
                                const section = div2.querySelector('section');
                                if (section) {
                                    const sectionDiv1 = section.firstElementChild;
                                    if (sectionDiv1) {
                                        const innerDiv = sectionDiv1.firstElementChild;
                                        if (innerDiv && innerDiv.children.length > 5) {
                                            const div6 = innerDiv.children[5];
                                            if (div6) {
                                                const innerDiv2 = div6.firstElementChild;
                                                if (innerDiv2 && innerDiv2.children.length > 1) {
                                                    const div2 = innerDiv2.children[1];
                                                    if (div2) {
                                                        const btn = div2.querySelector('button');
                                                        if (btn) {
                                                            btn.style.cssText = 'display:none!important;visibility:hidden!important;opacity:0!important;width:0!important;height:0!important;padding:0!important;margin:0!important;position:absolute!important;left:-9999px!important;pointer-events:none!important;';
                                                            try { 
                                                                btn.remove();
                                                            } catch(e) {
                                                                btn.parentNode && btn.parentNode.removeChild(btn);
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                        // Also check for div[7]
                                        if (innerDiv && innerDiv.children.length > 6) {
                                            const div7 = innerDiv.children[6];
                                            if (div7) {
                                                const innerDiv2 = div7.firstElementChild;
                                                if (innerDiv2 && innerDiv2.children.length > 1) {
                                                    const div2 = innerDiv2.children[1];
                                                    if (div2) {
                                                        const btn = div2.querySelector('button');
                                                        if (btn) {
                                                            btn.style.cssText = 'display:none!important;visibility:hidden!important;opacity:0!important;width:0!important;height:0!important;padding:0!important;margin:0!important;position:absolute!important;left:-9999px!important;pointer-events:none!important;';
                                                            try { 
                                                                btn.remove();
                                                            } catch(e) {
                                                                btn.parentNode && btn.parentNode.removeChild(btn);
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                } catch(e) {}
                
                // Method 4: By name attribute (backup)
                const buttons = document.querySelectorAll('button[name="keyboard_double_arrow_left"]');
                buttons.forEach(b => {
                    b.style.cssText = 'display:none!important;visibility:hidden!important;opacity:0!important;width:0!important;height:0!important;padding:0!important;margin:0!important;position:absolute!important;left:-9999px!important;pointer-events:none!important;';
                    try { b.remove(); } catch(e) {}
                });
            }
            
            removeBtn();
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', removeBtn);
            }
            setInterval(removeBtn, 1);
            requestAnimationFrame(function loop() { removeBtn(); requestAnimationFrame(loop); });
            
            const observer = new MutationObserver(removeBtn);
            if (document.body) {
                observer.observe(document.body, {childList: true, subtree: true, attributes: true});
            }
        })();
    </script>
    """, unsafe_allow_html=True)
    
    # Initialize theme in session state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    # Initialize custom locations in session state
    if 'custom_locations' not in st.session_state:
        st.session_state.custom_locations = {}
    
    # Load data first
    try:
        cities = load_data()
        all_locations = load_all_locations()
        
        # Merge custom locations from session state
        all_locations.update(st.session_state.custom_locations)
        
        location_names = sorted(all_locations.keys())
        location_categories = get_location_categories()
        
        # Check if there's a stored destination location name and update index
        if hasattr(st.session_state, 'selected_dest_location') and st.session_state.selected_dest_location:
            if st.session_state.selected_dest_location in location_names:
                st.session_state.dst_index = location_names.index(st.session_state.selected_dest_location)
                # Clear it after using
                st.session_state.selected_dest_location = None
        
        # Check if there's a stored source location name and update index
        if hasattr(st.session_state, 'selected_src_location') and st.session_state.selected_src_location:
            if st.session_state.selected_src_location in location_names:
                st.session_state.src_index = location_names.index(st.session_state.selected_src_location)
                # Clear it after using
                st.session_state.selected_src_location = None
    except FileNotFoundError:
        st.error("⚠️ Run `python data_preparation.py` first!")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        st.markdown("---")
        
        # Theme selector
        st.markdown("**🎨 Theme**")
        theme = st.radio(
            "Select theme",
            options=["dark", "light", "colorblind"],
            format_func=lambda x: {"dark": "🌙 Dark", "light": "☀️ Light", "colorblind": "👁️ Color Blind"}[x],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.session_state.theme = theme
        
        st.markdown("---")
        
        # Location browser
        st.markdown("**📍 Location Browser**")
        for cat, locs in location_categories.items():
            with st.expander(f"{cat} ({len(locs)})"):
                for loc in locs[:8]:
                    st.caption(f"• {loc}")
                if len(locs) > 8:
                    st.caption(f"*+{len(locs)-8} more*")
        
        st.markdown("---")
        st.metric("Total Locations", len(location_names))
    
    # Remove white 3-line toggle button FIRST - before CSS
    st.markdown("""
    <script>
        (function() {
            function removeToggle() {
                document.querySelectorAll('button[name="keyboard_double_arrow_left"]').forEach(btn => btn.remove());
            }
            removeToggle();
            setInterval(removeToggle, 100);
            new MutationObserver(removeToggle).observe(document.body, {childList: true, subtree: true});
        })();
    </script>
    """, unsafe_allow_html=True)
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)
    
    # Remove white 3-line toggle button - aggressive removal
    st.markdown("""
    <script>
        (function() {
            function removeToggleButton() {
                // Method 1: Remove by name attribute
                const toggleBtns = document.querySelectorAll('button[name="keyboard_double_arrow_left"]');
                toggleBtns.forEach(btn => {
                    btn.style.display = 'none';
                    btn.style.visibility = 'hidden';
                    btn.remove();
                });
                
                // Method 2: Find in sidebar section
                const sidebar = document.querySelector('section[data-testid="stSidebar"]');
                if (sidebar) {
                    // Find all buttons in sidebar
                    const allSidebarBtns = sidebar.querySelectorAll('button');
                    allSidebarBtns.forEach(btn => {
                        const btnName = btn.getAttribute('name') || '';
                        if (btnName === 'keyboard_double_arrow_left') {
                            btn.style.display = 'none';
                            btn.style.visibility = 'hidden';
                            btn.remove();
                        }
                    });
                    
                    // Also check first div's first button
                    const firstDiv = sidebar.querySelector('> div:first-child');
                    if (firstDiv) {
                        const firstBtn = firstDiv.querySelector('button:first-child');
                        if (firstBtn) {
                            const btnName = firstBtn.getAttribute('name') || '';
                            if (btnName === 'keyboard_double_arrow_left') {
                                firstBtn.style.display = 'none';
                                firstBtn.style.visibility = 'hidden';
                                firstBtn.remove();
                            }
                        }
                    }
                }
                
                // Method 3: Find by position (bottom left area)
                const allButtons = document.querySelectorAll('button');
                allButtons.forEach(btn => {
                    const btnName = btn.getAttribute('name') || '';
                    if (btnName === 'keyboard_double_arrow_left') {
                        const rect = btn.getBoundingClientRect();
                        // If it's in the bottom left area
                        if (rect.left < 100 && rect.bottom > window.innerHeight - 150) {
                            btn.style.display = 'none';
                            btn.style.visibility = 'hidden';
                            btn.remove();
                        }
                    }
                });
            }
            
            // Run immediately
            removeToggleButton();
            
            // Run on various events
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', removeToggleButton);
            }
            
            // Run multiple times with different delays
            [10, 50, 100, 200, 300, 500, 1000, 2000].forEach(delay => {
                setTimeout(removeToggleButton, delay);
            });
            
            // Continuous monitoring every 200ms
            setInterval(removeToggleButton, 200);
            
            // MutationObserver for dynamic content
            const observer = new MutationObserver(function(mutations) {
                removeToggleButton();
            });
            
            if (document.body) {
                observer.observe(document.body, { 
                    childList: true, 
                    subtree: true, 
                    attributes: true,
                    attributeFilter: ['style', 'class', 'name']
                });
            }
            
            // Also observe sidebar specifically
            const sidebarObserver = new MutationObserver(function(mutations) {
                removeToggleButton();
            });
            
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            if (sidebar) {
                sidebarObserver.observe(sidebar, { 
                    childList: true, 
                    subtree: true, 
                    attributes: true 
                });
            }
        })();
    </script>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="app-header">
        <div class="app-logo">🧭</div>
        <h1 class="app-title">SafarPak</h1>
        <p class="app-subtitle">Your Travel Companion Across Pakistan</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom Sidebar Toggle Button - Using Streamlit Button with Session State
    if 'sidebar_visible' not in st.session_state:
        st.session_state.sidebar_visible = True
    
    # Create fixed position toggle button
    st.markdown("""
    <style>
        .custom-sidebar-toggle {
            position: fixed !important;
            top: 10px !important;
            left: 10px !important;
            z-index: 9999 !important;
        }
        .custom-sidebar-toggle button {
            background: #22c55e !important;
            color: white !important;
            border: 2px solid #22c55e !important;
            border-radius: 10px !important;
            padding: 0.8rem 1rem !important;
            font-size: 1.2rem !important;
            font-weight: bold !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.25) !important;
            min-width: 50px !important;
        }
        .custom-sidebar-toggle button:hover {
            background: #16a34a !important;
            transform: scale(1.05) !important;
        }
    </style>
    <div class="custom-sidebar-toggle">
    """, unsafe_allow_html=True)
    
    # Streamlit button for toggling
    if st.button("☰", key="sidebar_toggle_btn", help="Toggle sidebar"):
        st.session_state.sidebar_visible = not st.session_state.sidebar_visible
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # JavaScript to toggle sidebar based on session state - runs on every rerun
    sidebar_should_be_visible = st.session_state.sidebar_visible
    st.markdown(f"""
    <script>
        (function() {{
            function toggleSidebar(show) {{
                const sidebar = document.querySelector('[data-testid="stSidebar"], section[data-testid="stSidebar"]');
                if (sidebar) {{
                    if (show) {{
                        sidebar.style.cssText = 'display: flex !important; visibility: visible !important; transform: translateX(0) !important; opacity: 1 !important; width: 21rem !important;';
                    }} else {{
                        sidebar.style.cssText = 'display: none !important; visibility: hidden !important;';
                    }}
                    return true;
                }}
                return false;
            }}
            
            // Apply immediately
            const applied = toggleSidebar({str(sidebar_should_be_visible).lower()});
            
            // If sidebar should be visible but wasn't found, try clicking Streamlit's native button
            if ({str(sidebar_should_be_visible).lower()} && !applied) {{
                setTimeout(function() {{
                    const header = document.querySelector('[data-testid="stHeader"]');
                    if (header) {{
                        const buttons = header.querySelectorAll('button');
                        for (let btn of buttons) {{
                            const ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
                            if (ariaLabel.includes('sidebar') || ariaLabel.includes('menu')) {{
                                btn.click();
                                break;
                            }}
                        }}
                        // Fallback: click first button
                        if (buttons.length > 0 && !document.querySelector('[data-testid="stSidebar"]')) {{
                            buttons[0].click();
                        }}
                    }}
                }}, 300);
            }}
        }})();
    </script>
    """, unsafe_allow_html=True)
    
    # Input Section
    col1, col2 = st.columns(2)
    
    # Initialize map picker state
    if 'show_map_picker_from' not in st.session_state:
        st.session_state.show_map_picker_from = False
    if 'show_map_picker_to' not in st.session_state:
        st.session_state.show_map_picker_to = False
    if 'src_index' not in st.session_state:
        st.session_state.src_index = location_names.index("DHA Karachi") if "DHA Karachi" in location_names else 0
    if 'dst_index' not in st.session_state:
        st.session_state.dst_index = location_names.index("F-7 Islamabad") if "F-7 Islamabad" in location_names else 1
    
    with col1:
        st.markdown("""
        <div class="input-label">
            <span class="input-icon">📍</span> FROM
        </div>
        """, unsafe_allow_html=True)
        
        # Create columns for selectbox and map picker button
        sel_col, btn_col = st.columns([4, 1])
        
        with sel_col:
            # Ensure index is valid
            if st.session_state.src_index >= len(location_names):
                st.session_state.src_index = 0
            
            source = st.selectbox("From", location_names, 
                                 index=st.session_state.src_index,
                                 label_visibility="collapsed", key="src")
            # Update index when user manually changes selection
            if source in location_names:
                st.session_state.src_index = location_names.index(source)
        
        with btn_col:
            if st.button("🗺️", key="map_picker_from_btn", help="Pick location on map", use_container_width=True):
                st.session_state.show_map_picker_from = not st.session_state.show_map_picker_from
                st.session_state.show_map_picker_to = False
        
        # Show map picker for From
        if st.session_state.show_map_picker_from:
            st.markdown("**📍 Drag the red pin or click on the map to select your starting location:**")
            st.caption("💡 Tip: You can drag the red marker pin to any location, or click anywhere on the map to move the pin there.")
            
            # Initialize marker position in session state
            if 'marker_pos_from' not in st.session_state or st.session_state.marker_pos_from is None:
                if source in all_locations:
                    st.session_state.marker_pos_from = [all_locations[source]["lat"], all_locations[source]["lon"]]
                else:
                    st.session_state.marker_pos_from = [30.3753, 69.3451]
            
            # Get current location center - ensure it's not None
            center = st.session_state.marker_pos_from
            if center is None:
                # Fallback to default if somehow None
                center = [30.3753, 69.3451]
                st.session_state.marker_pos_from = center
            
            # Show current coordinates before map
            st.info(f"📍 Current marker position: {center[0]:.6f}, {center[1]:.6f}")
            
            map_picker = create_map_picker(center[0], center[1], default_zoom=10)
            map_data = st_folium(map_picker, width=None, height=400, key="map_picker_from", returned_objects=["last_clicked", "last_object_clicked", "all_drawings"])
            
            # Check for marker drag or map click
            selected_lat = None
            selected_lon = None
            
            # Initialize selected coordinates with current marker position
            selected_lat = center[0]
            selected_lon = center[1]
            
            # Check if marker was clicked/dragged (last_object_clicked contains marker info)
            if map_data.get("last_object_clicked"):
                obj = map_data["last_object_clicked"]
                if obj.get("type") == "marker" or "marker" in str(obj).lower():
                    # Try to get coordinates from the object
                    if "lat" in obj and "lng" in obj:
                        selected_lat = obj["lat"]
                        selected_lon = obj["lng"]
                    elif "geometry" in obj and "coordinates" in obj["geometry"]:
                        coords = obj["geometry"]["coordinates"]
                        selected_lat = coords[1]
                        selected_lon = coords[0]
                    st.session_state.marker_pos_from = [selected_lat, selected_lon]
            
            # Check for map click (which also updates marker position)
            if map_data.get("last_clicked"):
                clicked_lat = map_data["last_clicked"]["lat"]
                clicked_lon = map_data["last_clicked"]["lng"]
                selected_lat = clicked_lat
                selected_lon = clicked_lon
                st.session_state.marker_pos_from = [selected_lat, selected_lon]
            
            # Check all_drawings for marker position (this might contain dragged marker position)
            if map_data.get("all_drawings"):
                for drawing in map_data["all_drawings"]:
                    if drawing.get("type") == "marker":
                        if "geometry" in drawing and "coordinates" in drawing["geometry"]:
                            coords = drawing["geometry"]["coordinates"]
                            # Coordinates are [lon, lat] in GeoJSON format
                            selected_lat = coords[1]
                            selected_lon = coords[0]
                            st.session_state.marker_pos_from = [selected_lat, selected_lon]
                            break
            
            # Always show the confirm button with current coordinates
            if selected_lat and selected_lon:
                col_confirm, col_cancel = st.columns([1, 1])
                with col_confirm:
                    if st.button("✅ Confirm Location", key="confirm_from", use_container_width=True):
                        # Find nearest location or create custom
                        nearest = find_nearest_location_name(selected_lat, selected_lon, all_locations, cities)
                        
                        if nearest.startswith("Custom Location"):
                            # Add as custom location
                            custom_name = f"Custom Location ({selected_lat:.4f}, {selected_lon:.4f})"
                            # Store in session state
                            st.session_state.custom_locations[custom_name] = {"lat": selected_lat, "lon": selected_lon, "type": "custom"}
                            selected_name = custom_name
                        else:
                            selected_name = nearest
                        
                        # Update all_locations to include the new custom location (if any)
                        all_locations.update(st.session_state.custom_locations)
                        
                        # Ensure the selected location exists in all_locations
                        if selected_name not in all_locations:
                            # Add it if it doesn't exist
                            all_locations[selected_name] = {"lat": selected_lat, "lon": selected_lon, "type": "custom"}
                            st.session_state.custom_locations[selected_name] = {"lat": selected_lat, "lon": selected_lon, "type": "custom"}
                        
                        # Update location_names list
                        location_names = sorted(all_locations.keys())
                        
                        # Update the selectbox index
                        try:
                            new_index = location_names.index(selected_name)
                            st.session_state.src_index = new_index
                            # Store the selected location name in session state for verification
                            st.session_state.selected_src_location = selected_name
                            st.success(f"✅ Location selected: {selected_name} (Index: {new_index})")
                            st.session_state.show_map_picker_from = False
                            st.session_state.marker_pos_from = None
                            # Force rerun to update the selectbox
                            st.rerun()
                        except ValueError:
                            st.error(f"⚠️ Location '{selected_name}' not found in list. Please try again.")
                            st.write(f"Debug: Selected name: '{selected_name}'")
                            st.write(f"Debug: Available locations: {len(location_names)} total")
                        else:
                            st.error(f"⚠️ Location '{selected_name}' not found in list. Please try again.")
                            st.write(f"Debug: Available locations: {len(location_names)} total")
                
                with col_cancel:
                    if st.button("❌ Cancel", key="cancel_from", use_container_width=True):
                        st.session_state.show_map_picker_from = False
                        st.session_state.marker_pos_from = None
                        st.rerun()
                
                # Show current coordinates
                st.info(f"📍 Selected coordinates: {selected_lat:.6f}, {selected_lon:.6f}")
    
    with col2:
        st.markdown("""
        <div class="input-label">
            <span class="input-icon">🎯</span> TO
        </div>
        """, unsafe_allow_html=True)
        
        # Create columns for selectbox and map picker button
        sel_col2, btn_col2 = st.columns([4, 1])
        
        with sel_col2:
            # Ensure index is valid
            if st.session_state.dst_index >= len(location_names):
                st.session_state.dst_index = 0
            
            dest = st.selectbox("To", location_names,
                               index=st.session_state.dst_index,
                               label_visibility="collapsed", key="dst")
            # Update index when user manually changes selection
            if dest in location_names:
                st.session_state.dst_index = location_names.index(dest)
        
        with btn_col2:
            if st.button("🗺️", key="map_picker_to_btn", help="Pick location on map", use_container_width=True):
                st.session_state.show_map_picker_to = not st.session_state.show_map_picker_to
                st.session_state.show_map_picker_from = False
        
        # Show map picker for To
        if st.session_state.show_map_picker_to:
            st.markdown("**🎯 Drag the red pin or click on the map to select your destination:**")
            st.caption("💡 Tip: You can drag the red marker pin to any location, or click anywhere on the map to move the pin there.")
            
            # Initialize marker position in session state
            if 'marker_pos_to' not in st.session_state or st.session_state.marker_pos_to is None:
                if dest in all_locations:
                    st.session_state.marker_pos_to = [all_locations[dest]["lat"], all_locations[dest]["lon"]]
                else:
                    st.session_state.marker_pos_to = [30.3753, 69.3451]
            
            # Get current location center - ensure it's not None
            center = st.session_state.marker_pos_to
            if center is None:
                # Fallback to default if somehow None
                center = [30.3753, 69.3451]
                st.session_state.marker_pos_to = center
            
            # Show current coordinates before map
            st.info(f"📍 Current marker position: {center[0]:.6f}, {center[1]:.6f}")
            
            map_picker = create_map_picker(center[0], center[1], default_zoom=10)
            map_data = st_folium(map_picker, width=None, height=400, key="map_picker_to", returned_objects=["last_clicked", "last_object_clicked", "all_drawings"])
            
            # Check for marker drag or map click
            selected_lat = None
            selected_lon = None
            
            # Initialize selected coordinates with current marker position
            selected_lat = center[0]
            selected_lon = center[1]
            
            # Check if marker was clicked/dragged (last_object_clicked contains marker info)
            if map_data.get("last_object_clicked"):
                obj = map_data["last_object_clicked"]
                if obj.get("type") == "marker" or "marker" in str(obj).lower():
                    # Try to get coordinates from the object
                    if "lat" in obj and "lng" in obj:
                        selected_lat = obj["lat"]
                        selected_lon = obj["lng"]
                    elif "geometry" in obj and "coordinates" in obj["geometry"]:
                        coords = obj["geometry"]["coordinates"]
                        selected_lat = coords[1]
                        selected_lon = coords[0]
                    st.session_state.marker_pos_to = [selected_lat, selected_lon]
            
            # Check for map click (which also updates marker position)
            if map_data.get("last_clicked"):
                clicked_lat = map_data["last_clicked"]["lat"]
                clicked_lon = map_data["last_clicked"]["lng"]
                selected_lat = clicked_lat
                selected_lon = clicked_lon
                st.session_state.marker_pos_to = [selected_lat, selected_lon]
            
            # Check all_drawings for marker position (this might contain dragged marker position)
            if map_data.get("all_drawings"):
                for drawing in map_data["all_drawings"]:
                    if drawing.get("type") == "marker":
                        if "geometry" in drawing and "coordinates" in drawing["geometry"]:
                            coords = drawing["geometry"]["coordinates"]
                            # Coordinates are [lon, lat] in GeoJSON format
                            selected_lat = coords[1]
                            selected_lon = coords[0]
                            st.session_state.marker_pos_to = [selected_lat, selected_lon]
                            break
            
            # Always show the confirm button with current coordinates
            if selected_lat and selected_lon:
                col_confirm, col_cancel = st.columns([1, 1])
                with col_confirm:
                    if st.button("✅ Confirm Location", key="confirm_to", use_container_width=True):
                        # Find nearest location or create custom
                        nearest = find_nearest_location_name(selected_lat, selected_lon, all_locations, cities)
                        
                        if nearest.startswith("Custom Location"):
                            # Add as custom location
                            custom_name = f"Custom Location ({selected_lat:.4f}, {selected_lon:.4f})"
                            # Store in session state
                            st.session_state.custom_locations[custom_name] = {"lat": selected_lat, "lon": selected_lon, "type": "custom"}
                            selected_name = custom_name
                        else:
                            selected_name = nearest
                        
                        # Ensure the selected location exists in all_locations first
                        if selected_name not in all_locations:
                            # Add it if it doesn't exist
                            all_locations[selected_name] = {"lat": selected_lat, "lon": selected_lon, "type": "custom"}
                            st.session_state.custom_locations[selected_name] = {"lat": selected_lat, "lon": selected_lon, "type": "custom"}
                        
                        # Update all_locations to include all custom locations from session state
                        all_locations.update(st.session_state.custom_locations)
                        
                        # Update location_names list - recalculate from all_locations
                        location_names = sorted(all_locations.keys())
                        
                        # Verify the location is in the list
                        if selected_name not in location_names:
                            # Force add it
                            location_names.append(selected_name)
                            location_names.sort()
                        
                        # Update the selectbox index
                        try:
                            new_index = location_names.index(selected_name)
                            st.session_state.dst_index = new_index
                            # Store the selected location name in session state for verification
                            st.session_state.selected_dest_location = selected_name
                            st.success(f"✅ Location selected: {selected_name} (Index: {new_index})")
                            st.session_state.show_map_picker_to = False
                            st.session_state.marker_pos_to = None
                            # Force rerun to update the selectbox
                            st.rerun()
                        except ValueError:
                            st.error(f"⚠️ Location '{selected_name}' not found in list. Please try again.")
                            st.write(f"Debug: Selected name: '{selected_name}'")
                            st.write(f"Debug: Available locations: {len(location_names)} total")
                            st.write(f"Debug: First 5 locations: {location_names[:5]}")
                
                with col_cancel:
                    if st.button("❌ Cancel", key="cancel_to", use_container_width=True):
                        st.session_state.show_map_picker_to = False
                        st.session_state.marker_pos_to = None
                        st.rerun()
                
                # Show current coordinates
                st.info(f"📍 Selected coordinates: {selected_lat:.6f}, {selected_lon:.6f}")
    
    # Settings Row 1
    c1, c2, c3 = st.columns(3)
    with c1:
        mode = st.selectbox("🚗 Mode", ["🚗 Car", "🏍️ Bike", "🚴 Cycle", "🚶 Walk"], label_visibility="collapsed")
        mode_key = mode.split()[1].lower()
    with c2:
        # Speed selector based on mode
        speed_options = {
            "car": [40, 50, 60, 70, 80, 90, 100, 110, 120],
            "bike": [30, 40, 50, 60, 70, 80],
            "cycle": [10, 15, 20, 25, 30],
            "walk": [3, 4, 5, 6, 7]
        }
        default_speeds = {"car": 60, "bike": 50, "cycle": 15, "walk": 5}
        selected_speed = st.selectbox(
            f"🏎️ Speed (km/h)", 
            options=speed_options.get(mode_key, [60]),
            index=speed_options.get(mode_key, [60]).index(default_speeds.get(mode_key, 60)) if default_speeds.get(mode_key, 60) in speed_options.get(mode_key, [60]) else 0,
            label_visibility="collapsed"
        )
    with c3:
        threshold = st.slider("🔗 Range (km)", 100, 500, 300, 25)
    
    # Settings Row 2
    c4, c5 = st.columns(2)
    with c4:
        fuel_avg = st.number_input("⛽ Car Avg (km/L)", 5.0, 30.0, 12.0, 0.5)
    with c5:
        fuel_price = st.number_input("💰 Fuel Price (Rs/L)", 100, 400, 260, 5)
    
    # Direct distance
    if source != dest:
        direct_straight = calculate_distance_km(
            all_locations[source]["lat"], all_locations[source]["lon"],
            all_locations[dest]["lat"], all_locations[dest]["lon"]
        )
        direct_road = get_road_distance(direct_straight)
        route_type = "🏙️ Local" if direct_straight < 50 else "🛣️ Inter-City"
        st.markdown(f'<p style="text-align:center;color:var(--text-muted);">📏 Est. Road Distance: <strong style="color:var(--accent);">~{direct_road:.0f} km</strong> • {route_type}</p>', unsafe_allow_html=True)
    
    # Initialize route state
    if 'route_data' not in st.session_state:
        st.session_state.route_data = None
    if 'route_source' not in st.session_state:
        st.session_state.route_source = None
    if 'route_dest' not in st.session_state:
        st.session_state.route_dest = None
    
    # Check if source/dest changed - if so, clear route data
    if (st.session_state.route_source is not None and st.session_state.route_source != source) or \
       (st.session_state.route_dest is not None and st.session_state.route_dest != dest):
        st.session_state.route_data = None
    
    # Update stored source/dest
    if st.session_state.route_data is None:
        st.session_state.route_source = source
        st.session_state.route_dest = dest
    
    # Find Route Button
    if st.button("🔍 FIND ROUTE", use_container_width=True):
        if source == dest:
            st.warning("⚠️ Select different locations!")
            st.session_state.route_data = None
        else:
            progress = st.progress(0)
            progress.progress(30)
            graph = build_city_graph(threshold)
            progress.progress(60)
            path, straight_distance, route_mode = find_route(source, dest, all_locations, cities, graph)
            # Apply road factor for realistic distance
            distance = get_road_distance(straight_distance)
            progress.progress(100)
            time.sleep(0.2)
            progress.empty()
            
            if path:
                # Store route data in session state
                st.session_state.route_data = {
                    'path': path,
                    'distance': distance,
                    'straight_distance': straight_distance,
                    'route_mode': route_mode,
                    'selected_speed': selected_speed,
                    'mode_key': mode_key,
                    'fuel_avg': fuel_avg,
                    'fuel_price': fuel_price,
                    'liters': distance / (fuel_avg * (1.5 if mode_key == "bike" else 1)) if mode_key in ["car", "bike"] else 0,
                    'fuel_cost': int((distance / (fuel_avg * (1.5 if mode_key == "bike" else 1))) * fuel_price) if mode_key in ["car", "bike"] else 0,
                }
                st.session_state.route_source = source
                st.session_state.route_dest = dest
    
    # Display route if it exists in session state
    if st.session_state.route_data:
        path = st.session_state.route_data['path']
        distance = st.session_state.route_data['distance']
        route_mode = st.session_state.route_data['route_mode']
        # Use current settings for display (speed, fuel) but keep route path
        # Recalculate fuel with current settings
        if mode_key in ["car", "bike"]:
            liters = distance / (fuel_avg * (1.5 if mode_key == "bike" else 1))
            fuel_cost = int(liters * fuel_price)
            fuel_display = f"Rs.{fuel_cost:,}"
        else:
            liters, fuel_cost = 0, 0
            fuel_display = "Free 🌱"
        travel_time = est_time(distance, selected_speed)
        
        if path:
            # Live badge
            st.markdown('<div class="live-badge"><div class="live-dot"></div><span class="live-text">Route Found</span></div>', unsafe_allow_html=True)
            
            # Route display
            st.markdown(f"""
            <div class="route-card">
                <p class="route-label">🛣️ OPTIMAL ROUTE</p>
                <p class="route-path">{format_route(path)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Stats
            stops = len(path) - 2 if len(path) > 2 else 0
            
            st.markdown(f"""
            <div class="stats-grid">
                <div class="stat-card"><p class="stat-value">~{distance:.0f}</p><p class="stat-label">Road KM</p></div>
                <div class="stat-card"><p class="stat-value">{stops}</p><p class="stat-label">Stops</p></div>
                <div class="stat-card"><p class="stat-value">{travel_time}</p><p class="stat-label">@ {selected_speed}km/h</p></div>
                <div class="stat-card"><p class="stat-value">{fuel_display}</p><p class="stat-label">Fuel Cost</p></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f'<p style="text-align:center;color:var(--text-muted);font-size:0.8rem;margin-top:-0.5rem;">📏 Distances are road estimates • ⏱️ Time based on {selected_speed} km/h average speed</p>', unsafe_allow_html=True)
            
            # Fuel breakdown
            if mode_key in ["car", "bike"]:
                st.markdown(f"""
                <div class="fuel-breakdown">
                    <p class="fuel-title">⛽ Fuel Breakdown</p>
                    <div class="fuel-details">
                        <span>Distance: {distance} km</span>
                        <span>Avg: {fuel_avg} km/L</span>
                        <span>Liters: {liters:.1f} L</span>
                        <span>@ Rs.{fuel_price}/L</span>
                        <span class="fuel-total">= Rs.{fuel_cost:,}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Stops overview
            if len(path) > 2:
                stops_html = '<div class="stops-container">'
                for i, stop in enumerate(path):
                    if i == 0:
                        stops_html += f'<span class="stop-badge stop-start">START: {stop}</span>'
                    elif i == len(path) - 1:
                        stops_html += f'<span class="stop-badge stop-end">END: {stop}</span>'
                    else:
                        stops_html += f'<span class="stop-badge stop-mid">STOP {i}: {stop}</span>'
                    if i < len(path) - 1:
                        stops_html += '<span class="stop-arrow">→</span>'
                stops_html += '</div>'
                st.markdown(stops_html, unsafe_allow_html=True)
            
            # Tabs
            tabs = st.tabs(["🗺️ MAP", "🚗 DRIVE", "📍 DIRECTIONS", "💾 OFFLINE", "🍽️ FOOD", "🏨 STAY", "☕ CAFÉS", "🌳 PARKS"])
            
            with tabs[0]:  # MAP
                st.markdown('<div class="map-container">', unsafe_allow_html=True)
                st_folium(create_map(path, all_locations, mode_key), width=None, height=450, returned_objects=[])
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<p style="text-align:center;color:var(--text-muted);margin-top:0.5rem;">🟢 Start • 🔵 Stop • 🔴 End</p>', unsafe_allow_html=True)
            
            with tabs[1]:  # DRIVE MODE
                # Initialize drive mode state
                if 'drive_step' not in st.session_state:
                    st.session_state.drive_step = 0
                
                current_step = st.session_state.drive_step
                
                if current_step < len(path) - 1:
                    current_loc = path[current_step]
                    next_loc = path[current_step + 1]
                    
                    seg_dist_straight = calculate_distance_km(
                        all_locations[current_loc]["lat"], all_locations[current_loc]["lon"],
                        all_locations[next_loc]["lat"], all_locations[next_loc]["lon"]
                    )
                    seg_dist = get_road_distance(seg_dist_straight)
                    
                    # Calculate remaining distance
                    remaining_straight = 0
                    for i in range(current_step, len(path) - 1):
                        remaining_straight += calculate_distance_km(
                            all_locations[path[i]]["lat"], all_locations[path[i]]["lon"],
                            all_locations[path[i+1]]["lat"], all_locations[path[i+1]]["lon"]
                        )
                    remaining = get_road_distance(remaining_straight)
                    
                    progress_pct = ((distance - remaining) / distance) * 100 if distance > 0 else 0
                    eta = est_time(remaining, selected_speed)
                    direction_icon = get_direction_icon(current_loc, next_loc, all_locations)
                    
                    # Create mini map for current segment
                    drive_map = folium.Map(
                        location=[all_locations[current_loc]["lat"], all_locations[current_loc]["lon"]],
                        zoom_start=10,
                        tiles='CartoDB dark_matter'
                    )
                    
                    # Add markers for current segment
                    folium.Marker(
                        [all_locations[current_loc]["lat"], all_locations[current_loc]["lon"]],
                        tooltip="📍 You are here",
                        icon=folium.Icon(color='green', icon='car', prefix='fa')
                    ).add_to(drive_map)
                    
                    folium.Marker(
                        [all_locations[next_loc]["lat"], all_locations[next_loc]["lon"]],
                        tooltip=f"🎯 Next: {next_loc}",
                        icon=folium.Icon(color='blue', icon='flag', prefix='fa')
                    ).add_to(drive_map)
                    
                    # Add route line
                    segment_coords = [
                        [all_locations[current_loc]["lat"], all_locations[current_loc]["lon"]],
                        [all_locations[next_loc]["lat"], all_locations[next_loc]["lon"]]
                    ]
                    folium.PolyLine(segment_coords, weight=6, color='#22c55e', opacity=0.9).add_to(drive_map)
                    plugins.AntPath(segment_coords, delay=800, weight=4, color='#22c55e', pulse_color='#fff').add_to(drive_map)
                    
                    drive_map.fit_bounds(segment_coords, padding=[50, 50])
                    
                    # Navigation Header Card
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #1a472a 0%, #0d1f12 100%); border-radius: 16px; padding: 20px; margin-bottom: 15px; border: 2px solid #22c55e;">
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div style="width: 12px; height: 12px; background: #22c55e; border-radius: 50%; animation: pulse 1.5s infinite;"></div>
                                    <span style="color: #22c55e; font-weight: 700; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">NAVIGATING</span>
                                </div>
                                <span style="color: #888; font-size: 0.85rem;">Step {current_step + 1}/{len(path) - 1}</span>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 4rem; margin-bottom: 5px;">{direction_icon}</div>
                                <p style="color: #fff; font-size: 1.8rem; font-weight: 700; margin: 10px 0;">Head to {next_loc}</p>
                                <p style="color: #22c55e; font-size: 3rem; font-weight: 800;">~{seg_dist:.0f} <span style="font-size: 1.2rem; color: #888;">km</span></p>
                            </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mini Map
                    st_folium(drive_map, width=None, height=250, returned_objects=[])
                    
                    # Info Cards Row
                    col_info1, col_info2, col_info3 = st.columns(3)
                    with col_info1:
                        st.markdown(f"""
                        <div style="background: #111; border-radius: 12px; padding: 15px; text-align: center;">
                            <p style="color: #666; font-size: 0.75rem; margin-bottom: 5px;">📍 FROM</p>
                            <p style="color: #fff; font-size: 1rem; font-weight: 600;">{current_loc}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_info2:
                        st.markdown(f"""
                        <div style="background: #111; border-radius: 12px; padding: 15px; text-align: center;">
                            <p style="color: #666; font-size: 0.75rem; margin-bottom: 5px;">🎯 TO</p>
                            <p style="color: #22c55e; font-size: 1rem; font-weight: 600;">{next_loc}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_info3:
                        st.markdown(f"""
                        <div style="background: #111; border-radius: 12px; padding: 15px; text-align: center;">
                            <p style="color: #666; font-size: 0.75rem; margin-bottom: 5px;">⏱️ SEGMENT</p>
                            <p style="color: #4ade80; font-size: 1rem; font-weight: 600;">{est_time(seg_dist, selected_speed)}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Progress Bar
                    st.markdown(f"""
                    <div style="background: #111; border-radius: 12px; padding: 15px; margin: 15px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span style="color: #888; font-size: 0.85rem;">Journey Progress</span>
                            <span style="color: #22c55e; font-weight: 600;">{progress_pct:.0f}%</span>
                        </div>
                        <div style="background: #222; border-radius: 10px; height: 12px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #22c55e, #4ade80); width: {progress_pct:.0f}%; height: 100%; border-radius: 10px; transition: width 0.5s;"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                            <span style="color: #888;">📏 {remaining:.0f} km left</span>
                            <span style="color: #22c55e; font-weight: 600;">🕐 ETA: {eta}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Next stop preview
                    if current_step + 2 < len(path):
                        st.markdown(f"""
                        <div style="background: #0a0a0a; border: 1px solid #222; border-radius: 12px; padding: 12px;">
                            <p style="color: #666; font-size: 0.75rem; margin-bottom: 5px;">⏭️ THEN CONTINUE TO</p>
                            <p style="color: #888; font-size: 0.95rem;">{path[current_step + 2]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Navigation Controls
                    col_d1, col_d2, col_d3 = st.columns([1, 1, 1])
                    with col_d1:
                        if st.button("⬅️ BACK", use_container_width=True, disabled=(current_step == 0)):
                            if st.session_state.drive_step > 0:
                                st.session_state.drive_step -= 1
                                st.rerun()
                    with col_d2:
                        if st.button("🔄 RESTART", use_container_width=True):
                            st.session_state.drive_step = 0
                            st.rerun()
                    with col_d3:
                        if st.button("NEXT ➡️", use_container_width=True, type="primary"):
                            if st.session_state.drive_step < len(path) - 2:
                                st.session_state.drive_step += 1
                                st.rerun()
                
                else:
                    # Arrived at destination
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a472a 0%, #0d1f12 100%); border-radius: 20px; padding: 40px; text-align: center; border: 3px solid #22c55e;">
                        <div style="font-size: 5rem; margin-bottom: 15px;">🏁</div>
                        <h2 style="color: #22c55e; font-size: 2rem; margin-bottom: 10px;">You Have Arrived!</h2>
                        <p style="color: #fff; font-size: 1.3rem; margin-bottom: 5px;">{path[-1]}</p>
                        <p style="color: #888; font-size: 1rem;">Journey Complete • Total: ~{distance:.0f} km</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("🔄 Start Over", use_container_width=True):
                        st.session_state.drive_step = 0
                        st.rerun()
                    
                    st.balloons()
            
            with tabs[2]:  # DIRECTIONS
                st.markdown("### 🧭 Directions")
                st.markdown(f"*Distances are road estimates at **{selected_speed} km/h***")
                badge_color = "var(--info)" if route_mode == "local" else "var(--success)"
                badge_text = "🏙️ Local" if route_mode == "local" else "🛣️ Inter-City"
                st.markdown(f'<span style="background:{badge_color};color:white;padding:4px 12px;border-radius:20px;font-size:0.8rem;">{badge_text}</span>', unsafe_allow_html=True)
                
                cumulative = 0
                for i in range(len(path) - 1):
                    frm, to = path[i], path[i+1]
                    seg_straight = calculate_distance_km(all_locations[frm]["lat"], all_locations[frm]["lon"],
                                                        all_locations[to]["lat"], all_locations[to]["lon"])
                    seg_dist = get_road_distance(seg_straight)
                    cumulative += seg_dist
                    direction = get_direction_icon(frm, to, all_locations)
                    st.markdown(f"""
                    <div class="nav-step">
                        <div class="nav-number">{direction}</div>
                        <div class="nav-content">
                            <p class="nav-cities">{frm} → {to}</p>
                            <p class="nav-meta">📏 ~{seg_dist:.0f} km • ⏱️ {est_time(seg_dist, selected_speed)} • Total: {cumulative:.0f} km</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="nav-step" style="border-left-color: var(--error);">
                    <div class="nav-number" style="background: var(--error);">🏁</div>
                    <div class="nav-content">
                        <p class="nav-cities">Arrived at {path[-1]}</p>
                        <p class="nav-meta">🎉 Journey Complete!</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with tabs[3]:  # OFFLINE SAVE
                st.markdown("### 💾 Save for Offline")
                st.markdown("*Download your route to use without internet*")
                
                # Generate offline data
                offline_data = generate_offline_data(path, distance, all_locations, mode_key, fuel_avg, fuel_price, selected_speed)
                text_route = create_text_route(offline_data)
                
                st.markdown("---")
                
                # Text file download
                st.markdown("""
                <div class="offline-card">
                    <p class="offline-title">📄 Text Route (Printable)</p>
                    <p class="offline-desc">Plain text format - perfect for printing or viewing on any device</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(get_download_link(text_route, f"SafarPak_Route_{path[0]}_to_{path[-1]}.txt", "text"), unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # JSON file download
                st.markdown("""
                <div class="offline-card">
                    <p class="offline-title">📊 JSON Data (Technical)</p>
                    <p class="offline-desc">Machine-readable format with coordinates for GPS apps</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(get_download_link(offline_data, f"SafarPak_Route_{path[0]}_to_{path[-1]}.json", "json"), unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Preview
                with st.expander("👁️ Preview Text Route"):
                    st.code(text_route, language=None)
                
                with st.expander("👁️ Preview JSON Data"):
                    st.json(offline_data)
                
                st.markdown("""
                <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 1rem; margin-top: 1rem;">
                    <p style="color: var(--text-secondary); font-size: 0.85rem;">
                        💡 <strong>Tip:</strong> Save these files before your journey. The text file works offline on any device, 
                        while the JSON file can be imported into GPS navigation apps.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Nearby places tabs (adjusted indices)
            categories = [(4, "restaurants", "🍽️"), (5, "hotels", "🏨"), (6, "cafes", "☕"), (7, "parks", "🌳")]
            
            for idx, cat, icon in categories:
                with tabs[idx]:
                    st.markdown(f"### {icon} Nearby {cat.title()}")
                    selected = st.selectbox(f"📍 Location:", path, index=len(path)-1, key=f"sel_{cat}", label_visibility="collapsed")
                    st.markdown(f"*Showing {cat} near **{selected}***")
                    
                    for place in get_nearby_places(selected, cat):
                        stars = "⭐" * int(place['rating'])
                        st.markdown(f"""
                        <div class="place-card">
                            <div class="place-icon">{icon}</div>
                            <div class="place-info">
                                <p class="place-name">{place['name']}</p>
                                <p class="place-detail">{place['type']} • {place['price']}</p>
                                <p class="place-rating">{stars} {place['rating']}</p>
                            </div>
                            <div class="place-distance">{place['distance']}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown(f'<div class="success-banner"><p class="success-text">✅ Route: {len(path)} locations, {distance} km</p></div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="error-banner">
                <p class="error-title">❌ No Route Found</p>
                <p class="error-text">Try increasing the range or select different locations.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p><strong>SafarPak</strong> — Explore Pakistan with Confidence 🇵🇰</p>
        <p style="font-size:0.75rem;margin-top:0.5rem;">Navigate • Discover • Experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Remove ONLY the button - keep sidebar content
    st.markdown("""
    <style>
        /* Force hide ONLY the button with maximum specificity */
        html body button[name="keyboard_double_arrow_left"],
        html body section[data-testid="stSidebar"] button[name="keyboard_double_arrow_left"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            position: absolute !important;
            left: -9999px !important;
            pointer-events: none !important;
        }
    </style>
    <script>
        (function() {
            function hideToggle() {
                // Remove ONLY the button, not the parent div
                document.querySelectorAll('button[name="keyboard_double_arrow_left"]').forEach(b => {
                    b.style.cssText = 'display:none!important;visibility:hidden!important;opacity:0!important;width:0!important;height:0!important;padding:0!important;margin:0!important;position:absolute!important;left:-9999px!important;pointer-events:none!important;';
                    try { b.remove(); } catch(e) {}
                });
            }
            hideToggle();
            setInterval(hideToggle, 5);
            requestAnimationFrame(function loop() { hideToggle(); requestAnimationFrame(loop); });
        })();
    </script>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
