import streamlit as st
from google import genai
import requests
import urllib.parse
import time

# --- 1. THE GLASSMORPHISM ENGINE ---
st.set_page_config(page_title="Subtext", layout="wide", initial_sidebar_state="collapsed")

def apply_cinematic_theme(poster_url):
    st.markdown(f"""
<style>
/* Base Layer & Hide Sidebar */
[data-testid="collapsedControl"], [data-testid="stSidebar"] {{ display: none !important; }}

.stApp {{
    background: url("{poster_url}");
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
    transition: background 1s ease-in-out;
}}

/* Unified Full-Screen Frost */
[data-testid="stAppViewContainer"] {{
    background-color: rgba(0, 0, 0, 0.75) !important; 
    backdrop-filter: blur(80px) saturate(150%) !important;
    -webkit-backdrop-filter: blur(80px) saturate(150%) !important;
}}

/* Typography */
h1, h2, h3, p, span {{ color: rgba(255,255,255,0.95); font-family: "SF Pro Display", sans-serif; }}
h1 {{ font-weight: 800; letter-spacing: -1.5px; }}

.gradient-text {{
    background: linear-gradient(90deg, #00f2fe, #4facfe, #f093fb, #f5576c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 25px rgba(245, 87, 108, 0.3);
}}

/* SPLASH SCREEN TYPING ANIMATION */
.splash-container {{ height: 80vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
.typewriter h1 {{
    overflow: hidden; border-right: 4px solid rgba(255,255,255,0.8); white-space: nowrap; margin: 0 auto; font-size: 6.5rem; width: 0;
    animation: typing 2s steps(30, end) forwards, blink-caret 1.5s step-end infinite;
}}
@keyframes typing {{ from {{ width: 0; }} to {{ width: 100%; }} }}
@keyframes blink-caret {{ from, to {{ border-color: transparent; }} 50% {{ border-color: rgba(255,255,255,0.8); }} }}

/* HEADERS */
.landing-title {{ font-size: 6.5rem !important; margin-bottom: 5px; text-align: center; }}
.landing-title::after {{
    content: ""; display: block; width: 140px; height: 3px; 
    background: #f5c518; margin: 25px auto 0 auto; 
    box-shadow: 0 0 15px rgba(245, 197, 24, 0.8); border-radius: 2px;
}}

.curated-title {{ text-align: center; font-size: 3.5rem; font-weight: 800; letter-spacing: -1.5px; margin: 80px 0 30px 0; }}
.curated-title::after {{
    content: ""; display: block; width: 60px; height: 3px; 
    background: #f5c518; margin: 20px auto 0 auto; 
    box-shadow: 0 0 15px rgba(245, 197, 24, 0.8); border-radius: 2px;
}}

.genre-header {{ 
    color: rgba(255,255,255,0.9); font-size: 1.8rem; font-weight: 700; letter-spacing: 0.5px; 
    margin-top: 50px; margin-bottom: 20px; padding-left: 15px; border-left: 4px solid #f5c518; 
}}

/* ANIMATIONS */
.entrance-anim {{ opacity: 0; transform: translateY(50px); animation: pullUpFade 1.5s cubic-bezier(0.22, 1, 0.36, 1) forwards; }}
.pull-top-left {{ opacity: 0; transform: translate(20%, 10vh) scale(1.1); animation: glideToLeft 1.5s cubic-bezier(0.22, 1, 0.36, 1) forwards; }}
.gallery-fade {{ opacity: 0; transform: translateX(40px); animation: pullUpFade 1.5s cubic-bezier(0.22, 1, 0.36, 1) forwards; animation-delay: 0.4s; }}
.terminal-fade {{ opacity: 0; transform: translateY(20px); animation: pullUpFade 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards; }}

.delay-1 {{ animation-delay: 0.1s; }}
.delay-2 {{ animation-delay: 0.2s; }}
.delay-3 {{ animation-delay: 0.3s; }}
.delay-4 {{ animation-delay: 0.4s; }}

@keyframes pullUpFade {{ 0% {{ opacity: 0; transform: translateY(40px); }} 100% {{ opacity: 1; transform: translateY(0); }} }}
@keyframes glideToLeft {{ 0% {{ opacity: 0; transform: translate(20%, 10vh) scale(1.1); }} 100% {{ opacity: 1; transform: translate(0, 0) scale(1); }} }}

/* UI ELEMENTS */
.poster-img {{ border-radius: 20px !important; overflow: hidden !important; box-shadow: 0 40px 80px rgba(0,0,0,0.7); margin-bottom: 20px; }}
.meta-badge {{ display: inline-block; padding: 6px 14px; margin: 4px; border-radius: 20px; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); font-size: 0.85rem; font-weight: 500; backdrop-filter: blur(10px); }}
.studio-badge {{ background: rgba(255, 255, 255, 0.25); color: #fff; border: 1px solid rgba(255,255,255,0.4); font-weight: 700; }}

div.stButton > button {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.02)) !important; 
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    backdrop-filter: blur(15px) !important; color: white !important; border-radius: 14px !important; width: 100% !important;
}}

[data-testid="stTextInput"] > div > div, .rainbow-btn button {{
    background-color: rgba(10, 10, 10, 0.6) !important; border-radius: 40px !important; border: 2px solid transparent !important;
    background-clip: padding-box, border-box !important; background-origin: padding-box, border-box !important;
    background-image: linear-gradient(rgba(10,10,10,0.8), rgba(10,10,10,0.8)), 
                      linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #8b00ff) !important;
}}
[data-testid="stTextInput"] input {{ color: white !important; text-align: center !important; background: transparent !important; }}
[data-testid="stTextInput"] {{ max-width: 340px; margin: 0 auto 15px auto; }}

.rainbow-btn {{ margin-bottom: 30px; display: flex; justify-content: center; width: 100%; }}
.rainbow-btn button {{ font-weight: 600 !important; font-size: 1.1rem !important; padding: 12px 30px !important; width: auto !important; min-width: 150px !important; }}

.rec-card {{ 
    background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.02); 
    border-radius: 16px; padding: 20px; text-align: center; backdrop-filter: blur(15px); height: 100%;
}}
.rec-card img {{ width: 100%; border-radius: 12px; margin-bottom: 15px; }}
iframe {{ border-radius: 16px; box-shadow: 0 15px 40px rgba(0,0,0,0.6); margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.1); }}

/* Suggested Prompt Pills */
.prompt-pill .stButton>button {{ 
    background: rgba(0,0,0,0.5) !important; border: 1px solid rgba(255,255,255,0.15) !important; 
    border-radius: 20px !important; font-size: 0.85rem !important; padding: 6px 14px !important; 
    color: rgba(255,255,255,0.7) !important; width: auto !important; min-width: 100px !important;
}}
.prompt-pill .stButton>button:hover {{ border-color: #f5c518 !important; color: #f5c518 !important; background: rgba(245, 197, 24, 0.1) !important; }}
</style>
    """, unsafe_allow_html=True)

