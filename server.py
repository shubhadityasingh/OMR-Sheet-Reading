from flask import Flask, request, Response, jsonify
import csv
import io
import main_code, exportCSV

app = Flask(__name__)

@app.route('/', methods=['GET'])
def default():
    return Response('<h1>Hello there</h1>')


@app.route('/read_omr', methods=['POST'])
def run_omr_code():
    data = request.get_json()
    print(data)
    status, message = main_code.everything(data['FTP_Path'], data['FTP_Paper_ID'], data['FTP_Student_ID'])
    if status == 1:
        status, message = exportCSV.exportCSVFile(data['FTP_Path'], data['FTP_Paper_ID'], data['FTP_Student_ID'])
    
    print(status, message)
    return jsonify(status=status, message=message)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')