# ============================================================================
# NBA Player Statistics Analysis
# This script analyzes NBA player statistics including 3-point accuracy trends,
# field goal statistics, and relevant statistical tests.
# ============================================================================

# Import libraries for data manipulation, statistical analysis, and numerical integration
import os
import numpy as np
from scipy import stats, integrate, interpolate

# Get the directory of the current script (currently unused)
os.path.join(os.path.dirname(__file__))

# Change working directory to data folder (commented out for flexibility)
 #os.chdir('/Users/vaishnav/Library/Mobile Documents/com~apple~CloudDocs/Python/')

# Load NBA player statistics from TSV file
data = np.genfromtxt(
     'NBA_Player_Stats.tsv', delimiter='\t', names=True, dtype=None, encoding='utf-8'
 )
# Filter data to include only regular season games
regular_season_mask = data['Stage'] == 'Regular_Season'
data = data[regular_season_mask]

# Filter data to include only regular season games
regular_season_mask = data['Stage'] == 'Regular_Season'
data = data[regular_season_mask]

# ============================================================================
# SECTION 2: FIND PLAYER WITH MOST SEASONS
# ============================================================================
max_seasons = 0
most_season_player = None

players = np.unique(data['Player'])

# Loop through each player and count their unique seasons
for player in players:
    player_data = data[data['Player'] == player]
    player_seasons = np.unique(player_data['Season'])
    num_seasons = len(player_seasons)

    # Track player with maximum seasons
    if num_seasons > max_seasons:
        max_seasons = num_seasons
        most_season_player = player

# Display the player with most seasons
max_player = most_season_player
print(f"Player with most regular seasons: {max_player}")
print(f"Number of seasons: {max_seasons}")

# ============================================================================
# SECTION 3: 3-POINT SHOOTING ACCURACY ANALYSIS
# ============================================================================

# Extract all seasons and 3-point data for the player with most seasons
max_player_data = data[data['Player'] == max_player]
seasons = np.unique(max_player_data['Season'])

years = []
accuracies = []

# Calculate 3-point shooting accuracy for each season
for idx, season in enumerate(seasons):
    season_data = max_player_data[max_player_data['Season'] == season]

    # Calculate 3-point makes and attempts from season data
    made = np.sum(season_data['3PM'])
    attempted = np.sum(season_data['3PA'])
    if attempted > 0:
        # Calculate shooting percentage from made and attempted shots
        accuracy = (made / attempted) * 100
        print(f"Season: {season}, Made: {made}, Attempted: {attempted}, Accuracy: {accuracy:.2f}%")
        # Extract year from season string and store data for analysis
        year = int(str(season)[:4])
        years.append(year)
        accuracies.append(accuracy)
    else:
        print(f"Season: {season}, Made: {made}, Attempted: {attempted}, Accuracy: N/A")

# ============================================================================
# SECTION 4: LINEAR REGRESSION AND TREND ANALYSIS
# ============================================================================

# Perform linear regression to find trend line for 3-point accuracy over time
# Perform linear regression to find trend line for 3-point accuracy over time
linear_model = stats.linregress(years, accuracies)

# Extract slope and intercept from linear regression results
m = linear_model.slope
b = linear_model.intercept

# Define range for numerical integration based on available years
xmin = min(years)
xmax = max(years)

# Define linear function for numerical integration (using regression line)
def my_func(x):
    return m * x + b

# Integrate the linear function over the year range using numerical integration
integral = integrate.quad(my_func, xmin, xmax)

# Calculate average accuracy from the fitted line and compare with actual average
# Average of regression line = integral / width of interval
avg_fit_accuracy = integral[0] / (xmax - xmin)
actual_avg_accuracy = np.mean(accuracies)

# Print comparison results between fitted line and actual data
print(f"Average line fit: {avg_fit_accuracy}%")
print(f"Actual average accuracy: {actual_avg_accuracy}%")
print(f"Difference: {abs(avg_fit_accuracy - actual_avg_accuracy)}")

# ============================================================================
# SECTION 5: INTERPOLATION FOR MISSING YEARS
# ============================================================================

# Convert lists to numpy arrays for interpolation operations
years = np.array(years)
accuracies = np.array(accuracies)

# Sort years and accuracies by year for proper interpolation
order = np.argsort(years)
years = years[order]
accuracies = accuracies[order]

# Create linear interpolation function from the data points
interpolate_function = interpolate.interp1d(years, accuracies, kind='linear')

# Use interpolation to estimate accuracy for specific years
# Note: 2002 estimates 2002-2003 season, 2015 estimates 2015-2016 season
est_2003 = interpolate_function(2002)
est_2016 = interpolate_function(2015)

print(f"Estimated 2002-2003 accuracy: {float(est_2003):.2f}%")
print(f"Estimated 2015-2016 accuracy: {float(est_2016):.2f}%")

# ============================================================================
# SECTION 6: FIELD GOALS STATISTICS (FGM and FGA ANALYSIS)
# ============================================================================

# Extract Field Goals Made (FGM) and Field Goals Attempted (FGA) columns from data
fgm = data['FGM']
fga = data['FGA']

# ============================================================================
# SECTION 6A: CALCULATE DESCRIPTIVE STATISTICS
# ============================================================================

# Calculate mean (average) for FGM and FGA
fgm_mean = np.mean(fgm)
fga_mean = np.mean(fga)

# Calculate sample variance (with Bessel's correction, ddof=1) for FGM and FGA
fgm_var = np.var(fgm, ddof=1)
fga_var = np.var(fga, ddof=1)

# Calculate skewness (measure of asymmetry in distribution) for FGM and FGA
fgm_skew = stats.skew(fgm)
fga_skew = stats.skew(fga)

# Calculate kurtosis (measure of tail heaviness in distribution) for FGM and FGA
fgm_kurtosis = stats.kurtosis(fgm)
fga_kurtosis = stats.kurtosis(fga)

# Print descriptive statistics for Field Goals Made
print(f"FGM - Mean: {fgm_mean}, Variance: {fgm_var}, Skewness: {fgm_skew}, Kurtosis: {fgm_kurtosis}")
# Print descriptive statistics for Field Goals Attempted
print(f"FGA - Mean: {fga_mean}, Variance: {fga_var}, Skewness: {fga_skew}, Kurtosis: {fga_kurtosis}")

# ============================================================================
# SECTION 6B: STATISTICAL TESTS
# ============================================================================

# Perform paired t-test comparing FGM and FGA (dependent samples)
# Tests if the means of FGM and FGA are significantly different
rel_test = stats.ttest_rel(fgm, fga)
print(f"Paired t-test: statistic = {rel_test.statistic}, p-value = {rel_test.pvalue}")

# Perform one-sample t-test for FGM against a null hypothesis of zero mean
# Tests if Field Goals Made is significantly different from zero
fgm_ttest = stats.ttest_1samp(fgm, 0)

print("\nOne-sample t-test (FGM vs 0):")
print(f"t-statistic: {fgm_ttest.statistic:.4f}")
print(f"p-value: {fgm_ttest.pvalue}")

# Perform one-sample t-test for FGA against a null hypothesis of zero mean
# Tests if Field Goals Attempted is significantly different from zero
fga_ttest = stats.ttest_1samp(fga, 0)

print("\nOne-sample t-test (FGA vs 0):")
print(f"t-statistic: {fga_ttest.statistic:.4f}")
print(f"p-value: {fga_ttest.pvalue}")