# --- 2. CONFIG & STATE ---
GEMINI_KEY = st.secrets["GEMINI_KEY"]
OMDB_KEY = st.secrets["OMDB_KEY"]
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]

client = genai.Client(api_key=GEMINI_KEY)

if "active_view" not in st.session_state: st.session_state.active_view = "splash"
if "chat_history" not in st.session_state: st.session_state.chat_history = {} 
if "current_movie_data" not in st.session_state: st.session_state.current_movie_data = None
if "recommendations" not in st.session_state: st.session_state.recommendations = []

@st.cache_data(show_spinner=False)
def fetch_omdb(title):
    url = f"https://www.omdbapi.com/?t={title}&apikey={OMDB_KEY}"
    try: return requests.get(url).json()
    except: return None

@st.cache_data(show_spinner=False)
def fetch_youtube_trailer(query):
    safe_query = urllib.parse.quote(f"{query} official trailer")
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={safe_query}&type=video&key={YOUTUBE_API_KEY}"
    try: return requests.get(url).json()["items"][0]["id"]["videoId"]
    except: return None

def generate_recommendations():
    defaults = ["Ex Machina", "The Social Network", "Blade Runner 2049"]
    st.session_state.recommendations = [fetch_omdb(m) for m in defaults]

if not st.session_state.recommendations: generate_recommendations()

CURATED_COLLECTIONS = {
    "Sci-Fi & Cyberpunk": ["Dune", "Interstellar", "The Matrix"],
    "Masterpiece Drama": ["The Godfather", "Parasite", "Whiplash"],
    "Visually Stunning": ["Mad Max: Fury Road", "Spider-Man: Into the Spider-Verse", "Avatar"]
}

if st.session_state.active_view in ["splash", "landing"]: 
    apply_cinematic_theme("https://m.media-amazon.com/images/M/MV5BNzA1Njg4NzYxOV5BMl5BanBnXkFtZTgwODk5NjU3MzI@._V1_SX300.jpg")
elif st.session_state.current_movie_data: 
    apply_cinematic_theme(st.session_state.current_movie_data.get('Poster'))

