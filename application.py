from flask import Flask, request, render_template

from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
from src.mlproject.pipelines.prediction_pipeline import CustomData, PredictPipeline

application = Flask(__name__)

app = application

# Fields match the actual data.csv schema (student performance dataset),
# minus the target column G3.
CATEGORICAL_FIELDS = [
    'school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 'Fjob',
    'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 'activities',
    'nursery', 'higher', 'internet', 'romantic',
]

NUMERIC_FIELDS = [
    'age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures',
    'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health',
    'absences', 'G1', 'G2',
]

REQUIRED_FIELDS = CATEGORICAL_FIELDS + NUMERIC_FIELDS


## Route for a home page

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')

    # --- Basic input validation ---
    missing = [f for f in REQUIRED_FIELDS if not request.form.get(f)]
    if missing:
        return render_template(
            'home.html',
            results=f"Missing required field(s): {', '.join(missing)}"
        )

    try:
        numeric_values = {f: int(request.form.get(f)) for f in NUMERIC_FIELDS}
    except ValueError:
        return render_template(
            'home.html',
            results="Numeric fields must contain whole numbers."
        )

    try:
        data = CustomData(
            school=request.form.get('school'),
            sex=request.form.get('sex'),
            address=request.form.get('address'),
            famsize=request.form.get('famsize'),
            Pstatus=request.form.get('Pstatus'),
            Mjob=request.form.get('Mjob'),
            Fjob=request.form.get('Fjob'),
            reason=request.form.get('reason'),
            guardian=request.form.get('guardian'),
            schoolsup=request.form.get('schoolsup'),
            famsup=request.form.get('famsup'),
            paid=request.form.get('paid'),
            activities=request.form.get('activities'),
            nursery=request.form.get('nursery'),
            higher=request.form.get('higher'),
            internet=request.form.get('internet'),
            romantic=request.form.get('romantic'),
            age=numeric_values['age'],
            Medu=numeric_values['Medu'],
            Fedu=numeric_values['Fedu'],
            traveltime=numeric_values['traveltime'],
            studytime=numeric_values['studytime'],
            failures=numeric_values['failures'],
            famrel=numeric_values['famrel'],
            freetime=numeric_values['freetime'],
            goout=numeric_values['goout'],
            Dalc=numeric_values['Dalc'],
            Walc=numeric_values['Walc'],
            health=numeric_values['health'],
            absences=numeric_values['absences'],
            G1=numeric_values['G1'],
            G2=numeric_values['G2'],
        )

        pred_df = data.get_data_as_data_frame()
        logging.info(f"Input dataframe for prediction:\n{pred_df}")

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        logging.info(f"Prediction completed successfully: {results[0]}")
        return render_template('home.html', results=round(float(results[0]), 2))

    except Exception as e:
        logging.error("Prediction failed", exc_info=True)
        return render_template(
            'home.html',
            results="Something went wrong while generating the prediction. Please try again."
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
