# ============================================================
# AeroRepeat - Statistical Plots
# ============================================================

# -----------------------------
# 1. Load packages
# -----------------------------

library(readr)
library(dplyr)
library(ggplot2)

# -----------------------------
# 2. Load dataset
# -----------------------------

data_path <- "../data/cleaned_aircraft_maintenance.csv"

maintenance <- read_csv(
  data_path,
  show_col_types = FALSE
)

# -----------------------------
# 3. Clean data
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


# ============================================================
# GRAPH 1
# Top 10 Part Names by Historical Records
# ============================================================

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

# Reverse order for horizontal chart
top_part_names <- top_part_names %>%
  arrange(RecordCount) %>%
  mutate(
    PartName = factor(
      PartName,
      levels = PartName
    )
  )

plot_part_names <- ggplot(
  top_part_names,
  aes(
    x = PartName,
    y = RecordCount
  )
) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Top 10 Part Names by Historical Records",
    subtitle = "AeroRepeat maintenance dataset",
    x = "Part Name",
    y = "Number of Records"
  ) +
  theme_minimal(base_size = 13) +
  theme(
    plot.title = element_text(
      face = "bold",
      size = 16
    ),
    plot.subtitle = element_text(
      size = 11
    ),
    axis.text.y = element_text(
      size = 10
    )
  )

# Save graph
ggsave(
  filename = "R/output/top_part_names.png",
  plot = plot_part_names,
  width = 10,
  height = 6,
  dpi = 300
)


# ============================================================
# GRAPH 2
# Top 10 Part Numbers by Replacement Records
# ============================================================

replacement_records <- maintenance %>%
  filter(
    grepl(
      "REPLACED|REPLACE|REMOVED AND REPLACED|R/R|R&R",
      Discrepancy,
      ignore.case = TRUE
    )
  )

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

# Reverse order for horizontal chart
top_replacement_part_numbers <- top_replacement_part_numbers %>%
  arrange(ReplacementCount) %>%
  mutate(
    PartNumber = factor(
      PartNumber,
      levels = PartNumber
    )
  )

plot_part_numbers <- ggplot(
  top_replacement_part_numbers,
  aes(
    x = PartNumber,
    y = ReplacementCount
  )
) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Top 10 Part Numbers by Replacement Records",
    subtitle = "Records containing replacement-related maintenance actions",
    x = "Part Number",
    y = "Replacement Records"
  ) +
  theme_minimal(base_size = 13) +
  theme(
    plot.title = element_text(
      face = "bold",
      size = 16
    ),
    plot.subtitle = element_text(
      size = 11
    ),
    axis.text.y = element_text(
      size = 10
    )
  )

# Save graph
ggsave(
  filename = "R/output/top_part_numbers.png",
  plot = plot_part_numbers,
  width = 10,
  height = 6,
  dpi = 300
)


# -----------------------------
# Completion message
# -----------------------------

cat("\n========================================\n")
cat("Graphs generated successfully!\n")
cat("========================================\n\n")

cat("Created:\n")
cat("R/output/top_part_names.png\n")
cat("R/output/top_part_numbers.png\n")