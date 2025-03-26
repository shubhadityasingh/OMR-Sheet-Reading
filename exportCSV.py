import ftplib


def exportCSVFile(FTP_Path, FTP_Paper_ID, FTP_Student_ID):
    try: 
        ftp_split = FTP_Path.split("/")
        print(ftp_split[2])

        ftpServer = ftplib.FTP(ftp_split[2])  
        ftpServer.login()
        ftpServer.cwd(f'learn/OMR_Response/{FTP_Paper_ID}/OMR_Output')
        
        local_file_path = f'OMR_Output/{FTP_Student_ID}.csv'
        
        with open(local_file_path, 'rb') as file:
            ftpServer.storbinary(f'STOR {FTP_Student_ID}.csv', file)  
            ftpServer.quit()
            print("Sent Successfully")
        
        return (1, "success")
    except Exception as e:
        return (0, e)