import json
import sys

import requests
from utils import (encode_city_name, extract_website_from_url,
                   scrape_data_from_url)


# check if the user provided the input arguments
if len(sys.argv) == 3:
    category = sys.argv[1]
    city = sys.argv[2]
    print(f"Scraping data for {category} in {city}...")
else:
    raise Exception("Please provide both category and location as input arguments.")


# dictionary to store all the data
businesses = {
    'bussinesses':[]
}

iteration = 0
while True:
    
    # use default search url if it's the first iteration, otherwise use the url with the offset
    if iteration != 0:
        search_url = f"https://www.yelp.com/search/snippet?find_desc={category}&find_loc={city}&start={iteration*10}&parent_request_id=0366dddfa08e03b6&request_origin=user"
    else:
        search_url = f"https://www.yelp.com/search/snippet?find_desc={category}&find_loc={city}&parent_request_id=0366dddfa08e03b6&request_origin=user"

    search_response = requests.get(search_url)

    # custom built pagination)
    try:
        search_results = search_response.json()['searchPageProps']['mainContentComponentsListProps']
    except:
        print("No more results")
        break

    num = 0

    is_request_valid = False
    for result in search_results:
        if "bizId" in result:  
            
            # if no element with bizId is found, it means that the request is invalid
            is_request_valid = True

            # parse the website url from XHR request 
            website = result['searchResultBusiness']['website']['href'] if result['searchResultBusiness']['website'] else None
            if website and 'adredir' in website:
                website = extract_website_from_url(website)

            # create a link for bussiness in yelp
            detailed_url = "https://www.yelp.com" + result['searchResultBusiness']['businessUrl']
            
            successful = False
            while not successful:   # this loop is required to retry scraping the data if an error occurs
                try:

                    # parsing name, location and date of the review
                    names = scrape_data_from_url(detailed_url, "user-passport-info")[1:6]
                    dates = scrape_data_from_url(detailed_url, "margin-b1-5__09f24__NHcQi")
                    dates  = [item for item in dates if '/' in item and not any(c.isalpha() for c in item)][0:5]
                    
                    # check if there are enough reviews
                    if len(dates) != 5 and result['searchResultBusiness']['reviewCount']>=5:
                        raise Exception("Not enough dates")
                    
                    # create 5 reviews for each bussiness
                    five_reviews = []
                    for i in range(len(names)):
                        name = names[i].split(".")[0] + '.' if "Qype" not in names[i] else names[i].split(")")[0]
                        try:   
                            location = names[i].split(".")[1]
                        except:
                            location = names[i].split(")")[1]
                        if "Elite 2023" in location:
                            location = location.replace("Elite 2023", "")
                        five_reviews.append(
                            {
                                "reviewer_name" : name,
                                "reviewer_location" : location,
                                "review_date" : dates[i]
                            }
                        )

                    successful = True

                    # add bussiness to the dictionary
                    businesses['bussinesses'].append(
                        {
                            "title" : result['searchResultBusiness']['name'],
                            "rating" : result['searchResultBusiness']['rating'],
                            "reviews_count" : result['searchResultBusiness']['reviewCount'],
                            "yelp_url" : "https://www.yelp.com" + result['searchResultBusiness']['businessUrl'],
                            "website" : website,
                            "reviews" : five_reviews
                        }
                    )

                    print(f"Page {iteration}, item {num} --->  {result['searchResultBusiness']['name']}")
                    num += 1
                    
                except Exception as e:
                    print(e)
                    successful = False

    if not is_request_valid:
        raise Exception("No information for this request on Yelp")
    
    iteration += 1


file_path = "data.json"

# Write the dictionary to the JSON file
with open(file_path, "w") as json_file:
    json.dump(businesses, json_file, indent=4)