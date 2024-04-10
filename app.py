import pandas as pd
from flask import Flask,render_template,request,redirect,url_for, send_file
import pickle
import os

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')


data=pd.read_csv("cleanedCancerDate.csv")
pipe=pickle.load(open('LogisticRegression_cancer.pkl','rb'))

predetermined_columns = ['radius_mean', 'texture_mean', 'smoothness_mean', 'compactness_mean',
       'concave_points_mean', 'symmetry_mean', 'fractal_dimension',
       'radius_se', 'texture_se', 'smoothness_se', 'compactness_se',
       'concavity_se', 'concave_points_se', 'symmetry_se',
       'fractal_dimension_se', 'smoothness_worst', 'concavity_worst',
       'symmetry_worst', 'fractal_dimension_worst', 'N Stage', '6th Stage', 'differentiate']


@app.route('/home')
@app.route('/report')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/templates/home.html')
def temphome():
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/templates/about.html')
def temphom():
    return redirect(url_for('about'))

@app.route('/bulkPredict')
def bulkPredict():
    return render_template('bulkPredict.html',columns = predetermined_columns)

@app.route('/templates/bulkPredict.html')
def temph():
    return redirect(url_for('bulkPredict'))

@app.route('/predict')
def report():
    
    elements=[
        'radius_mean', 'texture_mean', 'smoothness_mean', 'compactness_mean',
       'concave_points_mean', 'symmetry_mean', 'fractal_dimension',
       'radius_se', 'texture_se', 'smoothness_se', 'compactness_se',
       'concavity_se', 'concave_points_se', 'symmetry_se',
       'fractal_dimension_se', 'smoothness_worst', 'concavity_worst',
       'symmetry_worst', 'fractal_dimension_worst'
    ]

    return render_template('pred.html',elements=elements)
    # return render_template('index.html')

@app.route('/predict',methods=['Get','Post'])

def prediction():
    
    elements=[
        'radius_mean', 'texture_mean', 'smoothness_mean', 'compactness_mean',
       'concave_points_mean', 'symmetry_mean', 'fractal_dimension',
       'radius_se', 'texture_se', 'smoothness_se', 'compactness_se',
       'concavity_se', 'concave_points_se', 'symmetry_se',
       'fractal_dimension_se', 'smoothness_worst', 'concavity_worst',
       'symmetry_worst', 'fractal_dimension_worst',
        "N_Stage",
        "6th_Stage",
        "Differentiate"
    ]
    
    result=[]
    for i in elements:
       if i=="N_Stage" or i=="6th_Stage" or i=="Differentiate" :
          result.append(request.form.get(i))
       else:
          result.append(float(request.form.get(i)))
    
    # print(result)
    input=pd.DataFrame([result],columns=['radius_mean','texture_mean','smoothness_mean','compactness_mean','concave_points_mean','symmetry_mean','fractal_dimension','radius_se','texture_se','smoothness_se','compactness_se','concavity_se','concave_points_se','symmetry_se','fractal_dimension_se','smoothness_worst','concavity_worst','symmetry_worst','fractal_dimension_worst','N Stage','6th Stage','differentiate'])
    # print(input)
    prediction=pipe.predict(input)[0]

    return "The Diagnosis of Cancer is" + (" Malignant " if (prediction==1) else  " Benign ")

@app.route('/templates/predict.html')
def temphe():
    return redirect(url_for('report'))

@app.route('/bulkPredict', methods=['POST'])
def bulkPrediction():
    # Get the uploaded file
    file = request.files['file']
    if not file:
        return render_template('bulkPredict.html', message='No file uploaded')

    # Check file extension
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        print(df.head())
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        return render_template('bulkPredict', message='Invalid file format')

    df = df[predetermined_columns]
    X = df

    # Make predictions
    predictions = pipe.predict(X)
    # Return results
    df['Predictions'] = predictions
    output_file = 'predictions.csv'
    Predictionsonly_file = 'onlyPredictions.csv'
    df.to_csv(output_file, index=False)
    Dfpredictions = pd.DataFrame(predictions)
    Dfpredictions.to_csv(Predictionsonly_file, index=False)

    return render_template('result.html', predictions=predictions, output_file=output_file, Predictionsonly_file=Predictionsonly_file)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__=="__main__":
    app.run(port=5550,debug=True)