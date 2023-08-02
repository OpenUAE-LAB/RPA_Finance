from flask import Flask, render_template, request, jsonify, redirect, Response, send_file
import pandas as pd 
import os
import time
import shutil
import datetime
#from gcaa import GCAA

def GCAA():
    #################################################################
    
    # Rename Daily Traffic files to be DML_01012023
    files = glob.glob("app/Daily_Traffic/*")

    for file in files:
        df = pd.read_csv(file)
        date = df['ENTRY DATE'][0]
        matches = list(datefinder.find_dates(date))

        day = str(matches[0].day)
        Month = str(matches[0].month)

        if len(Month) == 1:
            Month = '0' + Month

        if len(day) == 1:
            day = '0' + day
        year = str(matches[0].year)  
        file_date =  day + Month  + year

        new_name = 'app/Daily_Traffic/'+'DML_'+file_date + '.csv'

        os.rename(file, new_name)
    #################################################################

    files = glob.glob("app/NO DML/*")

    for file in files:
        if "Non FIR Movements" in file:
            file_name = "Non FIR Movements - " + file.split('-')[-1].replace(" ","")
        else:
            file_name = "NO DML " + file.split(" ")[-1]

        ####################################################################################
        # Get date from file name in format ddmmyyyy for example 01012023
        matches = list(datefinder.find_dates(file_name))

        day = str(matches[0].day)
        Month = str(matches[0].month)

        if len(Month) == 1:
            Month = '0' + Month

        if len(day) == 1:
            day = '0' + day
        year = str(matches[0].year)  
        file_date =  day +  Month  + year
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        # Convert NO DML pdf files to xlsx
        if "Non FIR Movements" in file:

            # Read a PDF File
            df = tabula.read_pdf(file, pages='all')
            # convert PDF into CSV
            tabula.convert_into(file, 'nonradar.csv', output_format="csv", pages='all')

            ###############################################################################
            

            # open the CSV file
            with open('nonradar.csv', 'r') as csvfile:
                # create a CSV reader object
                reader = csv.reader(csvfile)

                # loop through each row in the CSV file
                data = []
                for row in reader:
                    # print each row
                    if len(row)  ==6 and 'CALLSIGN' not in row:
                        data.append(row)
            #             print(row)
            ##############################################################################            
            daf = pd.DataFrame(data , columns = [ "Callsign", "A/C", "ADEP" , "ATD", 'ADES',"ATA"])
            

            daf.insert(0, 'Date', day + '-' + Month  +'-'+ year)
            

#             daf['Date'] = pd.to_datetime(daf['Date'], format='%d-%m-%Y').dt.strftime('%d%m%Y')


            daf.to_excel(file_name.replace(".pdf", ".xlsx"), index=False)
    
       
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################   
        # Part 3: Create Radar Excel

        # Get the correct DML file name from NO DML file. So, we can compare each day separatly
        if "Non FIR Movements" in file:
            DML_file_name = "Daily_Traffic_" + file.split('-')[-1].replace(" ","").replace('.pdf','')

        else: 
            DML_file_name = "Daily_Traffic_" + file.split(" ")[-1].replace(".pdf", "")[:-2]+ str(matches[0].year) # use [:-2], so we may have months with more than 3 letters

        ##############################################################
        df_Radar = pd.read_csv("app/Daily_Traffic/DML_"+file_date+'.csv')

        df_Radar = df_Radar.rename(columns={'CALLSIGN CODE': 'Callsign', 'AIRCRAFT CODE': 'A/C', 'DEPARTURE': 'DEPATURE','DESTINATION': 'DESTINATION'})

        df_Radar.drop_duplicates(inplace = True)                  # Drop Duplicates from Radar data, to avoid duplicates in duplicate file. Added in 17-Feb-2023

        df_Radar.to_excel(DML_file_name + ".xlsx")
        
        
        
        
        
        ###########################################################################################################
        ###########################################################################################################
        ###########################################################################################################
        # Part 2: Validate NO DML data with Callsign data to correct wrong A/C values
