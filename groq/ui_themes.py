import streamlit as st

def init_theme_state():
    """Initialize theme state in session if not exists"""
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

def render_theme_toggle():
    """Render the theme toggle in sidebar"""
    st.sidebar.toggle("🌙 Dark Mode", key="dark_mode")

def get_dark_theme_css():
    """Return CSS for dark theme - Clean Matte Black & Grey"""
    return """
        <style>
            /* Hide Streamlit branding - ADD THIS SECTION */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Remove top padding */
            .main > div {
                padding-top: 0rem;
            }
            
            /* Main App Background - Matte Black */
            .stApp {
                background-color: #1a1a1a !important;
                color: #e5e5e5 !important;
            }

            /* Main App Background - Matte Black */
            .stApp {
                background-color: #1a1a1a !important;
                color: #e5e5e5 !important;
            }
            
            /* Sidebar - Matte Dark Grey */
            .stSidebar > div {
                background-color: #2d2d2d !important;
                color: #e5e5e5 !important;
            }
            
            /* Remove Unwanted Container Backgrounds */
            .stContainer, .element-container, .block-container {
                background-color: transparent !important;
                border: none !important;
            }
            
            /* Text Elements */
            .stMarkdown, .stText, p, span, div, label {
                color: #e5e5e5 !important;
            }
            
            /* Headers */
            h1, h2, h3, h4, h5, h6 {
                color: #ffffff !important;
                font-weight: 600 !important;
            }
            
            /* Input Fields - Match Light Mode Size */
            .stTextInput > div > div > input {
                background-color: #404040 !important;
                color: #ffffff !important;
                border: 1px solid #555555 !important;
                border-radius: 6px !important;
                padding: 0.5rem 0.75rem !important;
                min-height: 2.5rem !important;
                height: 2.5rem !important;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: #8b5cf6 !important;
                box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
            }
            
            .stTextInput > div > div > input::placeholder {
                color: #aaaaaa !important;
            }
            
            /* Fix Selectbox - Complete Dark Theme Solution */
            .stSelectbox > div > div > div {
                background-color: #404040 !important;
                color: #ffffff !important;
                border: 1px solid #555555 !important;
                border-radius: 6px !important;
                min-height: 2.5rem !important;
                height: 2.5rem !important;
                padding: 0.5rem 0.75rem !important;
            }

            /* Force Selected Value Text Color */
            div[data-baseweb="select"] span {
                color: #ffffff !important;
            }

            /* Force Input Text Color */
            div[data-baseweb="select"] input {
                color: #ffffff !important;
            }

            /* Selected Value Container */
            div[data-baseweb="select"] > div > div {
                color: #ffffff !important;
                background-color: #404040 !important;
            }

            /* Dropdown Menu Container */
            div[data-baseweb="menu"] {
                background-color: #404040 !important;
                border: 1px solid #555555 !important;
            }

            /* Dropdown Menu List */
            div[data-baseweb="menu"] ul {
                background-color: #404040 !important;
            }

            /* Individual Dropdown Options */
            div[data-baseweb="menu"] li {
                background-color: #404040 !important;
                color: #ffffff !important;
                padding: 0.75rem !important;
                font-weight: 500 !important;
            }

            /* Dropdown Options Hover Effect */
            div[data-baseweb="menu"] li:hover {
                background-color: #555555 !important;
                color: #ffffff !important;
            }

            /* Force Option Text Color */
            div[data-baseweb="menu"] span {
                color: #ffffff !important;
            }
            
            /* File Uploader - Match Light Mode Size */
            .stFileUploader {
                background: rgba(45, 45, 45, 0.95) !important;
                border: 1px dashed #666666 !important;
                border-radius: 8px !important;
                padding: 1rem !important;
                backdrop-filter: blur(10px) !important;
                box-shadow: none !important;
            }

            .stFileUploader:hover {
                border-color: rgba(139, 92, 246, 0.5) !important;
                background: rgba(55, 55, 55, 0.95) !important;
                transform: none !important;
                transition: all 0.3s ease !important;
            }

            /* File Uploader Text */
            .stFileUploader label {
                color: #ffffff !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
            }

            .stFileUploader div {
                color: #ffffff !important;
                font-weight: 500 !important;
            }

            /* Drag and Drop Text */
            .stFileUploader section > div {
                color: #ffffff !important;
                font-weight: 500 !important;
            }

            /* File Info Text */
            .stFileUploader span {
                color: #ffffff !important;
                font-weight: 400 !important;
            }

            /* File Size and Type Info */
            .stFileUploader small {
                color: #ffffff !important;
            }

            /* Any remaining blue text */
            .stFileUploader * {
                color: #ffffff !important;
            }

            /* Browse Files Button - Match Light Mode Size */
            .stFileUploader button {
                background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 0.5rem 1rem !important;
                font-weight: 600 !important;
                font-size: 0.875rem !important;
                transition: all 0.2s ease !important;
                min-height: 2.5rem !important;
                height: 2.5rem !important;
            }

            .stFileUploader button:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4) !important;
            }

            /* Uploaded File Display - Match Light Mode */
            .stFileUploader > div > div {
                background: rgba(35, 35, 35, 0.9) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 6px !important;
                color: #ffffff !important;
                padding: 0.75rem !important;
            }
            
            /* Sliders - Purple Accent */
            .stSlider > div > div > div > div {
                background-color: #8b5cf6 !important;
            }
            
            /* Primary Button - Match Light Mode Size Exactly */
            .stButton > button {
                background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 0.75rem 1.5rem !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3) !important;
                min-height: 3rem !important;
                height: 3rem !important;
                width: 100% !important;
                white-space: normal !important;
                text-align: center !important;
            }

            .stButton > button:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 8px rgba(139, 92, 246, 0.4) !important;
                background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
            }

            /* Update Summary Button - Force Purple Styling */
            button[kind="primary"], 
            button[data-testid*="update"], 
            button[title*="Update"], 
            .stDownloadButton > button {
                background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 0.75rem 1.5rem !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3) !important;
                min-height: 3rem !important;
                height: 3rem !important;
            }

            button[kind="primary"]:hover, 
            button[data-testid*="update"]:hover, 
            button[title*="Update"]:hover,
            .stDownloadButton > button:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 8px rgba(139, 92, 246, 0.4) !important;
                background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
            }

            /* JSON Display - Match Light Mode Size */
            .stJson {
                background-color: #404040 !important;
                border: 1px solid #555555 !important;
                border-radius: 8px !important;
                padding: 1rem !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
            }

            /* JSON Content Text Color */
            .stJson pre {
                color: #ffffff !important;
            }

            /* Expanders - Match Light Mode Size */
            div[data-testid="stExpander"] details summary {
                background: rgba(45, 45, 45, 0.95) !important;
                color: #ffffff !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 8px 8px 0 0 !important;
                padding: 1rem !important;
                font-weight: 600 !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
                backdrop-filter: blur(10px) !important;
            }

            div[data-testid="stExpander"] details summary:hover {
                background: rgba(55, 55, 55, 0.95) !important;
                border-color: rgba(139, 92, 246, 0.3) !important;
            }

            div[data-testid="stExpander"] > div > div {
                background: rgba(40, 40, 40, 0.95) !important;
                color: #e5e5e5 !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-top: none !important;
                border-radius: 0 0 8px 8px !important;
                padding: 1rem !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
                backdrop-filter: blur(10px) !important;
            }

            /* Column Alignment Fix */
            div[data-testid="column"] {
                display: flex !important;
                height: 100% !important;
            }

            div[data-testid="column"] > div {
                display: flex !important;
                flex-direction: column !important;
                height: 100% !important;
            }

            div[data-testid="column"] .stButton {
                flex: 1 !important;
                display: flex !important;
            }
            
            /* Progress Bar */
            .stProgress > div > div > div {
                background: linear-gradient(90deg, #8b5cf6, #7c3aed) !important;
            }
            
            /* Alerts & Messages - Match Light Mode */
            .stAlert {
                background-color: #404040 !important;
                color: #ffffff !important;
                border: 1px solid #555555 !important;
                border-radius: 6px !important;
                padding: 1rem !important;
            }
            
            /* Sidebar Specific Elements */
            .stSidebar .stSelectbox > div > div > div {
                background-color: #404040 !important;
                color: #ffffff !important;
                border: 1px solid #555555 !important;
                min-height: 2.5rem !important;
                height: 2.5rem !important;
            }
            
            .stSidebar .stSlider > div > div > div > div {
                background-color: #8b5cf6 !important;
            }
            
            .stSidebar h1, .stSidebar h2, .stSidebar h3 {
                color: #ffffff !important;
            }
            
            .stSidebar label {
                color: #e5e5e5 !important;
            }
            
            /* Caption Text */
            .stCaption {
                color: #aaaaaa !important;
            }
            
            /* Fix Toggle Switch */
            .stCheckbox > label {
                color: #e5e5e5 !important;
            }
            
            /* AGGRESSIVE FIXES FOR STUBBORN WHITE BACKGROUNDS */
            
            /* Fix File Uploader Inner Container */
            div[data-testid="stFileUploader"] {
                background-color: #404040 !important;
            }
            
            div[data-testid="stFileUploader"] > div {
                background-color: #404040 !important;
            }
            
            div[data-testid="stFileUploader"] section {
                background-color: #404040 !important;
                border: 2px dashed #666666 !important;
                padding: 1rem !important;
            }
            
            div[data-testid="stFileUploader"] section > div {
                background-color: transparent !important;
            }
            
            /* File Upload Drop Area */
            .uploadedFile {
                background-color: #404040 !important;
                border: 1px solid #555555 !important;
                padding: 0.75rem !important;
            }
            
            /* Fix Any Remaining White Containers */
            .stApp > div > div > div > div {
                background-color: transparent !important;
            }
            
            /* Nuclear option for any white divs */
            div[style*="background-color: rgb(255, 255, 255)"] {
                background-color: #404040 !important;
            }
            
            div[style*="background: rgb(255, 255, 255)"] {
                background-color: #404040 !important;
            }
            
            /* Fix specific file uploader elements */
            .stFileUploader > div > div > div {
                background-color: #404040 !important;
            }
            
            .stFileUploader button {
                background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
                color: #ffffff !important;
                border: none !important;
                min-height: 2.5rem !important;
                height: 2.5rem !important;
                padding: 0.5rem 1rem !important;
            }

            /* Match spacing between elements */
            .element-container {
                margin-bottom: 1rem !important;
            }

            /* Ensure consistent component heights */
            .stTextInput, .stSelectbox, .stFileUploader {
                min-height: auto !important;
            }
        </style>
    """

