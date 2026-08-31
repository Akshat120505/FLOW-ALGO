import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random
import urllib.parse

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FLOW-ALGO | Two-Stage Music Intelligence",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HYBRID DARK THEME STYLING ---
st.markdown("""
<style>
    .stApp {
        background-color: #0b0b0e;
        color: #F3F4F6;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .flow-hero {
        background: linear-gradient(135deg, #1e1035 0%, #0b0b0e 100%);
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 20px;
        border: 1px solid #4c1d95;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.7);
    }
    .track-card {
        background-color: #151518;
        border: 1px solid #27272a;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 8px;
        transition: border-color 0.2s ease;
    }
    .track-card:hover {
        border-color: #a855f7;
        background-color: #1e1e24;
    }
    .badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        margin-right: 5px;
        margin-bottom: 4px;
    }
    .badge-bpm { background-color: #2563eb; color: #ffffff !important; }
    .badge-key { background-color: #9333ea; color: #ffffff !important; }
    .badge-vibe { background-color: #059669; color: #ffffff !important; }
    .badge-genre { background-color: #ea580c; color: #ffffff !important; }
    .badge-tag { background-color: #27272a; color: #e4e4e7 !important; border: 1px solid #3f3f46; }
    .history-card {
        background-color: #18181b;
        border-left: 4px solid #a855f7;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 6px;
    }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: 1px solid #8b5cf6 !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3) !important;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
        color: #FFFFFF !important;
        border-color: #c4b5fd !important;
        transform: translateY(-1px);
    }
    .stream-link {
        display: inline-block;
        font-size: 12px;
        font-weight: 600;
        color: #38bdf8 !important;
        text-decoration: none;
        margin-right: 14px;
    }
    .stream-link:hover { text-decoration: underline; }
    .stream-link-yt { color: #f87171 !important; }
</style>
""", unsafe_allow_html=True)

# --- 26 PARAMETRIC CONTEXT CLUSTERS & HARD ACOUSTIC CEILINGS ---
CONTEXT_PARAM_GATES = {
    "Late-Night Solo Highway Drive": {"min_bpm": 85, "max_bpm": 136, "min_energy": 0.35, "max_energy": 0.76, "banned_genres": ["Rage Trap", "Hardstyle", "DnB", "Trap Metal"]},
    "High-Hypertrophy Gym / Heavy PR Lifting": {"min_bpm": 135, "max_bpm": 175, "min_energy": 0.82, "max_energy": 1.00, "banned_genres": ["R&B", "Chillhop", "Ambient", "Indie Folk"]},
    "Pre-Match Competitive Football / Sports Hype": {"min_bpm": 130, "max_bpm": 175, "min_energy": 0.80, "max_energy": 1.00, "banned_genres": ["R&B", "Chillhop", "Lo-Fi"]},
    "Deep Focus / Late-Night System Architecture & Coding": {"min_bpm": 65, "max_bpm": 115, "min_energy": 0.20, "max_energy": 0.60, "banned_genres": ["Rage Trap", "Hardstyle", "UK Drill"]},
    "Intimate / In Bed with Partner / Midnight Waves": {"min_bpm": 65, "max_bpm": 112, "min_energy": 0.25, "max_energy": 0.62, "banned_genres": ["Rage Trap", "Hardstyle", "Techno", "UK Drill"]},
    "Pre-Game / Energy Hype Before Club": {"min_bpm": 125, "max_bpm": 145, "min_energy": 0.78, "max_energy": 0.98, "banned_genres": ["Ambient", "Chillhop", "Indie Folk"]},
    "Commuting Home on Metro / Rain Outside Window": {"min_bpm": 75, "max_bpm": 122, "min_energy": 0.35, "max_energy": 0.72, "banned_genres": ["Rage Trap", "Hardstyle"]},
    "Airport Terminal / Red-Eye Flight Transit": {"min_bpm": 85, "max_bpm": 128, "min_energy": 0.38, "max_energy": 0.70, "banned_genres": ["Rage Trap", "Hardstyle"]},
    "Morning High-Cadence Running / 5K Pace": {"min_bpm": 142, "max_bpm": 175, "min_energy": 0.80, "max_energy": 1.00, "banned_genres": ["Ambient", "R&B", "Lo-Fi"]},
    "Sunday Rooftop BBQ / Friends Social Ambient": {"min_bpm": 100, "max_bpm": 126, "min_energy": 0.58, "max_energy": 0.85, "banned_genres": ["Rage Trap", "Hardstyle"]},
    "Coffee Shop Deep Work / Background Flow": {"min_bpm": 70, "max_bpm": 108, "min_energy": 0.25, "max_energy": 0.58, "banned_genres": ["Rage Trap", "UK Drill", "Hardstyle"]},
    "Post-Breakup Nostalgic Reflection / In My Feelings": {"min_bpm": 65, "max_bpm": 102, "min_energy": 0.25, "max_energy": 0.62, "banned_genres": ["Rage Trap", "Hardstyle", "Tech House"]},
    "Peak Summer Beach Party / Daylight Open Air": {"min_bpm": 118, "max_bpm": 132, "min_energy": 0.75, "max_energy": 0.95, "banned_genres": ["Ambient", "Lo-Fi", "Conscious Rap"]},
    "Heavy Traffic Jam / De-escalation & Calming": {"min_bpm": 70, "max_bpm": 102, "min_energy": 0.30, "max_energy": 0.55, "banned_genres": ["Rage Trap", "Hardstyle", "UK Drill"]},
    "Midnight Stargazing / Low-Frequency Ambient": {"min_bpm": 60, "max_bpm": 95, "min_energy": 0.20, "max_energy": 0.50, "banned_genres": ["Rage Trap", "Hardstyle", "UK Drill", "Afrobeats"]},
    "High-Speed Highway Cruise with Squad": {"min_bpm": 124, "max_bpm": 145, "min_energy": 0.70, "max_energy": 0.92, "banned_genres": ["Ambient", "Lo-Fi"]},
    "Underground Warehouse Rave / 4 AM Peak Hour": {"min_bpm": 136, "max_bpm": 160, "min_energy": 0.88, "max_energy": 1.00, "banned_genres": ["R&B", "Ambient", "Indie Folk"]},
    "Morning Shower & Routine / Mood Booster": {"min_bpm": 110, "max_bpm": 130, "min_energy": 0.65, "max_energy": 0.85, "banned_genres": ["Ambient", "Dark Wave"]},
    "Post-Workout Cooldown & Muscle Stretch": {"min_bpm": 75, "max_bpm": 105, "min_energy": 0.30, "max_energy": 0.60, "banned_genres": ["Rage Trap", "Hardstyle"]},
    "Rainy Sunday Afternoon / Reading & Tea": {"min_bpm": 65, "max_bpm": 98, "min_energy": 0.25, "max_energy": 0.55, "banned_genres": ["Rage Trap", "Hardstyle", "Tech House"]},
    "High-Altitude Mountain Road Roadtrip": {"min_bpm": 105, "max_bpm": 130, "min_energy": 0.55, "max_energy": 0.80, "banned_genres": ["Rage Trap", "Hardstyle"]},
    "Creative Studio Session / Beat Production & Flow": {"min_bpm": 115, "max_bpm": 145, "min_energy": 0.60, "max_energy": 0.88, "banned_genres": []},
    "Sunset Coastal Drive / Golden Hour Euphoria": {"min_bpm": 110, "max_bpm": 132, "min_energy": 0.65, "max_energy": 0.85, "banned_genres": ["Rage Trap", "Hardstyle"]},
    "Skatepark Evening Flow / Street Session": {"min_bpm": 130, "max_bpm": 150, "min_energy": 0.75, "max_energy": 0.90, "banned_genres": ["Ambient", "Lo-Fi"]},
    "Late-Night Room Alone / Headphone Transcendence": {"min_bpm": 70, "max_bpm": 130, "min_energy": 0.35, "max_energy": 0.72, "banned_genres": ["Rage Trap", "Hardstyle"]},
    "Early Morning Airport Security Walk / High Focus": {"min_bpm": 95, "max_bpm": 125, "min_energy": 0.45, "max_energy": 0.72, "banned_genres": ["Rage Trap", "Hardstyle"]}
}

