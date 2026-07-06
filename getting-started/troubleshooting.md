# Troubleshooting

## Common Issues

### Colab Won't Open Notebook

- Verify the repository name is correct
- Check your internet connection
- Try refreshing the page
- Clear browser cache if needed

### Package Installation Errors

In Colab, install missing packages:
```python
!pip install pandas matplotlib seaborn
```

### CSV File Not Found

Use the correct path in Colab:
```python
from google.colab import files
files.download('/content/')  # For downloading
```

Or load directly from URL:
```python
import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/GSIS-DS-Fall-2026/data-science-ai-global-decision-making/main/data/sample/global_indicators_sample.csv')
```

### Kernel Keeps Dying

- Reduce data size
- Simplify operations
- Try: Runtime -> Restart and run all

### Can't Save to GitHub

- Verify you have a GitHub account
- Check you're in the right repository
- Confirm you have write access

## Getting Help

1. Check this file
2. Review the Binder guide
3. Ask in Slack (link to be announced)
4. Email the instructor