def get_light_theme_css():
    """Return CSS for light theme - Clean & Professional"""
    return """
        <style>
             /* Hide Streamlit branding - ADD THIS SECTION */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Remove top padding */
            .main > div {
                padding-top: 0rem;
            }
            
            /* Main App Background - Matte Black */
            .stApp {
                background-color: #1a1a1a !important;
                color: #e5e5e5 !important;
            }
            
            /* Main App Background - Clean White */
            .stApp {
                background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
                color: #334155 !important;
            }
            
            /* Sidebar - Subtle Light */
            .stSidebar > div {
                background-color: rgba(248, 250, 252, 0.95) !important;
                border-right: 1px solid #e2e8f0 !important;
            }
            
            /* Remove Box Backgrounds - Keep It Clean */
            .stContainer, .element-container, .block-container {
                background-color: transparent !important;
                border: none !important;
            }
            
            /* Text Elements - Proper Contrast */
            .stMarkdown, .stText, p, span, div, label {
                color: #334155 !important;
            }
            
            /* Headers - Clean Dark */
            h1, h2, h3, h4, h5, h6 {
                color: #1e293b !important;
                font-weight: 600 !important;
            }
            
            /* Input Fields - Consistent Size */
            .stTextInput > div > div > input {
                background-color: rgba(255, 255, 255, 0.8) !important;
                color: #334155 !important;
                border: 1px solid #cbd5e1 !important;
                border-radius: 6px !important;
                backdrop-filter: blur(10px) !important;
                padding: 0.5rem 0.75rem !important;
                min-height: 2.5rem !important;
                height: 2.5rem !important;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: #8b5cf6 !important;
                box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.1) !important;
            }
            
            .stTextInput > div > div > input::placeholder {
                color: #64748b !important;
            }
            
            /* File Uploader - Consistent Size */
            .stFileUploader {
                background-color: rgba(255, 255, 255, 0.6) !important;
                border: 1px dashed #94a3b8 !important;
                border-radius: 8px !important;
                backdrop-filter: blur(10px) !important;
                padding: 1rem !important;
            }
            
            .stFileUploader:hover {
                border-color: #8b5cf6 !important;
                background-color: rgba(139, 92, 246, 0.02) !important;
            }
            
            /* Fix Selectbox - All Parts */
            .stSelectbox > div > div > div {
                background-color: rgba(255, 255, 255, 0.8) !important;
                color: #334155 !important;
                border: 1px solid #cbd5e1 !important;
                border-radius: 6px !important;
                min-height: 2.5rem !important;
                height: 2.5rem !important;
                padding: 0.5rem 0.75rem !important;
            }

            /* Force Selected Value Text Color */
            div[data-baseweb="select"] span {
                color: #334155 !important;
            }

            /* Force Input Text Color */
            div[data-baseweb="select"] input {
                color: #334155 !important;
            }

            /* Selected Value Container */
            div[data-baseweb="select"] > div > div {
                color: #334155 !important;
            }
            
            /* Primary Button - Consistent Size */
            .stButton > button {
                background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 0.75rem 1.5rem !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 2px 4px rgba(139, 92, 246, 0.2) !important;
                min-height: 3rem !important;
                height: 3rem !important;
                width: 100% !important;
                white-space: normal !important;
                text-align: center !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3) !important;
                background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
            }

            /* Update Summary Button - Force Purple Styling */
            button[kind="primary"], 
            button[data-testid*="update"], 
            button[title*="Update"], 
            .stDownloadButton > button {
                background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 0.75rem 1.5rem !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3) !important;
                min-height: 3rem !important;
                height: 3rem !important;
            }

            button[kind="primary"]:hover, 
            button[data-testid*="update"]:hover, 
            button[title*="Update"]:hover,
            .stDownloadButton > button:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 8px rgba(139, 92, 246, 0.4) !important;
                background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
            }
            
            /* JSON Display - Consistent Size */
            .stJson {
                background-color: rgba(248, 250, 252, 0.8) !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 8px !important;
                backdrop-filter: blur(10px) !important;
                padding: 1rem !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
            }
            
            /* Expanders - Consistent Size */
            div[data-testid="stExpander"] details summary {
                background: rgba(248, 250, 252, 0.8) !important;
                color: #334155 !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 8px 8px 0 0 !important;
                padding: 1rem !important;
                font-weight: 600 !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
                backdrop-filter: blur(10px) !important;
            }

            div[data-testid="stExpander"] details summary:hover {
                background: rgba(228, 232, 237, 0.8) !important;
                border-color: rgba(139, 92, 246, 0.3) !important;
            }

            div[data-testid="stExpander"] > div > div {
                background: rgba(255, 255, 255, 0.6) !important;
                color: #334155 !important;
                border: 1px solid #e2e8f0 !important;
                border-top: none !important;
                border-radius: 0 0 8px 8px !important;
                padding: 1rem !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
                backdrop-filter: blur(10px) !important;
            }

            /* Browse Files Button - Consistent Size */
            .stFileUploader button {
                background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 0.5rem 1rem !important;
                font-weight: 600 !important;
                font-size: 0.875rem !important;
                transition: all 0.2s ease !important;
                min-height: 2.5rem !important;
                height: 2.5rem !important;
            }

            /* Column Alignment Fix */
            div[data-testid="column"] {
                display: flex !important;
                height: 100% !important;
            }

            div[data-testid="column"] > div {
                display: flex !important;
                flex-direction: column !important;
                height: 100% !important;
            }

            div[data-testid="column"] .stButton {
                flex: 1 !important;
                display: flex !important;
            }
            
            /* Progress Bar */
            .stProgress > div > div > div {
                background: linear-gradient(90deg, #8b5cf6, #7c3aed) !important;
            }
            
            /* Alerts & Messages - Consistent Size */
            .stAlert {
                background-color: rgba(255, 255, 255, 0.8) !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 6px !important;
                backdrop-filter: blur(10px) !important;
                padding: 1rem !important;
            }
            
            /* Sidebar Elements */
            .stSidebar .stSlider > div > div > div > div {
                background-color: #8b5cf6 !important;
            }
            
            .stSidebar .stSelectbox > div > div {
                background-color: rgba(255, 255, 255, 0.8) !important;
                border: 1px solid #e2e8f0 !important;
                min-height: 2.5rem !important;
                height: 2.5rem !important;
            }
            
            .stSidebar h1, .stSidebar h2, .stSidebar h3 {
                color: #1e293b !important;
            }
            
            /* Remove Unnecessary Borders */
            .main .block-container {
                padding-top: 2rem !important;
            }
            
            /* Captions and Small Text */
            .stCaption {
                color: #64748b !important;
            }

            /* Match spacing between elements */
            .element-container {
                margin-bottom: 1rem !important;
            }

            /* Ensure consistent component heights */
            .stTextInput, .stSelectbox, .stFileUploader {
                min-height: auto !important;
            }
        </style>
    """