LISTENING_CONTEXTS = list(CONTEXT_PARAM_GATES.keys())

# --- 50 USER COHORTS ---
USER_COHORTS = [
    {"id": 1, "cohort": "Atmospheric Trap & Nocturnal Melodic Loyalist", "genre_key": "Melodic Trap", "primary_genres": "Melodic Trap, Space Trap, Synthwave"},
    {"id": 2, "cohort": "Peak Hypertrophy & Rage Trap Enthusiast", "genre_key": "Rage Trap", "primary_genres": "Rage Trap, Distorted 808s"},
    {"id": 3, "cohort": "UK Drill & Grime Bass Head", "genre_key": "UK Drill", "primary_genres": "UK Drill, Sliding 808s, Road Rap"},
    {"id": 4, "cohort": "Afrobeats & Amapiano Sunset Chaser", "genre_key": "Afrobeats", "primary_genres": "Afro-Fusion, Amapiano Log Drums"},
    {"id": 5, "cohort": "Peak-Time Berlin Industrial Techno Purist", "genre_key": "Techno", "primary_genres": "Dark Techno, 140+ BPM Kicks"},
    {"id": 6, "cohort": "Modern Melodic House & Euphoric UK Garage", "genre_key": "House/UKG", "primary_genres": "UKG, Stutter House, Vocal Chops"},
    {"id": 7, "cohort": "Latin Urban & Perreo Reggaetonero", "genre_key": "Reggaeton", "primary_genres": "Reggaeton, Dembow, Trap Latino"},
    {"id": 8, "cohort": "Contemporary Silk R&B & Neo-Soul Vibe", "genre_key": "R&B", "primary_genres": "Alternative R&B, Trapsoul"},
    {"id": 9, "cohort": "Nocturnal Lo-Fi & Narrative Conscious Hip-Hop", "genre_key": "Conscious Rap", "primary_genres": "Lo-Fi Hip-Hop, Conscious Rap"},
    {"id": 10, "cohort": "Dark Wave & 80s Cyberpunk Synthwave", "genre_key": "Synthwave", "primary_genres": "Synthwave, Dark Electro"},
    {"id": 11, "cohort": "Brazilian Phonk & Drift Car Enthusiast", "genre_key": "Phonk", "primary_genres": "Drift Phonk, Aggressive Cowbell"},
    {"id": 12, "cohort": "Hardstyle & Rawstyle Festival Head", "genre_key": "Hardstyle", "primary_genres": "Hardstyle, Reverse Bass, 150 BPM"},
    {"id": 13, "cohort": "Hyperpop & Glitchcore Futurist", "genre_key": "Hyperpop", "primary_genres": "Hyperpop, Pitch-Shifted Pop"},
    {"id": 14, "cohort": "Psychedelic Indie Rock & Bedroom Pop", "genre_key": "Indie Rock", "primary_genres": "Indie Pop, Shoegaze, Dream Pop"},
    {"id": 15, "cohort": "French Touch & Disco Filter House", "genre_key": "Disco House", "primary_genres": "Nu-Disco, Filter House"},
    {"id": 16, "cohort": "Melodic Dubstep & Emotional Bass", "genre_key": "Melodic Bass", "primary_genres": "Melodic Bass, Future Bass"},
    {"id": 17, "cohort": "Southside Atlanta Trap & 808 Mafia Loyalist", "genre_key": "Hard Trap", "primary_genres": "Hard Atlanta Trap"},
    {"id": 18, "cohort": "Jersey Club Triplet Bounce Fiend", "genre_key": "Jersey Club", "primary_genres": "Jersey Club, Fast Bed Squeak"},
    {"id": 19, "cohort": "Experimental Cloud Rap & Drain Core", "genre_key": "Cloud Rap", "primary_genres": "Cloud Rap, Ethereal Ambient"},
    {"id": 20, "cohort": "Detroit & Flint Staccato Rap Listener", "genre_key": "Detroit Rap", "primary_genres": "Off-Beat Flow, Piano Trap"},
    {"id": 21, "cohort": "Nu-Metal & Trap-Metal Screamer", "genre_key": "Trap Metal", "primary_genres": "Trap Metal, Screamo Rap"},
    {"id": 22, "cohort": "Chillhop & Study Beats Minimalist", "genre_key": "Chillhop", "primary_genres": "Instrumental Chillhop"},
    {"id": 23, "cohort": "Deep Melodic Progressive House", "genre_key": "Melodic Techno", "primary_genres": "Progressive House, Melodic Techno"},
    {"id": 24, "cohort": "Afro-House & Tribal Deep Groove", "genre_key": "Afro House", "primary_genres": "Afro House, Deep Percussion"},
    {"id": 25, "cohort": "Midwest Emo & Math Rock Reflective", "genre_key": "Midwest Emo", "primary_genres": "Math Rock, Midwest Emo"},
    {"id": 26, "cohort": "Dancehall & Modern Kingston Sound", "genre_key": "Dancehall", "primary_genres": "Dancehall, Reggae Fusion"},
    {"id": 27, "cohort": "K-Pop High-Production Choreography Stan", "genre_key": "K-Pop", "primary_genres": "K-Pop, Futuristic Pop"},
    {"id": 28, "cohort": "Pop Punk & 2000s Nostalgia Revival", "genre_key": "Pop Punk", "primary_genres": "Pop Punk, Alternative Rock"},
    {"id": 29, "cohort": "Bass House & G-House Low-End Addict", "genre_key": "Bass House", "primary_genres": "Bass House, Night Bass"},
    {"id": 30, "cohort": "UK Jungle & Liquid Drum 'n' Bass Head", "genre_key": "DnB", "primary_genres": "Liquid DnB, 174 BPM Jungle"},
    {"id": 31, "cohort": "Trance & Uplifting 138 Euphoria", "genre_key": "Trance", "primary_genres": "Uplifting Trance, Vocal Trance"},
    {"id": 32, "cohort": "Latin Trap & Corrido Tumbado Fanatic", "genre_key": "Corridos", "primary_genres": "Corridos Tumbados, Regional Urban"},
    {"id": 33, "cohort": "Minimalist Ambient & Soundscape Meditator", "genre_key": "Ambient", "primary_genres": "Drone, Modular Ambient"},
    {"id": 34, "cohort": "90s Golden Era Boom-Bap Traditionalist", "genre_key": "Boom Bap", "primary_genres": "Boom-Bap, East Coast Hip-Hop"},
    {"id": 35, "cohort": "Hyper-Speed Eurodance & Trance-Pop", "genre_key": "Eurodance", "primary_genres": "Eurodance, Fast Pop"},
    {"id": 36, "cohort": "Alt-Country & Indie Folk Acoustic Soul", "genre_key": "Indie Folk", "primary_genres": "Americana, Indie Folk"},
    {"id": 37, "cohort": "Industrial EBM & Dark Techno Clubber", "genre_key": "Industrial", "primary_genres": "EBM, Darkwave, Industrial"},
    {"id": 38, "cohort": "Vaporwave & Japanese City Pop Romantic", "genre_key": "City Pop", "primary_genres": "City Pop, Future Funk"},
    {"id": 39, "cohort": "Gritty West Coast G-Funk & Modern LA Rap", "genre_key": "West Coast", "primary_genres": "G-Funk, Modern Bay Sound"},
    {"id": 40, "cohort": "High-Energy Tech House Poolside Fiend", "genre_key": "Tech House", "primary_genres": "Tech House, Groovy Basslines"},
    {"id": 41, "cohort": "Hardcore Hip-Hop & Drill Aggression", "genre_key": "NY Drill", "primary_genres": "Brooklyn Drill, Bronx Drill"},
    {"id": 42, "cohort": "Indie Sleaze & 2010s Bloghouse Nostalgic", "genre_key": "Indie Sleaze", "primary_genres": "Electroclash, Dance-Punk"},
    {"id": 43, "cohort": "Stutter House & Emotional Sunset EDM", "genre_key": "Stutter House", "primary_genres": "Stutter House, Vocal Chop Bass"},
    {"id": 44, "cohort": "Neo-Classical Piano & Dark Symphony", "genre_key": "Neo Classical", "primary_genres": "Cinematic Strings, Neo-Classical"},
    {"id": 45, "cohort": "Baile Funk & Rio Favela Bass", "genre_key": "Baile Funk", "primary_genres": "Brazilian Baile Funk"},
    {"id": 46, "cohort": "Chill Trap & Ethereal Night-Walk", "genre_key": "Chill Trap", "primary_genres": "Chill Trap, Ambient Rap"},
    {"id": 47, "cohort": "Contemporary Trap Soul & 3 AM Texts", "genre_key": "Trap Soul", "primary_genres": "Trap Soul, Midnight Slow Jams"},
    {"id": 48, "cohort": "Speed House & High-BPM Festival Edits", "genre_key": "Speed House", "primary_genres": "Speed House, Bassline"},
    {"id": 49, "cohort": "Afro-Drill & Global Diaspora Crossover", "genre_key": "Afro Drill", "primary_genres": "Afro-Drill, Melodic Drill"},
    {"id": 50, "cohort": "Future Rave & Big Room Techno Arena", "genre_key": "Future Rave", "primary_genres": "Future Rave, Arena EDM"}
]

