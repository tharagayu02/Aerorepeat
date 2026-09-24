import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "cleaned_aircraft_maintenance.csv"


# ============================================================
# LOAD DATA
# ============================================================

def load_dataset():

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    required_columns = [
        "AircraftModel",
        "PartName",
        "PartNumber",
        "PartCondition",
        "Discrepancy",
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    df = df.copy()

    for col in required_columns:
        df[col] = (
            df[col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    df = df[
        df["Discrepancy"] != ""
    ].copy()

    df["AircraftModel"] = (
        df["AircraftModel"]
        .str.upper()
        .str.strip()
    )

    df["PartName"] = (
        df["PartName"]
        .str.upper()
        .str.strip()
    )

    df["PartNumber"] = (
        df["PartNumber"]
        .str.upper()
        .str.strip()
    )

    df["PartCondition"] = (
        df["PartCondition"]
        .str.upper()
        .str.strip()
    )

    df["text"] = (
        df["Discrepancy"]
        .str.lower()
        .str.replace(
            r"[^a-z0-9\s]",
            " ",
            regex=True
        )
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
        .str.strip()
    )

    df = df[
        df["text"] != ""
    ].reset_index(drop=True)

    return df


# ============================================================
# TF-IDF MODEL
# ============================================================

def build_model(df):

    vectorizer = TfidfVectorizer(
        max_features=50000,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
        sublinear_tf=True
    )

    matrix = vectorizer.fit_transform(
        df["text"]
    )

    return vectorizer, matrix


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(text):

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# DOMAIN DETECTION
# ============================================================

def detect_domain(text):

    t = str(text).upper()

    domains = []

    # --------------------------------------------------------
    # WEATHER RADAR
    # --------------------------------------------------------

    radar_terms = [
        "WEATHER RADAR",
        "WX RADAR",
        "WXR",
        "RADAR SYSTEM",
        "RADAR CONTROL UNIT",
        "WEATHER RADAR CONTROL UNIT",
    ]

    if any(term in t for term in radar_terms):
        domains.append("WEATHER_RADAR")

    # --------------------------------------------------------
    # WINDSHIELD / WINDOW HEAT
    # --------------------------------------------------------

    windshield_terms = [
        "WINDSHIELD",
        "WINDSCREEN",
        "WINDOW",
    ]

    heat_terms = [
        "HEAT",
        "HEATING",
        "HEATER",
    ]

    if (
        any(term in t for term in windshield_terms)
        and any(term in t for term in heat_terms)
    ):
        domains.append("WINDSHIELD_HEAT")

    # --------------------------------------------------------
    # BRAKE
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "BRAKE",
            "BRAKES",
            "BRAKING",
        ]
    ):
        domains.append("BRAKE")

    # --------------------------------------------------------
    # LANDING GEAR
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "LANDING GEAR",
            "NOSE GEAR",
            "MAIN GEAR",
            "GEAR DOOR",
        ]
    ):
        domains.append("LANDING_GEAR")

    # --------------------------------------------------------
    # FLAP
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "FLAP",
            "FLAPS",
            "SLAT",
            "SLATS",
        ]
    ):
        domains.append("FLIGHT_CONTROL_FLAP")

    # --------------------------------------------------------
    # SPOILER
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "SPOILER",
            "SPOILERS",
        ]
    ):
        domains.append("SPOILER")

    # --------------------------------------------------------
    # AILERON
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "AILERON",
            "AILERONS",
        ]
    ):
        domains.append("AILERON")

    # --------------------------------------------------------
    # ELEVATOR
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "ELEVATOR",
            "ELEVATORS",
        ]
    ):
        domains.append("ELEVATOR")

    # --------------------------------------------------------
    # RUDDER
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "RUDDER",
            "RUDDERS",
        ]
    ):
        domains.append("RUDDER")

    # --------------------------------------------------------
    # ENGINE
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "ENGINE",
            "ENGINES",
            "ENGINE CONTROL",
            "ENGINE CONTROL UNIT",
        ]
    ):
        domains.append("ENGINE")

    # --------------------------------------------------------
    # APU
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "APU",
            "AUXILIARY POWER UNIT",
        ]
    ):
        domains.append("APU")

    # --------------------------------------------------------
    # FUEL
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "FUEL",
            "FUEL PUMP",
            "FUEL VALVE",
        ]
    ):
        domains.append("FUEL")

    # --------------------------------------------------------
    # HYDRAULIC
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "HYDRAULIC",
            "HYDRAULICS",
        ]
    ):
        domains.append("HYDRAULIC")

    # --------------------------------------------------------
    # ELECTRICAL
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "ELECTRICAL",
            "ELECTRIC",
            "GENERATOR",
            "GEN",
        ]
    ):
        domains.append("ELECTRICAL")

    # --------------------------------------------------------
    # FLIGHT CONTROL
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "FLIGHT CONTROL",
            "FLIGHT CONTROLS",
            "CONTROL SURFACE",
            "CONTROL SURFACES",
        ]
    ):
        domains.append("FLIGHT_CONTROL")

    # --------------------------------------------------------
    # AVIONICS
    # --------------------------------------------------------

    if any(
        term in t
        for term in [
            "AVIONICS",
            "DISPLAY UNIT",
            "DISPLAY",
            "COMPUTER",
            "CONTROL UNIT",
            "CONTROLLER",
        ]
    ):
        domains.append("AVIONICS")

    return set(domains)