def apply_theme():
    """Apply the selected theme based on session state"""
    if st.session_state.dark_mode:
        st.markdown(get_dark_theme_css(), unsafe_allow_html=True)
    else:
        st.markdown(get_light_theme_css(), unsafe_allow_html=True)

def setup_theme_system():
    """Complete theme setup - call this once at the beginning of your app"""
    init_theme_state()
    render_theme_toggle()
    apply_theme()

# Additional utility functions for future enhancements
class ThemeConfig:
    """Configuration class for theme customization"""
    
    DARK_COLORS = {
        'primary': '#8b5cf6',
        'primary_hover': '#7c3aed',
        'background': '#1e1e1e',
        'sidebar': '#2a2a2a',
        'surface': '#404040',
        'text': '#ffffff',
        'text_secondary': '#aaaaaa',
        'border': '#555555'
    }
    
    LIGHT_COLORS = {
        'primary': '#8b5cf6',
        'primary_hover': '#7c3aed',
        'background': '#ffffff',
        'sidebar': '#f8f9fa',
        'surface': '#f8f9fa',
        'text': '#333333',
        'text_secondary': '#888888',
        'border': '#ddd'
    }

def create_custom_theme(colors):
    """Create a custom theme with provided color scheme"""
    # This function can be extended to create themes programmatically
    # using the provided color dictionary
    pass

def get_current_theme_colors():
    """Get current theme color scheme"""
    if st.session_state.get('dark_mode', False):
        return ThemeConfig.DARK_COLORS
    else:
        return ThemeConfig.LIGHT_COLORS