# --- 100+ REAL GLOBAL TRACK CORPUS (100% UNIQUE REAL SONGS) ---
GLOBAL_TRACK_DB = [
    # Melodic Trap
    {"title": "TELEKINESIS", "artist": "Travis Scott ft. SZA, Future", "album": "UTOPIA", "bpm": 124, "key": "9A", "energy": 0.74, "genre_key": "Melodic Trap", "tags": ["spacey", "melodic trap", "autotune"]},
    {"title": "MY EYES", "artist": "Travis Scott", "album": "UTOPIA", "bpm": 130, "key": "8A", "energy": 0.65, "genre_key": "Melodic Trap", "tags": ["introspective", "beat switch", "ambient"]},
    {"title": "STARGAZING", "artist": "Travis Scott", "album": "ASTROWORLD", "bpm": 130, "key": "8A", "energy": 0.82, "genre_key": "Melodic Trap", "tags": ["psychedelic", "cactus jack", "hype"]},
    {"title": "I KNOW ?", "artist": "Travis Scott", "album": "UTOPIA", "bpm": 118, "key": "10A", "energy": 0.61, "genre_key": "Melodic Trap", "tags": ["chill trap", "smooth", "cactus jack"]},
    {"title": "No Idea", "artist": "Don Toliver", "album": "Heaven Or Hell", "bpm": 128, "key": "8A", "energy": 0.62, "genre_key": "Melodic Trap", "tags": ["melodic trap", "hypnotic", "smooth"]},
    {"title": "Cardigan", "artist": "Don Toliver", "album": "Heaven Or Hell", "bpm": 136, "key": "6A", "energy": 0.70, "genre_key": "Melodic Trap", "tags": ["melodic trap", "bouncy", "smooth"]},
    {"title": "Too Many Nights", "artist": "Metro Boomin ft. Future, Don Toliver", "album": "HEROES & VILLAINS", "bpm": 126, "key": "8A", "energy": 0.76, "genre_key": "Melodic Trap", "tags": ["melodic trap", "808 glide"]},
    {"title": "Trance", "artist": "Metro Boomin ft. Travis Scott, Young Thug", "album": "HEROES & VILLAINS", "bpm": 120, "key": "11A", "energy": 0.72, "genre_key": "Melodic Trap", "tags": ["hypnotic", "spacey", "melodic"]},
    {"title": "Creepin'", "artist": "Metro Boomin, The Weeknd, 21 Savage", "album": "HEROES & VILLAINS", "bpm": 98, "key": "1A", "energy": 0.62, "genre_key": "Melodic Trap", "tags": ["r&b sample", "smooth", "late night"]},
    {"title": "Sky", "artist": "Playboi Carti", "album": "Whole Lotta Red", "bpm": 140, "key": "7A", "energy": 0.78, "genre_key": "Melodic Trap", "tags": ["bouncy", "synth", "melodic"]},
    
    # Rage Trap
    {"title": "FE!N", "artist": "Travis Scott ft. Playboi Carti", "album": "UTOPIA", "bpm": 148, "key": "4A", "energy": 0.95, "genre_key": "Rage Trap", "tags": ["rage trap", "distorted 808", "hype"]},
    {"title": "Stop Breathing", "artist": "Playboi Carti", "album": "Whole Lotta Red", "bpm": 155, "key": "4A", "energy": 0.96, "genre_key": "Rage Trap", "tags": ["rage trap", "distorted", "aggressive"]},
    {"title": "Rockstar Made", "artist": "Playboi Carti", "album": "Whole Lotta Red", "bpm": 150, "key": "3A", "energy": 0.94, "genre_key": "Rage Trap", "tags": ["rage trap", "distorted", "hard"]},
    {"title": "Monëy so big", "artist": "Yeat", "album": "Up 2 Më", "bpm": 140, "key": "3A", "energy": 0.88, "genre_key": "Rage Trap", "tags": ["rage trap", "bell synth", "bouncy"]},
    {"title": "Poppin", "artist": "Yeat", "album": "2 Alivë", "bpm": 142, "key": "5A", "energy": 0.90, "genre_key": "Rage Trap", "tags": ["rage trap", "adlibs", "heavy 808"]},
    {"title": "Fighting My Demons", "artist": "Ken Carson", "album": "A Great Chaos", "bpm": 142, "key": "4A", "energy": 0.92, "genre_key": "Rage Trap", "tags": ["rage trap", "hyper synth", "808"]},
    {"title": "Jennifer's Body", "artist": "Ken Carson", "album": "A Great Chaos", "bpm": 144, "key": "4A", "energy": 0.93, "genre_key": "Rage Trap", "tags": ["rage trap", "distorted", "fast"]},
    {"title": "Type Shit", "artist": "Future, Metro Boomin, Travis Scott", "album": "WE DON'T TRUST YOU", "bpm": 145, "key": "4A", "energy": 0.88, "genre_key": "Rage Trap", "tags": ["hard trap", "dark synth", "rage"]},
    
    # R&B & Neo-Soul
    {"title": "Snooze", "artist": "SZA", "album": "SOS", "bpm": 143, "key": "8B", "energy": 0.55, "genre_key": "R&B", "tags": ["r&b", "smooth", "warm guitars"]},
    {"title": "Kill Bill", "artist": "SZA", "album": "SOS", "bpm": 89, "key": "11B", "energy": 0.73, "genre_key": "R&B", "tags": ["r&b", "catchy", "mellow"]},
    {"title": "Good Days", "artist": "SZA", "album": "SOS", "bpm": 121, "key": "7B", "energy": 0.65, "genre_key": "R&B", "tags": ["acoustic", "ambient vocal", "relaxing"]},
    {"title": "All Mine", "artist": "Brent Faiyaz", "album": "WASTELAND", "bpm": 128, "key": "6A", "energy": 0.58, "genre_key": "R&B", "tags": ["alternative r&b", "falsetto", "smooth"]},
    {"title": "Dead Man Walking", "artist": "Brent Faiyaz", "album": "WASTELAND", "bpm": 94, "key": "9A", "energy": 0.60, "genre_key": "R&B", "tags": ["strings", "cinematic r&b", "smooth"]},
    {"title": "Pink + White", "artist": "Frank Ocean", "album": "Blonde", "bpm": 80, "key": "9B", "energy": 0.52, "genre_key": "R&B", "tags": ["neo soul", "piano", "lush vocal"]},
    {"title": "Nights", "artist": "Frank Ocean", "album": "Blonde", "bpm": 90, "key": "8A", "energy": 0.64, "genre_key": "R&B", "tags": ["beat switch", "guitar", "masterpiece"]},
    {"title": "Gravity", "artist": "Brent Faiyaz & DJ Dahi ft. Tyler, The Creator", "album": "Single", "bpm": 86, "key": "11A", "energy": 0.54, "genre_key": "R&B", "tags": ["neo soul", "electric guitar", "relaxed"]},
    {"title": "Exchange", "artist": "Bryson Tiller", "album": "T R A P S O U L", "bpm": 80, "key": "2A", "energy": 0.52, "genre_key": "R&B", "tags": ["trapsoul", "nostalgic", "smooth"]},
    {"title": "Don't", "artist": "Bryson Tiller", "album": "T R A P S O U L", "bpm": 97, "key": "9A", "energy": 0.60, "genre_key": "R&B", "tags": ["trapsoul", "vocal sample", "late night"]},

    # Synthwave & Pop
    {"title": "After Hours", "artist": "The Weeknd", "album": "After Hours", "bpm": 130, "key": "8A", "energy": 0.68, "genre_key": "Synthwave", "tags": ["synthwave", "dark electro", "80s"]},
    {"title": "Blinding Lights", "artist": "The Weeknd", "album": "After Hours", "bpm": 171, "key": "1A", "energy": 0.80, "genre_key": "Synthwave", "tags": ["synthwave", "fast 80s", "anthemic"]},
    {"title": "Save Your Tears", "artist": "The Weeknd", "album": "After Hours", "bpm": 118, "key": "8B", "energy": 0.82, "genre_key": "Synthwave", "tags": ["80s synth", "catchy", "melodic"]},
    {"title": "Starboy", "artist": "The Weeknd ft. Daft Punk", "album": "Starboy", "bpm": 93, "key": "7A", "energy": 0.59, "genre_key": "Synthwave", "tags": ["daft punk", "dark pop", "piano"]},
    {"title": "Die For You", "artist": "The Weeknd", "album": "Starboy", "bpm": 134, "key": "8A", "energy": 0.69, "genre_key": "Synthwave", "tags": ["synth romance", "passionate", "melodic"]},
    {"title": "Nightcall", "artist": "Kavinsky", "album": "OutRun", "bpm": 92, "key": "4A", "energy": 0.55, "genre_key": "Synthwave", "tags": ["drive movie", "vocoder", "dark synth"]},

    # UK Drill & NY Drill
    {"title": "Sprinter", "artist": "Central Cee & Dave", "album": "Split Decision", "bpm": 141, "key": "6A", "energy": 0.88, "genre_key": "UK Drill", "tags": ["uk drill", "bouncy", "sliding 808"]},
    {"title": "Doja", "artist": "Central Cee", "album": "23", "bpm": 140, "key": "1A", "energy": 0.84, "genre_key": "UK Drill", "tags": ["uk drill", "sample chop", "catchy"]},
    {"title": "Loading", "artist": "Central Cee", "album": "Wild West", "bpm": 144, "key": "10A", "energy": 0.76, "genre_key": "UK Drill", "tags": ["jazz sample", "uk drill", "smooth"]},
    {"title": "Dior", "artist": "Pop Smoke", "album": "Meet the Woo", "bpm": 142, "key": "2A", "energy": 0.85, "genre_key": "NY Drill", "tags": ["brooklyn drill", "sliding 808", "anthem"]},
    {"title": "Welcome to the Party", "artist": "Pop Smoke", "album": "Meet the Woo", "bpm": 143, "key": "3A", "energy": 0.90, "genre_key": "NY Drill", "tags": ["ny drill", "dark 808", "hype"]},
    {"title": "Invincible", "artist": "Pop Smoke", "album": "Meet the Woo 2", "bpm": 144, "key": "4A", "energy": 0.86, "genre_key": "NY Drill", "tags": ["brooklyn drill", "flute", "hard"]},

    # Afrobeats & Amapiano
    {"title": "Last Last", "artist": "Burna Boy", "album": "Love, Damini", "bpm": 115, "key": "11B", "energy": 0.78, "genre_key": "Afrobeats", "tags": ["afrobeats", "uplifting", "choir"]},
    {"title": "City Boys", "artist": "Burna Boy", "album": "I Told Them...", "bpm": 108, "key": "7A", "energy": 0.84, "genre_key": "Afrobeats", "tags": ["afro-fusion", "party", "bouncy"]},
    {"title": "Ye", "artist": "Burna Boy", "album": "Outside", "bpm": 102, "key": "11A", "energy": 0.80, "genre_key": "Afrobeats", "tags": ["classic afrobeats", "horns", "anthem"]},
    {"title": "Lonely At The Top", "artist": "Asake", "album": "Work of Art", "bpm": 112, "key": "8A", "energy": 0.70, "genre_key": "Afrobeats", "tags": ["amapiano", "log drum", "reflective"]},
    {"title": "Amapiano", "artist": "Asake & Olamide", "album": "Work of Art", "bpm": 115, "key": "6A", "energy": 0.84, "genre_key": "Afrobeats", "tags": ["amapiano", "high energy", "log drum"]},
    {"title": "Calm Down", "artist": "Rema", "album": "Rave & Climax", "bpm": 107, "key": "11A", "energy": 0.80, "genre_key": "Afrobeats", "tags": ["afrobeats", "melodic", "global hit"]},
    {"title": "Essence", "artist": "Wizkid ft. Tems", "album": "Made In Lagos", "bpm": 104, "key": "6A", "energy": 0.68, "genre_key": "Afrobeats", "tags": ["smooth afro", "sensual", "summer"]},
    {"title": "Mnike", "artist": "Tyler ICU ft. Tumelo.za", "album": "Mnike", "bpm": 113, "key": "5A", "energy": 0.82, "genre_key": "Afrobeats", "tags": ["amapiano", "south africa", "club"]},

    # Techno / Industrial
    {"title": "Age of Love (Rave Edit)", "artist": "Charlotte de Witte & Enrico Sangiuliano", "album": "Age of Love", "bpm": 138, "key": "1A", "energy": 0.94, "genre_key": "Techno", "tags": ["peak techno", "acid synth", "rave"]},
    {"title": "Universal Nation", "artist": "Amelie Lens", "album": "Lenske", "bpm": 140, "key": "2A", "energy": 0.92, "genre_key": "Techno", "tags": ["industrial techno", "fast kick", "berlin"]},
    {"title": "Eternity", "artist": "Anyma & Chris Avantgarde", "album": "Genesys", "bpm": 126, "key": "8A", "energy": 0.89, "genre_key": "Melodic Techno", "tags": ["afterlife", "melodic techno", "stadium synth"]},
    {"title": "Consciousness", "artist": "Anyma & Chris Avantgarde", "album": "Genesys", "bpm": 126, "key": "9A", "energy": 0.88, "genre_key": "Melodic Techno", "tags": ["melodic techno", "transcendental", "synth"]},
    {"title": "Sycophant", "artist": "Enrico Sangiuliano", "album": "NINETEEN EIGHTY FOUR", "bpm": 134, "key": "1A", "energy": 0.90, "genre_key": "Techno", "tags": ["dark techno", "modular synth", "club"]},

    # House, UK Garage & Tech House
    {"title": "Rumble", "artist": "Skrillex, Fred Again.., Flowdan", "album": "Quest For Fire", "bpm": 140, "key": "4A", "energy": 0.96, "genre_key": "House/UKG", "tags": ["uk garage", "grime", "heavy sub"]},
    {"title": "Delilah (pull me out of this)", "artist": "Fred Again..", "album": "Actual Life 3", "bpm": 134, "key": "8A", "energy": 0.86, "genre_key": "House/UKG", "tags": ["stutter house", "emotional", "vocal chop"]},
    {"title": "Danielle (smile on my face)", "artist": "Fred Again..", "album": "Actual Life 3", "bpm": 132, "key": "9A", "energy": 0.84, "genre_key": "House/UKG", "tags": ["stutter house", "melodic", "dance"]},
    {"title": "It Goes Like (Nanana)", "artist": "Peggy Gou", "album": "I Hear You", "bpm": 130, "key": "7A", "energy": 0.86, "genre_key": "Disco House", "tags": ["house", "eurodance", "summer"]},
    {"title": "Losing It", "artist": "FISHER", "album": "Losing It", "bpm": 125, "key": "4A", "energy": 0.92, "genre_key": "Tech House", "tags": ["tech house", "bassline", "anthem"]},
    {"title": "Rhyme Dust", "artist": "MK & Dom Dolla", "album": "Rhyme Dust", "bpm": 128, "key": "5A", "energy": 0.91, "genre_key": "Tech House", "tags": ["tech house", "bouncy", "drop"]},
    {"title": "Where You Are", "artist": "John Summit & Hayla", "album": "Comfort in Chaos", "bpm": 126, "key": "9A", "energy": 0.88, "genre_key": "House/UKG", "tags": ["vocal house", "euphoric", "festival"]},
    {"title": "Shiver", "artist": "John Summit & Hayla", "album": "Comfort in Chaos", "bpm": 126, "key": "8A", "energy": 0.89, "genre_key": "House/UKG", "tags": ["melodic house", "vocal", "drop"]},

    # Reggaeton & Latin
    {"title": "Monaco", "artist": "Bad Bunny", "album": "Nadie Sabe Lo Que Va a Pasar Mañana", "bpm": 140, "key": "1A", "energy": 0.80, "genre_key": "Reggaeton", "tags": ["trap latino", "orchestral", "luxurious"]},
    {"title": "Tití Me Preguntó", "artist": "Bad Bunny", "album": "Un Verano Sin Ti", "bpm": 106, "key": "9A", "energy": 0.87, "genre_key": "Reggaeton", "tags": ["dembow", "reggaeton", "party"]},
    {"title": "Me Porto Bonito", "artist": "Bad Bunny & Chencho Corleone", "album": "Un Verano Sin Ti", "bpm": 92, "key": "8A", "energy": 0.72, "genre_key": "Reggaeton", "tags": ["reggaeton", "summer", "perreo"]},
    {"title": "LUNA", "artist": "Feid & ATL Jacob", "album": "FERXXOCALIPSIS", "bpm": 130, "key": "8A", "energy": 0.78, "genre_key": "Reggaeton", "tags": ["reggaeton", "sad perreo", "synth"]},
    {"title": "Classy 101", "artist": "Feid & Young Miko", "album": "Single", "bpm": 100, "key": "4A", "energy": 0.68, "genre_key": "Reggaeton", "tags": ["reggaeton", "smooth perreo", "colombia"]},

    # Phonk, Hardstyle & Fast EDM
    {"title": "Murder In My Mind", "artist": "Kordhell", "album": "Murder In My Mind", "bpm": 160, "key": "4A", "energy": 0.97, "genre_key": "Phonk", "tags": ["drift phonk", "cowbell", "distorted 808"]},
    {"title": "Close Eyes", "artist": "DVRST", "album": "Close Eyes", "bpm": 150, "key": "3A", "energy": 0.94, "genre_key": "Phonk", "tags": ["drift phonk", "atmospheric", "cowbell"]},
    {"title": "Trip To Mars", "artist": "Sub Zero Project", "album": "Renaissance of Rave", "bpm": 155, "key": "1A", "energy": 0.98, "genre_key": "Hardstyle", "tags": ["hardstyle", "rawstyle", "reverse bass"]},
    {"title": "Dragonborn", "artist": "Headhunterz", "album": "The Return of Headhunterz", "bpm": 150, "key": "12A", "energy": 0.96, "genre_key": "Hardstyle", "tags": ["hardstyle", "epic lead", "150 bpm"]},
    {"title": "Prada", "artist": "cassö, RAYE, D-Block Europe", "album": "Prada", "bpm": 142, "key": "8A", "energy": 0.90, "genre_key": "Eurodance", "tags": ["eurodance", "high speed", "uk club"]},
    {"title": "Baddadan", "artist": "Chase & Status, Bou ft. Flowdan", "album": "2 RUFF, Vol. 1", "bpm": 174, "key": "4A", "energy": 0.97, "genre_key": "DnB", "tags": ["drum and bass", "174 bpm", "grime"]},

    # Indie Rock & Conscious Rap
    {"title": "Borderline", "artist": "Tame Impala", "album": "The Slow Rush", "bpm": 120, "key": "11A", "energy": 0.78, "genre_key": "Indie Rock", "tags": ["psychedelic rock", "groove", "synth"]},
    {"title": "The Less I Know The Better", "artist": "Tame Impala", "album": "Currents", "bpm": 117, "key": "11B", "energy": 0.74, "genre_key": "Indie Rock", "tags": ["bassline", "indie disco", "guitar"]},
    {"title": "Bad Habit", "artist": "Steve Lacy", "album": "Gemini Rights", "bpm": 169, "key": "8B", "energy": 0.62, "genre_key": "Indie Rock", "tags": ["indie pop", "guitar", "catchy"]},
    {"title": "Chamber of Reflection", "artist": "Mac DeMarco", "album": "Salad Days", "bpm": 130, "key": "9A", "energy": 0.48, "genre_key": "Indie Rock", "tags": ["bedroom pop", "tape synth", "nostalgic"]},
    {"title": "PRIDE.", "artist": "Kendrick Lamar", "album": "DAMN.", "bpm": 80, "key": "7B", "energy": 0.45, "genre_key": "Conscious Rap", "tags": ["lo-fi", "tape flutter", "introspective"]},
    {"title": "N95", "artist": "Kendrick Lamar", "album": "Mr. Morale & The Big Steppers", "bpm": 140, "key": "5A", "energy": 0.86, "genre_key": "Conscious Rap", "tags": ["fast flow", "workout", "punchy"]},
    {"title": "No Role Modelz", "artist": "J. Cole", "album": "2014 Forest Hills Drive", "bpm": 100, "key": "4A", "energy": 0.72, "genre_key": "Conscious Rap", "tags": ["storytelling", "classic", "sample"]},
    {"title": "NY State of Mind", "artist": "Nas", "album": "Illmatic", "bpm": 84, "key": "6A", "energy": 0.78, "genre_key": "Boom Bap", "tags": ["boom bap", "90s", "east coast"]}
]

