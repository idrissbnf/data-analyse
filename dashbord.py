import io
from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pyodbc
import tempfile
import os
from datetime import datetime
import base64


# Function to add background image
def add_bg_from_file(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()

    # CSS to set the background image
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def add_custom_css():
    st.markdown("""
    <style>
        /* Hide default navbar */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom navbar styles - full width and fixed at top */
        .custom-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background-color: var(--navbar-bg);
            color: var(--navbar-text);
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 999;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            width: 100%;
        }
        
        /* Change sidebar background color to match navbar */
        [data-testid="stSidebar"] {
            background-color: rgba(255,255,255,0.25);!important;
            color: white !important;
        }
        
        /* Make sidebar text white for better contrast */
        [data-testid="stSidebar"] .st-bq {
            color: white !important;
        }
        
        /* Make radio buttons text white */
        [data-testid="stSidebar"] .st-cj {
            color: white !important;
        }
        
        /* Navigation title color */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: white !important;
        }
        
        /* Navigation styles */
        .custom-navigation {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 8px 15px;
            background-color: var(--navigation-bg);
            color: var(--navbar-text);
            margin: 10px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .nav-item {
            padding: 8px 15px;
            margin: 0 5px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .nav-item:hover {
            background-color: rgba(255,255,255,0.2);
        }
        
        .nav-item.active {
            background-color: rgba(255,255,255,0.3);
            font-weight: bold;
        }
        
        /* Add padding to the top of content to account for fixed navbar */
        .main-content {
            padding-top: 60px;
        }
        
        /* Adjust sidebar to not overlap with navbar */
        [data-testid="stSidebar"] {
            margin-top: 60px !important;
            z-index: 998 !important;
        }
        
        /* Ensure sidebar content starts below navbar */
        [data-testid="stSidebarContent"] {
            padding-top: 0 !important;
        }
        
        /* Adjust main content area to account for sidebar and navbar */
        .main .block-container {
            padding-top: 1rem !important;
            margin-left: 0 !important;
        }
        
        .navbar-brand {
            font-size: 22px;
            font-weight: bold;
            display: flex;
            align-items: center;
        }
        
        .navbar-actions {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .social-icons {
            display: flex;
            gap: 10px;
        }
        
        .social-icon {
            font-size: 20px;
            color: var(--navbar-text);
            padding: 5px;
            border-radius: 5px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .social-icon:hover {
            transform: translateY(-2px);
            background-color: rgba(255,255,255,0.1);
        }
        
        /* Set fixed colors (no more dark/light mode) */
        :root {
            --navbar-bg: #1E3A8A;
            --navbar-text: white;
            --navigation-bg: #2563EB; /* Similar but different color than navbar */
        }
        
        /* Other styles from original code */
        div.stButton button {
            background: linear-gradient(45deg, #2b5876, #4e4376);
            color: white !important;
            font-weight: bold;
            border: none;
            padding: 12px 15px;
            width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            margin: 10px 0;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        div.stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            background: linear-gradient(45deg, #3a7bd5, #5d46a3);
        }
        
        div.stButton button:active {
            transform: translateY(1px);
        }
        
        .subButton button {
            background: linear-gradient(45deg, #4e54c8, #8f94fb) !important;
            padding: 10px !important;
            font-size: 14px !important;
        }
        
        .sidebar-header {
            background-color: #1E3A8A;
            padding: 12px;
            border-radius: 10px;
            margin: 15px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            color: white;
            border: none;
        }
        
        .section-header {
            background-color: #f0f2f6;
            padding: 8px;
            border-radius: 8px;
            margin: 10px 0;
            border: none;
        }
        
        div[data-testid="stVerticalBlock"] > div {
            background-color: transparent;
            border-radius: 10px;
            padding: 10px;
        }
        
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
            background-color: transparent;
            backdrop-filter: none;
            box-shadow: none;
        }
        
        .sidebar .sidebar-content {
            background-color: transparent;
        }
        
        .stCheckbox, .stRadio, .stSlider, .stSelectbox {
            background-color: transparent !important;
        }
        
        /* Enhanced Sidebar Navigation Styling */
        .enhanced-sidebar-title {
            background-color: #1E3A8A;
            color: white;
            padding: 15px 10px;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 25px;
            border-bottom: 2px solid rgba(255,255,255,0.2);
        }
        
        /* Style for sidebar navigation items */
        .sidebar-nav-item {
            display: flex;
            align-items: center;
            padding: 12px 15px;
            margin: 8px 5px;
            border-radius: 10px;
            cursor: pointer;
            background-color: rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }
        
        .sidebar-nav-item:hover {
            background-color: rgba(255,255,255,0.2);
            transform: translateX(5px);
        }
        
        .sidebar-nav-item.active {
            background-color: rgba(255,255,255,0.25);
            border-left: 4px solid white;
        }
        
        .sidebar-nav-icon {
            font-size: 20px;
            margin-right: 12px;
            width: 30px;
            text-align: center;
        }
        
        .sidebar-nav-text {
            font-weight: 500;
            color: white;
        }
        
        /* Hide radio button appearance but keep functionality */
        .st-cx {
            opacity: 0 !important;
            position: absolute !important;
        }
        
        /* Navigation container */
        .sidebar-nav-container {
            margin-bottom: 20px;
            padding: 0 10px;
        }
        
        /* Optional badge for showing notifications or new items */
        .sidebar-nav-badge {
            background-color: #FF5722;
            color: white;
            border-radius: 50%;
            padding: 2px 6px;
            font-size: 10px;
            margin-left: auto;
        }
        
        /* Divider between sections */
        .sidebar-divider {
            height: 1px;
            background-color: rgba(255,255,255,0.2);
            margin: 20px 5px;
        }
        
        /* Section heading in sidebar */
        .sidebar-section-heading {
            color: rgba(255,255,255,0.7);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin: 15px 10px 10px;
            padding-bottom: 5px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        /* Nouveau style pour les options de filtrage */
        .filtrage-titre {
            background-color: #FFFFFF;
            color: #1E3A8A;
            padding: 15px;
            border-radius: 10px 10px 0 0;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 0;
        }
        
        .option-filtrage {
            display: flex;
            flex-direction: column;
            margin-bottom: 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            border-radius: 10px;
            overflow: hidden;
        }
        
        .bouton-filtre {
            padding: 20px 15px;
            text-align: center;
            cursor: pointer;
            font-weight: bold;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        
        .bouton-categorie {
            background-color: #3F51B5;
            margin-bottom: 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }
        
        .bouton-numerique {
            background-color: #3949AB;
        }
        
        .icone-filtre {
            font-size: 24px;
            margin-right: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# Function to add custom navbar with Instagram and WhatsApp icons
def add_navbar():
    navbar_html = """
    <div class="custom-navbar">
        <div class="navbar-brand">
            <span>📊 DataAnalyzer Pro</span>
        </div>
        <div class="navbar-actions">
            <div class="social-icons">
                <a href="https://www.instagram.com/idriss__bnf?igsh=MTd5cXl1d2M2bnJ4eg%3D%3D&utm_source=qr" class="social-icon" title="Instagram" style="color: #E1306C;" ><i class="fab fa-instagram"></i></a>
                <a href="https://wa.me/qr/RJX7SXREUWZAM1" class="social-icon" title="WhatsApp" style="color: #25D366;"><i class="fab fa-whatsapp"></i></a>
                <a href="https://www.linkedin.com/in/idriss-benfanich-70231b348?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app" class="social-icon" title="LinkedIn" style="color: #ffffff;"><i class="fab fa-linkedin"></i></a>
                <a href="https://www.facebook.com/share/X3czgAntBT7npmJ1/?mibextid=dGKdO6" class="social-icon" title="facebook"  style="color: #ffffff;"><i class="fab fa-facebook-f"></i></a>
            </div>
        </div>
    </div>
    
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Add div for main content with padding to account for fixed navbar -->
    <div class="main-content">
    """
    st.markdown(navbar_html, unsafe_allow_html=True)

def create_enhanced_sidebar_navigation():
    # Get current page from session state or default
    nav_options = ["🏠 Accueil", "🔀 Fusion", "📊 Visualisation", "🤖 Prédiction"]
    current_page = st.session_state.get('current_page', nav_options[0])
    
    # Create custom navigation that matches the design in the image
    # Use a hidden container for the state management but don't display radio buttons
    with st.sidebar.container():
        # This hidden radio button maintains the state but won't be shown
        page = st.radio(
            "Navigation", 
            nav_options, 
            index=nav_options.index(current_page), 
            label_visibility="collapsed",
            key="hidden_nav"
        )
        
        # Update current page in session state
        if page != current_page:
            st.session_state['current_page'] = page
    
    # Custom navigation items styling for card-style buttons with reduced spacing
    st.sidebar.markdown("""
    <style>
 div[data-testid="stRadio"] {
            /* Not hiding completely - this was causing the issue */
            /* display: none !important; */
        }
    /* Card-style navigation item with reduced margins */
    .card-nav-item {
        background-color: rgba(255,255,255,0.2);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 8px; /* Reduced from 15px to 8px */
        display: flex;
        align-items: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .card-nav-item.active {
        background-color: rgba(255,255,255,0.3);
        border-left: 4px solid white;
    }
    
    .card-nav-item:hover {
        background-color: rgba(255,255,255,0.25);
        transform: translateX(5px);
    }
    
    .card-nav-icon {
        margin-right: 15px;
        font-size: 24px;
        color: white;
    }
    
    .card-nav-text {
        color: white;
        font-size: 18px;
        font-weight: 500;
    }
    
    /* Reduce spacing between buttons */
    .stButton {
        margin-bottom: 0px !important; /* Remove bottom margin from buttons */
    }
    
    /* Adjust button margins directly */
    div.stButton > button {
        margin-top: 2px !important;  /* Reduced top margin */
        margin-bottom: 2px !important;  /* Reduced bottom margin */
    }
    
    /* Fix for visible radio buttons that might show up despite the hide rule */
    div[data-testid="stRadio"] > div {
        display: none !important;
    }
    
    /* Ensure proper visibility on Streamlit's dark mode */
    @media (prefers-color-scheme: dark) {
        .card-nav-item {
            background-color: rgba(255,255,255,0.15);
        }
        
        .card-nav-item.active {
            background-color: rgba(255,255,255,0.25);
        }
        
        .card-nav-item:hover {
            background-color: rgba(255,255,255,0.2);
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a JavaScript function to handle navigation clicks
    st.sidebar.markdown("""
    <script>
    function navigateTo(index) {
        const radioInputs = document.querySelectorAll('input[name="hidden_nav"]');
        if (radioInputs && radioInputs[index]) {
            radioInputs[index].checked = true;
            radioInputs[index].dispatchEvent(new Event('change', { bubbles: true }));
        }
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Accueil item
    accueil_active = "active" if page == "🏠 Accueil" else ""
    if st.sidebar.button("🏠 Accueil", key="nav_home", use_container_width=True):
        st.session_state['current_page'] = "🏠 Accueil"
        st.rerun()
    
    # Fusion item
    fusion_active = "active" if page == "🔀 Fusion" else ""
    if st.sidebar.button("🔀 Fusion", key="nav_fusion", use_container_width=True):
        st.session_state['current_page'] = "🔀 Fusion"
        st.rerun()
    
    # Visualisation item
    visualisation_active = "active" if page == "📊 Visualisation" else ""
    if st.sidebar.button("📊 Visualisation", key="nav_viz", use_container_width=True):
        st.session_state['current_page'] = "📊 Visualisation"
        st.rerun()
    
    # Prédiction item with New badge
    prediction_active = "active" if page == "🤖 Prédiction" else ""
    if st.sidebar.button("🤖 Prédiction", key="nav_pred", use_container_width=True):
        st.session_state['current_page'] = "🤖 Prédiction"
        st.rerun()
    
    return page

# Nouvelle fonction pour afficher les options de filtrage améliorées
def display_enhanced_filter_options():
    st.sidebar.markdown("""
    <div class="option-filtrage">
        <div class="filtrage-titre">
            Options de filtrage
        </div>
    </div>
    
    <script>
    // JavaScript pour ajouter l'interactivité
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.bouton-filtre').forEach(function(btn) {
            btn.addEventListener('click', function() {
                // Animation simple
                this.style.backgroundColor = '#1E3A8A';
                setTimeout(() => {
                    this.style.backgroundColor = '';
                }, 300);
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Boutons cachés pour le clicage
    cat_filter_clicked = st.sidebar.button("Catégories", key="cat_filter", on_click=None)
    num_filter_clicked = st.sidebar.button("Numériques", key="num_filter", on_click=None)
    
    # Logic for filter buttons
    if cat_filter_clicked:
        st.session_state["show_filter_category"] = not st.session_state["show_filter_category"]
        st.session_state["show_filter_numeric"] = False
        st.rerun()

    if num_filter_clicked:
        st.session_state["show_filter_numeric"] = not st.session_state["show_filter_numeric"]
        st.session_state["show_filter_category"] = False
        st.rerun()

# Configuration de la page
st.set_page_config(
    page_title="Analyse, Nettoyage et Préparation des Données", layout="wide"
)

# Add custom CSS and navbar
add_custom_css()
add_navbar()

# ADD YOUR BACKGROUND IMAGE HERE - PLACE THIS AFTER set_page_config
# Replace 'path/to/your/image.jpg' with the actual path to your image file
try:
    add_bg_from_file(
        "C:/Users/surface/Desktop/mon_tableau_de_bord/images/2.jpeg"
    )  # <- REPLACE THIS WITH YOUR IMAGE PATH
except:
    st.warning("Background image not found. Please update the path.")

# Initialisation des variables dans session_state
if "df" not in st.session_state:
    st.session_state["df"] = None
if "df_filtered" not in st.session_state:
    st.session_state["df_filtered"] = None
if "db_path" not in st.session_state:
    st.session_state["db_path"] = None
if "tables" not in st.session_state:
    st.session_state["tables"] = []
if "show_cleaning" not in st.session_state:
    st.session_state["show_cleaning"] = False  # Affichage du menu de nettoyage (uniquement sur Accueil)
if "show_filtering" not in st.session_state:
    st.session_state["show_filtering"] = False  # Affichage du menu de filtrage (uniquement sur Accueil)
if "show_filter_category" not in st.session_state:
    st.session_state["show_filter_category"] = False  # Affichage du filtre des catégories
if "show_filter_numeric" not in st.session_state:
    st.session_state["show_filter_numeric"] = False  # Affichage du filtre numérique
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🏠 Accueil"

# Use the enhanced sidebar navigation instead of the original radio button
page = create_enhanced_sidebar_navigation()

# La section ci-dessous concerne uniquement la modification de la page d'accueil (🏠 Accueil)
if page == "🏠 Accueil":
    # Titre avec animation et style amélioré
    st.markdown(
        """
    <div style="background-color:rgba(30, 58, 138, 0.9); padding:10px; border-radius:10px; margin-bottom:20px;">
        <h1 style="color:white; text-align:center;">📊 Analyse, Nettoyage et Préparation des Données</h1>
        <p style="color:white; text-align:center;">Votre assistant intelligent pour l'analyse de données</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Disposition en colonnes pour une meilleure organisation
    col1, col2 = st.columns([2, 1])

    with col1:
        # Téléchargement du fichier avec interface améliorée
        st.markdown(
            """
        <div style="background-color:rgba(248, 249, 250, 0.9); padding:15px; border-radius:10px; border:1px solid #ddd;">
            <h3 style="color:#1E3A8A;">📂 Importer vos données</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Téléchargez un fichier CSV, Excel ou Access", type=["csv", "xlsx", "accdb"]
        )

        if uploaded_file:
            with st.spinner("Chargement des données en cours..."):
                file_extension = uploaded_file.name.split(".")[-1]

                if "df" not in st.session_state or st.session_state["df"] is None:
                    if file_extension == "csv":
                        df = pd.read_csv(uploaded_file)
                    elif file_extension == "xlsx":
                        df = pd.read_excel(uploaded_file)
                    elif file_extension == "accdb":
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".accdb") as tmp_file:
                            tmp_file.write(uploaded_file.read())
                            st.session_state["db_path"] = tmp_file.name

                        conn_str = f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state['db_path']}"
                        conn = pyodbc.connect(conn_str)
                        cursor = conn.cursor()

                        st.session_state["tables"] = [
                            table.table_name for table in cursor.tables(tableType="TABLE")
                        ]
                        selected_table = st.selectbox(
                            "📑 Sélectionnez une table", st.session_state["tables"]
                        )

                        if selected_table:
                            df = pd.read_sql(f"SELECT * FROM [{selected_table}]", conn)

                        conn.close()

                    st.session_state["df"] = df
                    st.session_state["df_filtered"] = df.copy()
                    st.success(f"✅ Fichier {uploaded_file.name} chargé avec succès!")

    with col2:
        # Statistiques du jeu de données
        if st.session_state["df"] is not None:
            nb_lignes = len(st.session_state["df"])
            nb_colonnes = len(st.session_state["df"].columns)
            nb_valeurs_manquantes = st.session_state["df"].isna().sum().sum()

    # Organisation des boutons d'actions dans la sidebar - UNIQUEMENT SI UN FICHIER EST CHARGÉ
    if st.session_state["df"] is not None:
        # Affichage des actions disponibles seulement si un fichier est chargé
        st.sidebar.markdown(
            """
        <div class="sidebar-section-heading">
            ACTIONS
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Boutons avec callbacks directs mais style préservé
        sidebar_col1, sidebar_col2 = st.sidebar.columns(2)

        with sidebar_col1:
            clean_clicked = st.button("🧹clean", key="clean_btn")

        with sidebar_col2:
            filter_clicked = st.button("🎛️ Filtrer", key="filter_btn")

        # Logique des boutons
        if clean_clicked:
            st.session_state["show_cleaning"] = not st.session_state["show_cleaning"]
            st.session_state["show_filtering"] = False
            st.rerun()

        if filter_clicked:
            st.session_state["show_filtering"] = not st.session_state["show_filtering"]
            st.session_state["show_cleaning"] = False
            st.rerun()

        # Affichage des options de filtrage améliorées
        if st.session_state["show_filtering"]:
            # Utiliser la nouvelle fonction pour afficher les options de filtrage améliorées
            display_enhanced_filter_options()

        # Options de nettoyage des données
        if st.session_state["show_cleaning"]:
            st.sidebar.markdown(
                """
            <div class="section-header">
                <h4 style="color:#1E3A8A; margin:0 0 8px 0;">🧹 Options de nettoyage</h4>
            </div>
            """,
                unsafe_allow_html=True,
            )

            cleaning_options = {}
            cleaning_options["dropna"] = st.sidebar.checkbox(
                "🗑️ Supprimer les lignes avec valeurs manquantes"
            )
            cleaning_options["fillna"] = st.sidebar.checkbox(
                "🔄 Remplacer valeurs manquantes par la moyenne"
            )
            cleaning_options["dropduplicates"] = st.sidebar.checkbox("📌 Supprimer les doublons")
            cleaning_options["normalize"] = st.sidebar.checkbox(
                "📊 Normaliser les données numériques"
            )

            apply_cleaning_clicked = st.sidebar.button(
                "✅ Appliquer le nettoyage", key="apply_cleaning"
            )

            if apply_cleaning_clicked:
                with st.spinner("Nettoyage en cours..."):
                    df_filtered = st.session_state["df"].copy()

                    if cleaning_options["dropna"]:
                        df_filtered.dropna(inplace=True)

                    if cleaning_options["fillna"]:
                        numeric_cols = df_filtered.select_dtypes(
                            include=["float64", "int64"]
                        ).columns
                        for col in numeric_cols:
                            df_filtered[col] = df_filtered[col].fillna(df_filtered[col].mean())

                    if cleaning_options["dropduplicates"]:
                        df_filtered.drop_duplicates(inplace=True)

                    if cleaning_options["normalize"]:
                        numeric_cols = df_filtered.select_dtypes(
                            include=["float64", "int64"]
                        ).columns
                        for col in numeric_cols:
                            min_val = df_filtered[col].min()
                            max_val = df_filtered[col].max()
                            if max_val > min_val:  # Éviter la division par zéro
                                df_filtered[col] = (df_filtered[col] - min_val) / (max_val - min_val)

                    st.session_state["df_filtered"] = df_filtered
                    st.success("✅ Nettoyage appliqué avec succès!")

        # Filtrage par catégories
        if st.session_state["show_filter_category"]:
            st.sidebar.markdown(
                """
            <div class="section-header">
                <h4 style="color:#1E3A8A; margin:0 0 8px 0;">📌 Filtrage par catégories</h4>
            </div>
            """,
                unsafe_allow_html=True,
            )

            df_filtered = st.session_state["df"].copy()
            cat_columns = df_filtered.select_dtypes(include=["object", "category"]).columns
            filter_changes = False
            category_filters = {}

            for col in cat_columns:
                category_filters[col] = st.sidebar.multiselect(
                    f"📌 {col}", df_filtered[col].dropna().unique()
                )
                if category_filters[col]:
                    filter_changes = True

            if filter_changes:
                apply_cat_filters_clicked = st.sidebar.button(
                    "✅ Appliquer les filtres", key="apply_cat_filters"
                )

                if apply_cat_filters_clicked:
                    # Appliquer les filtres
                    for col, values in category_filters.items():
                        if values:
                            df_filtered = df_filtered[df_filtered[col].isin(values)]

                    st.session_state["df_filtered"] = df_filtered
                    st.success("✅ Filtres catégoriels appliqués!")

        # Filtrage par valeurs numériques
        if st.session_state["show_filter_numeric"]:
            st.sidebar.markdown(
                """
            <div class="section-header">
                <h4 style="color:#1E3A8A; margin:0 0 8px 0;">📏 Filtrage par valeurs numériques</h4>
            </div>
            """,
                unsafe_allow_html=True,
            )

            df_filtered = st.session_state["df"].copy()
            num_columns = df_filtered.select_dtypes(include=["int64", "float64"]).columns
            filter_changes = False
            numeric_filters = {}

            for col in num_columns:
                min_val, max_val = float(df_filtered[col].min()), float(df_filtered[col].max())
                if min_val < max_val:
                    numeric_filters[col] = st.sidebar.slider(
                        f"📏 {col}", min_val, max_val, (min_val, max_val)
                    )
                    filter_changes = True

            if filter_changes:
                apply_num_filters_clicked = st.sidebar.button(
                    "✅ Appliquer les filtres", key="apply_num_filters"
                )

                if apply_num_filters_clicked:
                    # Appliquer les filtres
                    for col, range_vals in numeric_filters.items():
                        df_filtered = df_filtered[
                            (df_filtered[col] >= range_vals[0]) & (df_filtered[col] <= range_vals[1])
                        ]

                    st.session_state["df_filtered"] = df_filtered
                    st.success("✅ Filtres numériques appliqués!")

    # Affichage des données avec un titre adaptatif et des métriques
    if st.session_state["df"] is not None:
        container = st.container()

        if st.session_state["show_cleaning"]:
            container.markdown(
                """
            <div style="background-color:rgba(232, 244, 248, 0.9); padding:10px; border-radius:10px; margin-bottom:10px;">
                <h3 style="color:#000000; margin:0;">✅ Données nettoyées</h3>
            </div>
            """,
                unsafe_allow_html=True,
            )
        elif st.session_state["show_filtering"]:
            container.markdown(
                """
            <div style="background-color:rgba(232, 244, 248, 0.9); padding:10px; border-radius:10px; margin-bottom:10px;">
                <h3 style="color:#000000; margin:0;">✅ Données filtrées</h3>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            container.markdown(
                """
            <div style="background-color:rgba(232, 244, 248, 0.9); padding:10px; border-radius:10px; margin-bottom:10px;">
                <h3 style="color:#000000; margin:0;">🔍 Aperçu des données</h3>
            </div>
            """, unsafe_allow_html=True,
            )
            # Métriques des données filtrées vs données originales
        if st.session_state["df"] is not None and st.session_state["df_filtered"] is not None:
            orig_rows = len(st.session_state["df"])
            filtered_rows = len(st.session_state["df_filtered"])
            percentage = (
                round((filtered_rows / orig_rows) * 100, 1) if orig_rows > 0 else 0
            )

            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.metric("Lignes d'origine", orig_rows)
            with metric_col2:
                st.metric("Lignes filtrées", filtered_rows)
            with metric_col3:
                st.metric("Données conservées", f"{percentage}%")

        # Tableau de données avec options d'affichage
        tab1, tab2 = st.tabs(["📋 Tableau de données", "📊 Résumé statistique"])

        with tab1:
            # Option pour voir toutes les données ou limiter l'affichage
            show_all = st.checkbox("Afficher toutes les lignes", value=False)

            if show_all:
                st.dataframe(st.session_state["df_filtered"], use_container_width=True)
            else:
                st.dataframe(st.session_state["df_filtered"].head(50), use_container_width=True)
                st.info(
                    f"Affichage limité aux 50 premières lignes. {len(st.session_state['df_filtered'])} lignes au total."
                )

        with tab2:
            if not st.session_state["df_filtered"].empty:
                st.write(st.session_state["df_filtered"].describe())

                # Informations sur les types de données
                st.markdown("#### Types de données:")
                dtypes = st.session_state["df_filtered"].dtypes.reset_index()
                dtypes.columns = ["Colonne", "Type"]
                st.dataframe(dtypes, use_container_width=True)
            else:
                st.warning("Aucune donnée disponible après filtrage.")
 
  
 
            
# Nouvelle Page: Fusion et Nettoyage de Données
if page == "🔀 Fusion":
    st.title("🔀 Fusion et Nettoyage de Données")
    
    if st.session_state["db_path"]:
        conn_str = f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state['db_path']}"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Sélection des tables
        selected_tables = st.multiselect("Sélectionnez les tables à combiner", st.session_state["tables"])
        
        combined_df = pd.DataFrame()
        selected_columns = {}
        
        if selected_tables:
            for table in selected_tables:
                df_temp = pd.read_sql(f"SELECT * FROM [{table}]", conn)
                columns = st.multiselect(f"Sélectionnez les colonnes de {table}", df_temp.columns, key=table)
                if columns:
                    selected_columns[table] = columns
                    if combined_df.empty:
                        combined_df = df_temp[columns]
                    else:
                        combined_df = pd.concat([combined_df, df_temp[columns]], axis=1)
            
            st.session_state["df_merged"] = combined_df
            st.write("### Données combinées :")
            st.dataframe(combined_df)
        
        conn.close()
    
    # Nettoyage des données fusionnées
    if "df_merged" in st.session_state:
        df_cleaned = st.session_state["df_merged"].copy()
        
        if st.sidebar.button("🧹 Nettoyage des Données"):
            st.session_state["show_cleaning_fusion"] = not st.session_state.get("show_cleaning_fusion", False)

        if st.sidebar.button("🎛️ Filtrage des Données"):
            st.session_state["show_filtering_fusion"] = not st.session_state.get("show_filtering_fusion", False)
        
        if st.sidebar.button("📈 Visualisation des Données"):
            st.session_state["show_visualization_fusion"] = not st.session_state.get("show_visualization_fusion", False)

        # Nettoyage des données fusionnées
        if st.session_state.get("show_cleaning_fusion", False):
            st.subheader("🧹 Nettoyage des Données")
            if st.checkbox("Supprimer les valeurs manquantes"):
                df_cleaned.dropna(inplace=True)
                st.write("✔️ Valeurs manquantes supprimées.")
                
            if st.checkbox("Supprimer les doublons"):
                df_cleaned.drop_duplicates(inplace=True)
                st.write("✔️ Doublons supprimés.")
            
            numeric_cols = df_cleaned.select_dtypes(include=['float64', 'int64']).columns
            if st.checkbox("Normaliser les données numériques") and len(numeric_cols) > 0:
                df_cleaned[numeric_cols] = (df_cleaned[numeric_cols] - df_cleaned[numeric_cols].min()) / (df_cleaned[numeric_cols].max() - df_cleaned[numeric_cols].min())
                st.write("✔️ Normalisation appliquée.")
        
        # Filtrage dynamique
        df_filtered = df_cleaned.copy()
        if st.session_state.get("show_filtering_fusion", False):
            st.subheader("🎛️ Filtrage des Données")
            
            if st.sidebar.button("Filtrer les catégories"):
                cat_columns = df_filtered.select_dtypes(include=["object", "category"]).columns
                for col in cat_columns:
                    selected_values = st.sidebar.multiselect(f"Filtrer {col}", df_filtered[col].dropna().unique())
                    if selected_values:
                        df_filtered = df_filtered[df_filtered[col].isin(selected_values)]
            
            if st.sidebar.button("Filtrer les nombres"):
                num_columns = df_filtered.select_dtypes(include=["int64", "float64"]).columns
                for col in num_columns:
                    min_val, max_val = float(df_filtered[col].min()), float(df_filtered[col].max())
                    if min_val < max_val:
                        selected_range = st.sidebar.slider(f"Filtrer {col}", min_val, max_val, (min_val, max_val))
                        df_filtered = df_filtered[(df_filtered[col] >= selected_range[0]) & (df_filtered[col] <= selected_range[1])]
        
        st.write("### Données après Nettoyage et Filtrage :")
        st.dataframe(df_filtered)
        
        # Résumé statistique
        st.subheader("📊 Résumé Statistique des Données Fusionnées :")
        if not df_filtered.empty:
            st.write(df_filtered.describe())
        else:
            st.warning("Aucune donnée après nettoyage et filtrage.")
        
        # Visualisation des données fusionnées
        if st.session_state.get("show_visualization_fusion", False):
            st.subheader("📈 Visualisation des Données Fusionnées")
            if not df_filtered.empty:
                graph_type = st.selectbox("Choisissez un type de graphique", ["Histogramme", "Nuage de points", "Graphique en barres", "Camembert"])
                
                if graph_type == "Histogramme":
                    column = st.selectbox("Sélectionnez une colonne numérique", df_filtered.select_dtypes(include=['int64', 'float64']).columns)
                    if column:
                        fig = px.histogram(df_filtered, x=column, nbins=30, title=f"Histogramme de {column}")
                        st.plotly_chart(fig)
                
                elif graph_type == "Nuage de points":
                    x_col = st.selectbox("Sélectionnez l'axe X", df_filtered.columns)
                    y_col = st.selectbox("Sélectionnez l'axe Y", df_filtered.columns)
                    if x_col and y_col:
                        fig = px.scatter(df_filtered, x=x_col, y=y_col, title=f"Nuage de points : {x_col} vs {y_col}")
                        st.plotly_chart(fig)
                
                elif graph_type == "Graphique en barres":
                    column = st.selectbox("Sélectionnez une colonne catégorielle", df_filtered.select_dtypes(include=['object', 'category']).columns)
                    if column:
                        fig = px.bar(df_filtered[column].value_counts().reset_index(), x='index', y=column, title=f"Graphique en barres de {column}")
                        st.plotly_chart(fig)
                
                elif graph_type == "Camembert":
                    column = st.selectbox("Sélectionnez une colonne catégorielle", df_filtered.select_dtypes(include=['object', 'category']).columns)
                    if column:
                        fig = px.pie(df_filtered, names=column, title=f"Répartition de {column}")
                        st.plotly_chart(fig)
            else:
                st.warning("Aucune donnée disponible pour la visualisation.")
                
if page == "📊 Visualisation":
    st.title("📊 Tableau de Bord Analytique")
    
    if st.session_state["df"] is not None:
        # On vérifie d'abord le type de fichier chargé en session
        file_type = None
        if "db_path" in st.session_state and st.session_state["db_path"]:
            file_type = "access"
        elif "df" in st.session_state and st.session_state["df"] is not None:
            file_type = "excel_csv"
        
        df = None
        
        # Si fichier Access
        if file_type == "access":
            selected_table = st.sidebar.selectbox("Sélectionnez une table", st.session_state["tables"])
            
            if selected_table:
                conn_str = f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={st.session_state['db_path']}"
                conn = pyodbc.connect(conn_str)
                df = pd.read_sql(f"SELECT * FROM [{selected_table}]", conn)
                conn.close()
        
        # Si fichier Excel ou CSV
        elif file_type == "excel_csv":
            df = st.session_state["df"].copy()
            st.sidebar.info("Données chargées à partir d'un fichier Excel ou CSV")
        
        if df is not None:
            # Liste des colonnes disponibles pour les graphiques
            all_columns = df.columns.tolist()
            num_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            cat_columns = df.select_dtypes(include=['object']).columns.tolist()
            
            # Initialiser les variables avec des valeurs par défaut
            color_primary = "#1E3A8A"
            color_secondary = "#2CFF1C"
            
            # Variables pour les graphiques avec des valeurs par défaut
            bar_x = cat_columns[0] if len(cat_columns) > 0 else "Aucune colonne"
            bar_y = num_columns[0] if len(num_columns) > 0 else "Aucune colonne"
            show_second_year = True
            second_y = num_columns[1] if len(num_columns) > 1 else None
            
            pie_col = cat_columns[0] if len(cat_columns) > 0 else "Aucune colonne"
            center_value = 45
            
            line_x = all_columns[0] if len(all_columns) > 0 else "Aucune colonne"
            line_y = num_columns[:1] if len(num_columns) > 0 else []
            
            bubble_x = num_columns[0] if len(num_columns) > 0 else "Aucune colonne"
            bubble_y = num_columns[1] if len(num_columns) > 1 else "Aucune colonne"
            bubble_size = num_columns[0] if len(num_columns) > 0 else "Aucune colonne"
            bubble_color = cat_columns[0] if len(cat_columns) > 0 else "Aucune colonne"
            
            boxplot_col = num_columns[0] if len(num_columns) > 0 else "Aucune colonne"
            group_by = "Aucun"
            
            # Initialiser la liste des tableaux sauvegardés si elle n'existe pas
            if "saved_dashboards" not in st.session_state:
                st.session_state["saved_dashboards"] = []
            
            # ----- SECTION SAUVEGARDE DU TABLEAU DE BORD -----
            st.sidebar.markdown("## 💾 Tableaux sauvegardés")
            
            # Style CSS personnalisé pour améliorer l'apparence des tableaux sauvegardés
            st.sidebar.markdown("""
            <style>
                .dashboard-item {
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                    padding: 12px;
                    margin-bottom: 10px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    transition: all 0.3s ease;
                }
                .dashboard-item:hover {
                    background-color: rgba(255, 255, 255, 0.15);
                    transform: translateY(-2px);
                }
                .dashboard-name {
                    font-weight: bold;
                    font-size: 1.1em;
                    margin-bottom: 5px;
                }
                .dashboard-date {
                    font-size: 0.85em;
                    color: rgba(255, 255, 255, 0.7);
                    margin-bottom: 10px;
                }
                .dashboard-actions {
                    display: flex;
                    justify-content: space-between;
                    margin-top: 8px;
                }
                .action-button {
                    border-radius: 5px;
                    padding: 5px 10px;
                    font-size: 0.9em;
                    cursor: pointer;
                    text-align: center;
                }
                .load-button {
                    background-color: #1E3A8A;
                    color: white;
                    flex: 2;
                    margin-right: 5px;
                }
                .delete-button {
                    background-color: rgba(220, 53, 69, 0.7);
                    color: white;
                    flex: 1;
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Nom du tableau de bord
            dashboard_name = st.sidebar.text_input("Nom du tableau de bord", "Mon Tableau de Bord")
            
            # Afficher les tableaux de bord sauvegardés
            if st.session_state["saved_dashboards"]:
                for i, dashboard in enumerate(st.session_state["saved_dashboards"]):
                    # Utiliser un conteneur HTML personnalisé pour chaque élément
                    dashboard_html = f"""
                    <div class="dashboard-item" id="dashboard-{i}">
                        <div class="dashboard-name">{dashboard['name']}</div>
                        <div class="dashboard-date">{dashboard['timestamp']}</div>
                        <div class="dashboard-actions">
                            <div class="action-button load-button" id="load-{i}">📊 Charger</div>
                            <div class="action-button delete-button" id="delete-{i}">🗑️</div>
                        </div>
                    </div>
                    """
                    st.sidebar.markdown(dashboard_html, unsafe_allow_html=True)
                    
                    # Créer des boutons "invisibles" qui détectent les clics sur les éléments HTML
                    col1, col2 = st.sidebar.columns([2, 1])
                    with col1:
                        if st.button("Charger", key=f"load_{i}", help="Charger ce tableau de bord"):
                            # Mettre en place les flags dans session_state
                            st.session_state["dashboard_to_load"] = True
                            st.session_state["color_primary"] = dashboard["colors"]["primary"]
                            st.session_state["color_secondary"] = dashboard["colors"]["secondary"]
                            
                            # Stocker les paramètres des graphiques
                            st.session_state["selected_bar_x"] = dashboard["charts"]["bar"]["x"]
                            st.session_state["selected_bar_y"] = dashboard["charts"]["bar"]["y"]
                            st.session_state["selected_show_second"] = dashboard["charts"]["bar"]["show_second"]
                            st.session_state["selected_second_y"] = dashboard["charts"]["bar"]["second_y"]
                            
                            st.session_state["selected_pie_col"] = dashboard["charts"]["pie"]["col"]
                            st.session_state["selected_center_value"] = dashboard["charts"]["pie"]["center_value"]
                            
                            st.session_state["selected_line_x"] = dashboard["charts"]["line"]["x"]
                            st.session_state["selected_line_y"] = dashboard["charts"]["line"]["y"]
                            
                            st.session_state["selected_bubble_x"] = dashboard["charts"]["bubble"]["x"]
                            st.session_state["selected_bubble_y"] = dashboard["charts"]["bubble"]["y"]
                            st.session_state["selected_bubble_size"] = dashboard["charts"]["bubble"]["size"]
                            st.session_state["selected_bubble_color"] = dashboard["charts"]["bubble"]["color"]
                            
                            st.session_state["selected_boxplot_col"] = dashboard["charts"]["box"]["col"]
                            st.session_state["selected_group_by"] = dashboard["charts"]["box"]["group_by"]
                            
                            st.rerun()
                    
                    with col2:
                        if st.button("🗑️", key=f"delete_{i}", help="Supprimer ce tableau de bord"):
                            # Supprimer le tableau de bord
                            del st.session_state["saved_dashboards"][i]
                            st.rerun()
            else:
                st.sidebar.info("Aucun tableau de bord sauvegardé.")
            
            # Récupérer les valeurs des tableaux chargés si disponibles
            if "dashboard_to_load" in st.session_state and st.session_state["dashboard_to_load"]:
                # Récupérer les valeurs stockées
                color_primary = st.session_state["color_primary"]
                color_secondary = st.session_state["color_secondary"]
                
                bar_x = st.session_state["selected_bar_x"]
                bar_y = st.session_state["selected_bar_y"]
                show_second_year = st.session_state["selected_show_second"]
                second_y = st.session_state["selected_second_y"]
                
                pie_col = st.session_state["selected_pie_col"]
                center_value = st.session_state["selected_center_value"]
                
                line_x = st.session_state["selected_line_x"]
                line_y = st.session_state["selected_line_y"]
                
                bubble_x = st.session_state["selected_bubble_x"]
                bubble_y = st.session_state["selected_bubble_y"]
                bubble_size = st.session_state["selected_bubble_size"]
                bubble_color = st.session_state["selected_bubble_color"]
                
                boxplot_col = st.session_state["selected_boxplot_col"]
                group_by = st.session_state["selected_group_by"]
                
                # Réinitialiser le flag après utilisation
                st.session_state["dashboard_to_load"] = False
            
            # ----- SECTION PARAMÈTRES DES GRAPHIQUES -----
            st.sidebar.markdown("## 📈 Paramètres des graphiques")
            
            # Personnalisation des couleurs en haut pour affecter tous les graphiques
            st.sidebar.markdown("### 🎨 Couleurs")
            col1, col2 = st.sidebar.columns(2)
            with col1:
                color_primary = st.color_picker("Principale", color_primary)
            with col2:
                color_secondary = st.color_picker("Secondaire", color_secondary)
            
            # Organisation des paramètres graphiques
            graph_tabs = st.sidebar.tabs([
                "Barres", "Circulaire", "Ligne", "Bulles", "Boîte"
            ])
            
            # Tab 1: Graphique à barres
            with graph_tabs[0]:
                st.markdown("### 📊 Graphique à barres")
                # Utiliser les valeurs par défaut ou chargées
                bar_x = st.selectbox("Axe X (Catégorie)", 
                                    cat_columns if len(cat_columns) > 0 else ["Aucune colonne"],
                                    index=cat_columns.index(bar_x) if bar_x in cat_columns else 0)
                bar_y = st.selectbox("Axe Y (Valeur)", 
                                    num_columns if len(num_columns) > 0 else ["Aucune colonne"],
                                    index=num_columns.index(bar_y) if bar_y in num_columns else 0)
                show_second_year = st.checkbox("Afficher une seconde série", value=show_second_year)
                if show_second_year and len(num_columns) > 1:
                    second_y_options = [col for col in num_columns if col != bar_y]
                    second_y_index = second_y_options.index(second_y) if second_y in second_y_options else 0
                    second_y = st.selectbox("Seconde valeur", second_y_options, index=second_y_index)
            
            # Tab 2: Graphique circulaire
            with graph_tabs[1]:
                st.markdown("### 🍩 Graphique circulaire")
                pie_col = st.selectbox("Catégorie", 
                                      cat_columns if len(cat_columns) > 0 else ["Aucune colonne"],
                                      index=cat_columns.index(pie_col) if pie_col in cat_columns else 0)
                center_value = st.slider("Valeur centrale (%)", 0, 100, center_value)
            
            # Tab 3: Graphique en ligne
            with graph_tabs[2]:
                st.markdown("### 📈 Graphique en ligne")
                line_x = st.selectbox("Axe X", 
                                     all_columns if len(all_columns) > 0 else ["Aucune colonne"],
                                     index=all_columns.index(line_x) if line_x in all_columns else 0,
                                     key="line_x_widget")
                
                # Pour les multiselect, on doit s'assurer que toutes les valeurs sont disponibles
                valid_line_y = [y for y in line_y if y in num_columns]
                line_y = st.multiselect("Axe Y (Métriques)", 
                                       num_columns if len(num_columns) > 0 else ["Aucune colonne"],
                                       default=valid_line_y if valid_line_y else num_columns[:1] if len(num_columns) > 0 else [],
                                       key="line_y_widget")
            
            # Tab 4: Graphique à bulles
            with graph_tabs[3]:
                st.markdown("### 🔵 Graphique à bulles")
                bubble_x = st.selectbox("Axe X", 
                                       num_columns if len(num_columns) > 0 else ["Aucune colonne"],
                                       index=num_columns.index(bubble_x) if bubble_x in num_columns else 0,
                                       key="bubble_x_widget")
                
                bubble_y_options = [col for col in num_columns if col != bubble_x] if len(num_columns) > 1 else ["Aucune colonne"]
                bubble_y_index = bubble_y_options.index(bubble_y) if bubble_y in bubble_y_options else 0
                bubble_y = st.selectbox("Axe Y", 
                                       bubble_y_options,
                                       index=bubble_y_index,
                                       key="bubble_y_widget")
                
                bubble_size = st.selectbox("Taille des bulles", 
                                          num_columns if len(num_columns) > 0 else ["Aucune colonne"],
                                          index=num_columns.index(bubble_size) if bubble_size in num_columns else 0,
                                          key="bubble_size_widget")
                
                bubble_color = st.selectbox("Couleur des bulles", 
                                           cat_columns if len(cat_columns) > 0 else ["Aucune colonne"],
                                           index=cat_columns.index(bubble_color) if bubble_color in cat_columns else 0,
                                           key="bubble_color_widget")
            
            # Tab 5: Boîte à moustaches
            with graph_tabs[4]:
                st.markdown("### 📦 Boîte à moustaches")
                boxplot_col = st.selectbox("Colonne numérique", 
                                          num_columns if len(num_columns) > 0 else ["Aucune colonne"],
                                          index=num_columns.index(boxplot_col) if boxplot_col in num_columns else 0,
                                          key="boxplot_col_widget")
                
                group_by_options = ["Aucun"] + cat_columns
                group_by_index = group_by_options.index(group_by) if group_by in group_by_options else 0
                group_by = st.selectbox("Grouper par (optionnel)", 
                                       group_by_options,
                                       index=group_by_index,
                                       key="group_by_widget")
            
            # Bouton pour sauvegarder le tableau de bord actuel
            if st.sidebar.button("💾 Sauvegarder ce tableau", 
                                help="Sauvegarder la configuration actuelle du tableau de bord"):
                # Collecter tous les paramètres actuels
                dashboard_config = {
                    "name": dashboard_name,
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "colors": {
                        "primary": color_primary,
                        "secondary": color_secondary
                    },
                    "charts": {
                        "bar": {
                            "x": bar_x,
                            "y": bar_y,
                            "show_second": show_second_year,
                            "second_y": second_y
                        },
                        "pie": {
                            "col": pie_col,
                            "center_value": center_value
                        },
                        "line": {
                            "x": line_x,
                            "y": line_y
                        },
                        "bubble": {
                            "x": bubble_x,
                            "y": bubble_y,
                            "size": bubble_size,
                            "color": bubble_color
                        },
                        "box": {
                            "col": boxplot_col,
                            "group_by": group_by
                        }
                    }
                }
                
                # Vérifier si un tableau de bord avec ce nom existe déjà
                existing_idx = next((i for i, d in enumerate(st.session_state["saved_dashboards"]) 
                                  if d["name"] == dashboard_name), None)
                
                if existing_idx is not None:
                    # Mettre à jour le tableau existant
                    st.session_state["saved_dashboards"][existing_idx] = dashboard_config
                    st.sidebar.success(f"✅ Tableau '{dashboard_name}' mis à jour!")
                else:
                    # Ajouter un nouveau tableau
                    st.session_state["saved_dashboards"].append(dashboard_config)
                    st.sidebar.success(f"✅ Tableau '{dashboard_name}' sauvegardé!")
            
            # Paramètres globaux pour tous les graphiques
            smaller_height = 240  # Hauteur réduite pour les graphiques
            
            # Aperçu des données masqué par défaut mais accessible
            with st.expander("Aperçu des données"):
                st.dataframe(df)
            
            # Cartes récapitulatives en haut (en une seule ligne)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div style="background-color:{}; padding:5px; border-radius:10px; text-align:center;">
                    <h4 style="color:white; margin:0; font-size:0.9em;">Total Données</h4>
                    <h2 style="color:white; font-size:1.8em; margin:0;">{}</h2>
                </div>
                """.format(color_primary, len(df)), unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                <div style="background-color:white; padding:5px; border-radius:10px; border:1px solid #ddd; text-align:center;">
                    <h4 style="color:#333; margin:0; font-size:0.9em;">Colonnes</h4>
                    <h2 style="color:#333; font-size:1.8em; margin:0;">{}</h2>
                </div>
                """.format(len(df.columns)), unsafe_allow_html=True)
                
            with col3:
                unique_count = 0
                if len(cat_columns) > 0:
                    unique_count = df[cat_columns[0]].nunique()
                
                st.markdown("""
                <div style="background-color:white; padding:5px; border-radius:10px; border:1px solid #ddd; text-align:center;">
                    <h4 style="color:#333; margin:0; font-size:0.9em;">Valeurs Uniques</h4>
                    <h2 style="color:#333; font-size:1.8em; margin:0;">{}</h2>
                </div>
                """.format(unique_count), unsafe_allow_html=True)
                
            with col4:
                avg_value = 0
                if len(num_columns) > 0:
                    avg_value = round(df[num_columns[0]].mean(), 1)
                
                st.markdown("""
                <div style="background-color:white; padding:5px; border-radius:10px; border:1px solid #ddd; text-align:center;">
                    <h4 style="color:#333; margin:0; font-size:0.9em;">Moyenne</h4>
                    <h2 style="color:#333; font-size:1.8em; margin:0;">{}</h2>
                </div>
                """.format(avg_value), unsafe_allow_html=True)
            
            # SECTION POUR LES 5 GRAPHIQUES PRINCIPAUX VISIBLES SANS DÉFILEMENT
            st.markdown("### Principaux Indicateurs")
            
            # Première ligne - 3 graphiques en row
            col1, col2, col3 = st.columns([1, 1, 1])
            
            # Variables pour stocker les figures pour l'exportation PDF
            bar_fig = None
            pie_fig = None
            line_fig = None
            bubble_fig = None
            box_fig = None
            
            # Graphique 1 - Barres
            with col1:
                st.markdown("<div style='background-color:white; padding:10px; border-radius:10px; border:1px solid #ddd;'>", unsafe_allow_html=True)
                st.markdown("<h5 style='color:#333; margin-top:0;'>Tendances</h5>", unsafe_allow_html=True)
                
                if len(num_columns) > 0 and len(cat_columns) > 0 and bar_x in df.columns and bar_y in df.columns:
                    fig = px.bar(df, x=bar_x, y=bar_y, 
                                 color_discrete_sequence=[color_primary],
                                 template="plotly_white")
                    
                    if show_second_year and second_y and second_y in df.columns:
                        fig.add_bar(x=df[bar_x], y=df[second_y], 
                                   name=second_y, marker_color=color_secondary)
                        fig.update_layout(barmode='group')
                    
                    fig.update_layout(
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        margin=dict(l=10, r=10, t=10, b=10),
                        height=smaller_height
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    bar_fig = fig
                else:
                    st.info("Données insuffisantes ou colonnes invalides")
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Graphique 2 - Circulaire
            with col2:
                st.markdown("<div style='background-color:white; padding:10px; border-radius:10px; border:1px solid #ddd;'>", unsafe_allow_html=True)
                st.markdown("<h5 style='color:#333; margin-top:0;'>Répartition</h5>", unsafe_allow_html=True)
                
                if len(cat_columns) > 0 and pie_col in df.columns:
                    fig = px.pie(df, names=pie_col, hole=0.6,
                                color_discrete_sequence=[color_primary, color_secondary, "#2D7DD2", "#97CC04"])
                    
                    fig.update_layout(
                        annotations=[dict(text=f"{center_value}%", x=0.5, y=0.5, font_size=20, showarrow=False)],
                        margin=dict(l=10, r=10, t=10, b=10),
                        height=smaller_height,
                        showlegend=False  # Masquer la légende pour gagner de l'espace
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    pie_fig = fig
                else:
                    st.info("Données insuffisantes ou colonne invalide")
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Graphique 3 - Ligne
            with col3:
                st.markdown("<div style='background-color:white; padding:10px; border-radius:10px; border:1px solid #ddd;'>", unsafe_allow_html=True)
                st.markdown("<h5 style='color:#333; margin-top:0;'>Évolution</h5>", unsafe_allow_html=True)
                
                if len(line_y) > 0 and line_x in df.columns and all(col in df.columns for col in line_y):
                    fig = px.line(df, x=line_x, y=line_y, 
                                  color_discrete_sequence=[color_primary, color_secondary])
                    
                    for trace in fig.data:
                        trace.mode = "lines+markers"
                    
                    fig.update_layout(
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        margin=dict(l=10, r=10, t=10, b=10),
                        height=smaller_height
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    line_fig = fig
                else:
                    st.info("Sélectionnez des métriques valides")
                st.markdown("</div>", unsafe_allow_html=True)
                
            # Deuxième ligne - 2 graphiques supplémentaires
            col1, col2 = st.columns(2)
            
            # Graphique 4 - Bulles
            with col1:
                st.markdown("<div style='background-color:white; padding:10px; border-radius:10px; border:1px solid #ddd;'>", unsafe_allow_html=True)
                st.markdown("<h5 style='color:#333; margin-top:0;'>Comparaison Multidimensionnelle</h5>", unsafe_allow_html=True)
                
                valid_bubble_columns = (len(num_columns) >= 3 and len(cat_columns) > 0 and 
                                       bubble_x in df.columns and bubble_y in df.columns and 
                                       bubble_size in df.columns and bubble_color in df.columns)
                
                if valid_bubble_columns:
                    fig = px.scatter(df, x=bubble_x, y=bubble_y, 
                                     size=bubble_size, 
                                     color=bubble_color,
                                     hover_name=cat_columns[0] if cat_columns else None,
                                     color_discrete_sequence=px.colors.sequential.Viridis)
                    
                    fig.update_layout(
                        margin=dict(l=10, r=10, t=10, b=10),
                        height=smaller_height
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    bubble_fig = fig
                else:
                    st.info("Données insuffisantes ou colonnes invalides")
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Graphique 5 - Boîte à moustaches
            with col2:
                st.markdown("<div style='background-color:white; padding:10px; border-radius:10px; border:1px solid #ddd;'>", unsafe_allow_html=True)
                st.markdown("<h5 style='color:#333; margin-top:0;'>Distribution des Valeurs</h5>", unsafe_allow_html=True)
                
                if len(num_columns) > 0 and boxplot_col in df.columns:
                    if group_by != "Aucun" and group_by in df.columns:
                        fig = px.box(df, x=group_by, y=boxplot_col, 
                                    color=group_by,
                                    color_discrete_sequence=[color_primary, color_secondary, "#2D7DD2", "#97CC04"])
                    else:
                        fig = px.box(df, y=boxplot_col, 
                                    color_discrete_sequence=[color_primary])
                    
                    fig.update_layout(
                        margin=dict(l=10, r=10, t=10, b=10),
                        height=smaller_height,
                        showlegend=False  # Masquer la légende pour gagner de l'espace
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    box_fig = fig
                else:
                    st.info("Données insuffisantes ou colonne invalide")
                st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.warning("Veuillez d'abord importer un fichier dans l'onglet 'Importation'.")

# Page Prédiction
if page == "🤖 Prédiction":
    st.title("🤖 Modèles Prédictifs")
    
    if st.session_state["df"] is not None:
        df = st.session_state["df"].copy()
        
        # Section de sélection des paramètres du modèle
        st.sidebar.markdown("## 🎛️ Paramètres du modèle")
        
        # Sélection de la variable cible
        target_col = st.sidebar.selectbox(
            "📌 Variable cible (Y)",
            df.columns
        )
        
        # Sélection des caractéristiques
        feature_cols = st.sidebar.multiselect(
            "📊 Caractéristiques (X)",
            [col for col in df.columns if col != target_col],
            default=[col for col in df.columns if col != target_col][:3]  # Par défaut, sélectionner les 3 premières colonnes
        )
        
        # Option pour le traitement des valeurs catégorielles
        handle_categorical = st.sidebar.checkbox("Encoder les variables catégorielles", value=True)
        
        # Type de modèle à utiliser
        model_type = st.sidebar.selectbox(
            "🧠 Type de modèle",
            ["Régression linéaire", "Classification logistique", "Arbre de décision"]
        )
        
        # Paramètres de validation
        test_size = st.sidebar.slider("Taille de l'ensemble de test (%)", 10, 50, 20) / 100
        
        # Affichage des informations et sélections
        st.markdown("""
        <div style="background-color:#1E3A8A; padding:15px; border-radius:10px; margin-bottom:20px;">
            <h1 style="color:white; text-align:center;">🤖 Modèles Prédictifs</h1>
            <p style="color:white; text-align:center;">Prédisez des résultats à partir de vos données</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Prévisualisation du jeu de données
        st.markdown("""
        <div style="background-color:#f8f9fa; padding:10px; border-radius:10px; margin-bottom:10px;">
            <h3 style="color:#1E3A8A; margin:0;">📊 Aperçu des données</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(df.head())
        
        # Section: Préparation des données
        st.markdown("""
        <div style="background-color:#f8f9fa; padding:10px; border-radius:10px; margin:20px 0 10px 0;">
            <h3 style="color:#1E3A8A; margin:0;">⚙️ Préparation des données</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Variable cible**: {target_col}")
            if target_col in df.columns:
                if pd.api.types.is_numeric_dtype(df[target_col].dtype):
                    st.write(f"Type: Numérique (moyenne: {df[target_col].mean():.2f})")
                else:
                    st.write(f"Type: Catégoriel ({len(df[target_col].unique())} catégories)")
        
        with col2:
            st.markdown(f"**Caractéristiques**: {len(feature_cols)} sélectionnées")
            st.write(f"Taille du jeu d'entraînement: {int((1-test_size)*100)}%")
            st.write(f"Taille du jeu de test: {int(test_size*100)}%")
        
        # Bouton pour lancer l'entraînement du modèle
        train_model = st.button("🚀 Entraîner le modèle", use_container_width=True)
        
        if train_model:
            st.markdown("""
            <div style="background-color:#f8f9fa; padding:10px; border-radius:10px; margin:20px 0 10px 0;">
                <h3 style="color:#1E3A8A; margin:0;">📈 Résultats du modèle</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Simulation de résultats (dans une application réelle, cette partie implémentera scikit-learn)
            with st.spinner("Entraînement du modèle en cours..."):
                import time
                time.sleep(2)  # Simule le temps d'entraînement
                
                # Affichage des métriques simulées
                met_col1, met_col2, met_col3, met_col4 = st.columns(4)
                
                with met_col1:
                    if model_type == "Régression linéaire":
                        st.metric("R² Score", "0.85")
                    else:
                        st.metric("Précision", "87%")
                
                with met_col2:
                    if model_type == "Régression linéaire":
                        st.metric("Erreur moyenne", "1.25")
                    else:
                        st.metric("Rappel", "0.82")
                
                with met_col3:
                    if model_type == "Régression linéaire":
                        st.metric("Erreur abs. moyenne", "0.95")
                    else:
                        st.metric("F1-Score", "0.84")
                
                with met_col4:
                    st.metric("Temps d'entraînement", "1.8s")
                
                # Graphique de résultats simulés
                st.markdown("### 📊 Visualisation des résultats")
                
                # Créer des données simulées pour les graphiques
                import numpy as np
                
                if model_type == "Régression linéaire":
                    x = np.linspace(0, 10, 100)
                    y_true = 2 * x + 1 + np.random.normal(0, 1, 100)
                    y_pred = 1.8 * x + 1.2
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=x, y=y_true, mode='markers', name='Données réelles', marker=dict(color='blue')))
                    fig.add_trace(go.Scatter(x=x, y=y_pred, mode='lines', name='Prédictions', line=dict(color='red')))
                    
                    fig.update_layout(
                        title="Régression: Valeurs réelles vs prédites",
                        xaxis_title="Caractéristique",
                        yaxis_title="Valeur cible",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Afficher les erreurs de prédiction
                    errors = y_true - y_pred
                    fig_error = go.Figure()
                    fig_error.add_trace(go.Histogram(x=errors, marker_color='red'))
                    
                    fig_error.update_layout(
                        title="Distribution des erreurs",
                        xaxis_title="Erreur",
                        yaxis_title="Fréquence",
                        height=300
                    )
                    
                    st.plotly_chart(fig_error, use_container_width=True)
                    
                elif model_type in ["Classification logistique", "Arbre de décision"]:
                    # Simuler une matrice de confusion
                    conf_matrix = np.array([[42, 8], [6, 44]])
                    
                    fig = px.imshow(
                        conf_matrix,
                        text_auto=True,
                        labels=dict(x="Prédiction", y="Réalité"),
                        x=["Négatif", "Positif"],
                        y=["Négatif", "Positif"],
                        color_continuous_scale="Blues"
                    )
                    
                    fig.update_layout(
                        title="Matrice de confusion",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Simuler une courbe ROC
                    fpr = np.linspace(0, 1, 100)
                    tpr = np.sqrt(fpr)  # Courbe ROC simplifié (mieux que aléatoire)
                    
                    fig_roc = go.Figure()
                    fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name='Modèle', line=dict(color='blue', width=3)))
                    fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Aléatoire', line=dict(color='red', dash='dash')))
                    
                    fig_roc.update_layout(
                        title="Courbe ROC",
                        xaxis_title="Taux de faux positifs",
                        yaxis_title="Taux de vrais positifs",
                        height=400,
                        xaxis=dict(range=[0, 1]),
                        yaxis=dict(range=[0, 1])
                    )
                    
                    st.plotly_chart(fig_roc, use_container_width=True)
                    
                    # Simuler l'importance des caractéristiques
                    feature_importance = np.random.uniform(0, 1, len(feature_cols))
                    feature_imp_df = pd.DataFrame({
                        'Caractéristique': feature_cols,
                        'Importance': feature_importance
                    }).sort_values('Importance', ascending=False)
                    
                    fig_imp = px.bar(
                        feature_imp_df,
                        x='Importance',
                        y='Caractéristique',
                        orientation='h',
                        title="Importance des caractéristiques",
                        color='Importance',
                        color_continuous_scale="Blues"
                    )
                    
                    st.plotly_chart(fig_imp, use_container_width=True)
                
                # Section: Faire une prédiction avec le modèle
                st.markdown("""
                <div style="background-color:#f8f9fa; padding:10px; border-radius:10px; margin:20px 0 10px 0;">
                    <h3 style="color:#1E3A8A; margin:0;">🔮 Faire une prédiction</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Création d'un formulaire pour les prédictions
                predict_col1, predict_col2 = st.columns(2)
                
                prediction_inputs = {}
                
                with predict_col1:
                    st.markdown("#### Entrez les valeurs des caractéristiques")
                    
                    # Pour chaque caractéristique sélectionnée, créer un champ d'entrée approprié
                    for feature in feature_cols[:len(feature_cols)//2 + len(feature_cols)%2]:
                        if feature in df.columns:
                            if pd.api.types.is_numeric_dtype(df[feature].dtype):
                                # Pour les caractéristiques numériques
                                min_val = float(df[feature].min())
                                max_val = float(df[feature].max())
                                default_val = float(df[feature].mean())
                                
                                prediction_inputs[feature] = st.number_input(
                                    f"{feature}",
                                    min_value=min_val,
                                    max_value=max_val,
                                    value=default_val,
                                    format="%.2f"
                                )
                            else:
                                # Pour les caractéristiques catégorielles
                                options = df[feature].unique().tolist()
                                prediction_inputs[feature] = st.selectbox(
                                    f"{feature}",
                                    options=options
                                )
                
                with predict_col2:
                    if len(feature_cols) > 1:
                        st.markdown("#### Entrez les valeurs des caractéristiques (suite)")
                        
                        # Continuer avec les caractéristiques restantes
                        for feature in feature_cols[len(feature_cols)//2 + len(feature_cols)%2:]:
                            if feature in df.columns:
                                if pd.api.types.is_numeric_dtype(df[feature].dtype):
                                    # Pour les caractéristiques numériques
                                    min_val = float(df[feature].min())
                                    max_val = float(df[feature].max())
                                    default_val = float(df[feature].mean())
                                    
                                    prediction_inputs[feature] = st.number_input(
                                        f"{feature}",
                                        min_value=min_val,
                                        max_value=max_val,
                                        value=default_val,
                                        format="%.2f"
                                    )
                                else:
                                    # Pour les caractéristiques catégorielles
                                    options = df[feature].unique().tolist()
                                    prediction_inputs[feature] = st.selectbox(
                                        f"{feature}",
                                        options=options
                                    )
                
                # Bouton pour effectuer la prédiction
                if st.button("🔮 Prédire", use_container_width=True):
                    with st.spinner("Calcul de la prédiction en cours..."):
                        time.sleep(1)  # Simuler le temps de calcul
                        
                        # Simulation d'une prédiction (dans une application réelle, utiliser le modèle entraîné)
                        if model_type == "Régression linéaire":
                            prediction_value = np.random.normal(df[target_col].mean(), df[target_col].std() / 3, 1)[0]
                            
                            st.success(f"**Prédiction**: {prediction_value:.2f}")
                            
                            # Afficher où se situe la prédiction dans la distribution des valeurs
                            fig_dist = go.Figure()
                            fig_dist.add_trace(go.Histogram(x=df[target_col], name="Distribution", marker_color="blue", opacity=0.7))
                            fig_dist.add_trace(go.Scatter(x=[prediction_value, prediction_value], y=[0, df[target_col].value_counts().max() / 2],
                                            mode="lines", name="Prédiction", line=dict(color="red", width=3, dash="dash")))
                            
                            fig_dist.update_layout(
                                title=f"Positionnement de la prédiction ({prediction_value:.2f})",
                                xaxis_title=target_col,
                                yaxis_title="Fréquence",
                                height=300
                            )
                            
                            st.plotly_chart(fig_dist, use_container_width=True)
                            
                        else:  # Pour les modèles de classification
                            # Simulation d'une classification avec probabilités
                            classes = ["Classe A", "Classe B"] if len(df[target_col].unique()) <= 2 else ["Classe A", "Classe B", "Classe C"]
                            probs = np.random.dirichlet(np.ones(len(classes)), size=1)[0]
                            predicted_class = classes[np.argmax(probs)]
                            
                            st.success(f"**Classe prédite**: {predicted_class}")
                            
                            # Afficher les probabilités de chaque classe
                            fig_probs = go.Figure()
                            fig_probs.add_trace(go.Bar(
                                x=classes,
                                y=probs,
                                marker_color=["blue" if i == np.argmax(probs) else "lightblue" for i in range(len(classes))],
                                text=[f"{p:.1%}" for p in probs],
                                textposition="auto"
                            ))
                            
                            fig_probs.update_layout(
                                title="Probabilités par classe",
                                xaxis_title="Classe",
                                yaxis_title="Probabilité",
                                height=300,
                                yaxis=dict(range=[0, 1])
                            )
                            
                            st.plotly_chart(fig_probs, use_container_width=True)
                
                # Section: Exportation du modèle (simulée)
                st.markdown("""
                <div style="background-color:#f8f9fa; padding:10px; border-radius:10px; margin:20px 0 10px 0;">
                    <h3 style="color:#1E3A8A; margin:0;">💾 Exporter le modèle</h3>
                </div>
                """, unsafe_allow_html=True)
                
                export_options = st.radio("Format d'exportation:", ["Fichier pickle (.pkl)", "ONNX (.onnx)", "TensorFlow SavedModel (.tf)"], horizontal=True)
                
                if st.button("📥 Télécharger le modèle"):
                    # Simuler un téléchargement
                    st.success("Le modèle a été préparé pour le téléchargement!")
                    
                    st.download_button(
                        label="Télécharger le modèle",
                        data="Ceci est un modèle fictif",  # Dans une application réelle, ce serait le modèle sérialisé
                        file_name=f"modele_{model_type.lower().replace(' ', '_')}.pkl",
                        mime="application/octet-stream"
                    )
    else:
        st.info("Aucune donnée chargée. Veuillez charger un fichier depuis la page d'accueil.")