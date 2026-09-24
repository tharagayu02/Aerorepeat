import base64
from pathlib import Path

import pandas as pd
import streamlit as st

from aerorepeat import (
    load_dataset,
    build_model,
    analyze_description,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AeroRepeat",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DATASET_PATH = DATA_DIR / "cleaned_aircraft_maintenance.csv"
BACKGROUND_IMAGE = DATA_DIR / "aircraft_background.jpg"

BASE_DIR = Path(__file__).resolve().parent

GRAPH_1 = BASE_DIR / "r" / "output" / "top_part_names.png"
GRAPH_2 = BASE_DIR / "r" / "output" / "top_part_numbers.png"
# ============================================================
# AIRCRAFT BACKGROUND
# ============================================================

def get_background_css():
    """
    Returns CSS for the application background.
    """

    if not BACKGROUND_IMAGE.exists():
        return """
        .stApp {
            background:
                linear-gradient(
                    135deg,
                    #071a2e 0%,
                    #12395a 100%
                );
        }
        """

    try:
        image_bytes = BACKGROUND_IMAGE.read_bytes()

        encoded_image = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        return f"""
        .stApp {{
            background-image:
                linear-gradient(
                    rgba(5, 18, 35, 0.78),
                    rgba(5, 18, 35, 0.86)
                ),
                url("data:image/jpeg;base64,{encoded_image}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        """

    except Exception:
        return """
        .stApp {
            background:
                linear-gradient(
                    135deg,
                    #071a2e 0%,
                    #12395a 100%
                );
        }
        """


# ============================================================
# APPLICATION STYLING
# ============================================================

background_css = get_background_css()

st.markdown(
    f"""
    <style>
    
    /* Aircraft model selectbox */
div[data-baseweb="select"] > div {{
    background-color: rgba(255, 255, 255, 0.95) !important;
    color: #111827 !important;
    border-radius: 8px !important;
}}

div[data-baseweb="select"] span {{
    color: #111827 !important;
}}

div[data-baseweb="select"] input {{
    color: #111827 !important;
}}

/* Dropdown options */
ul[role="listbox"] {{
    background-color: #ffffff !important;
}}

ul[role="listbox"] li {{
    color: #111827 !important;
    background-color: #ffffff !important;
}}

ul[role="listbox"] li:hover {{
    background-color: #e5e7eb !important;
}}
    
    {background_css}

    /* Main application text */
    .stApp,
    .stApp p,
    .stApp span,
    .stApp label,
    .stApp div {{
        color: #ffffff;
    }}

    /* Main headings */
    h1, h2, h3, h4, h5, h6 {{
        color: #ffffff !important;
    }}

    /* Header */
    header[data-testid="stHeader"] {{
        background: transparent;
    }}

    /* Main container */
    .block-container {{
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background:
            linear-gradient(
                180deg,
                rgba(5, 20, 36, 0.98),
                rgba(8, 34, 56, 0.98)
            );
    }}

    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {{
        color: #ffffff !important;
    }}

    /* Sidebar select box */
    section[data-testid="stSidebar"] div[data-baseweb="select"] {{
        background: rgba(255,255,255,0.12);
    }}

    /* Metrics */
    div[data-testid="stMetric"] {{
        background: rgba(10, 30, 50, 0.90);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 14px;
        padding: 0.9rem;
        box-shadow:
            0 8px 22px rgba(0, 0, 0, 0.25);
    }}

    div[data-testid="stMetricLabel"] {{
        color: #ffffff !important;
        font-weight: 700 !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: #ffffff !important;
        font-weight: 800 !important;
    }}

    div[data-testid="stMetricDelta"] {{
        color: #ffffff !important;
    }}

    /* Text input */
    textarea {{
        background-color: rgba(255,255,255,0.96) !important;
        color: #111827 !important;
        border-radius: 12px !important;
    }}

    textarea::placeholder {{
        color: #6b7280 !important;
    }}

    /* Select boxes */
    div[data-baseweb="select"] {{
        color: #ffffff !important;
    }}

    div[data-baseweb="select"] > div {{
        background-color: rgba(255,255,255,0.12) !important;
        color: #ffffff !important;
        border-color: rgba(255,255,255,0.30) !important;
    }}

    /* Buttons */
    .stButton > button {{
        border-radius: 12px;
        min-height: 3rem;
        font-weight: 800;
        color: #ffffff !important;
    }}

    /* Dataframes */
    div[data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
        box-shadow:
            0 8px 22px rgba(0, 0, 0, 0.25);
    }}

    /* Expanders */
    div[data-testid="stExpander"] {{
        background: rgba(10, 30, 50, 0.90);
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.25);
    }}

    div[data-testid="stExpander"] * {{
        color: #ffffff !important;
    }}

    /* Info / warning messages */
    div[data-testid="stAlert"] {{
        color: #ffffff !important;
    }}

    div[data-testid="stAlert"] * {{
        color: #ffffff !important;
    }}

    /* Captions */
    .stCaption,
    [data-testid="stCaptionContainer"] {{
        color: #ffffff !important;
    }}

    /* Slider */
    div[data-testid="stSlider"] label {{
        color: #ffffff !important;
    }}

    /* Progress bar */
    div[data-testid="stProgress"] {{
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }}
     

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================

st.title("✈️ AeroRepeat")

st.subheader(
    "Historical Aircraft-Maintenance Similarity Analysis"
)

st.caption(
    "TF-IDF similarity • Historical component evidence • "
    "Part-number evidence • Repeat-event analysis"
)


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data(show_spinner="Loading maintenance dataset...")
def get_dataset():
    return load_dataset()


# ============================================================
# BUILD MODEL
# ============================================================

@st.cache_resource(show_spinner="Building TF-IDF model...")
def get_model():
    dataframe = get_dataset()
    return build_model(dataframe)


# ============================================================
# INITIALIZE DATA
# ============================================================

try:

    df = get_dataset()

    vectorizer, matrix = get_model()

except Exception as error:

    st.error("AeroRepeat could not load the dataset.")

    st.code(
        str(error),
        language="text",
    )

    st.info("Required dataset:")

    st.code(
        str(DATASET_PATH),
        language="text",
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Analysis Settings")

    st.caption(
        "Configure the historical search."
    )

    st.divider()

    # --------------------------------------------------------
    # AIRCRAFT MODEL
    # --------------------------------------------------------

    aircraft_options = sorted(
        [
            str(value)
            for value in df["AircraftModel"].unique()
            if str(value).strip()
        ]
    )

    aircraft_selection = st.selectbox(
        "Aircraft Model",
        ["ALL AIRCRAFT"] + aircraft_options,
    )

    if aircraft_selection == "ALL AIRCRAFT":
        selected_aircraft = None
    else:
        selected_aircraft = aircraft_selection

    # --------------------------------------------------------
    # TF-IDF THRESHOLD
    # --------------------------------------------------------

    similarity_threshold = st.slider(
        "TF-IDF similarity threshold",
        min_value=0.10,
        max_value=0.60,
        value=0.25,
        step=0.05,
        format="%.2f",
    )

    st.divider()

    # --------------------------------------------------------
    # DATASET INFORMATION
    # --------------------------------------------------------

    st.header("📊 Dataset")

    st.metric(
        "Maintenance Records",
        f"{len(df):,}",
    )

    st.metric(
        "Aircraft Models",
        f"{df['AircraftModel'].nunique():,}",
    )

    st.metric(
        "Part Names",
        f"{df['PartName'].nunique():,}",
    )

    st.divider()

    st.caption(
        "Historical analytics only. Verify maintenance "
        "decisions against approved maintenance documentation."
    )


# ============================================================
# MAINTENANCE DESCRIPTION
# ============================================================

st.header("📝 Maintenance Problem Description")

default_description = (
    "LEFT WINDSHIELD HEAT CONTROL UNIT FAULTY. "
    "WINDSHIELD HEAT FAIL MESSAGE DISPLAYED DURING FLIGHT. "
    "REMOVED AND REPLACED THE WINDSHIELD HEAT CONTROL UNIT. "
    "PERFORMED OPERATIONAL CHECK AND SYSTEM OPERATED "
    "SATISFACTORILY."
)

description = st.text_area(
    "Enter maintenance discrepancy",
    value=default_description,
    height=180,
    placeholder=(
        "Example: WINDSHIELD HEAT FAIL MESSAGE..."
    ),
)

analyze_button = st.button(
    "🔍 Analyze Maintenance Problem",
    type="primary",
    use_container_width=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None


# ============================================================
# RUN ANALYSIS
# ============================================================

if analyze_button:

    if not description.strip():

        st.warning(
            "Please enter a maintenance description."
        )

        st.stop()

    with st.spinner(
        "Analyzing historical maintenance records..."
    ):

        try:

            result = analyze_description(
                description=description,
                df=df,
                vectorizer=vectorizer,
                matrix=matrix,
                aircraft_model=selected_aircraft,
            )

            st.session_state.analysis_result = result

        except Exception as error:

            st.error("Analysis failed.")

            st.exception(error)

            st.stop()


# ============================================================
# WAIT FOR ANALYSIS
# ============================================================

if st.session_state.analysis_result is None:

    st.info(
        "Enter a maintenance description and click "
        "**Analyze Maintenance Problem**."
    )

    st.stop()


# ============================================================
# RESULT
# ============================================================

result = st.session_state.analysis_result


# ============================================================
# RESULT VALUES
# ============================================================

component = result.get(
    "component",
    "UNKNOWN",
)

part_number = result.get(
    "part_number",
    "UNKNOWN",
)

best_tfidf = float(
    result.get(
        "best_tfidf",
        0.0,
    )
)

best_combined = float(
    result.get(
        "best_combined",
        0.0,
    )
)

problem_occurrences = int(
    result.get(
        "problem_occurrences",
        0,
    )
)

replacement_occurrences = int(
    result.get(
        "replacement_occurrences",
        0,
    )
)

all_matches = result.get(
    "matches",
    pd.DataFrame(),
)

relevant_matches = result.get(
    "relevant_matches",
    pd.DataFrame(),
)


# ============================================================
# DISPLAY VALUES
# ============================================================

historical_match_score = max(
    0.0,
    min(
        1.0,
        best_combined,
    ),
)

tfidf_percentage = best_tfidf * 100

combined_percentage = historical_match_score * 100


# ============================================================
# THRESHOLD COUNT
# ============================================================

if not all_matches.empty:

    records_above_threshold = int(
        (
            all_matches["TFIDF"]
            >= similarity_threshold
        ).sum()
    )

else:

    records_above_threshold = 0


# ============================================================
# PART NUMBER OCCURRENCE
# ============================================================

if (
    part_number != "UNKNOWN"
    and not relevant_matches.empty
):

    pn_mask = (
        relevant_matches["PartNumber"]
        .astype(str)
        .str.upper()
        .str.strip()
        ==
        str(part_number)
        .upper()
        .strip()
    )

    part_number_occurrences = int(
        pn_mask.sum()
    )

else:

    part_number_occurrences = 0


# ============================================================
# PART NUMBER SUMMARY
# ============================================================

if not relevant_matches.empty:

    pn_table = relevant_matches[
        [
            "PartName",
            "PartNumber",
            "AircraftModel",
            "TFIDF",
            "CombinedScore",
        ]
    ].copy()

    pn_summary = (
        pn_table
        .groupby(
            [
                "PartName",
                "PartNumber",
            ],
            dropna=False,
        )
        .agg(
            Records=(
                "PartNumber",
                "size",
            ),
            Best_TFIDF=(
                "TFIDF",
                "max",
            ),
            Best_Combined=(
                "CombinedScore",
                "max",
            ),
        )
        .reset_index()
    )

    pn_summary["Best TF-IDF (%)"] = (
        pn_summary["Best_TFIDF"] * 100
    ).round(2)

    pn_summary["Best Combined (%)"] = (
        pn_summary["Best_Combined"] * 100
    ).round(2)

    pn_summary = (
        pn_summary
        .sort_values(
            [
                "Best_Combined",
                "Records",
            ],
            ascending=False,
        )
    )

else:

    pn_summary = pd.DataFrame()


# ============================================================
# PREDICTION SUMMARY
# ============================================================

st.header("🎯 Prediction Summary")

col1, col2, col3 = st.columns(3)

with col1:

    st.subheader("Predicted Component")

    st.metric(
        "Component",
        str(component),
    )

    st.caption(
        "Historical component association"
    )


with col2:

    st.subheader("Historical Part Number")

    st.metric(
        "Part Number",
        str(part_number),
    )

    st.caption(
        "Supported by relevant historical records"
    )


with col3:

    st.subheader("Historical Match Score")

    st.metric(
        "Match Score",
        f"{combined_percentage:.2f}%",
    )

    st.caption(
        "Heuristic historical ranking score"
    )


st.info(
    "The Historical Match Score measures how strongly the "
    "maintenance description matches historical records "
    "using the application's similarity and domain-matching "
    "logic. It is NOT a probability of failure and should "
    "not be interpreted as prediction accuracy."
)


# ============================================================
# PROBLEM OCCURRENCE
# ============================================================

st.header("🔁 Problem Occurrence")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Related Problem Records",
        f"{problem_occurrences:,}",
    )

with col2:

    st.metric(
        "Replacement Records",
        f"{replacement_occurrences:,}",
    )

with col3:

    if part_number != "UNKNOWN":
        occurrence_label = f"{part_number} Records"
    else:
        occurrence_label = "Predicted PN Records"

    st.metric(
        occurrence_label,
        f"{part_number_occurrences:,}",
    )

with col4:

    st.metric(
        "TF-IDF ≥ Threshold",
        f"{records_above_threshold:,}",
    )


# ============================================================
# SIMILARITY ANALYSIS
# ============================================================

st.header("📊 Similarity Analysis")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Best TF-IDF",
        f"{tfidf_percentage:.2f}%",
    )

with col2:

    st.metric(
        "Best Combined Match",
        f"{combined_percentage:.2f}%",
    )

with col3:

    st.metric(
        "Similarity Threshold",
        f"{similarity_threshold:.2f}",
    )

st.progress(
    min(
        max(
            best_tfidf,
            0.0,
        ),
        1.0,
    )
)

st.caption(
    "The progress bar represents the best TF-IDF similarity "
    "found in the historical search."
)


# ============================================================
# WHY AEROREPEAT
# ============================================================

st.header("🧠 Why AeroRepeat Made This Prediction")

with st.container(border=True):

    st.subheader(
        "Historical-record based analysis"
    )

    st.write(
        "AeroRepeat compares the entered maintenance "
        "description against individual historical "
        "maintenance records."
    )

    st.write(
        "The analysis considers:"
    )

    st.markdown(
        """
        - TF-IDF text similarity
        - Windshield/window heat terminology
        - Controller/control-unit terminology
        - Failure and inoperative terminology
        - Replacement actions
        - Aircraft-model context when selected
        - Penalties for unrelated maintenance domains
        """
    )

    st.write(
        "The part number is associated with historical "
        "records supporting the predicted component rather "
        "than being selected simply because it is common "
        "within the component category."
    )


# ============================================================
# RELEVANT HISTORICAL PART NUMBERS
# ============================================================

st.header("🔩 Relevant Historical Part Numbers")

if pn_summary.empty:

    st.info(
        "No sufficiently relevant historical part-number "
        "evidence was identified."
    )

else:

    display_pn = pn_summary[
        [
            "PartName",
            "PartNumber",
            "Records",
            "Best TF-IDF (%)",
            "Best Combined (%)",
        ]
    ].copy()

    display_pn = display_pn.rename(
        columns={
            "PartName": "Part Name",
            "PartNumber": "Part Number",
        }
    )

    st.dataframe(
        display_pn,
        use_container_width=True,
        hide_index=True,
        height=350,
    )


# ============================================================
# TOP HISTORICAL MATCHES
# ============================================================

st.header("📚 Top Historical Matches")

if all_matches.empty:

    st.info(
        "No historical matches were found."
    )

else:

    top_matches = (
        all_matches
        .head(10)
        .copy()
    )

    top_matches["TF-IDF (%)"] = (
        top_matches["TFIDF"] * 100
    ).round(2)

    if "SemanticBonus" in top_matches.columns:

        top_matches["Semantic Bonus (%)"] = (
            top_matches["SemanticBonus"] * 100
        ).round(2)

    else:

        top_matches["Semantic Bonus (%)"] = 0.0

    top_matches["Combined Score (%)"] = (
        top_matches["CombinedScore"] * 100
    ).round(2)

    top_matches = top_matches[
        [
            "AircraftModel",
            "PartName",
            "PartNumber",
            "TF-IDF (%)",
            "Semantic Bonus (%)",
            "Combined Score (%)",
            "Discrepancy",
        ]
    ]

    top_matches = top_matches.rename(
        columns={
            "AircraftModel": "Aircraft Model",
            "PartName": "Part Name",
            "PartNumber": "Part Number",
        }
    )

    st.dataframe(
        top_matches,
        use_container_width=True,
        hide_index=True,
        height=430,
    )


# ============================================================
# EVIDENCE
# ============================================================

st.header("🧾 Evidence Supporting the Prediction")

if relevant_matches.empty:

    st.info(
        "No directly relevant historical evidence was identified."
    )

else:

    evidence = (
        relevant_matches
        .head(10)
        .copy()
    )

    evidence["TF-IDF (%)"] = (
        evidence["TFIDF"] * 100
    ).round(2)

    evidence["Combined (%)"] = (
        evidence["CombinedScore"] * 100
    ).round(2)

    evidence = evidence[
        [
            "AircraftModel",
            "PartName",
            "PartNumber",
            "TF-IDF (%)",
            "Combined (%)",
            "Discrepancy",
        ]
    ]

    evidence = evidence.rename(
        columns={
            "AircraftModel": "Aircraft Model",
            "PartName": "Part Name",
            "PartNumber": "Part Number",
        }
    )

    st.dataframe(
        evidence,
        use_container_width=True,
        hide_index=True,
        height=400,
    )


# ============================================================
# AIRCRAFT CONTEXT
# ============================================================

if selected_aircraft:

    st.header("✈️ Aircraft Context")

    aircraft_records = df[
        df["AircraftModel"]
        .astype(str)
        .str.upper()
        .str.strip()
        ==
        selected_aircraft.upper().strip()
    ]

    st.info(
        f"Aircraft model **{selected_aircraft}** is selected. "
        f"There are **{len(aircraft_records):,}** historical "
        f"records available for this model."
    )

else:

    st.header("🌐 Aircraft Context")

    st.info(
        "ALL AIRCRAFT is selected. Historical evidence can "
        "therefore come from multiple aircraft models. "
        "A historical part number should not be treated as "
        "aircraft-configuration specific without verification."
    )


# ============================================================
# ANALYZED DESCRIPTION
# ============================================================

with st.expander(
    "📝 View analyzed maintenance description"
):

    st.write(description)


# ============================================================
# TECHNICAL DETAILS
# ============================================================

with st.expander(
    "⚙️ Technical analysis details"
):

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"Dataset records: {len(df):,}"
        )

        st.write(
            f"Aircraft models: "
            f"{df['AircraftModel'].nunique():,}"
        )

        st.write(
            f"Part names: "
            f"{df['PartName'].nunique():,}"
        )

    with col2:

        st.write(
            "TF-IDF vectorizer: Word and bigram features"
        )

        st.write(
            "Maximum TF-IDF features: 50,000"
        )

        st.write(
            f"Current threshold: "
            f"{similarity_threshold:.2f}"
        )
    st.markdown("---")

st.header("📊 Statistical Analysis")

st.write(
    "Historical statistical analysis of the AeroRepeat "
    "maintenance dataset."
)

# ----------------------------------------
# Graph 1
# ----------------------------------------

if GRAPH_1.exists():

    st.subheader(
        "Top 10 Part Names by Historical Records"
    )

    st.image(
        str(GRAPH_1),
        use_container_width=True
    )

else:

    st.warning(
        "Top part names graph was not found."
    )


# ----------------------------------------
# Graph 2
# ----------------------------------------

if GRAPH_2.exists():

    st.subheader(
        "Top 10 Part Numbers by Replacement Records"
    )

    st.image(
        str(GRAPH_2),
        use_container_width=True
    )

else:

    st.warning(
        "Top part numbers graph was not found."
    )

# ============================================================
# DISCLAIMER
# ============================================================

st.header(
    "⚠️ AeroRepeat — Historical Analytics Only"
)

st.warning(
    "AeroRepeat identifies patterns in the supplied historical "
    "aircraft-maintenance dataset. Part-number applicability "
    "and maintenance action must be verified against the "
    "applicable AMM, IPC, FIM, aircraft configuration, "
    "engineering instructions and other approved maintenance "
    "data before maintenance action."
)