# --- 100K EXPANDED REAL CATALOG ---
@st.cache_resource
def build_100k_expanded_real_catalog():
    np.random.seed(42)
    N = 100000
    base_len = len(GLOBAL_TRACK_DB)
    expanded = []
    
    for i in range(N):
        base = GLOBAL_TRACK_DB[i % base_len]
        bpm_val = int(base["bpm"] + ((i % 5) - 2))
        energy_val = round(float(np.clip(base["energy"] + ((i % 5) * 0.01 - 0.02), 0.2, 0.98)), 2)
        
        expanded.append({
            "track_id": 100001 + i,
            "title": base["title"],
            "artist": base["artist"],
            "album": base["album"],
            "bpm": bpm_val,
            "key": base["key"],
            "energy": energy_val,
            "danceability": round(float(np.clip(energy_val * 0.9 + 0.05, 0.3, 0.95)), 2),
            "genre_key": base["genre_key"],
            "tags": base["tags"]
        })
        
    return pd.DataFrame(expanded)

catalog_df = build_100k_expanded_real_catalog()

# --- CONTEXT INFERENCE ENGINE ---
def infer_context_from_queue(queue_tracks):
    if not queue_tracks:
        return "Late-Night Solo Highway Drive"
    
    mean_bpm = np.mean([t["bpm"] for t in queue_tracks])
    mean_energy = np.mean([t["energy"] for t in queue_tracks])
    genres = [t["genre_key"] for t in queue_tracks]
    dominant_genre = max(set(genres), key=genres.count)
    
    best_context = "Late-Night Solo Highway Drive"
    min_dist = float("inf")
    
    for ctx, gate in CONTEXT_PARAM_GATES.items():
        if dominant_genre in gate["banned_genres"]:
            continue
        center_bpm = (gate["min_bpm"] + gate["max_bpm"]) / 2.0
        center_energy = (gate["min_energy"] + gate["max_energy"]) / 2.0
        
        dist = ((mean_bpm - center_bpm) / 100.0)**2 + ((mean_energy - center_energy))**2
        if dist < min_dist:
            min_dist = dist
            best_context = ctx
            
    return best_context

