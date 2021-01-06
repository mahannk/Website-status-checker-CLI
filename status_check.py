# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 12:04:36 2020

@author: Mahan

Website Status Checker

Main fuction modified from "Python 3 - Command Line Arguments" obtained "from https://www.tutorialspoint.com/python3/python_command_line_arguments.htm"
"""
import requests
import time
import concurrent.futures
import sys, getopt, os
import pandas as pd


def main(argv):
    
    input_file = None;
    output_file = None;
    
    try: 
        opts, args = getopt.getopt(argv, 'hi:o:t:')
    except Exception as e:
        print(e)
        print('status_check.py -i <inputFile.xlsx> -o [outputFile.xlsx] -t [read timeout]')
        sys.exit(2)
    
    timeout = 10
    for opt, arg in opts:
        if opt in ['-i']:
            input_file = arg
        elif opt in ['-o']:
            output_file = arg
        elif opt in ['-t']:
            try:
                timeout = int(arg)
            except:
                pass
        else:
            raise ValueError('Something went wrong')
            print('status_check.py -i <inputFile.xlsx> -o [outputFile.xlsx] -t [read timeout]')
       
    if not input_file: # input is not provided
        print('status_check.py -i <inputFile.xlsx> -o [outputFile.xlsx] -t [read timeout]')
    else:
        if not output_file: # if no output_file provide, output_file becomes input_file
            output_file = input_file
            
        if not input_file.endswith('.xlsx'):
            input_file += '.xlsx'
        if not output_file.endswith('.xlsx'):
            output_file += '.xlsx'    
        
        if os.path.exists(input_file): # if the input file exist  
            print(f'Input file is : {input_file}\nOutput file is : {output_file}')
            rs(input_file, output_file, timeout)
        else: 
            print(f"Input file '{input_file}' does not exist")
            sys.exit(0)
    
def rs(in_file, out_file, time_out):
    
    df = pd.io.excel.read_excel(in_file, sheet_name=0, header=None) # read input xlsx file
    
    if 'URL' in df.loc[0].values: # replacing Header with Top row
        df.columns = df.iloc[0]
        df = df[1:]
    else:
        df = pd.DataFrame(df.iloc[:,0])
        df.columns = ['URL']
    
    
    df_out = pd.DataFrame()
    
    def checking_url(url, timeout=5):
        url = url[1]
        try:
            r = requests.get(url.URL, timeout=time_out) # request 
            if len(r.history) > 0: # url is redirected
                url['Status_Code'] = r.history.pop().status_code
                url['Redirected_URL'] = r.url
            
            else:
                url['Status_Code'] = r.status_code
                url['Redirected_URL'] = None
            
        except Exception as e:
            print(e)
            url['Status_Code'] = None
            url['Redirected_URL'] = None
            
        return url
            
        
    
    
    t1 = time.perf_counter()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        rs = executor.map(checking_url, df.iterrows())
        
        df_out = df_out.append([r for r in rs])
    
    
    df_out.to_excel(out_file, index=False)
    
    t2 = time.perf_counter()
    print(f'Finished in {round(t2-t1)} seconds')
    
    
if __name__ == "__main__":
   main(sys.argv[1:])    