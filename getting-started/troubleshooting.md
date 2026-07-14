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

Course notebooks should load the sample data directly from its public URL:
```python
import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/GSIS-DS/data-science-ai-global-decision-making/main/data/sample/global_indicators_sample.csv')
```

If you cloned the repository, run notebooks from the repository root or use the documented loader in the notebook. Do not use `files.download()` to load a CSV; that function downloads a file from Colab to your computer.

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
