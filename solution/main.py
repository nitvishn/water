import math
from classes import *

def community_score(curr_comm, next_comm, consumption, tanker, month, period):
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

def tsp(vendor, month):
  """
  INPUT 
  vendor is a Vendor object 
  month is a datetime object

  OUTPUT
  dictionary mapping tankers to an ordered list of communities to visit 
  """
  def compute_scores(curr_comm, communities, tanker, month, period):
    """
    INPUT 
    curr_comm is a Community object
    communities is a list of Community objects 
    tanker is a Tanker object 
    month is a datetime object 
    period is an int

    OUTPUT 
    returns dictionary mapping each community to its score 
    """
    scores = {}
    for community in communities:
      scores[community] = community_score(curr_comm, community, community.consumption, tanker, month, period)
    communities.sort(key=lambda x: scores[x])
    return scores
  def pop_next_community(communitites, scores):
    """
    INPUT 
    communities is a list of Community objects
    scores is a dictionary mapping each community to its score 

    OUTPUT 
    returns
    """
    i = 0 
    while i < (len(communities) - 1)  and scores[communities] > i: 
      community.pop(i)
      i += 1