# ============================================================
# SPECIFIC DOMAIN TESTS
# ============================================================

def is_windshield_heat_problem(text):

    return "WINDSHIELD_HEAT" in detect_domain(text)


def is_weather_radar_problem(text):

    return "WEATHER_RADAR" in detect_domain(text)


# ============================================================
# DOMAIN COMPATIBILITY
# ============================================================

def domain_score(query, historical):

    query_domains = detect_domain(query)
    historical_domains = detect_domain(historical)

    if not query_domains:
        return 0.0

    if not historical_domains:
        return -0.05

    overlap = query_domains.intersection(
        historical_domains
    )

    if overlap:
        return 0.15

    # Strong penalty for clearly different known domains.
    return -0.20


# ============================================================
# SEMANTIC BONUS
# ============================================================

def semantic_bonus(query, historical):

    q = str(query).upper()
    h = str(historical).upper()

    bonus = 0.0

    # --------------------------------------------------------
    # DOMAIN MATCH
    # --------------------------------------------------------

    bonus += domain_score(q, h)

    # --------------------------------------------------------
    # WEATHER RADAR
    # --------------------------------------------------------

    q_radar = any(
        x in q
        for x in [
            "WEATHER RADAR",
            "WX RADAR",
            "WXR",
            "RADAR SYSTEM",
            "RADAR CONTROL UNIT",
        ]
    )

    h_radar = any(
        x in h
        for x in [
            "WEATHER RADAR",
            "WX RADAR",
            "WXR",
            "RADAR SYSTEM",
            "RADAR CONTROL UNIT",
        ]
    )

    if q_radar and h_radar:
        bonus += 0.15

    # --------------------------------------------------------
    # WINDSHIELD / WINDOW HEAT
    # --------------------------------------------------------

    q_window_heat = (
        any(
            x in q
            for x in [
                "WINDSHIELD",
                "WINDSCREEN",
                "WINDOW",
            ]
        )
        and
        any(
            x in q
            for x in [
                "HEAT",
                "HEATING",
                "HEATER",
            ]
        )
    )

    h_window_heat = (
        any(
            x in h
            for x in [
                "WINDSHIELD",
                "WINDSCREEN",
                "WINDOW",
            ]
        )
        and
        any(
            x in h
            for x in [
                "HEAT",
                "HEATING",
                "HEATER",
            ]
        )
    )

    if q_window_heat and h_window_heat:
        bonus += 0.10

    # --------------------------------------------------------
    # CONTROL UNIT
    # --------------------------------------------------------

    q_control = any(
        x in q
        for x in [
            "CONTROL UNIT",
            "CONTROLLER",
        ]
    )

    h_control = any(
        x in h
        for x in [
            "CONTROL UNIT",
            "CONTROLLER",
        ]
    )

    if q_control and h_control:
        bonus += 0.08

    # --------------------------------------------------------
    # FAILURE TERMS
    # --------------------------------------------------------

    failure_terms = [
        "FAULT",
        "FAULTY",
        "FAIL",
        "FAILED",
        "FAILURE",
        "INOPERATIVE",
        "INOP",
        "MALFUNCTION",
    ]

    if any(x in q for x in failure_terms):
        if any(x in h for x in failure_terms):
            bonus += 0.08

    # --------------------------------------------------------
    # MESSAGE / INDICATION
    # --------------------------------------------------------

    indication_terms = [
        "MESSAGE",
        "FAIL MESSAGE",
        "FAIL INDICATION",
        "WARNING",
        "CAUTION",
        "DISPLAYED",
        "INDICATION",
    ]

    if any(x in q for x in indication_terms):
        if any(x in h for x in indication_terms):
            bonus += 0.04

    # --------------------------------------------------------
    # REPLACEMENT
    # --------------------------------------------------------

    replacement_terms = [
        "REPLACED",
        "REPLACE",
        "REMOVED AND REPLACED",
        "R&R",
        "R/R",
    ]

    if any(x in q for x in replacement_terms):
        if any(x in h for x in replacement_terms):
            bonus += 0.05

    # --------------------------------------------------------
    # OPERATIONAL TEST
    # --------------------------------------------------------

    test_terms = [
        "OPERATIONAL TEST",
        "OPERATIONAL CHECK",
        "FUNCTIONAL TEST",
        "FUNCTIONAL CHECK",
        "SYSTEM OPERATED SATISFACTORILY",
        "SYSTEM OPERATED",
    ]

    if any(x in q for x in test_terms):
        if any(x in h for x in test_terms):
            bonus += 0.04

    return bonus


