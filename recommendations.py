import googlemaps
import pandas as pd
import time

API_KEY = 'AIzaSyBIfvotj8AMSUUPMb0ZrOq0lMJiYKfeNjA'
map_client = googlemaps.Client(API_KEY)

def generate_excel_info(location: tuple[float,float], cuisine_type : str, radius: int):
    '''

    :param location: center location as tuple (lat,long)
    :param cuisine_type: appropriate cuisine type as string
    :param radius: radius of search, smaller radius is closer to center but larger radius gets better results
    :return: None, creates Excel sheet with url and other info
    '''

    business_list = []

    response = map_client.places_nearby(
        location = location,
        keyword = cuisine_type,
        radius = radius
    )

    #check if any results were gotten
    print(response)

    #if results empty break
    if len(response.get('results')) == 0:
        print("No results were found, try increasing the radius")
        return

    business_list.extend(response.get('results'))
    next_page_token = response.get('next_page_token')

    while next_page_token:

        #tutorial guy said if there was no pause something bad would happen
        time.sleep(2)
        response = map_client.places_nearby(
            location=location,
            keyword=cuisine_type,
            radius=radius,
            page_token = next_page_token
        )

        business_list.extend(response.get('results'))
        next_page_token = response.get('next_page_token')

    df = pd.DataFrame(business_list)
    df['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df['place_id']

    df.to_excel(f'{cuisine_type} list.xlsx',index=False)

def find_center(location_list: list[tuple]) -> tuple:
    '''

    :param location_list: list of locations as tuples (lat, long)
    :return: center of these locations
    '''

    n = len(location_list)

    sum_x = 0
    sum_y = 0

    for location in location_list:
        sum_x += location[0]
        sum_y += location[1]

    result = (sum_x/n,sum_y/n)

    return result

def recommendation(location_list: list[tuple], cuisine_type: str, radius: int):
    center = find_center(location_list)
    generate_excel_info(center,cuisine_type,radius)