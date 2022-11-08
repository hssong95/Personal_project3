from flask import Flask, render_template, Blueprint, request
from markupsafe import escape
from werkzeug.datastructures import MultiDict
import pickle
import pandas as pd
import numpy as np

# from project_app.routes import 
app = Flask(__name__)

@app.route('/')
def index():
    # if request.method == 'POST':
    head = '창업자를 위한 지역, 업종 별 전기료 예측 서비스'
    head2 = 'Section 3'
    return render_template('service_input_box.html', head=head, head2=head2)

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/result', methods=['POST'])
# def get_value():
    
#     input_metro = request.form.get("metro_id")
#     input_metro = str(input_metro)
#     print(input_metro)
#         # val = request.form
#         # print(val)
#     # return render_template('value_receiver.html', result = val)
#     return render_template('value_receiver.html')

        
# @app.route('/metro/<metro_name>')
# def get_metro(metro_name):
#     global input_metro
#     input_metro = metro_name
#     print(input_metro)
#     return f'선택하신 도는 {metro_name}입니다'

@app.route('/form', methods=['POST'])
def form():
    metro_name= request.form.get("metro_name")
    city_name= request.form.get("City_name")
    biz_name= request.form.get("Biz_name")
    electric= request.form.get("Electric_num")
    
    feature=['year','metro','city','biz','power_per_cust']
    x_test = pd.DataFrame(columns=feature)
    x_test.loc[0]=[2023,metro_name,city_name,biz_name,electric]
    model = None
    with open('model.pkl','rb') as pickle_file:
        model = pickle.load(pickle_file)

    y_pred=model.predict(x_test)
    y_pred=int(y_pred)

    return render_template('form.html', pred=y_pred, metro=metro_name,city=city_name,biz=biz_name,elec=electric)

if __name__ =='__main__':
    app.run(debug=True)