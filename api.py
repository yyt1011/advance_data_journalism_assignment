######################

# QUESTION 1: Import the modules you'll need for this assignment (json, requests)
import json
import requests

######################

# This is a working API key for the ProPublica Congress API. Don't change it.
API_KEY = 'OylOqGPorg2UjpgDMgoGnVtRBKDhcNn7q6XF0rVb'

def get_votes_by_date(chamber, start_date, end_date):
    # '''
    # Return all votes from a given day. You will be provided four input variables here:
    # chamber: Denotes the chamber (Senate or House)
    # start_date: The beginning of the time window you'd like to search for votes
    # end_date: The end of the time window
    # Construct the URL by plugging them into the correct places. The ProPublica docs
    # don't do a good job of explaining this with start/end dates, but the correct URL
    # will look like:
    # https://api.propublica.org/congress/v1/{chamber}/votes/{start_date}/{end_date}.json
    # The URL should be stored in a variable called url.
    # You should then process the resulting data using the json module and return it in
    # a variable called data.
    # '''

    ###################

    # QUESTION 2: Define the proper URL here. It should use the chamber, start_date and end_date arguments 
    # provided by the function.

    url = 'https://api.propublica.org/congress/v1/%s/votes/%s/%s.json' % ('senate', '2017-04-06', '2017-04-06')

    ###################

    response = requests.get(url, headers={"X-API-Key": API_KEY}).content

    ###################

    # QUESTION 3: Use the "loads" method of the json module to turn the "response" variable into Python objects.
    # Put that into the "data" variable below.

    data = json.loads(response)

    ###################

    return data


def format_nomination_votes(data):
    # '''
    # Your next task is to take the results of the API response and extract several of the most
    # important pieces of information. We do this at the Times to ultimately save the data into
    # a database, but you could also use it to produce a CSV for analysis.
    # Specifically, the information you'll need to extract from each result is:
    
    # - Vote date
    # - Vote question
    # - Vote description
    # - Vote result
    # - Total number of votes for each "yes," "no," "present," and "not voting"
    # Fill out each of the following variables with the appropriate information (and pay attention
    # to the correct level of indentation).
    # '''
    output = [['date', 'question', 'description', 'result', 'yes', 'no', 'present', 'not_voting']]

    ###################

    # QUESTION 4: Dig through the response to pull out the data corresponding to each item below. Use
    # the "date" variable as an example, and rely on your knowledge of dictionary and list lookup syntax.

    for vote in data['results']['votes']: 
    
        date = vote['date']

        question = vote['question']

        description = vote['description']

        result = vote['result']

        yes = vote['total']['yes']

        no = vote['total']['no']

        present = vote['total']['present']

        not_voting = vote['total']['not_voting']

    ###################

        output.append([date, question, description, result, yes, no, present, not_voting])

    return output


########## YOU CAN IGNORE THIS ##########

if __name__ == '__main__':
    votes = get_votes_by_date('senate', '2017-04-06', '2017-04-06')

    if votes == None:
        print "Looks like you haven't finished implementing the get_votes_by_date method ..."
        exit()
    elif type(votes) != dict:
        print "Something's wrong. You might still need to process the data using the json module."
        exit()
    elif type(votes) == dict:
        print 'Your data looks ok!'
        print votes

    formatted = format_nomination_votes(votes)

    if len(formatted) <= 1:
        print 'You only seem to have one item in your output. Did you append records for the others?'
        exit()

    print 'Output:'
    print formatted