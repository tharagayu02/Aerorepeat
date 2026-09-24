# ✈️ AeroRepeat

AeroRepeat is a historical aircraft-maintenance analysis application that uses historical maintenance records to identify similar maintenance events, related components, and historical part-number associations.

## Features

- Historical maintenance record search
- TF-IDF text similarity
- Maintenance problem matching
- Component identification
- Historical part-number association
- Windshield/window heat problem analysis
- Replacement-event analysis
- Aircraft-model filtering
- Interactive Streamlit dashboard
- R-based statistical analysis

## Project Structure

```text
AeroRepeat/
│
├── app.py
├── aerorepeat.py
├── clean.py
│
├── data/
│   ├── SDR-2026.csv
│   └── cleaned_aircraft_maintenance.csv
│
├── r/
│   └── R statistical analysis files
│
├── README.md
├── requirements.txt
└── .gitignore