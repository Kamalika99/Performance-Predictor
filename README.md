# Student Performance Prediction

## End-to-End ML Project

## Overview

This project is an end-to-end machine learning web application that predicts a
student's final grade. It covers data ingestion, preprocessing, model training,
and serving predictions through a Flask web interface.

---

## Dataset

The project uses the provided `data.csv` (the UCI/Kaggle "Student Performance"
dataset for a Portuguese-language course): 649 rows and 33 columns, no missing
values.

- **Target column: `G3`** — the student's final grade, on a 0–20 scale.
- **Features (32 columns):**
  - Numerical: `age`, `Medu`, `Fedu`, `traveltime`, `studytime`, `failures`,
    `famrel`, `freetime`, `goout`, `Dalc`, `Walc`, `health`, `absences`,
    `G1` (first period grade), `G2` (second period grade)
  - Categorical: `school`, `sex`, `address`, `famsize`, `Pstatus`, `Mjob`,
    `Fjob`, `reason`, `guardian`, `schoolsup`, `famsup`, `paid`, `activities`,
    `nursery`, `higher`, `internet`, `romantic`

---

## ML Pipeline

```
data.csv
   |
Data Ingestion         -> train/test split, saved to artifacts/
   |
Data Transformation     -> impute + scale numeric, impute + one-hot encode categorical
   |
Model Training           -> trains and compares several regressors, saves the best one
   |
artifacts/model.pkl, artifacts/preprocessor.pkl
   |
Prediction Pipeline     -> loads the saved model/preprocessor, transforms new input
   |
Flask Application       -> web form collects input, shows the predicted G3
```

Model training compares Linear Regression, Ridge, K-Neighbors, Decision Tree,
Random Forest, Gradient Boosting, XGBoost, CatBoost, and AdaBoost regressors on
R2 score, and saves the best-performing model.

---

## Project Structure

```
.
├── application.py               # Flask web application
├── main.py                      # ML pipeline orchestration (training)
├── setup.py                     # Python package configuration
├── requirements.txt             # Dependencies
├── data.csv                     # Source dataset
├── artifacts/                   # Generated: train.csv, test.csv, preprocessor.pkl, model.pkl
├── templates/
│   ├── index.html               # Landing page
│   └── home.html                # Prediction form and result
├── test_application.py          # Flask route tests
└── src/
    └── mlproject/
        ├── components/          # Data ingestion, transformation, model training
        ├── pipelines/           # Prediction pipeline (CustomData, PredictPipeline)
        ├── exception.py         # Custom exception class
        ├── logger.py            # Logging utility
        └── utils.py             # save_object / load_object / evaluate_models
```

---

## Technologies Used

- Python
- Flask
- Scikit-learn, XGBoost, CatBoost
- Pandas, NumPy
- HTML/CSS
- Logging and Exception Handling

---

## Installation

```bash
pip install -r requirements.txt
```

## Training the Model

Runs the full data ingestion -> transformation -> training pipeline and saves
`artifacts/preprocessor.pkl` and `artifacts/model.pkl`:

```bash
python main.py
```

## Running the Flask Application

```bash
python application.py
```

Then open `http://localhost:5000/` in a browser, click through to the
prediction form, fill in a student's details, and submit to see the predicted
final grade (G3).

---

## Author

**Kamalika Kommineni**
Email: kamalikak99@gmail.com
