import math
import requests
import argparse
import time

#Write you own function that moves the droon from one place to another 
#the function returns the droon's current location while moving
#====================================================================================================
def your_function(drone_coords, goal_coords):
    long=drone_coords[0]
    lat=drone_coords[1]
    
    if long<goal_coords[0]:
        long=long+1/10000 
    elif long>goal_coords[0]:
        long=long-1/10000
        
    if lat<goal_coords[1]:
        lat=lat + 1/10000   
    elif lat>goal_coords[1]:
        lat=lat-1/10000
    
    return (long, lat)
#====================================================================================================


def run(current_coords, from_coords, to_coords, SERVER_URL):
    # Compmeleet the while loop:
    # 1. Change the loop condition so that it stops sending location to the data base when the drone arrives the to_address
    # 2. Plan a path with your own function, so that the drone moves from [current_address] to [from_address], and the from [from_address] to [to_address]. 
    # 3. While moving, the drone keeps sending it's location to the database.
    #====================================================================================================
    moving = True
    drone_coords=current_coords
    goal_coords=from_coords
    
    while moving:
        new_coords = your_function(drone_coords, goal_coords)
        drone_coords = new_coords
        
        with requests.Session() as session:
            drone_location = {'longitude': drone_coords[0],
                              'latitude': drone_coords[1]
                    }
        resp = session.post(SERVER_URL, json=drone_location)
            
        arrived = bool(abs(drone_coords[0]-goal_coords[0])<1/10000) & bool(abs(drone_coords[1]-goal_coords[1])<1/10000)
            
        if arrived:
            if goal_coords==to_coords:
                moving=False
            else:
                goal_coords=to_coords
                    
        time.sleep(0.1)
        #print(drone_coords)
                    
  #====================================================================================================

   
if __name__ == "__main__":
    SERVER_URL = "http://127.0.0.1:5001/drone"

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--flong", help='longitude of input [from address]',type=float)
    parser.add_argument("--flat", help='latitude of input [from address]' ,type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    args = parser.parse_args()

    current_coords = (args.clong, args.clat)
    from_coords = (args.flong, args.flat)
    to_coords = (args.tlong, args.tlat)

    print(current_coords)
    print(from_coords)
    print(to_coords)

    run(current_coords, from_coords, to_coords, SERVER_URL)