#         df_Callsign_aircraftType = pd.read_excel("Callsign vs Aircraft type.xlsx")
        
        df_NON_Radar = pd.read_excel(file_name.replace(".pdf", ".xlsx"))

        for i in range(len(df_NON_Radar)):
            for j in range(len(df_Radar)):
                if df_NON_Radar['Callsign'][i] == df_Radar['Callsign'][j]:
                    df_NON_Radar.loc[i, 'A/C'] = df_Radar.loc[j, 'A/C']     # Use this line to avoid the warning



        df_NON_Radar.to_excel(file_name.replace(".pdf", ".xlsx"),  index=False)
        #########################################################################################################
        #########################################################################################################
        #########################################################################################################
        # Adjust Date Format

        # read the Excel file into a pandas dataframe
        df = pd.read_excel(file_name.replace(".pdf", ".xlsx"))

        # # convert the date column to datetime format
        df['Date'] = day + '-' +Month  + '-' + year 
        df['Date'] = pd.to_datetime(df['Date'] , dayfirst  = True)

        # # convert the date format to ddmmyyyy
        df['Date'] = df['Date'].dt.strftime('%d%m%Y')

        # create an ExcelWriter object and write the dataframe to a new Excel file
        writer = pd.ExcelWriter(file_name.replace(".pdf", ".xlsx"), engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        # set the date format for the date column in the Excel file
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        date_format = workbook.add_format({'num_format': 'ddmmyyyy'})
        worksheet.set_column('A:A', None, date_format)

        # save the Excel file
        writer.close()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        # Part 4: Separate NO DML csv file to duplicates and Non-Duplicates 
        df_NON_Radar = pd.read_excel(file_name.replace(".pdf", ".xlsx") , dtype=str )        
        df_Radar = pd.read_excel(DML_file_name + ".xlsx")

        duplicates_Callsign = []
        duplicates_AcType = []
        duplicates_Depa = []
        duplicates_Des = []
        duplicates_Date = []
        duplicates_ATD = []
        duplicates_ATA = []
        drop_rows = []

        # Updated Part Start
        ###################################################        12 Duplicates ,   17 Non Duplicates
        for i in range (len(df_NON_Radar)):
            flag = True
            for j in range(len(df_Radar)):  
                if  ((df_Radar['Callsign'][j] == df_NON_Radar['Callsign'][i] and df_Radar['A/C'][j] == df_NON_Radar['A/C'][i] and df_Radar['DEPATURE'][j] == df_NON_Radar['ADEP'][i] and df_Radar['DESTINATION'][j] == df_NON_Radar['ADES'][i] ) or (df_Radar['Callsign'][j] == df_NON_Radar['Callsign'][i] and df_Radar['A/C'][j] == df_NON_Radar['A/C'][i] and df_Radar['ENTRY FIX'][j] == df_NON_Radar['ADEP'][i] and df_Radar['EXIT FIX'][j] == df_NON_Radar['ADES'][i] )) and flag:                      
                    duplicates_Callsign.append(df_NON_Radar['Callsign'][i])
                    duplicates_AcType.append(df_NON_Radar['A/C'][i])
                    duplicates_Depa.append(df_NON_Radar['ADEP'][i])
                    duplicates_Des.append(df_NON_Radar['ADES'][i])
                    duplicates_Date.append(df_NON_Radar['Date'][i])

                    duplicates_ATD.append(df_NON_Radar['ATD'][i])
                    duplicates_ATA.append(df_NON_Radar['ATA'][i])

                    drop_rows.append(i)
                    flag = False
        
        # Updated Part End          
        ########################################
        #Save Non Duplicates
#         df_NON_Radar.drop(index = drop_rows , inplace = True)
#         df_NON_Radar.to_csv( file_name.replace(".pdf", "")+'_Non_Duplicates.csv',  index=False , header=None)
        
        ########################################
        #Save Non Duplicates
        df_NON_Radar.drop(index = drop_rows , inplace = True)
        # df_NON_Radar.to_csv( 'Non_Duplicates.csv',  index=False , header=None)

        # create an ExcelWriter object and write the dataframe to a new Excel file
        writer = pd.ExcelWriter(file_name.replace(".pdf", "")+'_Non_Duplicates.xlsx', engine='xlsxwriter')
        df_NON_Radar.to_excel(writer, index=False, sheet_name='Sheet1', header = True)

        # set the date format for the date column in the Excel file
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        date_format = workbook.add_format({'num_format': 'ddmmyyyy'})
        worksheet.set_column('A:A', None, date_format)

        # save the Excel file
        writer.close()
        
        
        #######################################   
        # Save Duplicates
        data_dup = { "Date" : duplicates_Date , "Callsign": duplicates_Callsign ,"A/C": duplicates_AcType , "ADEP":  duplicates_Depa ,"ATD": duplicates_ATD ,"ADES": duplicates_Des , "ATA": duplicates_ATA}
        df_dup = pd.DataFrame(data = data_dup)
        # df_dup.to_csv('Duplicates.csv',  index=False , header=None)

        # create an ExcelWriter object and write the dataframe to a new Excel file
        writer = pd.ExcelWriter(file_name.replace(".pdf", "")+'_Duplicates.xlsx', engine='xlsxwriter')
        df_dup.to_excel(writer, index=False, sheet_name='Sheet1', header = True)

        # set the date format for the date column in the Excel file
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        date_format = workbook.add_format({'num_format': 'ddmmyyyy'})
        worksheet.set_column('A:A', None, date_format)

        # save the Excel file
        writer.close()

        
        #######################################
        os.remove('nonradar.csv')
        os.remove(DML_file_name + ".xlsx")
        
        
        
        ###########################################################
        # Remove Header and Time columns

        # All
        df = pd.read_excel(file_name.replace(".pdf", ".xlsx") , dtype = str)
        df = df.drop(['ATD', 'ATA'], axis=1)
        df.to_excel('app/output/'+file_name.replace(".pdf", ".xlsx") , index=False,  header = False)
        os.remove(file_name.replace(".pdf", ".xlsx"))

        # Duplicates
        df_dup = pd.read_excel(file_name.replace(".pdf", "")+'_Duplicates.xlsx' , dtype = str)
        df_dup = df_dup.drop(['ATD', 'ATA'], axis=1)
        df_dup.to_excel('app/output/'+file_name.replace(".pdf", "")+'_Duplicates.xlsx' , index=False,  header = False)
        os.remove(file_name.replace(".pdf", "")+'_Duplicates.xlsx')

        # Non Duplicates
        df_non_dup = pd.read_excel(file_name.replace(".pdf", "")+'_Non_Duplicates.xlsx' , dtype = str)
        df_non_dup = df_non_dup.drop(['ATD', 'ATA'], axis=1)
        df_non_dup.to_excel('app/output/'+file_name.replace(".pdf", "")+'_Non_Duplicates.xlsx' , index=False,  header = False)
        os.remove(file_name.replace(".pdf", "")+'_Non_Duplicates.xlsx')

def create_app():

    def delete_files_in_directory(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


    app = Flask(__name__)

    @app.route('/')
    def main_page():
        delete_files_in_directory('app/Daily_Traffic/')
        delete_files_in_directory('app/NO DML/')
        delete_files_in_directory('app/output/')

        if (os.path.exists('output_files.zip')):
            os.remove('output_files.zip')

        return render_template('Upload2.html')

    @app.route('/loading')
    def loading_page():
        return render_template('processing2.html')

    @app.route('/upload')
    def upload():
        return render_template('Upload2.html')

    @app.route('/processing')
    def processing_page():
        GCAA()
        return render_template('download2.html')

    @app.route('/reroute')
    def reroute():
        return redirect('/')

    # Enables admin to download all currently uploaded files
    @app.route('/download_output', methods = ['GET'])
    def output_download():
        if request.method == 'GET':
            shutil.make_archive('output_files', format='zip', root_dir='app/output')
            files_path = '../output_files.zip'
            return send_file(files_path, as_attachment=True)

    @app.route('/DML_file', methods = [ "POST"])
    def DML_file():
        if request.method == 'POST':
            f = request.files['file']
            file_path = "app/Daily_Traffic/"+f.filename
            f.save(file_path)
        return 'success'

    @app.route('/NON_DML_file', methods = [ "POST"])
    def NON_DML_file():
        if request.method == 'POST':
            f = request.files['file']
            file_path = "app/NO DML/"+f.filename
            f.save(file_path)
        return 'success'

    @app.route('/download')
    def download_page():
        return render_template('download2.html')

    # @app.route('/process')
    # def automation_process():
    #     # Add the python function to be used
    #     GCAA()
    #     return 'sucess'

    # Enables admin to delete the uploaded files from the system
    @app.route('/download_NONDML/<filename>', methods = ['GET'])
    def fileNON_download(filename):
        if request.method == 'GET':
            file_path = 'NO DML/' + str(filename) #Here can we unify the name of the
            return send_file(file_path, as_attachment=True)

    # Enables admin to delete the uploaded files from the system
    @app.route('/download_DML/<filename>', methods = ['GET'])
    def file_download(filename):
        if request.method == 'GET':
            file_path = 'Daily_Traffic/' + str(filename)
            return send_file(file_path, as_attachment=True)

    if __name__ == "__main__":
        app.run(debug=True)

    return app