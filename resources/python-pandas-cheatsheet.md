# Python/Pandas Cheatsheet

## Import and Load

```python
import pandas as pd
df = pd.read_csv('data.csv')
```

## Inspect

```python
df.head()       # First rows
df.info()       # Column types and missing
df.describe()   # Summary statistics
df.columns      # Column names
```

## Select

```python
df['column']           # Single column (Series)
df[['col1', 'col2']]   # Multiple columns (DataFrame)
df[df['col'] > 10]     # Filter rows
df.iloc[0:5]            # First 5 rows by position
```

## Transform

```python
df['new'] = df['col1'] + df['col2']  # New column
df['log_col'] = np.log(df['col'])     # Math
df.rename(columns={'old': 'new'})     # Rename
df.sort_values('col')                  # Sort
```

## Aggregate

```python
df.groupby('category')['value'].mean()
df.groupby('category').agg({'value': ['mean', 'std']})
```

## Export

```python
df.to_csv('output.csv', index=False)
```