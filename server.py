from flask import Flask, request, Response
import csv
import io
import main_code, exportCSV

app = Flask(__name__)

@app.route('/', methods=['GET'])
def default():
    return Response('hello there')


@app.route('/read_omr', methods=['POST'])
def run_omr_code():
    data = request.get_json()
    print(data)
    omr_status, message = main_code.everything(data['FTP_Path'], data['FTP_Paper_ID'], data['FTP_Student_ID'])
    if omr_status == 1:
        export_status, message = exportCSV.exportCSVFile(data['FTP_Path'], data['FTP_Paper_ID'], data['FTP_Student_ID'])
    
    print(type(message), message)
    return Response(message)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')