# ============================================================
# FIND SIMILAR RECORDS
# ============================================================

def find_similar_reports(
    description,
    df,
    vectorizer,
    matrix,
    top_k=50,
    aircraft_model=None
):

    query = normalize_text(description)

    query_vector = vectorizer.transform(
        [query]
    )

    similarities = cosine_similarity(
        query_vector,
        matrix
    )[0]

    results = df.copy()

    results["TFIDF"] = similarities

    results["SemanticBonus"] = results[
        "Discrepancy"
    ].apply(
        lambda x: semantic_bonus(
            description,
            x
        )
    )

    results["CombinedScore"] = (
        results["TFIDF"]
        + results["SemanticBonus"]
    )

    results["CombinedScore"] = (
        results["CombinedScore"]
        .clip(lower=0)
    )

    # --------------------------------------------------------
    # AIRCRAFT MATCH
    # --------------------------------------------------------

    if aircraft_model:
        model = str(
            aircraft_model
        ).upper().strip()

        results["AircraftMatch"] = (
            results["AircraftModel"] == model
        )

        results.loc[
            results["AircraftMatch"],
            "CombinedScore"
        ] += 0.05

    else:
        results["AircraftMatch"] = False

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    results = results.sort_values(
        [
            "CombinedScore",
            "TFIDF"
        ],
        ascending=False
    ).reset_index(drop=True)

    return results.head(top_k)


# ============================================================
# FIND RELEVANT HISTORICAL RECORDS
# ============================================================

def get_relevant_records(
    description,
    matches
):

    query_domains = detect_domain(
        description
    )

    relevant = matches.copy()

    # --------------------------------------------------------
    # If query has a known domain, prefer records
    # from that same domain.
    # --------------------------------------------------------

    if query_domains:

        domain_mask = relevant[
            "Discrepancy"
        ].apply(
            lambda x:
                bool(
                    query_domains.intersection(
                        detect_domain(x)
                    )
                )
        )

        domain_matches = relevant[
            domain_mask
        ].copy()

        if not domain_matches.empty:
            relevant = domain_matches

    # --------------------------------------------------------
    # Never return unrelated records simply because
    # they share generic words such as "CONTROL UNIT".
    # --------------------------------------------------------

    return relevant.reset_index(drop=True)


# ============================================================
# PREDICT COMPONENT
# ============================================================

