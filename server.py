from flask import Flask, request, Response, jsonify
import csv
import io
import main_code, exportCSV
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def default():
    return jsonify(status=1, message="Get working")


@app.route('/omr', methods=['GET'])
def executeOMRReadingCode():
    FTP_Path = request.args.get('FTP_Path')
    print(FTP_Path)
    if FTP_Path == None or FTP_Path == '' or FTP_Path == ' ':
        FTP_Path = os.getenv('FTP_PATH')
    FTP_Paper_ID = request.args.get('FTP_Paper_ID')
    if FTP_Paper_ID == None:
        FTP_Paper_ID = ''
    FTP_Student_ID = request.args.get('FTP_Student_ID')
    if FTP_Student_ID == None:
        FTP_Student_ID = ''
    
    print(FTP_Path, ' | ', FTP_Paper_ID, ' | ', FTP_Student_ID)
    status, message = main_code.processOMR(FTP_Path, FTP_Paper_ID, FTP_Student_ID)
    print("01 | OMR Processing Status -- ", status, " | Message -- ", message)
    if status == 1:
        status, message = exportCSV.exportCSVFile(FTP_Path, FTP_Paper_ID, FTP_Student_ID)
        print("02 | CSV Exporting Status -- ", status, " | Message -- ", message)
    return jsonify(status=status, message=message)


@app.route('/batch_omr', methods=['GET'])
def executeBatchOMRReading():
    FTP_Path = request.args.get('FTP_Path')
    print(FTP_Path)
    if FTP_Path == None or FTP_Path == '' or FTP_Path == ' ':
        FTP_Path = os.getenv('FTP_PATH')
    FTP_Paper_ID = request.args.get('FTP_Paper_ID')
    if FTP_Paper_ID == None:
        FTP_Paper_ID = ''
    FTP_Batch_Name = request.args.get('FTP_Batch_Name')
    if FTP_Batch_Name == None:
        FTP_Batch_Name = ''
    
    print(FTP_Path, ' | ', FTP_Paper_ID, ' | ', FTP_Batch_Name)
    status, message = main_code.batchProcessOMR(FTP_Path, FTP_Paper_ID, FTP_Batch_Name)
    print("01 | OMR Processing Status -- ", status, " | Message -- ", message)
    if status == 1:
        status, message = exportCSV.exportBatchCSVFile(FTP_Path, FTP_Paper_ID, FTP_Batch_Name)
        print("02 | CSV Exporting Status -- ", status, " | Message -- ", message)
    
    if status == 1:
        status, message = main_code.batchDeleteImageFiles(FTP_Paper_ID)
        print("03 | Deleting Cached Images Status -- ", status, " | Message -- ", message)

    if status == 1:
        status, message = main_code.batchDeleteCSVFiles(FTP_Paper_ID)
        print("04 | Deleting Cached CSVs Status -- ", status, " | Message -- ", message)

    return jsonify(status=status, message=message)



@app.route('/read_omr', methods=['POST'])
def run_omr_code():
    data = request.get_json()
    print(data)
    status, message = main_code.processOMR(data['FTP_Path'], data['FTP_Paper_ID'], data['FTP_Student_ID'])
    if status == 1:
        status, message = exportCSV.exportCSVFile(data['FTP_Path'], data['FTP_Paper_ID'], data['FTP_Student_ID'])
    
    print(status, message)
    return jsonify(status=status, message=message)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')