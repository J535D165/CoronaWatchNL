import textract

import re

## Median age (from first page)
def extract_median_age(lines):
    
    i = lines.index("Samenvatting")
    
    text = " ".join(lines[i:i+20])
    
    matches = re.findall(r"Van alle gemelde patiënten is de helft (\d+) jaar en ouder.", text)
        
    return matches[0]   
    

## Table 1
def extract_table_1_values(lines):
  
    i = lines.index("Gezondheidsstatus")
    
    for val in lines[i:i+20]:
        print(val)
    
    totaal_gemeld = lines[i+12]
    ziekenhuisopname = lines[i+13].split(" ")[0]
    overleden = lines[i+14].split(" ")[0]
    
    return(totaal_gemeld, ziekenhuisopname, overleden)
    
    
if __name__ == '__main__':
    
    filename = 'reports/COVID-19_WebSite_rapport_20200328_mvb.pdf'
#     filename = 'reports/COVID-19_WebSite_rapport_20200329.pdf'
#     filename = 'reports/Epidemiologische situatie COVID-19 30 maart 2020.pdf'

    text = textract.process(filename)

    lines = text.decode("utf-8").split("\n")
    
    print(extract_median_age(lines))
    print(extract_table_1_values(lines))
    
