from flask import Flask, request, jsonify
import os
import pandas as pd
from werkzeug.utils import secure_filename
from plot import *
app = Flask(__name__)

# Set up file upload directory
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/process-file', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    plot_type = request.form.get('plotType')
    timeInterval = request.form.get('timeInterval')
    startdate = request.form.get('startDate')
    endDate = request.form.get('endDate')
    predict_date = request.form.get('predict_date')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    df = pd.read_excel(file_path)
    graph = Graph(df,startdate, endDate,predict_date,timeInterval)
    basic_x,basic_y = graph.basic_plot()
    if plot_type == 'hyperbolic':
        ori_x,ori_y,ori_x2,ori_y2, reg_x, reg_y,reg_y2 =graph.hyperbolic_plot()
        return jsonify({'basic_x': basic_x.tolist(), 'basic_y': basic_y.tolist(), 'ori_x': ori_x.tolist(), 'ori_y': ori_y.tolist(), 'ori_x2': ori_x2.tolist(), 'ori_y2': ori_y2.tolist(),'reg_x': reg_x.tolist(),'reg_y': reg_y.tolist(),'reg_y2':reg_y2.tolist()})


    os.remove(file_path)
    return jsonify({'message': plot_type}), 200


if __name__ == '__main__':
    app.run(port=5000)