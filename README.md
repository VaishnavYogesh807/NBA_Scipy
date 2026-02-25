# NBA_Scipy

## Purpose

NBA player statistics from a TSV file are analyzed in this project. It looks at the player's 3-point accuracy trend, finds the player with the most consistent seasons, and runs statistical analyses on field goal data.

## Implementation

* Uses **NumPy** to load data and filters for games in the Regular Season.
* Determines which player has the most seasons.* Determines 3-point accuracy annually.
* Trend analysis is done using **linear regression**, **integration**, and **interpolation**.
* Determines t-tests and descriptive statistics for **FGM** and **FGA**.

## Classes

Custom classes are not used in this project. SciPy functions and NumPy arrays are used for all analysis.

## Key Variables

* `data` — player statistics
* `max_player` — player with most seasons
* `years`, `accuracies` — 3-point trend data
* `fgm`, `fga` — field goal metrics

## Limitations

* Assumes that the TSV file path is accurate.
* Minimal attention to error.
* Trends may be oversimplified by linear models.
* No visualizations provided.
