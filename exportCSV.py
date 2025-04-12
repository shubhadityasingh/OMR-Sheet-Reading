import os
import ftplib
from dotenv import load_dotenv

load_dotenv()

def exportBatchCSVFile(FTP_Path, FTP_Paper_ID, FTP_Batch_Name):
    try: 
        ftp_host = os.getenv('FTP_HOST')
        ftp_user = os.getenv('FTP_USER')
        ftp_pass = os.getenv('FTP_PASS')

        ftp_file_path = os.getenv('FTP_FILE_PATH')

        batch_output_dir = os.path.join(os.getcwd(), 'Batch_OMR_Output', FTP_Paper_ID, FTP_Batch_Name + '.csv')

        with ftplib.FTP(host=ftp_host, user=ftp_user, passwd=ftp_pass) as ftpServer:
            ftpServer.login()
            # ftpServer.cwd(f'learn/OMR_Response/{FTP_Paper_ID}/OMR_Output')
            ftpServer.cwd(f'{ftp_file_path}/{FTP_Paper_ID}/OMR_Output')
            
            local_file_path = batch_output_dir
            
            with open(local_file_path, 'rb') as file:
                ftpServer.storbinary(f'STOR {FTP_Batch_Name}.csv', file)  
                ftpServer.quit()
                print("Sent Successfully")
        
        return (1, "success")
    except Exception as e:
        error_msg = str(e)
        return (0, error_msg)


def exportCSVFile(FTP_Path, FTP_Paper_ID, FTP_Student_ID):
    try: 
        ftp_split = FTP_Path.split("/")

        ftp_host = os.getenv('FTP_HOST') if os.getenv('FTP_HOST') != '' else split(split(ftp_split[2], '@')[-1], ':')[-1]
        ftp_user = os.getenv('FTP_USER')
        ftp_pass = os.getenv('FTP_PASS')

        ftp_file_path = os.getenv('FTP_FILE_PATH')

        with ftplib.FTP(host=ftp_host, user=ftp_user, passwd=ftp_pass) as ftpServer:
            ftpServer.login()
            # ftpServer.cwd(f'learn/OMR_Response/{FTP_Paper_ID}/OMR_Output')
            ftpServer.cwd(f'{ftp_file_path}/{FTP_Paper_ID}/OMR_Output')
            
            local_file_path = f'OMR_Output/{FTP_Student_ID}.csv'
            
            with open(local_file_path, 'rb') as file:
                ftpServer.storbinary(f'STOR {FTP_Student_ID}.csv', file)  
                ftpServer.quit()
                print("Sent Successfully")
        
        return (1, "success")
    except Exception as e:
        error_msg = str(e)
        return (0, error_msg)