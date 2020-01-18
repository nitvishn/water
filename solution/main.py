import math
from classes import *


def tsp():
  def community_score(curr_comm, next_comm, consumption):
    #need to know the period and month before using this function
    """
    INPUT 
    curr_comm is a Community object that represents the community the tanker is currently on
    next_comm is a Community object that represents the next community for which the score is to be calculated
    consumption is an int representing the daily water consumption for next_comm
  
    OUTPUT
    outputs a float representing the score for next_comm
    the lower the score, the more desirable next_comm
    """
    earth_radius = 6371
    # Converting the latitude and longitude degrees to radians
    curr_lat_rad = curr_comm.x * math.pi / 180
    curr_long_rad = curr_comm.y * math.pi / 180
    next_lat_rad = next_comm.x * math.pi / 180
    next_long_rad = next_comm.y * math.pi / 180
    # Equirectangular approximation
    x = (next_long_rad - curr_long_rad) * math.cos((curr_lat_rad + next_lat_rad) / 2)
    y = (next_lat_rad - curr_lat_rad)
    distance = earth_radius * math.sqrt(x**2 + y**2)
    score = ((tanker.cur_capacity - (next_comm.predict(month) * period) * 0.2) + (distance * 0.8))
    return score
    