def predict_component(
    description,
    df,
    vectorizer,
    matrix,
    aircraft_model=None
):

    # Get a reasonably large candidate pool first.
    matches = find_similar_reports(
        description,
        df,
        vectorizer,
        matrix,
        top_k=100,
        aircraft_model=aircraft_model
    )

    # Then determine which records actually belong to
    # the same maintenance domain.
    relevant_matches = get_relevant_records(
        description,
        matches
    )

    # --------------------------------------------------------
    # FALLBACK
    #
    # If there is no known domain match, use the best
    # TF-IDF/semantic record rather than returning 0%.
    # --------------------------------------------------------

    if relevant_matches.empty:

        relevant_matches = matches.head(10).copy()

    if relevant_matches.empty:

        return {
            "component": "UNKNOWN",
            "part_number": "UNKNOWN",
            "matches": matches,
            "relevant_matches": relevant_matches,
            "best_tfidf": 0.0,
            "best_combined": 0.0,
        }

    # --------------------------------------------------------
    # BEST HISTORICAL RECORD
    # --------------------------------------------------------

    best_row = relevant_matches.iloc[0]

    best_tfidf = float(
        best_row["TFIDF"]
    )

    best_combined = float(
        best_row["CombinedScore"]
    )

    component = str(
        best_row["PartName"]
    ).strip()

    if not component:
        component = "UNKNOWN"

    # --------------------------------------------------------
    # PART NUMBER SELECTION
    #
    # IMPORTANT:
    # PN must come from the relevant historical records,
    # not from every record sharing the same PartName.
    # --------------------------------------------------------

    pn_records = relevant_matches.copy()

    pn_records["PartNumber"] = (
        pn_records["PartNumber"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    pn_records = pn_records[
        pn_records["PartNumber"] != ""
    ].copy()

    if pn_records.empty:

        part_number = "UNKNOWN"

    else:

        # Only positive evidence contributes.
        pn_records["Weight"] = (
            pn_records["CombinedScore"]
            .clip(lower=0)
        )

        pn_support = (
            pn_records
            .groupby("PartNumber")
            .agg(
                Support=("Weight", "sum"),
                BestScore=("CombinedScore", "max"),
                BestTFIDF=("TFIDF", "max"),
                Occurrences=("PartNumber", "size")
            )
            .sort_values(
                [
                    "Support",
                    "BestScore",
                    "BestTFIDF",
                    "Occurrences"
                ],
                ascending=False
            )
        )

        if pn_support.empty:

            part_number = "UNKNOWN"

        else:

            candidate_pn = str(
                pn_support.index[0]
            )

            candidate_score = float(
                pn_support.iloc[0]["BestScore"]
            )

            candidate_tfidf = float(
                pn_support.iloc[0]["BestTFIDF"]
            )

            # Require actual historical similarity.
            if (
                candidate_score >= 0.12
                or candidate_tfidf >= 0.20
            ):
                part_number = candidate_pn
            else:
                part_number = "UNKNOWN"

    return {
        "component": component,
        "part_number": part_number,
        "matches": matches,
        "relevant_matches": relevant_matches,
        "best_tfidf": best_tfidf,
        "best_combined": best_combined,
    }


# ============================================================
# OCCURRENCE ANALYSIS
# ============================================================

def calculate_occurrences(
    description,
    df
):

    # Determine the domain of the user's query.
    query_domains = detect_domain(
        description
    )

    # --------------------------------------------------------
    # Find historical records in the same domain.
    # --------------------------------------------------------

    if query_domains:

        domain_mask = df[
            "Discrepancy"
        ].apply(
            lambda x:
                bool(
                    query_domains.intersection(
                        detect_domain(x)
                    )
                )
        )

        problem_records = df[
            domain_mask
        ].copy()

    else:

        # For unknown domains, do not pretend there is
        # a domain-specific occurrence count.
        problem_records = df.copy()

    # --------------------------------------------------------
    # Replacement records
    # --------------------------------------------------------

    replacement_records = problem_records[
        problem_records["Discrepancy"]
        .str.upper()
        .str.contains(
            r"REPLACED|REPLACE|R/R|R&R|REMOVED AND REPLACED",
            regex=True,
            na=False
        )
    ]

    return {
        "problem_occurrences": len(
            problem_records
        ),
        "replacement_occurrences": len(
            replacement_records
        )
    }


# ============================================================
# COMPLETE ANALYSIS
# ============================================================

def analyze_description(
    description,
    df,
    vectorizer,
    matrix,
    aircraft_model=None
):

    prediction = predict_component(
        description,
        df,
        vectorizer,
        matrix,
        aircraft_model
    )

    occurrences = calculate_occurrences(
        description,
        df
    )

    return {
        **prediction,
        **occurrences
    }