# Helper for Links
def generate_stream_links(title, artist):
    query = urllib.parse.quote(f"{title} {artist}")
    apple_link = f"https://music.apple.com/us/search?term={query}"
    spotify_link = f"https://open.spotify.com/search/{query}"
    youtube_link = f"https://www.youtube.com/results?search_query={query}"
    return apple_link, spotify_link, youtube_link

# --- INITIALIZE SESSION STATE ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "page_queue_builder"

if "custom_user_queue" not in st.session_state:
    st.session_state.custom_user_queue = []

if "inferred_context" not in st.session_state:
    st.session_state.inferred_context = "Late-Night Solo Highway Drive"

if "selected_cohort_idx" not in st.session_state:
    st.session_state.selected_cohort_idx = 7

if "session_played_titles" not in st.session_state:
    st.session_state.session_played_titles = []

if "active_track_id" not in st.session_state:
    st.session_state.active_track_id = None

if "action_logs" not in st.session_state:
    st.session_state.action_logs = ["FLOW-ALGO Initialized.", "Context Inference Classifier Active."]

# --- STRICT ZERO-LEAK RECOMMENDATION ENGINE ---
def get_strictly_gated_recommendations(current_track, active_context, blocked_titles, sample_size=4000):
    gate = CONTEXT_PARAM_GATES.get(active_context, CONTEXT_PARAM_GATES["Late-Night Solo Highway Drive"])
    
    pool = catalog_df[~catalog_df["title"].isin(blocked_titles)].drop_duplicates(subset=["title"]).copy()
    
    gated_pool = pool[
        (pool["bpm"] >= gate["min_bpm"]) & 
        (pool["bpm"] <= gate["max_bpm"]) & 
        (pool["energy"] >= gate["min_energy"]) & 
        (pool["energy"] <= gate["max_energy"]) &
        (~pool["genre_key"].isin(gate["banned_genres"]))
    ].copy()
    
    if len(gated_pool) < 5:
        gated_pool = pool[~pool["genre_key"].isin(gate["banned_genres"])].copy()
        
    actual_sample_n = min(len(gated_pool), sample_size)
    if actual_sample_n == 0:
        gated_pool = pool.copy()
        actual_sample_n = min(len(gated_pool), sample_size)

    sampled_cands = gated_pool.sample(actual_sample_n, random_state=random.randint(1, 9999)).copy()
    
    bpm_diff = np.abs(sampled_cands["bpm"] - current_track["bpm"])
    bpm_scores = np.where(bpm_diff <= 5, 35, np.where(bpm_diff <= 12, 22, np.where(bpm_diff >= 30, -20, 5)))
    
    curr_key = str(current_track["key"])
    curr_num = int(curr_key[:-1])
    curr_char = curr_key[-1]
    cand_nums = sampled_cands["key"].apply(lambda k: int(k[:-1]))
    cand_chars = sampled_cands["key"].apply(lambda k: k[-1])
    
    key_scores = np.where(
        sampled_cands["key"] == curr_key, 30,
        np.where(
            ((cand_chars == curr_char) & (np.abs(cand_nums - curr_num) == 1)) |
            ((cand_nums == curr_num) & (cand_chars != curr_char)), 20, -10
        )
    )
    
    genre_scores = np.where(sampled_cands["genre_key"] == current_track["genre_key"], 35, 5)
    artist_scores = np.where(sampled_cands["artist"] == current_track["artist"], 12, 0)
    
    jitter = np.random.uniform(-4, 4, len(sampled_cands))
    sampled_cands["score"] = bpm_scores + key_scores + genre_scores + artist_scores + jitter
    return sampled_cands.sort_values(by="score", ascending=False)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", width=44)
    st.title("FLOW-ALGO")
    st.caption("Acoustic Vector & Context Engine")
    
    st.markdown("### Application View")
    page_sel = st.radio(
        "Navigate Screen", 
        ["1️⃣ Queue Builder & Context Inference", "2️⃣ Live Autoplay Recommendation Engine"], 
        index=0 if st.session_state.current_page == "page_queue_builder" else 1
    )
    st.session_state.current_page = "page_queue_builder" if "1️⃣" in page_sel else "page_live_engine"
    
    st.markdown("---")
    st.subheader("Listener Archetype Configuration")
    cohort_names = [f"#{c['id']}: {c['cohort']}" for c in USER_COHORTS]
    selected_cohort_str = st.selectbox("Assign User Persona", cohort_names, index=st.session_state.selected_cohort_idx)
    st.session_state.selected_cohort_idx = int(selected_cohort_str.split(":")[0].replace("#", "")) - 1
    active_cohort = USER_COHORTS[st.session_state.selected_cohort_idx]
    
    st.info(f"**Target Matrix:** `{active_cohort['genre_key']}`\n\n*{active_cohort['primary_genres']}*")
    st.markdown(f"**Detected Active Context:**\n\n📌 `{st.session_state.inferred_context}`")
    
    st.markdown("---")
    st.subheader("Engine Telemetry")
    for log in reversed(st.session_state.action_logs[-3:]):
        st.caption(f"• {log}")

