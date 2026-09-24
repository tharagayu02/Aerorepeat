# ============================================================
# AeroRepeat - Statistical Analysis
# ============================================================
# Purpose:
#   Perform statistical analysis on the cleaned aircraft
#   maintenance dataset.
#
# Dataset:
#   ../data/cleaned_aircraft_maintenance.csv
# ============================================================

# -----------------------------
# 1. Load required packages
# -----------------------------

library(readr)
library(dplyr)

# -----------------------------
# 2. Load dataset
# -----------------------------

data_path <- "../data/cleaned_aircraft_maintenance.csv"

maintenance <- read_csv(
  data_path,
  show_col_types = FALSE
)

# -----------------------------
# 3. Basic cleaning
# -----------------------------

maintenance <- maintenance %>%
  mutate(
    AircraftModel = trimws(as.character(AircraftModel)),
    PartName = trimws(as.character(PartName)),
    PartNumber = trimws(as.character(PartNumber)),
    PartCondition = trimws(as.character(PartCondition)),
    Discrepancy = trimws(as.character(Discrepancy))
  ) %>%
  filter(
    !is.na(Discrepancy),
    Discrepancy != ""
  )

# -----------------------------
# 4. Dataset overview
# -----------------------------

cat("\n========================================\n")
cat("        AeroRepeat Dataset Summary\n")
cat("========================================\n\n")

cat("Total maintenance records:",
    nrow(maintenance), "\n")

cat("Unique aircraft models:",
    n_distinct(maintenance$AircraftModel), "\n")

cat("Unique part names:",
    n_distinct(maintenance$PartName), "\n")

cat("Unique part numbers:",
    n_distinct(maintenance$PartNumber), "\n\n")


# -----------------------------
# 5. Top Part Names
# -----------------------------

top_part_names <- maintenance %>%
  filter(
    !is.na(PartName),
    PartName != ""
  ) %>%
  count(
    PartName,
    name = "RecordCount",
    sort = TRUE
  ) %>%
  slice_head(n = 10)

cat("========================================\n")
cat("Top 10 Part Names\n")
cat("========================================\n\n")

print(top_part_names)


# -----------------------------
# 6. Top Part Numbers
# -----------------------------

top_part_numbers <- maintenance %>%
  filter(
    !is.na(PartNumber),
    PartNumber != ""
  ) %>%
  count(
    PartNumber,
    name = "RecordCount",
    sort = TRUE
  ) %>%
  slice_head(n = 10)

cat("\n========================================\n")
cat("Top 10 Part Numbers\n")
cat("========================================\n\n")

print(top_part_numbers)


# -----------------------------
# 7. Part Condition Analysis
# -----------------------------

condition_summary <- maintenance %>%
  filter(
    !is.na(PartCondition),
    PartCondition != ""
  ) %>%
  count(
    PartCondition,
    name = "RecordCount",
    sort = TRUE
  )

cat("\n========================================\n")
cat("Part Condition Summary\n")
cat("========================================\n\n")

print(condition_summary)


# -----------------------------
# 8. Aircraft Model Analysis
# -----------------------------

top_aircraft_models <- maintenance %>%
  filter(
    !is.na(AircraftModel),
    AircraftModel != ""
  ) %>%
  count(
    AircraftModel,
    name = "RecordCount",
    sort = TRUE
  ) %>%
  slice_head(n = 10)

cat("\n========================================\n")
cat("Top 10 Aircraft Models\n")
cat("========================================\n\n")

print(top_aircraft_models)


# -----------------------------
# 9. Replacement record analysis
# -----------------------------
# A record is treated as a replacement-related
# record when the discrepancy contains common
# replacement/removal terminology.

replacement_records <- maintenance %>%
  filter(
    grepl(
      "REPLACED|REPLACE|REMOVED AND REPLACED|R/R|R&R",
      Discrepancy,
      ignore.case = TRUE
    )
  )

cat("\n========================================\n")
cat("Replacement Analysis\n")
cat("========================================\n\n")

cat(
  "Replacement-related records:",
  nrow(replacement_records),
  "\n"
)


# -----------------------------
# 10. Top replacement Part Numbers
# -----------------------------

top_replacement_part_numbers <- replacement_records %>%
  filter(
    !is.na(PartNumber),
    PartNumber != ""
  ) %>%
  count(
    PartNumber,
    name = "ReplacementCount",
    sort = TRUE
  ) %>%
  slice_head(n = 10)

cat("\n========================================\n")
cat("Top 10 Part Numbers by Replacement Records\n")
cat("========================================\n\n")

print(top_replacement_part_numbers)


# -----------------------------
# 11. Save analysis results
# -----------------------------

write_csv(
  top_part_names,
  "output/top_part_names.csv"
)

write_csv(
  top_part_numbers,
  "output/top_part_numbers.csv"
)

write_csv(
  top_replacement_part_numbers,
  "output/top_replacement_part_numbers.csv"
)

cat("\nAnalysis completed successfully.\n")