import pandas as pd
from pathlib import Path


# ============================================================
# AEROREPEAT - DATA CLEANING
# ============================================================

# Find the folder where this clean.py file is located
BASE_DIR = Path(__file__).resolve().parent

# Dataset folder
DATA_DIR = BASE_DIR / "data"

# Input and output files
INPUT_FILE = DATA_DIR / "SDR-2026.csv"
OUTPUT_FILE = DATA_DIR / "cleaned_aircraft_maintenance.csv"


# ============================================================
# 1. CHECK INPUT FILE
# ============================================================

print("=" * 70)
print("AEROREPEAT - DATA CLEANING")
print("=" * 70)

print("\nChecking dataset...")

print(f"Input file : {INPUT_FILE}")
print(f"Output file: {OUTPUT_FILE}")


if not INPUT_FILE.exists():

    print("\nERROR!")
    print("The original dataset was not found.")

    print("\nExpected location:")
    print(INPUT_FILE)

    print("\nYour folder should look like:")
    print("aerorepeat/")
    print("    clean.py")
    print("    app.py")
    print("    aerorepeat.py")
    print("    data/")
    print("        SDR-2026.csv")
    print("        cleaned_aircraft_maintenance.csv")

    raise FileNotFoundError(
        f"\nDataset not found: {INPUT_FILE}"
    )


# ============================================================
# 2. LOAD ORIGINAL DATASET
# ============================================================

print("\nLoading original dataset...")

df = pd.read_csv(
    INPUT_FILE,
    low_memory=False
)

print(f"Original rows    : {len(df):,}")
print(f"Original columns : {len(df.columns)}")


# ============================================================
# 3. REQUIRED COLUMNS
# ============================================================

required_columns = [
    "AircraftModel",
    "PartName",
    "PartNumber",
    "PartCondition",
    "Discrepancy"
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    print("\nERROR!")
    print("The following required columns are missing:")

    for column in missing_columns:
        print(f"  - {column}")

    print("\nAvailable columns:")

    for column in df.columns:
        print(f"  - {column}")

    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ============================================================
# 4. KEEP ONLY REQUIRED COLUMNS
# ============================================================

df = df[
    required_columns
].copy()

print("\nRequired columns retained.")


# ============================================================
# 5. HANDLE MISSING VALUES
# ============================================================

print("\nCleaning missing values...")

for column in required_columns:

    df[column] = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )


# ============================================================
# 6. REMOVE EMPTY DISCREPANCIES
# ============================================================

before_empty_removal = len(df)

df = df[
    df["Discrepancy"].str.strip() != ""
].copy()

empty_removed = (
    before_empty_removal
    - len(df)
)

print(
    f"Empty discrepancy records removed: "
    f"{empty_removed:,}"
)


# ============================================================
# 7. NORMALIZE AIRCRAFT MODEL
# ============================================================

df["AircraftModel"] = (
    df["AircraftModel"]
    .str.upper()
    .str.replace(
        r"\s+",
        " ",
        regex=True
    )
    .str.strip()
)


# ============================================================
# 8. NORMALIZE PART NAME
# ============================================================

df["PartName"] = (
    df["PartName"]
    .str.upper()
    .str.replace(
        r"\s+",
        " ",
        regex=True
    )
    .str.strip()
)


# ============================================================
# 9. NORMALIZE PART NUMBER
# ============================================================

df["PartNumber"] = (
    df["PartNumber"]
    .str.upper()
    .str.replace(
        r"\s+",
        " ",
        regex=True
    )
    .str.strip()
)


# ============================================================
# 10. NORMALIZE PART CONDITION
# ============================================================

df["PartCondition"] = (
    df["PartCondition"]
    .str.upper()
    .str.replace(
        r"\s+",
        " ",
        regex=True
    )
    .str.strip()
)


# ============================================================
# 11. NORMALIZE DISCREPANCY
# ============================================================

df["Discrepancy"] = (
    df["Discrepancy"]
    .str.replace(
        r"\s+",
        " ",
        regex=True
    )
    .str.strip()
)


# ============================================================
# 12. REMOVE DUPLICATE RECORDS
# ============================================================

before_duplicates = len(df)

df = (
    df
    .drop_duplicates()
    .reset_index(drop=True)
)

duplicates_removed = (
    before_duplicates
    - len(df)
)

print(
    f"Duplicate records removed: "
    f"{duplicates_removed:,}"
)


# ============================================================
# 13. FINAL EMPTY CHECK
# ============================================================

df = df[
    df["Discrepancy"].str.strip() != ""
].copy()

df = df.reset_index(drop=True)


# ============================================================
# 14. SAVE CLEANED DATASET
# ============================================================

print("\nSaving cleaned dataset...")

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# ============================================================
# 15. VERIFY OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("CLEANING COMPLETED")
print("=" * 70)

print(
    f"Final rows    : {len(df):,}"
)

print(
    f"Final columns : {len(df.columns)}"
)

print(
    f"Output file   : {OUTPUT_FILE}"
)


if OUTPUT_FILE.exists():

    file_size = OUTPUT_FILE.stat().st_size

    print(
        f"File size     : "
        f"{file_size / 1024:.2f} KB"
    )

    print(
        "\n✓ Cleaned dataset saved successfully!"
    )

else:

    print(
        "\n✗ ERROR: Cleaned dataset "
        "was not created."
    )

    raise FileNotFoundError(
        f"Output file was not created: "
        f"{OUTPUT_FILE}"
    )


# ============================================================
# 16. DATASET SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("DATASET SUMMARY")
print("=" * 70)

print(
    f"Rows                 : {len(df):,}"
)

print(
    f"Aircraft models      : "
    f"{df['AircraftModel'].nunique():,}"
)

print(
    f"Part names           : "
    f"{df['PartName'].nunique():,}"
)

print(
    f"Part numbers         : "
    f"{df['PartNumber'].nunique():,}"
)

print(
    f"Part conditions      : "
    f"{df['PartCondition'].nunique():,}"
)


# ============================================================
# 17. SHOW PART DISTRIBUTION
# ============================================================

print("\nTop Part Names:")

part_counts = (
    df["PartName"]
    .value_counts()
    .head(15)
)

print(part_counts.to_string())


# ============================================================
# 18. SHOW SAMPLE RECORDS
# ============================================================

print("\n" + "=" * 70)
print("SAMPLE CLEANED RECORDS")
print("=" * 70)

print(
    df[
        [
            "AircraftModel",
            "PartName",
            "PartNumber",
            "PartCondition",
            "Discrepancy"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 19. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("READY FOR AEROREPEAT")
print("=" * 70)

print(
    "\nThe cleaned dataset is now available at:"
)

print(
    OUTPUT_FILE
)

print(
    "\nYou can now run:"
)

print(
    "    streamlit run app.py"
)