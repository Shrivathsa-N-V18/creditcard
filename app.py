from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
from datetime import date
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('minip.pkl','rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('Index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        AATD = float(request.form['AATD'])
        Transaction_Amount=float(request.form['Transaction_Amount'])
        Decline_Count=int(request.form['Decline_Count'])
        Daily_Charge_Back_Amount=int(request.form['Daily_Charge_Back_Amount'])
        Six_Daily_Charge_Back_Amount=float(request.form['Six_Daily_Charge_Back_Amount'])
        Six_Daily_Charge_Back_Amount_Freq=int(request.form['Six_Daily_Charge_Back_Amount_Freq'])
        Average=float(request.form['Average'])
        Declined=int(request.form['Declined'])
        ForeignTransaction=int(request.form['ForeignTransaction'])
        RiskCountry = int(request.form['RiskCountry'])
        arr=np.array([AATD,Transaction_Amount,Declined,Decline_Count,ForeignTransaction,RiskCountry,Daily_Charge_Back_Amount,Six_Daily_Charge_Back_Amount,Six_Daily_Charge_Back_Amount_Freq,Average])
        arr=arr.reshape(1,10)
        prediction=model.predict(arr)[0]
        output=prediction
        print(output)
        if output==np.int64(0):
            return render_template('Index.html',prediction_text="Not A Fraud Transaction")
        else:
            return render_template('Index.html',prediction_text="Fraud Transaction")
    else:
        return render_template('Index.html')

if __name__=="__main__":
    app.run(debug=True)

