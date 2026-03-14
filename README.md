# IPL Dashboard — Python Data Analysis Project

A data-analysis project that loads IPL ball-by-ball and match data, computes batting and bowling statistics, and generates nine publication-ready charts using **Pandas**, **Seaborn**, and **Matplotlib**.

---

## Table of contents

1. [What was built (ordered list)](#1-what-was-built)
2. [Output files](#2-output-files)
3. [Libraries used and why](#3-libraries-used-and-why)
4. [Complete syntax reference — every syntax explained](#4-complete-syntax-reference)
5. [Setup and run](#5-setup-and-run)
6. [Dataset required](#6-dataset-required)
7. [Next improvements (optional)](#7-next-improvements-optional)

---

## 1. What was built

The following analyses and charts were built inside `project.py`, in order:

1. **Top 10 run scorers** — groups every delivery by batsman, sums the runs each batsman scored across all IPL matches, and plots a horizontal bar chart sorted from highest to lowest scorer.
2. **Top 10 strike rates (overall)** — computes each batsman's career strike rate (runs ÷ balls × 100) and plots a vertical bar chart of the 10 highest strike rates in IPL history.
3. **Per-innings strike-rate spread — box + strip chart** — calculates the strike rate for every individual innings played by the top 8 run scorers, then shows the distribution (median, quartiles, and outliers) using a box plot layered with individual data points using a strip plot.
4. **Strike rate vs balls faced — scatter plot** — plots each innings as a dot: x = balls faced, y = strike rate, colour = batsman. Reveals whether a batsman hits fast from ball one or accelerates as an innings progresses.
5. **Average strike rate by season — heatmap** — merges innings data with the matches table to find the season of each match, pivots the data into a batsman × season grid, and colours each cell by the average strike rate for that combination.
6. **Distribution of all per-innings strike rates — histogram + KDE curve** — shows the full shape of the strike-rate distribution across every innings in the dataset, including a smooth density curve.
7. **Top 10 wicket takers** — filters out run-outs and fielder-only dismissals, counts bowler-credited wickets per bowler, and plots a horizontal bar chart of the top 10.
8. **Top 10 best economy rates** — computes economy rate (runs conceded per over, excluding byes and leg-byes; counting only legal deliveries) and plots the 10 bowlers with the lowest (best) economy.
9. **Top 10 worst economy rates** — same computation as above, but plots the 10 bowlers with the highest (worst) economy.

---

## 2. Output files

Running `python project.py` generates the following images (already committed to this repo):

| File | What it shows |
|---|---|
| `top_scorers_plot.png` | Top 10 run scorers — horizontal bar chart |
| `top_strike_rates_plot.png` | Top 10 strike rates — vertical bar chart |
| `strike_rate_box_strip.png` | Per-innings strike-rate spread — box + strip |
| `strike_rate_scatter.png` | Strike rate vs balls faced — scatter |
| `strike_rate_heatmap.png` | Avg strike rate by season — heatmap |
| `strike_rate_distribution.png` | All-innings strike-rate distribution — histogram/KDE |
| `top_wicket_takers_plot.png` | Top 10 wicket takers — horizontal bar chart |
| `top10_best_economy.png` | Top 10 best economy rates — horizontal bar chart |
| `top10_worst_economy.png` | Top 10 worst economy rates — horizontal bar chart |

---

## 3. Libraries used and why

```bash
pip install pandas numpy matplotlib seaborn streamlit
```

| Library | Alias | Purpose in this project |
|---|---|---|
| **pandas** | `pd` | Load CSV files, group rows, aggregate values, filter rows, merge tables, create pivot tables |
| **numpy** | `np` | Imported for potential numeric operations (available for array maths) |
| **matplotlib** | `plt` | Low-level figure creation, axis labels, titles, saving and showing plots |
| **seaborn** | `sns` | High-level statistical charts (bar, box, strip, scatter, heatmap, histogram) built on top of Matplotlib |
| **streamlit** | `st` | Imported for future conversion to an interactive web dashboard |

---

## 4. Complete syntax reference

Every piece of Python/Pandas/Seaborn/Matplotlib syntax used in `project.py` is listed here with a plain-English explanation of **what it does** and **why it was used**.

---

### 4.1 Imports

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
```

**What it does:** Loads external libraries into the script under short alias names.  
**Why:** Writing `pd.read_csv(...)` instead of `pandas.read_csv(...)` is shorter and is the universally accepted convention for these libraries. Every syntax in the rest of the file relies on these imports being present.

---

### 4.2 Loading data — `pd.read_csv()`

```python
df1 = pd.read_csv("c:\\Users\\ISHAAN\\Downloads\\matches.csv")
df2 = pd.read_csv("c:\\Users\\ISHAAN\\Downloads\\deliveries.csv")
```

**What it does:** Reads a comma-separated values file from disk and returns a **DataFrame** — a table with labelled rows and columns.  
**Why:** The entire project is built around two CSV files from the Kaggle IPL dataset. `df1` holds one row per match; `df2` holds one row per delivery (ball). `pd.read_csv` is the standard Pandas function for ingesting flat-file data into a DataFrame.

> **Note on paths:** The script currently uses hardcoded Windows paths. See [Section 6](#6-dataset-required) for the recommended fix so anyone can run it.

---

### 4.3 Setting the plot style — `sns.set_style()`

```python
sns.set_style('whitegrid')
```

**What it does:** Applies Seaborn's `'whitegrid'` theme globally — white background with light grey horizontal grid lines — to every chart that follows.  
**Why:** Called **once** at the very top so every plot in the script has a consistent, clean look without repeating the styling code per chart. `'whitegrid'` is ideal for bar charts because the grid lines help the viewer trace a bar back to its exact value on the axis.

---

### 4.4 Grouping data — `.groupby()`

```python
grouped_data = df2.groupby('batsman')
```

```python
df2.groupby('bowler')['dismissal_kind'].count()
```

**What it does:** Splits the DataFrame into separate sub-tables, one for each unique value in the specified column. The result is a **GroupBy object** — no computation happens yet; it only defines the groups.  
**Why:** The deliveries table has one row per ball. To find how many runs each *batsman* scored in total, the rows must first be grouped by batsman name so that `.sum()` is applied per player, not across the whole dataset at once.

---

### 4.5 Aggregating — `.sum()` and `.count()`

```python
total_runs = grouped_data['batsman_runs'].sum()
```

```python
strike_rates = grouped_data['batsman_runs'].sum() / grouped_data['batsman_runs'].count() * 100
```

**What `.sum()` does:** Adds up all values in the selected column within each group — giving total runs per batsman.  
**What `.count()` does:** Counts how many rows exist in each group — which equals the number of balls faced (each row = one delivery).  
**Why both are needed:** `sum()` accumulates runs; `count()` measures exposure (balls faced). Dividing sum by count and multiplying by 100 gives the **strike rate formula**: `(runs scored ÷ balls faced) × 100`.

---

### 4.6 Sorting — `.sort_values()`

```python
top_scorers  = total_runs.sort_values(ascending=False)
top_strike_rates = strike_rates.sort_values(ascending=False)
top_wicket_takers = bowler_wickets_count.sort_values(ascending=False)
top10_worst  = economy.sort_values(ascending=False).head(10)
top10_best   = economy.sort_values(ascending=True).head(10)
```

**What it does:** Rearranges the Series (or DataFrame) from largest to smallest (`ascending=False`) or smallest to largest (`ascending=True`).  
**Why:** The goal in each case is to rank players. `ascending=False` surfaces the **highest** values (most runs, most wickets, worst economy) at position 0. `ascending=True` surfaces the **lowest** values (best economy) at position 0. After sorting, `.head(10)` trivially extracts the top 10.

---

### 4.7 Selecting top rows — `.head()`

```python
top10 = top_scorers.head(10)
top_bats = top_scorers.head(8).index.tolist()
```

**What it does:** Returns the first *n* rows of a Series or DataFrame (default n = 5).  
**Why:** After sorting, the best players are at the top. `.head(10)` is a clean, readable way to keep only the top 10 without writing an explicit slice like `[:10]`.

---

### 4.8 Slice notation — `.iloc[::1]`

```python
top10 = top10.iloc[::1]
```

**What it does:** `iloc[start:stop:step]` selects rows by integer position. `[::1]` means "start from the beginning, go to the end, step by 1" — which returns all rows unchanged, in their existing order. (To actually reverse, the step would need to be `-1`.)  
**Why:** The original code comment says "reverse so highest scorer appears at top", but this call **does not reverse** the data. The Series is already sorted descending by `sort_values(ascending=False)` above, so the highest scorer is already at position 0. The `.iloc[::1]` line is effectively a no-op and serves as an explicit reminder that the order is intentional.

---

### 4.9 Bar chart — `sns.barplot()`

```python
# Horizontal bar chart (x = numeric, y = categorical player names)
sns.barplot(x=top10.values, y=top10.index, palette=sns.color_palette("viridis", len(top10)))

# Vertical bar chart (x = categorical, y = numeric)
sns.barplot(data=top10_strike_df, x='batsman', y='strike_rate', palette='magma')

sns.barplot(x=top10_bowlers.values, y=top10_bowlers.index, palette='magma')
sns.barplot(x=top10_best.values,   y=top10_best.index,    palette='Blues_r')
sns.barplot(x=top10_worst.values,  y=top10_worst.index,   palette='Reds')
```

**What it does:** Draws a bar chart. When `x` is numeric and `y` is categorical the bars run **horizontally**; when `x` is categorical and `y` is numeric the bars run **vertically**.  
**Why horizontal bars for top-10 lists:** Player names are long strings. Placing them on the y-axis (horizontal bars) means they can be read easily without rotation and without being cut off.  
**Why vertical bars for strike rates:** The category (batsman name) has only 10 items and is placed on the x-axis; rotation with `plt.xticks(rotation=45)` makes the names legible at that scale.  
**Why `sns.barplot` instead of `plt.bar`:** Seaborn's version handles color palettes automatically and integrates cleanly with DataFrames using `data=`, `x=`, `y=` column names.

---

### 4.10 Color palettes — `sns.color_palette()` / named palette strings

```python
palette=sns.color_palette("viridis", len(top10))
palette='magma'
palette='Blues_r'
palette='Reds'
```

**What it does:** Assigns a sequence of colors — one per bar — from a named color map.  
**Why `viridis` / `magma`:** These are **perceptually uniform** color maps: the visual difference between two colors accurately represents the data difference between two values. They are also readable by people with color-vision deficiencies.  
**Why `Blues_r` for best economy:** Blue is conventionally calm / positive. The `_r` suffix *reverses* the palette so the lowest (best) value gets the darkest blue, visually spotlighting the best performers.  
**Why `Reds` for worst economy:** Red signals danger or poor performance, making it immediately clear that a high economy rate is bad for the bowler.

---

### 4.11 Plot labels and title — `plt.title()`, `plt.xlabel()`, `plt.ylabel()`

```python
plt.title('Top 10 Run Scorers in IPL')
plt.xlabel('Total Runs Scored')
plt.ylabel('Batsman')
```

**What it does:** Adds a title string above the chart and axis-label strings along the x and y axes.  
**Why:** Without axis labels a viewer cannot understand what the numbers represent. Seaborn does not automatically add descriptive axis titles, so they must be set manually after each plot call.

---

### 4.12 Layout adjustment — `plt.tight_layout()`

```python
plt.tight_layout()
```

**What it does:** Automatically adjusts subplot spacing (padding around the plot area) so that axis labels, tick labels, and the title do not overlap or get clipped.  
**Why:** When player names are long, or when the legend is placed inside the axes, the default Matplotlib layout often clips text at the edges. `tight_layout()` resolves this in one call without manually tweaking `subplots_adjust` values.

---

### 4.13 Saving a figure — `plt.savefig()`

```python
plt.savefig('top_scorers_plot.png')
```

**What it does:** Writes the current figure to a file. The image format is inferred from the file extension (`.png` here).  
**Why:** Saves each chart as a static image that can be committed to the repository, shared in reports, or displayed on a web page — without needing to re-run the script.

---

### 4.14 Displaying a figure — `plt.show()`

```python
plt.show()
```

**What it does:** Renders the current figure in a GUI window (when running locally) and then **clears** it, so the next `plt` commands start on a fresh canvas.  
**Why:** Without `plt.show()`, all subsequent drawing commands would be added on top of the previous chart. It acts as a "finish and reset" boundary between charts.

---

### 4.15 Resetting the index — `.reset_index()`

```python
top10_strike_df = top10_strike.reset_index()
```

```python
innings = (
    df2[df2['wide_runs'] == 0]
    .groupby(['match_id', 'batsman'])
    .agg(...)
    .reset_index()
)
```

**What it does:** Converts the **index** of a Series (or the group-key columns of a GroupBy result) into regular columns of a DataFrame, replacing the index with the default integer sequence 0, 1, 2, …  
**Why:** After `groupby + agg`, the grouped-by columns (`match_id`, `batsman`) are stored in the index, not as regular columns. Seaborn's `data=`, `x=`, `y=` parameters need regular column names. `reset_index()` promotes the index levels to columns so they become accessible by name.

---

### 4.16 Renaming columns — `df.columns = [...]`

```python
top10_strike_df.columns = ['batsman', 'strike_rate']
```

**What it does:** Replaces every column name in the DataFrame with the names in the provided list.  
**Why:** After `reset_index()` the columns were named `['batsman', 'batsman_runs']`. Renaming the second column to `'strike_rate'` makes the `y='strike_rate'` argument in `sns.barplot` readable and self-documenting.

---

### 4.17 Creating a new figure with a size — `plt.figure(figsize=...)`

```python
plt.figure(figsize=(8, 6))
plt.figure(figsize=(10, 6))
plt.figure(figsize=(8, 5))
```

**What it does:** Creates a new, empty Matplotlib figure with the given width × height in inches.  
**Why:** Different charts need different canvas sizes. A scatter plot with a legend placed outside the axes needs extra width. A box plot with eight batsman names on the x-axis needs more horizontal space than a simple bar chart. Controlling `figsize` prevents labels from overlapping and ensures exported PNGs have a sensible resolution.

---

### 4.18 Rotating x-axis tick labels — `plt.xticks(rotation=..., ha=...)`

```python
plt.xticks(rotation=45, ha='right')
```

**What it does:** Rotates every x-axis tick label by 45 degrees. `ha='right'` aligns the label so its **right** end sits under the tick mark, preventing text from drifting toward the next tick.  
**Why:** Batsman names are long strings. At 0° they overlap each other along the x-axis. A 45° rotation with right-alignment is the standard readable compromise between fully vertical and fully horizontal text.

---

### 4.19 Boolean indexing / filtering rows — `df[condition]`

```python
df2[df2['wide_runs'] == 0]
bowler_wickets_df = df2[df2['dismissal_kind'].isin(bowler_stats_criteria)]
innings[innings['batsman'].isin(top_bats)]
```

**What it does:** Creates a boolean Series (True/False per row) by comparing each row's value to a condition. Passing that Series inside `df[...]` returns only the rows where the condition is `True`.  
**Why `wide_runs == 0`:** Wide deliveries are not counted as balls faced. Excluding them before counting deliveries gives an accurate balls-faced number per innings.  
**Why filter dismissal kinds:** Not all wickets are credited to the bowler (a run-out involves a fielder). Filtering to only bowler-credited dismissal types gives an accurate wicket count per bowler.

---

### 4.20 Multi-column groupby

```python
df2[df2['wide_runs'] == 0]
    .groupby(['match_id', 'batsman'])
    .agg(...)
```

**What it does:** Groups rows by a combination of two columns — each unique `(match_id, batsman)` pair forms one group.  
**Why:** The goal is per-*innings* strike rates — one strike rate for a specific batsman in a specific match. Grouping by `match_id` alone would merge all batsmen per match; grouping by `batsman` alone would merge all their innings. Grouping by both gives exactly one row per innings.

---

### 4.21 Named aggregation — `.agg(name=('col', 'func'))`

```python
.agg(runs=('batsman_runs', 'sum'), balls=('batsman_runs', 'count'))
```

**What it does:** Applies multiple aggregation functions to columns in a single call and assigns a custom name to each result. `runs=('batsman_runs', 'sum')` means "sum the `batsman_runs` column and store the result in a column called `runs`".  
**Why:** This is cleaner than chaining `.sum()` and `.count()` separately and then merging. It produces a DataFrame with descriptive column names immediately, without an extra rename step.

---

### 4.22 Creating a new computed column — `df['new'] = ...`

```python
innings['strike_rate'] = innings['runs'] / innings['balls'] * 100
df2['runs_conceded_ball'] = df2['total_runs'] - df2['bye_runs'] - df2['legbye_runs']
```

**What it does:** Adds a brand-new column by performing element-wise arithmetic across existing columns. Every row gets its own computed value.  
**Why `innings['strike_rate']`:** Strike rate is not in the raw data; it must be derived. Adding it as a column makes it available for all subsequent plot calls using `y='strike_rate'`.  
**Why `runs_conceded_ball`:** Economy rate must count only the runs the *bowler* is responsible for. Byes and leg-byes occur due to the wicket-keeper/fielder missing the ball, so they are subtracted to get the runs the bowler alone conceded per delivery.

---

### 4.23 Getting the index as a Python list — `.index.tolist()`

```python
top_bats = top_scorers.head(8).index.tolist()
```

**What it does:** Extracts the index values of a Series as a plain Python list.  
**Why:** Seaborn's `order=` parameter (used in `sns.boxplot` and `sns.stripplot`) requires a Python list, not a Pandas Index. `.tolist()` does the conversion. Passing `order=top_bats` ensures both plots draw their x-axis categories in the same left-to-right sequence, which is essential so the box plot and strip plot align correctly when overlaid.

---

### 4.24 Filtering with a list — `.isin()`

```python
bowler_wickets_df = df2[df2['dismissal_kind'].isin(bowler_stats_criteria)]
innings[innings['batsman'].isin(top_bats)]
```

**What it does:** Returns `True` for every row whose value is found in the provided list; `False` otherwise. Works like a multi-value `==` check.  
**Why:** Instead of a long chain of `(col == 'bowled') | (col == 'lbw') | ...`, `.isin(list)` does the same thing in one concise line. It is the idiomatic Pandas way to keep rows matching any value in a set of allowed values.

---

### 4.25 Box plot — `sns.boxplot()`

```python
sns.boxplot(data=innings[innings['batsman'].isin(top_bats)],
            x='batsman', y='strike_rate', order=top_bats)
```

**What it does:** Draws a box-and-whisker plot per category. The box spans the interquartile range (25th–75th percentile); the line inside the box is the median; the whiskers extend to 1.5× IQR; dots beyond the whiskers are outliers.  
**Why:** A single bar chart of average strike rates hides whether a batsman is *consistently* fast or just had a few explosive innings. The box plot reveals the **spread** and **consistency**: a narrow box = consistent performance; a wide box = highly variable innings.

---

### 4.26 Strip plot — `sns.stripplot()`

```python
sns.stripplot(data=innings[innings['batsman'].isin(top_bats)],
              x='batsman', y='strike_rate', order=top_bats,
              color='k', size=3, alpha=0.5)
```

**What it does:** Plots every individual data point as a small dot along the categorical axis, jittered slightly so overlapping points are visible.  
**Why:** Overlaying a strip plot on the box plot shows the **actual data density** — the viewer sees not just summary statistics (box) but every single innings point. `color='k'` (black), `size=3` (small dots), and `alpha=0.5` (50% transparent) prevent the points from visually overwhelming the box.

---

### 4.27 Scatter plot — `sns.scatterplot()`

```python
sns.scatterplot(data=sample, x='balls', y='strike_rate', hue='batsman', alpha=0.7)
```

**What it does:** Draws one dot per row. `x` and `y` set the two numeric axes; `hue` assigns a different color per unique category value (one color per batsman).  
**Why:** A scatter plot is the right chart for exploring the relationship between two continuous variables — here, "balls faced" (volume) vs "strike rate" (efficiency). `hue='batsman'` adds a third dimension by color-coding points so the viewer can track individual players across the cloud of dots.

---

### 4.28 Positioning the legend outside the axes — `plt.legend(bbox_to_anchor=...)`

```python
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
```

**What it does:** Moves the legend box outside the plot area to the right. `bbox_to_anchor=(1.05, 1)` anchors the legend 5% beyond the right edge of the axes; `loc='upper left'` aligns the upper-left corner of the legend to that anchor point.  
**Why:** When `hue='batsman'` generates 8 colored legend entries, the default legend overlaps scatter points inside the plot area. Placing it outside preserves the full view of the data.

---

### 4.29 Checking whether a column exists — `if 'col' in df.columns`

```python
if 'match_id' in df2.columns and 'id' in df1.columns and 'season' in df1.columns:
```

**What it does:** Checks whether a column-name string is present in the list of column names of a DataFrame.  
**Why:** The heatmap requires merging on `match_id`, `id`, and `season`. Not all versions of the IPL dataset include a `season` column. This guard prevents a `KeyError` crash when the column is absent; the heatmap is simply skipped instead of crashing the entire script.

---

### 4.30 Merging two DataFrames — `.merge()`

```python
merged = innings.merge(df1[['id', 'season']], left_on='match_id', right_on='id', how='left')
```

**What it does:** Joins two DataFrames on key columns (like SQL `JOIN`). `left_on='match_id'` is the key in `innings`; `right_on='id'` is the matching key in `df1`. `how='left'` keeps all rows from the left DataFrame and fills with `NaN` for any match not found in `df1`.  
**Why:** The deliveries table (`df2`) does not contain `season`; that information lives in the matches table (`df1`). To know which season each innings belongs to, the two tables must be joined on their shared match identifier.

---

### 4.31 Pivot table — `.pivot_table()`

```python
pivot = (
    merged[merged['batsman'].isin(top_bats)]
    .pivot_table(index='batsman', columns='season',
                 values='strike_rate', aggfunc='mean')
)
```

**What it does:** Reshapes the DataFrame so that unique values of one column (`batsman`) become the row index, unique values of another column (`season`) become column headers, and each cell is the aggregate (`mean`) of `strike_rate` for that batsman-season combination.  
**Why:** A heatmap needs a 2-D matrix (rows × columns → value). `pivot_table` is the standard way to transform long-format data (one row per innings) into the wide matrix (batsman × season → average strike rate) that `sns.heatmap` expects.

---

### 4.32 Heatmap — `sns.heatmap()`

```python
sns.heatmap(pivot, cmap='magma', annot=True, fmt='.1f', linewidths=.5)
```

**What it does:** Draws a color-coded grid where each cell's color represents its numeric value. `cmap='magma'` sets the color scale; `annot=True` prints the numeric value inside each cell; `fmt='.1f'` formats each number to one decimal place; `linewidths=.5` draws thin separating lines between cells.  
**Why:** The heatmap lets the viewer scan across both dimensions at once — spotting which batsman performed best in which season, or noticing multi-season trends — something that would require many separate charts to achieve with bars or lines.

---

### 4.33 Histogram with KDE — `sns.histplot(kde=True)`

```python
sns.histplot(innings['strike_rate'], kde=True)
```

**What it does:** Draws a histogram (bars showing the count of values in each numeric bin) and overlays a **KDE (Kernel Density Estimate)** — a smooth continuous curve approximating the probability distribution of the data.  
**Why:** The histogram answers "how many innings had a strike rate between 100 and 120?". Adding `kde=True` adds a smoothed curve that shows the overall **shape** of the distribution (e.g., is it bell-shaped? skewed right?). This is more informative than bars alone for understanding the typical and extreme strike-rate values across all IPL innings.

---

### 4.34 Error handling — `try / except`

```python
try:
    innings = (...)
    # ... all additional visualizations ...
except Exception as e:
    print('Could not build additional visualizations:', e)
```

**What it does:** Executes the code inside `try`. If any line raises an exception, execution jumps to `except`, where the error message is printed and the script continues normally.  
**Why:** The additional visualizations (box, scatter, heatmap, histogram) depend on intermediate computations that might fail if the dataset has an unexpected schema or missing columns. Wrapping them in `try/except` means the script still produces the main charts (run scorers, wicket takers, economy) even if an edge-case data issue prevents the advanced charts.

---

### 4.35 Compound boolean filter — `&` operator

```python
df2[(df2['wide_runs'] == 0) & (df2['noball_runs'] == 0)].groupby('bowler').size()
```

**What it does:** Combines two boolean conditions with `&` (element-wise AND). Each condition must be wrapped in its own parentheses because `&` has higher operator precedence than `==`.  
**Why:** To count "legal deliveries" (for computing overs bowled), both wide balls and no-balls must be excluded simultaneously. Excluding only one at a time would overcount deliveries. The `&` ensures a ball is counted as legal only when *both* conditions are satisfied.

---

### 4.36 Counting rows per group — `.groupby().size()`

```python
legal_balls = df2[(df2['wide_runs'] == 0) & (df2['noball_runs'] == 0)].groupby('bowler').size()
```

**What it does:** Returns the number of rows in each group as a Series. Unlike `.count()` (which operates on a specific column and skips `NaN`), `.size()` counts every row in the group regardless of `NaN` values.  
**Why:** There is no "balls bowled" column in the raw dataset. The number of legal deliveries per bowler must be derived by counting how many qualifying rows belong to each bowler after filtering for legal deliveries.

---

### 4.37 Index union — `.index.union()`

```python
bowlers = runs_conceded.index.union(legal_balls.index)
```

**What it does:** Returns the sorted set-union of two Index objects — all unique bowler names that appear in either Series.  
**Why:** A bowler who conceded runs might not have bowled any legal deliveries in the filtered subset (and vice versa). Without the union, `.reindex()` below could accidentally drop bowlers who appear in one Series but not the other, producing incorrect economy calculations.

---

### 4.38 Reindexing a Series — `.reindex(fill_value=...)`

```python
runs_conceded = runs_conceded.reindex(bowlers, fill_value=0)
legal_balls   = legal_balls.reindex(bowlers, fill_value=0)
```

**What it does:** Conforms the Series to a new index. Any label present in `bowlers` but missing from the Series receives `fill_value` (here `0`) instead of `NaN`.  
**Why:** Both Series must share the exact same index (same bowlers in the same order) before element-wise arithmetic is possible. `fill_value=0` correctly represents "this bowler conceded 0 runs in that sub-table" rather than leaving an unknown `NaN`.

---

### 4.39 Creating an empty Series — `pd.Series(index=..., dtype=...)`

```python
economy = pd.Series(index=bowlers, dtype=float)
```

**What it does:** Creates a new Series with a specified index and data type, but no values (all `NaN` by default).  
**Why:** An empty Series is created first so that the masked assignment in the next step (`economy[valid] = ...`) can safely fill only the rows where dividing by overs is valid (overs > 0), leaving the rest as `NaN` to be removed by `.dropna()` later.

---

### 4.40 Boolean mask — `valid = series > value`

```python
valid = overs > 0
```

**What it does:** Produces a boolean Series of the same length where each entry is `True` if the corresponding bowler bowled more than 0 legal deliveries.  
**Why:** Dividing by zero raises an error or produces `inf`. Creating a mask first and only computing economy for `valid` rows is safer and clearer than wrapping each division in an `if` statement inside a loop.

---

### 4.41 Masked assignment — `series[mask] = ...`

```python
economy[valid] = runs_conceded[valid] / overs[valid]
```

**What it does:** Updates only the elements of `economy` where `valid` is `True`; all other positions remain `NaN`.  
**Why:** This is the clean Pandas pattern for conditional element-wise computation — compute and assign the economy rate only for bowlers with at least one legal delivery, while leaving bowlers with zero legal deliveries as `NaN` (to be removed by `.dropna()`).

---

### 4.42 Dropping missing values — `.dropna()`

```python
economy = economy.dropna()
```

**What it does:** Removes all rows where the value is `NaN`.  
**Why:** Bowlers with 0 legal deliveries have `NaN` in the `economy` Series (because their economy was never computed in the masked assignment). Keeping them would pollute the top-10 ranking and cause plotting errors. `.dropna()` removes them in one call.

---

### 4.43 Checking emptiness — `if not series.empty`

```python
if not top10_best.empty:
    plt.figure(...)
    sns.barplot(...)
    ...

if not top10_worst.empty:
    plt.figure(...)
    sns.barplot(...)
    ...
```

**What it does:** `series.empty` is `True` when the Series (or DataFrame) contains zero rows. The `if not` guard skips the plotting block when the data is empty.  
**Why:** If the dataset is filtered so aggressively that no bowlers qualify, calling `sns.barplot()` on an empty Series would raise an error or produce a blank chart. The guard ensures the script exits gracefully in such edge cases.

---

## 5. Setup and run

### 1) Clone the repository

```bash
git clone https://github.com/Ishaan2008-op/ipl-dashboard.git
cd ipl-dashboard
```

### 2) Create and activate a virtual environment (recommended)

**Windows (PowerShell)**
```bash
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install pandas numpy matplotlib seaborn streamlit
```

### 4) Run the analysis script

```bash
python project.py
```

This executes the full pipeline and generates all nine PNG charts in the current directory.

### 5) Run as a Streamlit dashboard (optional)

```bash
streamlit run project.py
```

> Note: `project.py` currently uses `print()` and Matplotlib's `plt.show()`. To make it a fully interactive dashboard, replace `print()` with `st.write()` and display figures with `st.pyplot(fig)`.

---

## 6. Dataset required

Place the following Kaggle IPL CSV files in the repository folder (same level as `project.py`):

- `matches.csv` — one row per match
- `deliveries.csv` — one row per delivery (ball)

Then update the `pd.read_csv` calls in `project.py`:

```python
df1 = pd.read_csv("matches.csv")
df2 = pd.read_csv("deliveries.csv")
```

---

## 7. Next improvements (optional)

- Add a `requirements.txt` so setup is one command (`pip install -r requirements.txt`).
- Convert `project.py` into a full Streamlit dashboard (`st.sidebar`, `st.selectbox`, `st.pyplot`).
- Include sample/anonymised data so contributors can run the script without downloading from Kaggle.
