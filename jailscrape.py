#import urllib2, a module defines functions that enable users to open the URL and get the information
#import csv, a module implements classes to read and write tabular data in CSV format
import urllib2, csv
#import BeautifulSoup, a Python library for getting data out of HTML and XML files
from bs4 import BeautifulSoup

#a built-in function that has two arguments — a value and a mode. In this case, this snippet opens a file named "jaildata.csv" and allows developers to edit and write new information to the file.
outfile = open('jaildata.csv', 'w')
#write new data into a file named "outfile", csv.writer function will return a writer object which converts the input data into delimited strings on the given file.
writer = csv.writer(outfile)

#the web page on which the data we want to use is stored
url = 'https://report.boonecountymo.org/mrcjava/servlet/SH01_MP.I00290s?max_rows=500'
#open the web page and give the data into "html"
html = urllib2.urlopen(url).read()

#BeautifulSoup function has two arguments - the file that the developers want to get and the html parser they want to use. In this case, the information stored in "html" will be read by html.parser.
soup = BeautifulSoup(html, "html.parser")

#find strings tagged by "tbody" with stripe class
tbody = soup.find('tbody', {'class': 'stripe'})
#find all the strings that is tagged by "tr"
rows = tbody.find_all('tr')

#a loop that iterates all the rows
for row in rows:
    #find all the rows that is tagged by "td"
    cells = row.find_all('td')
    #set an empty list called data
    data = []
    #a loop that iterates all the rows tagged by "td" and store the results in data list
    for cell in cells:
        data.append(cell.text)
    #use writerow() method to pass the data to the jaildata file
    writer.writerow(data)
