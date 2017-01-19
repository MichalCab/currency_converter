# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 17:06:55 2017

@author: joe
"""
#from babel.numbers import get_currency_code
#from sys import argv
from forex_python.converter import CurrencyCodes
from yahoo_finance import Currency
from forex_python.converter import CurrencyRates
#get_currency_code('$', locale='en_US')
import sys
import getopt
import json


def usage():
    print("USAGE:\n mandatory options :\n -a --amount <number> :amount of money to convert \n -i --input_currency <symbol or 3 letters code> : the currency to convert \n \n optionnal:\
    \n -h : this help \n -o --output_currency <symbol or 3 letters code> : the target currency")


#Small function that create a dictionnary to convert symbols to currency code (using forex_python why not...it works)
def get_ccode():
    code_trans = CurrencyCodes()
    code_symb={}
    c = CurrencyRates()
    for code in c.get_rates('USD').keys():
        code_symb[code]=code_trans.get_symbol(code)
    code_symb[u'USD']=u'$'
    return code_symb
    
#main function using the aguments
def main(argv):   
    #get the symbol/code dic
    trans_code_symb=get_ccode()

    try:                                
        opts, args = getopt.getopt(argv, "ha:i:o:", ["help","amount=", "input_currency=","output_currency="])
    except getopt.GetoptError:
        print "error"
        usage()
        sys.exit(2)
    
    input_dir={}
    output_dir={}
    out_cur=[]
    for o, a in opts:
            #help
            if o in ("-h","--help"):
                usage()
                sys.exit(2)
                
            #save the amount
            if o in ("-a","--amount"):
                input_dir["amount"]=a
                
            #save the input currency, convert the symbol to code if necessary
            elif o in ("-i", "--input_currency"):
                #better safe than sorry
                a=a.decode("utf8")
                for code,symbol in trans_code_symb.items():
                    if symbol==a:
                        a=code
                input_dir["currency"]=a
                
            #the same for output currency
            elif o in ("-o", "--output_currency"):
                #better safe than sorry
                a=a.decode("utf8")
                for code,symbol in trans_code_symb.items():
                    if symbol==a:
                        a=code
                out_cur.append(a)
            
            else:
                assert False, "unhandled option"
      
    #check if the user gave an existing code          
    code_exists=0
    incorrect_code=""
    #check for the output currency if available
    if len(out_cur)==0:
        code_exists+=1
    else:
        if out_cur[0] in trans_code_symb.keys():
            code_exists+=1
        else:
            incorrect_code=out_cur[0]
    #check the input currency
    if input_dir["currency"] in trans_code_symb.keys():
        code_exists+=1
    else:
        incorrect_code=input_dir["currency"]
    #exit if the code is incorrect
    if code_exists<2:
        print "Currency code "+incorrect_code+" does not exist."
        sys.exit(2)
        
       
    #both -a and -i are mandatory, show help it one is missing
    if len(input_dir)!=2:
        print "\n ERROR: one input argument is missing \n"
        usage()
        sys.exit(2)
    
   #if no output currency convert for every currency
    if len(out_cur)==0 :
        for cur in trans_code_symb.keys():
             if cur!=input_dir["currency"]:
                 icur_ocur = Currency(input_dir["currency"]+cur)
                 output_dir[cur]=float(icur_ocur.get_rate())*float(input_dir['amount'])
                 
    #else do the job for just the output currency
    else:
        icur_ocur = Currency(input_dir["currency"]+out_cur[0])
        output_dir[out_cur[0]]=float(icur_ocur.get_rate())*float(input_dir['amount'])
        
    #prepare the final json
    final_dir={}
    final_dir["input"]=input_dir 
    final_dir["output"]=output_dir
    final_json=json.dumps(final_dir)
    #proudly print the result
    print final_json
    
    
    
if __name__ == "__main__":
   main(sys.argv[1:])
    

