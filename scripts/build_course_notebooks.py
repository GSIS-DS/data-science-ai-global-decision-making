"""Build the public course notebooks from readable, versioned cell definitions.

Run from the repository root with `python scripts/build_course_notebooks.py`.
The generated notebooks intentionally contain no executed outputs.
"""

from __future__ import annotations

import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_URL = (
    "https://raw.githubusercontent.com/GSIS-DS/"
    "data-science-ai-global-decision-making/main/"
    "data/sample/global_indicators_sample.csv"
)


def md(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def loader() -> str:
    return f'''from pathlib import Path
import pandas as pd

DATA_URL = "{DATA_URL}"
LOCAL_PATHS = [
    Path("data/sample/global_indicators_sample.csv"),
    Path("../../data/sample/global_indicators_sample.csv"),
]
local_path = next((path for path in LOCAL_PATHS if path.exists()), None)
data_source = str(local_path) if local_path else DATA_URL
df = pd.read_csv(data_source)
print(f"Loaded {{len(df)}} rows from {{data_source}}")
df.head()'''


def write(path: str, cells: list[dict]) -> None:
    for index, cell in enumerate(cells):
        cell["id"] = hashlib.sha1(f"{path}:{index}".encode()).hexdigest()[:8]
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    write("notebooks/week-01/01_data_ai_evidence_global_decision_making.ipynb", [
        md("""# Week 1: Data, AI, and Evidence for Global Decision-Making

**Learning objective:** Distinguish observation, pattern, interpretation, and decision claim while learning the course workflow.

**Expected outputs:** a data preview, one regional chart, and four carefully labeled statements.

**Data source:** Synthetic teaching data created for classroom exercises only; not for empirical analysis or policy decisions.

[Open this notebook in Colab](https://colab.research.google.com/github/GSIS-DS/data-science-ai-global-decision-making/blob/main/notebooks/week-01/01_data_ai_evidence_global_decision_making.ipynb). Save a copy in Drive before editing."""),
        md("""## Course workflow

GitHub repository -> Google Colab notebook -> saved analysis -> GitHub/LMS submission

Evidence does not speak for itself. We separate what the data directly show from explanations and recommendations that require additional reasoning."""),
        code(loader()),
        code("""required = {'country', 'year', 'gdp_growth', 'region'}
assert required.issubset(df.columns), f"Missing columns: {required - set(df.columns)}"
df[['country', 'year', 'gdp_growth', 'region']].head(10)"""),
        code("""import matplotlib.pyplot as plt

avg_growth = df.groupby('region', as_index=False)['gdp_growth'].mean().sort_values('gdp_growth')
ax = avg_growth.plot(kind='barh', x='region', y='gdp_growth', legend=False, figsize=(8, 4), color='#3572A5')
ax.set_title('Average GDP growth by region, 2020-2022')
ax.set_xlabel('Average annual GDP growth (%)')
ax.set_ylabel('')
ax.text(0, -0.22, 'Source: synthetic course dataset; classroom use only.', transform=ax.transAxes, fontsize=9)
plt.tight_layout()
plt.show()"""),
        md("""## Exercise: evidence ladder

Write four bullets:

1. **Observation:** one value or ranking directly visible in the chart.
2. **Pattern:** a broader regularity across regions.
3. **Interpretation:** one plausible explanation that would require more evidence.
4. **Decision claim:** one possible action, explicitly conditional on further verification.

**Expected form:** four labeled sentences. Do not claim that trade, policy, or any other factor caused the pattern."""),
    ])

    write("notebooks/week-02/02_working_with_data_in_python.ipynb", [
        md("""# Week 2: Working with Data in Python

**Learning objective:** Use variables and core pandas operations to answer a focused global-data question.

**Expected outputs:** column inspection, a 2022 subset, summary statistics, and two exercise responses.

**Data source:** Synthetic course data, not official statistics. [Open in Colab](https://colab.research.google.com/github/GSIS-DS/data-science-ai-global-decision-making/blob/main/notebooks/week-02/02_working_with_data_in_python.ipynb)."""),
        md("""## Question

How did inflation and unemployment vary across regions in 2022? We need only variables, importing pandas, selecting columns, filtering, and summaries—no loops or object-oriented programming."""),
        code(loader()),
        code("""year_of_interest = 2022
selected_columns = ['country', 'region', 'year', 'inflation', 'unemployment_percent']
df[selected_columns].head()"""),
        code("""subset_2022 = df.loc[df['year'] == year_of_interest, selected_columns].copy()
print(f"Countries in subset: {subset_2022['country'].nunique()}")
subset_2022.head()"""),
        code("""subset_2022[['inflation', 'unemployment_percent']].describe().round(2)"""),
        md("""## Exercises

1. Filter `subset_2022` to one region and calculate mean inflation. **Expected output:** one number and the region name.
2. Find one country above the 2022 median unemployment rate. **Expected output:** country, value, median, and one descriptive sentence.

Replace the placeholders below, then verify the comparison yourself."""),
        code("""chosen_region = 'East Asia & Pacific'
region_mean = subset_2022.loc[subset_2022['region'] == chosen_region, 'inflation'].mean()
print(chosen_region, round(region_mean, 2))

median_unemployment = subset_2022['unemployment_percent'].median()
above_median = subset_2022.loc[subset_2022['unemployment_percent'] > median_unemployment,
                               ['country', 'unemployment_percent']]
above_median.head()"""),
    ])

    write("notebooks/week-03/03_cleaning_transforming_data.ipynb", [
        md("""# Week 3: Cleaning and Transforming Data

**Learning objective:** Diagnose data-quality issues, make justified transformations, and document checks.

**Expected outputs:** quality profile, cleaned teaching copy, derived variable, group summary, and transformation log.

**Data source:** Synthetic course data. The raw file is complete; this notebook deliberately creates a messy copy for practice. [Open in Colab](https://colab.research.google.com/github/GSIS-DS/data-science-ai-global-decision-making/blob/main/notebooks/week-03/03_cleaning_transforming_data.ipynb)."""),
        code(loader()),
        md("""## 1. Inspect before changing

Never clean silently. Record row count, types, duplicates, and missing values before deciding what needs correction."""),
        code("""print('Shape:', df.shape)
display(df.dtypes.to_frame('dtype'))
display(df.isna().sum().to_frame('missing'))
print('Duplicate rows:', df.duplicated().sum())"""),
        md("""## 2. Practice on a deliberately messy copy

The next cell introduces one missing value, one duplicate row, and a year stored as text. These issues are instructional and are not present in the source CSV."""),
        code("""messy = df.copy()
messy.loc[0, 'inflation'] = pd.NA
messy['year'] = messy['year'].astype(str)
messy = pd.concat([messy, messy.iloc[[1]]], ignore_index=True)

print('Missing inflation:', messy['inflation'].isna().sum())
print('Duplicate rows:', messy.duplicated().sum())
print('Year type:', messy['year'].dtype)"""),
        code("""clean = messy.drop_duplicates().copy()
clean['year'] = pd.to_numeric(clean['year'], errors='raise')

# Keep the missing value rather than inventing an inflation rate.
# Drop it only from calculations that require inflation.
clean['trade_balance_usd_bn'] = clean['exports_usd_bn'] - clean['imports_usd_bn']

assert clean.duplicated().sum() == 0
assert pd.api.types.is_numeric_dtype(clean['year'])
clean[['country', 'year', 'inflation', 'trade_balance_usd_bn']].head()"""),
        code("""regional_summary = (clean.dropna(subset=['inflation'])
                    .groupby(['region', 'year'], as_index=False)
                    .agg(mean_inflation=('inflation', 'mean'),
                         mean_trade_balance=('trade_balance_usd_bn', 'mean'))
                    .round(2))
regional_summary.head(10)"""),
        md("""## Data-quality checklist and exercise

- Are required columns present and correctly typed?
- Are duplicates defined using the right keys?
- Is missingness handled without inventing evidence?
- Are units and transformations documented?

Write a 3-5 line transformation log using: **input issue -> change -> reason -> verification -> interpretive effect**.

**Example:** `year` arrived as text in the practice copy. I converted it with `pd.to_numeric(..., errors='raise')` so numeric comparisons are reliable. I verified the resulting dtype. This change does not alter values but makes invalid text fail visibly."""),
    ])

    write("notebooks/week-04/04_combining_reshaping_global_data.ipynb", [
        md("""# Week 4: Combining and Reshaping Global Data

**Learning objective:** Merge related tables safely and reshape data between long and wide forms.

**Expected outputs:** key checks, a successful merge, an unmatched-row audit, and long/wide tables.

**Data source:** Synthetic course data. [Open in Colab](https://colab.research.google.com/github/GSIS-DS/data-science-ai-global-decision-making/blob/main/notebooks/week-04/04_combining_reshaping_global_data.ipynb)."""),
        code(loader()),
        md("""## 1. Define tables, grain, and keys

Both tables should contain one row per ISO3 code and year. Check that claim before merging."""),
        code("""macro = df[['country', 'iso3', 'year', 'gdp_growth', 'inflation', 'region']].copy()
trade = df[['iso3', 'year', 'exports_usd_bn', 'imports_usd_bn', 'trade_openess_percent']].copy()
keys = ['iso3', 'year']
print('Macro duplicate keys:', macro.duplicated(keys).sum())
print('Trade duplicate keys:', trade.duplicated(keys).sum())"""),
        code("""merged = macro.merge(trade, on=keys, how='left', validate='one_to_one', indicator=True)
display(merged['_merge'].value_counts())
assert (merged['_merge'] == 'both').all()
merged.head()"""),
        md("""## 2. Deliberate unmatched-row example

Real sources rarely align perfectly. Remove one trade row to simulate a coverage gap, then audit rather than silently dropping the country-year."""),
        code("""trade_incomplete = trade.iloc[1:].copy()
audit_merge = macro.merge(trade_incomplete, on=keys, how='left', validate='one_to_one', indicator=True)
unmatched = audit_merge.loc[audit_merge['_merge'] != 'both', keys + ['country', '_merge']]
unmatched"""),
        md("""A left join preserves every macro row. The unmatched record now has missing trade measures. Before analysis, investigate source coverage and decide whether exclusion, imputation, or an explicit limitation is justified."""),
        md("""## 3. Reshape between long and wide"""),
        code("""long_df = (merged[['iso3', 'year', 'gdp_growth', 'inflation']]
           .melt(id_vars=['iso3', 'year'], var_name='metric', value_name='value'))
long_df.head(8)"""),
        code("""wide_df = (long_df.pivot(index=['iso3', 'year'], columns='metric', values='value')
           .reset_index()
           .rename_axis(columns=None))
wide_df.head()"""),
        md("""## Exercises and source-documentation checkpoint

1. Change the successful merge to an inner join. Report whether the row count changes. **Expected output:** before/after counts plus one sentence.
2. Create a wide table with years as columns for one metric. **Expected output:** one row per ISO3 and one column per year.
3. Record source file, table grain, keys, join type, validation rule, unmatched-row count, and one merge risk.

Never describe a merge as successful only because Python produced a table."""),
    ])

    write("labs/lab-00-data-readiness/starter.ipynb", [
        md("# Lab 00: Data Readiness\n\n**Output:** saved notebook with a preview, summary, and test chart. Data are synthetic and for classroom use only. [Open in Colab](https://colab.research.google.com/github/GSIS-DS/data-science-ai-global-decision-making/blob/main/labs/lab-00-data-readiness/starter.ipynb)."),
        code(loader()),
        code("""import matplotlib
import seaborn
import sklearn
print('Shape:', df.shape)
print('Mean GDP growth:', round(df['gdp_growth'].mean(), 2))"""),
        code("""import matplotlib.pyplot as plt
ax = df.groupby('region')['gdp_growth'].mean().sort_values().plot(kind='barh', color='#3572A5')
ax.set_title('Environment test: average GDP growth by region')
ax.set_xlabel('Average annual GDP growth (%)')
ax.set_ylabel('')
plt.tight_layout()
plt.show()"""),
        md("## Completion note\n\nRestart the runtime and run all cells. Record whether it succeeded and where you saved the copy."),
    ])

    write("labs/lab-01-data-wrangling/starter.ipynb", [
        md("# Lab 01: Data Wrangling\n\n**Output:** inspected and transformed data plus a transformation log. [Open in Colab](https://colab.research.google.com/github/GSIS-DS/data-science-ai-global-decision-making/blob/main/labs/lab-01-data-wrangling/starter.ipynb)."),
        code(loader()),
        code("""profile = pd.DataFrame({'dtype': df.dtypes.astype(str), 'missing': df.isna().sum()})
display(profile)
print('Duplicate rows:', df.duplicated().sum())"""),
        md("## Tasks\n\n1. Make a copy and create one documented quality issue for practice.\n2. Correct it without changing the raw `df`.\n3. Create `trade_balance_usd_bn`.\n4. Filter a region and summarize by year."),
        code("""working = df.copy()
# Add your deliberate practice issue and correction here.
working['trade_balance_usd_bn'] = working['exports_usd_bn'] - working['imports_usd_bn']
assert working['trade_balance_usd_bn'].notna().all()
working.head()"""),
        code("""chosen_region = 'Europe & Central Asia'
summary = (working.loc[working['region'] == chosen_region]
           .groupby('year', as_index=False)['trade_balance_usd_bn'].mean()
           .round(2))
summary"""),
        md("## Transformation log\n\nComplete: **input issue -> change -> reason -> verification -> effect on interpretation**."),
    ])

    write("labs/lab-02-visualization/starter.ipynb", [
        md("# Lab 02: Visualization Critique and Revision\n\n**Output:** critique, revised accessible chart, and 3-5 sentence interpretation. [Open in Colab](https://colab.research.google.com/github/GSIS-DS/data-science-ai-global-decision-making/blob/main/labs/lab-02-visualization/starter.ipynb)."),
        code(loader()),
        code("""import matplotlib.pyplot as plt

country_values = df.loc[df['year'] == 2022, ['country', 'internet_users_percent']].head(5)
ax = country_values.plot(kind='bar', x='country', y='internet_users_percent', legend=False, color='red')
ax.set_ylim(80, 100)  # A truncated bar axis exaggerates differences.
ax.set_title('Internet use')
plt.show()"""),
        md("## Critique\n\nIdentify problems with scale, labels, scope, source, color, and what a reader could mistakenly conclude."),
        code("""ax = country_values.sort_values('internet_users_percent').plot(
    kind='barh', x='country', y='internet_users_percent', legend=False, color='#3572A5', figsize=(8, 4))
ax.set_xlim(0, 100)
ax.set_title('Internet use in five displayed countries, 2022')
ax.set_xlabel('Internet users (% of population)')
ax.set_ylabel('')
ax.text(0, -0.22, 'Source: synthetic course dataset; selected rows; classroom use only.', transform=ax.transAxes, fontsize=9)
plt.tight_layout()
plt.show()"""),
        md("## Interpretation\n\nWrite 3-5 sentences: direct observation, comparison, limitation, and what additional evidence a decision-maker would need. Do not claim causality."),
    ])

    write("labs/lab-03-llm-verification/starter.ipynb", [
        md("# Lab 03: LLM Verification\n\nAudit a prepared fictional model response; no external AI service is required. [Open in Colab](https://colab.research.google.com/github/GSIS-DS/data-science-ai-global-decision-making/blob/main/labs/lab-03-llm-verification/starter.ipynb)."),
        code(loader()),
        md("""## Prepared fictional AI output

> “In 2022, Europe & Central Asia had average inflation of 2.1%, the lowest of all regions. The code below proves that greater trade openness causes lower inflation.”

```python
df.groupby('region')['inflation'].min().sort_values()
```

Audit questions: Does the code filter 2022? Does `min()` calculate an average? Is the number correct? Can this dataset establish causation?"""),
        code("""check = (df.loc[df['year'] == 2022]
         .groupby('region', as_index=False)
         .agg(mean_inflation=('inflation', 'mean'),
              mean_trade_openness=('trade_openess_percent', 'mean'))
         .sort_values('mean_inflation'))
check.round(2)"""),
        code("""# Independent spot check for the named region
rows = df.loc[(df['year'] == 2022) & (df['region'] == 'Europe & Central Asia'),
              ['country', 'inflation']]
display(rows)
print('Recalculated mean:', round(rows['inflation'].mean(), 2))"""),
        md("## Audit record\n\nCreate a table with: claim/code element, check performed, result, correction, and remaining limitation. Then complete `AI_USE_TEMPLATE.md`, noting that the supplied response was prepared for the lab."),
    ])

    write("labs/lab-04-bounded-agent-workflow/starter.ipynb", [
        md("# Lab 04: Bounded-Agent Workflow\n\nQuestion -> defined data/tools -> analytical steps -> draft -> verification -> human decision. No paid API or autonomous agent is used. [Open in Colab](https://colab.research.google.com/github/GSIS-DS/data-science-ai-global-decision-making/blob/main/labs/lab-04-bounded-agent-workflow/starter.ipynb)."),
        code(loader()),
        code("""QUESTION = 'Which regions had the highest average trade openness in 2022?'
ALLOWED_COLUMNS = ['region', 'year', 'trade_openess_percent']

def draft_regional_comparison(data, year):
    scoped = data.loc[data['year'] == year, ALLOWED_COLUMNS].copy()
    summary = (scoped.groupby('region', as_index=False)['trade_openess_percent']
               .mean().sort_values('trade_openess_percent', ascending=False))
    leader = summary.iloc[0]
    draft = f"{leader['region']} ranks first in this synthetic dataset at {leader['trade_openess_percent']:.1f}%."
    return scoped, summary, draft

scoped, summary, draft = draft_regional_comparison(df, 2022)
display(summary.round(2))
print(draft)"""),
        code("""# Verification checkpoint
assert scoped['year'].eq(2022).all()
assert scoped['trade_openess_percent'].notna().all()
manual = scoped.loc[scoped['region'] == summary.iloc[0]['region'], 'trade_openess_percent'].mean()
assert abs(manual - summary.iloc[0]['trade_openess_percent']) < 1e-9
print('Verification passed. This checks calculation, not external validity or causality.')"""),
        md("## Human decision\n\nAccept, revise, or reject the draft. Address synthetic-data limits, whether ranking supports a recommendation, and what real source would be required. Complete the AI Workflow Card even if no generative model was used."),
    ])

    write("examples/good-visualization-example.ipynb", [
        md("# Good Visualization Example\n\nA compact model of accurate scale, labels, source note, accessible color, and bounded interpretation."),
        code(loader()),
        code("""import matplotlib.pyplot as plt
summary = df.groupby('region')['gdp_growth'].mean().sort_values()
ax = summary.plot(kind='barh', color='#3572A5', figsize=(8, 4))
ax.set_title('Average GDP growth by region, 2020-2022')
ax.set_xlabel('Average annual GDP growth (%)')
ax.set_ylabel('')
ax.text(0, -0.22, 'Source: synthetic course dataset; classroom use only.', transform=ax.transAxes, fontsize=9)
plt.tight_layout()
plt.show()
summary.round(2)"""),
        md("**Interpretation:** The chart describes regional averages in this small synthetic dataset. It does not establish that region causes growth differences, nor should it guide real policy."),
    ])

    write("examples/misleading-visualization-example.ipynb", [
        md("# Misleading Visualization and Revision\n\nCompare an exaggerated truncated-axis bar chart with a corrected display."),
        code("""import matplotlib.pyplot as plt
countries = ['South Korea', 'Japan', 'Germany']
values = [1.7, 1.9, 1.7]
fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=False)
axes[0].bar(countries, values, color='red')
axes[0].set_ylim(1.5, 2.0)
axes[0].set_title('Misleading: truncated bar axis')
axes[1].bar(countries, values, color='#3572A5')
axes[1].set_ylim(0, 2.1)
axes[1].set_title('Revised: zero baseline')
for ax in axes:
    ax.set_ylabel('GDP growth (%)')
    ax.tick_params(axis='x', rotation=25)
fig.suptitle('Illustrative fictional values')
plt.tight_layout()
plt.show()"""),
        md("The left chart exaggerates a 0.2 percentage-point difference. The right chart preserves a zero baseline appropriate for bars. A dot plot could also show small differences without encoding values as bar lengths."),
    ])

    write("examples/reproducible-notebook-example.ipynb", [
        md("# Reproducible Notebook Example\n\nQuestion, source, code, checks, output, interpretation, and limitations are kept together."),
        md("## Question\n\nHow do average synthetic GDP growth and inflation compare by region from 2020-2022?"),
        code(loader()),
        code("""required = {'region', 'gdp_growth', 'inflation'}
assert required.issubset(df.columns)
assert df[list(required)].notna().all().all()
summary = df.groupby('region')[['gdp_growth', 'inflation']].mean().round(2)
summary"""),
        md("## Interpretation and limitations\n\nReport one direct comparison from the displayed table. These synthetic regional means describe only the teaching file; they are not official estimates, causal evidence, or a basis for decisions."),
    ])

    write("templates/assignment-template/starter.ipynb", [
        md("# Assignment Title\n\n**Question:** [focused analytical question]\n\n**Expected outputs:** [list]\n\n**Data source and license:** [source, retrieval date, license]\n\n**Run instructions:** [Colab or repository steps]"),
        code("""import pandas as pd
import matplotlib.pyplot as plt

# Load documented data here. Avoid machine-specific absolute paths.
"""),
        md("## Inspect and verify\n\nRecord shape, columns, types, missingness, duplicates, and relevant scope checks."),
        code("# Your inspection and validation code here"),
        md("## Analysis and outputs\n\nKeep each major analytical step next to a short explanation."),
        code("# Your analysis here"),
        md("## Interpretation and limitations\n\nSeparate direct observations from explanations and recommendations. Complete `AI_USE.md` when material AI use applies."),
    ])


if __name__ == "__main__":
    main()