def init_movie_state(movie_data):
    title = movie_data["Title"]
    if title not in st.session_state.chat_history:
        st.session_state.chat_history[title] = {"data": movie_data, "messages": [], "chat_active": False}
    st.session_state.current_movie_data = movie_data
    st.session_state.active_view = "discovery"

# --- 3. VIEW LOGIC ---
if st.session_state.active_view == "splash":
    st.markdown("""<div class="splash-container"><div class="typewriter"><h1><span class="gradient-text">Explore the Subtext.</span></h1></div></div>""", unsafe_allow_html=True)
    time.sleep(6); st.session_state.active_view = "landing"; st.rerun()
else:
    _, main_col, _ = st.columns([1, 8, 1])
    with main_col:
        if st.session_state.active_view == "landing":
            st.markdown("""<div class='entrance-anim delay-1' style='text-align: center; padding-top: 40px;'><h1 class='landing-title'><span class='gradient-text'>Explore the Subtext.</span></h1><p style='color: rgba(255,255,255,0.6); font-size: 1.2rem;'>Select a recommended film or search to begin deconstruction.</p></div>""", unsafe_allow_html=True)
            sc1, sc2, sc3 = st.columns([1, 2, 1])
            with sc2:
                st.markdown("<div class='entrance-anim delay-2'>", unsafe_allow_html=True)
                search_query = st.text_input("Search", placeholder="Search a film title...", label_visibility="collapsed")
                if search_query:
                    data = fetch_omdb(search_query)
                    if data and data.get("Response") == "True": init_movie_state(data); st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            
            cols = st.columns(3)
            for i, rec in enumerate(st.session_state.recommendations):
                with cols[i]:
                    st.markdown(f"<div class='rec-card entrance-anim delay-{i+2}'><img src='{rec['Poster']}'><h3>{rec['Title']}</h3><p style='color: #f5c518; font-weight: bold;'>IMDb: {rec['imdbRating']}</p></div>", unsafe_allow_html=True)
                    if st.button(f"Analyze {rec['Title']}", key=f"rec_{i}"): init_movie_state(rec); st.rerun()
                            
            st.markdown("<h2 class='curated-title entrance-anim delay-4'><span class='gradient-text'>Curated Collections</span></h2>", unsafe_allow_html=True)
            for genre, titles in CURATED_COLLECTIONS.items():
                st.markdown(f"<div class='genre-header entrance-anim delay-4'>{genre}</div>", unsafe_allow_html=True)
                genre_cols = st.columns(3)
                for i, title in enumerate(titles):
                    m = fetch_omdb(title)
                    with genre_cols[i]:
                        st.markdown(f"<div class='rec-card entrance-anim delay-4'><img src='{m['Poster']}'><h3>{m['Title']}</h3><p style='color: #f5c518; font-weight: bold;'>IMDb: {m.get('imdbRating')}</p></div>", unsafe_allow_html=True)
                        if st.button(f"Analyze {m['Title']}", key=f"curated_{genre}_{i}"): init_movie_state(m); st.rerun()

        elif st.session_state.active_view == "discovery" and st.session_state.current_movie_data:
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.markdown("<div class='rainbow-btn entrance-anim' style='margin-top: 20px;'>", unsafe_allow_html=True)
                if st.button("Home", key="home_btn"): st.session_state.active_view = "landing"; st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            movie = st.session_state.current_movie_data
            title = movie['Title']
            movie_state = st.session_state.chat_history[title]
            
            # Formatted Awards logic
            awards_raw = movie.get('Awards', 'N/A')
            major_awards = awards_raw.split('.')[0] if '.' in awards_raw else awards_raw
            nom_count = awards_raw.split('.')[-1] if '.' in awards_raw else ""
            director = movie.get('Director', 'the director').split(',')[0]

            col1, col2 = st.columns([1.2, 2.5], gap="large")
            with col1:
                st.markdown(f"""
<div class='pull-top-left' style='padding-top: 20px;'>
<img src='{movie['Poster']}' class='poster-img' style='width: 100%;'>
<h1 style='font-size: 2.5rem;'>{movie['Title']}</h1>
<div style='margin-bottom: 15px;'>
<span class='meta-badge studio-badge'>{movie.get('Production', 'N/A')}</span>
<span class='meta-badge'>{movie.get('Year', 'N/A')}</span>
<span class='meta-badge' style='border-color: #f5c518; color: #f5c518;'>IMDb: {movie.get('imdbRating', 'N/A')}</span>
</div>
<p style='color: rgba(255,255,255,0.8); font-size: 1.1rem;'>"{movie.get('Plot', '')}"</p>
<div style='background: rgba(255,255,255,0.03); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);'>
<div style='display: flex; margin-bottom: 8px;'><div style='width: 85px; flex-shrink: 0;'><strong style='color: rgba(255,255,255,0.5); text-transform: uppercase; font-size: 0.8rem;'>Director</strong></div><div style='color: #fff; font-size: 0.85rem;'>{movie.get('Director', 'N/A')}</div></div>
<div style='display: flex; margin-bottom: 8px;'><div style='width: 85px; flex-shrink: 0;'><strong style='color: rgba(255,255,255,0.5); text-transform: uppercase; font-size: 0.8rem;'>Writer</strong></div><div style='color: #fff; font-size: 0.85rem;'>{movie.get('Writer', 'N/A')}</div></div>
<div style='display: flex; margin-bottom: 8px;'><div style='width: 85px; flex-shrink: 0;'><strong style='color: rgba(255,255,255,0.5); text-transform: uppercase; font-size: 0.8rem;'>Cast</strong></div><div style='color: #fff; font-size: 0.85rem;'>{movie.get('Actors', 'N/A')}</div></div>
<div style='display: flex;'><div style='width: 85px; flex-shrink: 0;'><strong style='color: rgba(255,255,255,0.5); text-transform: uppercase; font-size: 0.8rem;'>Country</strong></div><div style='color: #fff; font-size: 0.85rem;'>{movie.get('Country', 'N/A')}</div></div>
</div>
</div>
                """, unsafe_allow_html=True)
                
            with col2:
                if not movie_state.get('chat_active', False):
                    st.markdown("<div class='gallery-fade' style='padding-top: 30px;'>", unsafe_allow_html=True)
                    tid = fetch_youtube_trailer(f"{title} {movie.get('Year')}")
                    if tid: st.video(f"https://www.youtube.com/watch?v={tid}")
                    st.markdown(f"""
<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;'>
<div style='background: rgba(255,255,255,0.03); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);'><p style='color: rgba(255,255,255,0.5); font-size: 0.8rem; text-transform: uppercase;'>Box Office</p><p style='font-weight: bold; font-size: 1.4rem;'>{movie.get('BoxOffice', 'N/A')}</p></div>
<div style='background: rgba(255,255,255,0.03); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);'><p style='color: rgba(255,255,255,0.5); font-size: 0.8rem; text-transform: uppercase;'>Metascore</p><p style='color: #66cc33; font-weight: bold; font-size: 1.4rem;'>{movie.get('Metascore', 'N/A')}</p></div>
</div>
<div style='background: rgba(255,255,255,0.03); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 30px;'>
<p style='color: rgba(255,255,255,0.5); font-size: 0.8rem; text-transform: uppercase;'>Accolades</p>
<p style='font-weight: bold; font-size: 1.3rem;'>{major_awards}</p><p style='font-size: 0.95rem; color: rgba(255,255,255,0.6);'>{nom_count}</p>
</div>
                    """, unsafe_allow_html=True)
                    if st.button("Initialize Deep Dive", key="enter_chat"):
                        movie_state['chat_active'] = True
                        st.rerun()
                else:
                    st.markdown("<div class='terminal-fade' style='padding-top: 10px; display: flex; justify-content: space-between; align-items: center;'><h3>Subtext Analysis Terminal</h3></div>", unsafe_allow_html=True)
                    if st.button("Close Terminal"):
                        movie_state['chat_active'] = False
                        st.rerun()
                    st.write("---")
                    
                    if not movie_state['messages']:
                        st.markdown("<div class='prompt-pill'>", unsafe_allow_html=True)
                        pc1, pc2, pc3 = st.columns(3)
                        p1 = "What thematic subtext is hidden in the opening act?"
                        p2 = f"How does {director} use lighting to build tension?"
                        p3 = "Analyze the psychological arc of the main character."
                        if pc1.button(p1): movie_state['messages'].append({"role": "user", "content": p1}); st.rerun()
                        if pc2.button(p2): movie_state['messages'].append({"role": "user", "content": p2}); st.rerun()
                        if pc3.button(p3): movie_state['messages'].append({"role": "user", "content": p3}); st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)

                    chat_container = st.container(height=500, border=False)
                    with chat_container:
                        for msg in movie_state['messages']:
                            with st.chat_message(msg["role"]): st.markdown(msg["content"])
                        if movie_state['messages'] and movie_state['messages'][-1]["role"] == "user":
                            with st.chat_message("assistant"):
                                response = client.chats.create(model="gemini-3-flash-preview").send_message(movie_state['messages'][-1]["content"])
                                st.markdown(response.text); movie_state['messages'].append({"role": "assistant", "content": response.text})
                    if p := st.chat_input("Transmit inquiry..."): movie_state['messages'].append({"role": "user", "content": p}); st.rerun()
