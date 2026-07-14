# Contributing to the Course Repository

This public repository welcomes corrections and focused improvements to course materials. It must never contain student records, grading keys, API credentials, unreleased solutions, or copyrighted data that cannot be redistributed.

## Before Proposing a Change

1. Keep the finalized Spring 2027 sequence and assessment terminology consistent.
2. Preserve beginner-friendly Colab execution and the synthetic-data warning.
3. Avoid paid APIs and machine-specific paths.
4. Use existing folder and naming conventions so published links remain stable.

## Validation

From the repository root, run:

```bash
python scripts/build_course_notebooks.py
python scripts/verify_course.py
jupyter nbconvert --to notebook --execute notebooks/week-01/01_data_ai_evidence_global_decision_making.ipynb --output week-01-test.ipynb
```

For notebook changes, also test **Restart and run all** in a clean Colab runtime. Do not commit the generated test output.

## Review Expectations

A contribution should state its learner-facing purpose, identify affected weeks or assessments, and note any accessibility, licensing, or AI-use implications.