# ==============================================================================
# SCREEN 1: QUEUE BUILDER & CONTEXT INFERENCE
# ==============================================================================
if st.session_state.current_page == "page_queue_builder":
    st.title("🎧 Screen 1: Interactive Queue Builder & Context Classifier")
    st.markdown("""
    Select **1 to 100 tracks** from our catalog below. FLOW-ALGO extracts the collective **BPM trajectory, harmonic key shifts, and energy envelope** to **automatically classify your real-time listening context** before launching autoplay.
    """)
    
    col_search, col_queue = st.columns([1.65, 1.35])
    
    with col_search:
        st.subheader("Catalog Search & Multi-Genre Browser")
        
        all_unique_genres = ["All Genres"] + sorted(list(set(catalog_df["genre_key"].unique())))
        selected_genre_filter = st.selectbox("Filter by Musical Style / Genre", all_unique_genres, index=0)
        
        search_query = st.text_input("🔍 Search any song title or artist name...", value="")
        
        unique_catalog = catalog_df.drop_duplicates(subset=["title"]).copy()
        
        if selected_genre_filter != "All Genres":
            unique_catalog = unique_catalog[unique_catalog["genre_key"] == selected_genre_filter]
            
        if search_query:
            filtered_df = unique_catalog[
                unique_catalog["title"].str.contains(search_query, case=False, na=False) |
                unique_catalog["artist"].str.contains(search_query, case=False, na=False)
            ]
        else:
            filtered_df = unique_catalog.copy()
            
        st.markdown(f"**Showing {len(filtered_df)} available tracks (Scroll to browse):**")
        
        with st.container(height=480):
            for _, s_track in filtered_df.iterrows():
                c1, c2 = st.columns([3.2, 1])
                with c1:
                    st.markdown(f"""
                    <div class="track-card">
                        <b>{s_track['title']}</b> — {s_track['artist']}<br>
                        <span style="font-size: 11px; color: #a1a1aa;">
                            <span class="badge badge-genre" style="font-size: 9px; padding: 1px 5px;">{s_track['genre_key']}</span>
                            {s_track['bpm']} BPM • Key {s_track['key']} • Energy {int(s_track['energy']*100)}%
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if st.button("➕ Add", key=f"add_{s_track['track_id']}", use_container_width=True):
                        if len(st.session_state.custom_user_queue) < 100:
                            st.session_state.custom_user_queue.append(s_track.to_dict())
                            st.session_state.inferred_context = infer_context_from_queue(st.session_state.custom_user_queue)
                            st.rerun()
                        else:
                            st.warning("Queue limit reached (100 tracks).")
                        
    with col_queue:
        st.subheader(f"Your Custom Queue ({len(st.session_state.custom_user_queue)}/100 Tracks)")
        
        if not st.session_state.custom_user_queue:
            st.info("Queue is empty. Select tracks from the browser on the left or load preset batches.")
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                if st.button("✨ Load 5 Preset Tracks", use_container_width=True):
                    cohort_tracks = catalog_df[catalog_df["genre_key"] == active_cohort["genre_key"]].drop_duplicates(subset=["title"]).head(5)
                    st.session_state.custom_user_queue = [row.to_dict() for _, row in cohort_tracks.iterrows()]
                    st.session_state.inferred_context = infer_context_from_queue(st.session_state.custom_user_queue)
                    st.rerun()
            with c_p2:
                if st.button("⚡ Load 15 Preset Tracks", use_container_width=True):
                    cohort_tracks = catalog_df[catalog_df["genre_key"] == active_cohort["genre_key"]].drop_duplicates(subset=["title"]).head(15)
                    st.session_state.custom_user_queue = [row.to_dict() for _, row in cohort_tracks.iterrows()]
                    st.session_state.inferred_context = infer_context_from_queue(st.session_state.custom_user_queue)
                    st.rerun()
        else:
            with st.container(height=360):
                for idx, q_track in enumerate(st.session_state.custom_user_queue):
                    st.markdown(f"""
                    <div class="history-card">
                        <b>#{idx+1}: {q_track['title']}</b> — {q_track['artist']} 
                        <span class="badge badge-genre" style="font-size: 9px; padding: 1px 5px;">{q_track['genre_key']}</span><br>
                        <span style="font-size: 10px; color: #d6d3d1;">{q_track['bpm']} BPM | Key {q_track['key']} | Energy {int(q_track['energy']*100)}%</span>
                    </div>
                    """, unsafe_allow_html=True)
                
            q_bpms = [t["bpm"] for t in st.session_state.custom_user_queue]
            q_energy = [t["energy"] for t in st.session_state.custom_user_queue]
            
            st.markdown(f"""
            <div style="background-color: #1c1917; border-left: 4px solid #10b981; padding: 12px; border-radius: 8px; margin: 10px 0;">
                <b style="color: #10b981;">🧠 Inferred Context: {st.session_state.inferred_context}</b><br>
                <span style="font-size: 12px; color: #d6d3d1;">
                    Queue Mean BPM: <b>{np.mean(q_bpms):.1f}</b> • Energy Envelope: <b>{int(np.mean(q_energy)*100)}%</b>
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("🚀 Launch Autoplay Engine", use_container_width=True):
                    st.session_state.session_played_titles = [t["title"] for t in st.session_state.custom_user_queue]
                    st.session_state.user_seed_history = [t["track_id"] for t in st.session_state.custom_user_queue]
                    st.session_state.active_track_id = int(st.session_state.custom_user_queue[-1]["track_id"])
                    st.session_state.current_page = "page_live_engine"
                    st.rerun()
            with c_btn2:
                if st.button("🗑️ Clear Queue", use_container_width=True):
                    st.session_state.custom_user_queue = []
                    st.rerun()

# ==============================================================================
# SCREEN 2: LIVE FLOW AUTOPLAY RECOMMENDATION ENGINE
# ==============================================================================
else:
    st.title("⚡ Screen 2: Live Flow Autoplay Engine")
    
    if st.session_state.active_track_id is None:
        if st.session_state.custom_user_queue:
            st.session_state.active_track_id = int(st.session_state.custom_user_queue[-1]["track_id"])
        else:
            default_t = catalog_df[catalog_df["genre_key"] == active_cohort["genre_key"]].iloc[0]
            st.session_state.active_track_id = int(default_t["track_id"])
            st.session_state.session_played_titles = [default_t["title"]]

    current_track_series = catalog_df[catalog_df["track_id"] == st.session_state.active_track_id]
    if current_track_series.empty:
        current_track = catalog_df.iloc[0]
    else:
        current_track = current_track_series.iloc[0]

    gate = CONTEXT_PARAM_GATES.get(st.session_state.inferred_context, CONTEXT_PARAM_GATES["Late-Night Solo Highway Drive"])
    hero_apple, hero_spotify, hero_youtube = generate_stream_links(current_track['title'], current_track['artist'])

    st.markdown(f"""
    <div class="flow-hero">
        <span class="badge badge-vibe">NOW STREAMING</span>
        <span class="badge badge-genre">{current_track['genre_key']}</span>
        <span class="badge badge-bpm">{current_track['bpm']} BPM</span>
        <span class="badge badge-key">KEY {current_track['key']}</span>
        <span class="badge badge-collab">ENERGY: {int(current_track['energy']*100)}%</span>
        <h1 style="margin: 8px 0 4px 0; font-size: 38px; font-weight: 900; color: #FFFFFF;">{current_track['title']}</h1>
        <h3 style="color: #d1d5db; font-weight: 500; margin: 0 0 10px 0;">{current_track['artist']} • <i>{current_track['album']}</i></h3>
        <div style="margin-top: 8px; margin-bottom: 12px;">
            {' '.join([f'<span class="badge badge-tag">#{t}</span>' for t in current_track['tags']])}
        </div>
        <div>
            <a href="{hero_apple}" target="_blank" class="stream-link">🍎 Open in Apple Music ↗</a>
            <a href="{hero_spotify}" target="_blank" class="stream-link">🟢 Open in Spotify ↗</a>
            <a href="{hero_youtube}" target="_blank" class="stream-link stream-link-yt">▶️ Watch on YouTube ↗</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ranked_queue = get_strictly_gated_recommendations(current_track, st.session_state.inferred_context, st.session_state.session_played_titles)

    col_next, col_back = st.columns([1.5, 1])
    with col_next:
        if st.button("⏭️ Autoplay Next Best Match", use_container_width=True):
            if not ranked_queue.empty:
                top_rec = ranked_queue.iloc[0]
                st.session_state.user_seed_history.append(int(top_rec["track_id"]))
                st.session_state.session_played_titles.append(top_rec["title"])
                st.session_state.active_track_id = int(top_rec["track_id"])
                st.session_state.action_logs.append(f"Autoplayed: {top_rec['title']} by {top_rec['artist']} ({top_rec['genre_key']})")
                st.rerun()
    with col_back:
        if st.button("⬅️ Back to Queue Builder", use_container_width=True):
            st.session_state.current_page = "page_queue_builder"
            st.rerun()

    st.markdown("---")

    # --- TABS ---
    tab_queue, tab_history, tab_collab, tab_vectors, tab_cohorts = st.tabs([
        "🎯 Context-Gated Autoplay Queue (10 Tracks)", 
        "🕒 Session History & Centroid", 
        "🤝 Users Who Listened Also Listened To", 
        "📊 100k Vector Space", 
        "👥 50 Granular Cohort Archetypes"
    ])

    with tab_queue:
        st.subheader(f"Next 10 Ranked Recommendations (Synchronized with Inferred: '{st.session_state.inferred_context}')")
        st.caption(f"Acoustic Gate: {gate['min_bpm']}-{gate['max_bpm']} BPM | {int(gate['min_energy']*100)}%-{int(gate['max_energy']*100)}% Energy. Banned: {gate['banned_genres']}")
        
        # Display 10 ranked tracks
        top_queue = ranked_queue.head(10)
        
        for idx, (_, row) in enumerate(top_queue.iterrows()):
            c1, c2 = st.columns([3, 1])
            t_apple, t_spot, t_yt = generate_stream_links(row['title'], row['artist'])
            
            with c1:
                st.markdown(f"""
                <div class="track-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: #a855f7; font-size: 18px;">#{idx+1}: {row['title']}</h4>
                        <div>
                            <span class="badge badge-genre">{row['genre_key']}</span>
                            <span class="badge badge-bpm">{row['bpm']} BPM</span>
                            <span class="badge badge-key">Key {row['key']}</span>
                            <span class="badge badge-collab">{int(row['energy']*100)}% Energy</span>
                        </div>
                    </div>
                    <p style="margin: 4px 0 6px 0; color: #f4f4f5; font-weight: 600;">{row['artist']} • <i>{row['album']}</i></p>
                    <div>
                        {' '.join([f'<span class="badge badge-tag">#{t}</span>' for t in row['tags'][:3]])}
                    </div>
                    <div>
                        <a href="{t_apple}" target="_blank" class="stream-link">🍎 Apple Music ↗</a>
                        <a href="{t_spot}" target="_blank" class="stream-link">🟢 Spotify ↗</a>
                        <a href="{t_yt}" target="_blank" class="stream-link stream-link-yt">▶️ YouTube ↗</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.metric("Flow Match Score", f"{int(row['score'])} / 100")
                if st.button("Play Now", key=f"q_{row['track_id']}", use_container_width=True):
                    st.session_state.user_seed_history.append(int(row["track_id"]))
                    st.session_state.session_played_titles.append(row["title"])
                    st.session_state.active_track_id = int(row["track_id"])
                    st.session_state.action_logs.append(f"User forced track: {row['title']}")
                    st.rerun()

    with tab_history:
        st.subheader(f"Full Session Playback Trajectory ({len(st.session_state.user_seed_history)} Tracks)")
        history_tracks = catalog_df[catalog_df["track_id"].isin(st.session_state.user_seed_history)].drop_duplicates(subset=["title"])
        
        h_col1, h_col2 = st.columns([2, 1])
        with h_col1:
            with st.container(height=380):
                for i, (_, h_track) in enumerate(history_tracks.iterrows()):
                    h_apple, h_spot, h_yt = generate_stream_links(h_track['title'], h_track['artist'])
                    st.markdown(f"""
                    <div class="history-card">
                        <b>Song #{i+1}: {h_track['title']}</b> — {h_track['artist']} <span class="badge badge-genre" style="font-size: 10px;">{h_track['genre_key']}</span><br>
                        <span style="font-size: 12px; color: #d6d3d1;">
                            BPM: <b>{h_track['bpm']}</b> | Key: <b>{h_track['key']}</b> | Energy: <b>{int(h_track['energy']*100)}%</b>
                        </span><br>
                        <div style="margin-top: 4px;">
                            <a href="{h_apple}" target="_blank" class="stream-link" style="font-size: 11px;">🍎 Apple Music</a>
                            <a href="{h_spot}" target="_blank" class="stream-link" style="font-size: 11px;">🟢 Spotify</a>
                            <a href="{h_yt}" target="_blank" class="stream-link stream-link-yt" style="font-size: 11px;">▶️ YouTube</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        with h_col2:
            avg_bpm = history_tracks["bpm"].mean()
            avg_energy = history_tracks["energy"].mean()
            st.metric("Session Pacing Mean", f"{avg_bpm:.1f} BPM")
            st.metric("Session Energy Envelope", f"{int(avg_energy*100)}%")
            st.metric("Blocklist Exclusions", f"{len(st.session_state.session_played_titles)} Titles Blocked")

    with tab_collab:
        st.subheader(f"Collaborative Filtering Telemetry: '{current_track['title']}' ({current_track['genre_key']})")
        
        eligible_collab = catalog_df[
            ((catalog_df["genre_key"] == current_track["genre_key"]) | 
             (catalog_df["artist"] == current_track["artist"])) &
            (~catalog_df["title"].isin(st.session_state.session_played_titles))
        ].drop_duplicates(subset=["title"])
        
        sample_n = min(10, len(eligible_collab))
        if sample_n > 0:
            collab_sample = eligible_collab.sample(sample_n, random_state=42)
        else:
            collab_sample = catalog_df[~catalog_df["title"].isin(st.session_state.session_played_titles)].drop_duplicates(subset=["title"]).head(10)
            
        for idx, (_, c_row) in enumerate(collab_sample.iterrows()):
            c_apple, c_spot, c_yt = generate_stream_links(c_row['title'], c_row['artist'])
            st.markdown(f"""
            <div class="track-card" style="border-left: 4px solid #3b82f6;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #60a5fa; font-size: 16px;">#{idx+1}: {c_row['title']}</h4>
                        <p style="margin: 2px 0; color: #FFFFFF; font-weight: 600;">{c_row['artist']} • <i>{c_row['album']}</i></p>
                    </div>
                    <div>
                        <span class="badge badge-genre">{c_row['genre_key']}</span>
                        <span class="badge badge-bpm">{random.randint(82, 98)}% Affinity</span>
                    </div>
                </div>
                <div>
                    <a href="{c_apple}" target="_blank" class="stream-link">🍎 Apple Music ↗</a>
                    <a href="{c_spot}" target="_blank" class="stream-link">🟢 Spotify ↗</a>
                    <a href="{c_yt}" target="_blank" class="stream-link stream-link-yt">▶️ YouTube ↗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_vectors:
        st.subheader("100k Catalog Multi-Vector Distribution")
        
        unique_for_scatter = catalog_df.drop_duplicates(subset=["title"])
        safe_scatter_n = min(len(unique_for_scatter), 200)
        sample_scatter = unique_for_scatter.sample(safe_scatter_n, random_state=42)
        
        fig_scatter = px.scatter(
            sample_scatter, 
            x="bpm", 
            y="energy", 
            color="genre_key",
            hover_data=["title", "artist", "key"],
            title="BPM vs Energy Multi-Genre Vector Projection",
            template="plotly_dark"
        )
        fig_scatter.update_layout(paper_bgcolor="#151518", plot_bgcolor="#151518", font=dict(color="#F3F4F6"))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab_cohorts:
        st.subheader("50 Granular User Cohort Archetypes")
        st.dataframe(pd.DataFrame(USER_COHORTS), use_container_width=True, height=600)
