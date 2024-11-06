import requests
import time
import os

# URLs to the APIs
apis = [
    "https://politics.api.cnn.io/results/bop/2024-PG-US.json",
    "https://static01.nyt.com/elections-assets/pages/data/2024-11-05/results-president.json",
    "https://api-election.cbsnews.com/api/public/candsummary/2024/G/P",
    "https://s3.amazonaws.com/graphics.axios.com/elex-results-2024/live/2024-11-05/results-president-summary-latest.json?1730870544794"
]

def check_votes():
    highest_trump_votes = 0
    highest_harris_votes = 0
    trump_source = ""
    harris_source = ""
    
    try:
        for api in apis:
            response = requests.get(api)
            data = response.json()
            
            try:
                # get vote from api :P
                if 'cnn' in api:
                    trump_votes = data['children'][0]['value']
                    harris_votes = data['children'][1]['value']
                elif 'nyt' in api:
                    # nyt funky
                    party_data = data.get('partyControlData', {}).get('results', [])[0].get('offices', {}).get('P', {}).get('party_balance', {})
                    trump_votes = party_data.get('GOP', {}).get('seats', 0)
                    harris_votes = party_data.get('DEM', {}).get('seats', 0)
                elif 'cbsnews' in api:
                    trump_votes = next((c['win'] for c in data['candidates'] if c['party'] == 'REP'), 1)
                    harris_votes = next((c['win'] for c in data['candidates'] if c['party'] == 'DEM'), 0)
                elif 'axios' in api:
                    trump_votes = next((c['electoralVotesWon'] for c in data['candidates'] if c['party'] == 'REP'), 0)
                    harris_votes = next((c['electoralVotesWon'] for c in data['candidates'] if c['party'] == 'DEM'), 1)
                
                # find wat api has the highest vote count for each candidate
                if trump_votes > highest_trump_votes:
                    highest_trump_votes = trump_votes
                    trump_source = api
                if harris_votes > highest_harris_votes:
                    highest_harris_votes = harris_votes
                    harris_source = api

                # check if any1 has 270
                if trump_votes >= 270:
                    print(f"Trump has reached 270 votes! ): Source: {trump_source}")
                    print(f"Trump has reached 270 votes! ): Source: {trump_source}")
                    print(f"Trump has reached 270 votes! ): Source: {trump_source}")
                    print(f"Trump has reached 270 votes! ): Source: {trump_source}")
                    print(f"Trump has reached 270 votes! ): Source: {trump_source}")
                    os.system("color 48")  # cmd color to red
                    return True
                elif harris_votes >= 270:
                    print(f"Harris has reached 270 votes! :3 Source: {harris_source}")
                    print(f"Harris has reached 270 votes! :3 Source: {harris_source}")
                    print(f"Harris has reached 270 votes! :3 Source: {harris_source}")
                    print(f"Harris has reached 270 votes! :3 Source: {harris_source}")
                    print(f"Harris has reached 270 votes! :3 Source: {harris_source}")
                    os.system("color 18")  # cmd color to blue
                    return True
            
            except KeyError as e:
                print(f"Missing key in {api} response:", e, "Data structure:", data)
                continue

        # giv vote updates
        print(f"    Trump: {highest_trump_votes} (Source: {trump_source})")
        print(f"    Harris: {highest_harris_votes} (Source: {harris_source})")

        # change text color to red or blue based on who winnin
        if highest_trump_votes > highest_harris_votes:
            os.system("color 04")  # red :O
        else:
            os.system("color 01")  # blu :3

    except Exception as e:
        print(f"Unexpected error: {e}")
    return False

# lop in circle
while True:
    if check_votes():
        break  # stop if any1 win heh
    time.sleep(1)
