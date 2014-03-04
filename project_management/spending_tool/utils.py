from datetime import *

def return_quarter_year():
    time=datetime.now()
    year=time.year
    month=time.month
    day=time.day	  
    if month==7 and day>=27:
    	quarter_number==1
    	year=year+1
    if month==8 or month==9:
    	quarter_number=1
    	year=year+1
    if month == 10 and day <27:
    	quarter_number=1
    	year=year+1
    if month==10 and day >= 26:
    	quarter_number=2
    	year=year+1
    if month==11 or month == 12:
    	quarter_number=2
    	year=year+1
    if month==1 and day <26:
    	quarter_number=2
    if month==1 and day >=26:
    	quarter_number=3
    if month==2 or month==3:
    	quarter_number=3
    if month==4 and day<27:
    	quarter_number=3
    if month==4 and day >=27:
    	quarter_number=4
    if month==5 or month==6:
    	quarter_number=4
    if month==7 and day<27:
    	quarter_number=4
    date=[quarter_number, year]
    return date