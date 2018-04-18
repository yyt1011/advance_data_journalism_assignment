import urllib2, requests
import datetime
import json
import os
import time
from bs4 import BeautifulSoup

RANGE = int(os.environ.get('CHICAGO_RANGE', 2))
SEQUENCE = os.environ.get('CHICAGO_SEQUENCE', 0)
LOAD_ID = str(time.mktime(datetime.datetime.now().timetuple())).split('.')[0]

########## YOUR CODE GOES HERE ##########

def get_html(ward):
    '''
    This should return the HTML of the Chicago precinct results page, by ward. You'll notice that the
    function takes an argument, called ward. This is an integer used to specify which ward the results
    will be from. You'll need to insert this into the URL string.

    The base URL is: http://www.chicagoelections.com/en/pctlevel3.asp

    It also takes 3 get parameters:

    elec_code=9
    race_number=10
    ward=whatever the "ward" argument to the function is

    You should save the resulting HTML in a variable called html.
    '''

    url = 'https://chicagoelections.com/en/pctlevel3.asp?elec_code=9&race_number=10&ward=1'

    # we'll talk about this Friday
    html = requests.get(url).content

    return html # Leave this line here. Just be sure to call your variable html.

def get_table(html):
    '''
    This should return the HTML of the table on the page, which you can find using BeautifulSoup. The function
    takes the HTML of the page as input, so your job is to take that HTML, process it using BeautifulSoup,
    and return just the HTML for the table.

    The variable that contains the table should be called table.
    '''

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table')

    return table # Leave this line here. Just be sure to call your variable table.


########## YOUR CODE ENDS HERE ##########

def set_load_id():
    os.environ['CHICAGO_LOAD_ID'] = LOAD_ID

def load_results():
    """
    Loops over wards, loading HTML either from the internet (CHICAGO_MODE=live)
    or locally (CHICAGO_MODE=test).
    """
    message = None
    results = []

    for ward in range(1, RANGE):
        html = get_html(ward)
        table = get_table(html)

        ward_dict = {}
        ward_dict['ward'] = ward
        ward_dict['precincts'] = []
        ward_dict['totals'] = {}

        for row in table.select('tr')[3:]:
            cells = row.select('td')
            try:
                int(cells[0].text.strip())
                precinct_dict = {}
                precinct_dict['total_votes'] = int(cells[1].text.strip())
                precinct_dict['rahm_votes'] = int(cells[2].text.strip())
                precinct_dict['garcia_votes'] = int(cells[4].text.strip())

                precinct_dict['rahm_pct'] = float(cells[3].text.replace('%', '').strip())
                precinct_dict['garcia_pct'] = float(cells[5].text.replace('%', '').strip())
                ward_dict['precincts'].append(precinct_dict)
            except ValueError:
                if cells[0].text.strip().lower() == 'total':
                    ward_dict['totals']['total_votes'] = int(cells[1].text.strip())
                    ward_dict['totals']['rahm_votes'] = int(cells[2].text.strip())
                    ward_dict['totals']['garcia_votes'] = int(cells[4].text.strip())

                    ward_dict['totals']['rahm_pct'] = float(cells[3].text.replace('%', '').strip())
                    ward_dict['totals']['garcia_pct'] = float(cells[5].text.replace('%', '').strip())

        results.append(ward_dict)

    return results, message


def print_results(payload):
    """
    Save the JSON results.
    """
    payload = json.dumps(payload)
    print payload

    success = True
    return success


def main():

    print "Loading timestamp %s" % LOAD_ID

    payload = load_results()
    success = print_results(payload)
    if success:
        set_load_id()

if __name__ == "__main__":
    main()
