This folder holds REAL evaluation results used by the "Model performance" page.
It is intentionally empty until you generate them:

    python scripts/evaluate_model.py --csv path\to\test.csv --images path\to\test_images

That creates: confusion_matrix.csv, classification_report.txt, metrics.json
The website shows them automatically. Do not edit these files by hand.
