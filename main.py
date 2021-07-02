import math
from classes import *
from app import db
from app.models import Community_table, Vendor_table
from copy import deepcopy


def loadCommunitiesCSV(filename):
    communities_df = pd.read_csv(filename)
    communities = []
    for i in range(len(communities_df)):
        row = communities_df.iloc[i, :]
        communities.append(Community(
            row['Name'],
            row['Latitude'],
            row['Longitude'],
            row['Type'],
            row['Locality'],
            row['VendorId']))
    return communities


def loadVendorsCSV(filename):
    vendors_df = pd.read_csv(filename)
    vendors = []
    for i in range(len(vendors_df)):
        row = vendors_df.iloc[i, :]
        vendors.append(Vendor(
            row['Id'],
            row['Name'],
            row['NumTankers'],
            row['TankerCapacity'],
            row['Latitude'],
            row['Longitude']))
    return vendors


def loadVendors():
    vendors = []
    for vendor in Vendor_table.query.all():
        vendors.append(Vendor(
            vendor.id,
            vendor.name,
            vendor.num_tankers,
            vendor.tanker_capacity,
            # int.from_bytes(vendor.num_tankers, "little"),
            # int.from_bytes(vendor.tanker_capacity, "little"),
            vendor.latitude,
            vendor.longitude
        ))
    return vendors


def loadCommunities():
    communities = []
    for community in Community_table.query.all():
        communities.append(Community(
            community.name,
            community.latitude,
            community.longitude,
            community.type,
            community.locality,
            community.vendor_id,
            # int.from_bytes(community.vendor_id, "little")
        ))
        communities[-1].num_persons = community.num_persons
    return communities


def community_score(curr_comm, next_comm, consumption, tanker, month, period):
    # need to know the period and month before using this function
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
    curr_lat_rad = curr_comm['x'] * math.pi / 180
    curr_long_rad = curr_comm['y'] * math.pi / 180
    next_lat_rad = next_comm.x * math.pi / 180
    next_long_rad = next_comm.y * math.pi / 180
    # Equirectangular approximation
    x = (next_long_rad - curr_long_rad) * \
        math.cos((curr_lat_rad + next_lat_rad) / 2)
    y = (next_lat_rad - curr_lat_rad)
    distance = earth_radius * math.sqrt(x**2 + y**2)
    score = ((tanker.cur_capacity - (next_comm.predict(month)
                                     * period) * 0.2) + (distance * 0.8))
    return score


def tsp(vendor, date):
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
            scores[community] = community_score(
                curr_comm, community, community.consumption, tanker, month, period)
        communities.sort(key=lambda x: scores[x])
        return scores

    def getNextCommunity(communities, scores):
        """
          INPUT
          communities is a list of Community objects
          scores is a dictionary mapping each community to its score

          OUTPUT
          returns
        """
        i = 0
        while(i < len(communities) - 1 and scores[communities[i]] < 0):
            i += 1
            if(scores[communities[i]] < 0):
                return False
        return communities[i]

    def solution(vendor, month, period):
        communities = deepcopy(vendor.communities)
        for community in communities:
            community.consumption = community.predict(month)
        route_list = []

        for day in range(period):
            tanker_routes = []
            for tanker in vendor.tankers:
                route = [vendor.serialisable_dict(), ]
                scores = compute_scores(
                    route[-1], communities, tanker, month, period)
                while(len(communities) > 0 and max(scores.values()) > 0):
                    communities.sort(key=lambda x: scores[x])
                    next = getNextCommunity(communities, scores)
                    print(next)
                    if next:
                        if tanker.cur_capacity >= next.consumption:
                            tanker.cur_capacity -= next.consumption
                            communities.remove(next)
                        else:
                            next.consumption -= tanker.cur_capacity
                            tanker.cur_capacity = 0
                        route.append(next.serialisable_dict(month))
                    else:
                        break
                    scores = compute_scores(
                        route[-1], communities, tanker, month, period)
                tanker_routes.append(route)
            tanker_routes.sort(key=lambda x: len(x), reverse=True)
            route_list.append(tanker_routes)

        return len(communities), route_list

    period=1
    month = datetime.datetime(date.year, date.month, period)
    num_left, route_list = solution(vendor, month, period)
    return_dict = {}
    return_dict['data'] = route_list[0]
    return return_dict


def main():
    import matplotlib.pyplot as plt

    plt.bar(['Previous', 'With Optimisation'], [30, 24])
    plt.show()

    # from dateutil.relativedelta import relativedelta
    # random.seed(0)
    # today=datetime.datetime(2002, 1, 1)
    # datem=datetime.datetime(today.year, today.month, 1)
    #
    # dates = []
    # for i in range(12 * 10):
    #     today += relativedelta(months=1)
    #     dates.append(today)
    # dates = numpy.array(dates)
    #
    # data = pd.read_csv('csvdata/austin_water.csv')
    # x = list(set(data['Year Month']))
    # x.sort()
    # y = []
    # for date in x:
    #     y.append(sum(data.loc[data['Year Month'] == date]['Total Gallons']))
    # xShow = [datetime.datetime.strptime(str(i), "%Y%m") for i in x]
    # x = numpy.array([date_valuation(k) for k in xShow])
    # res = fit_sin(x, y)
    # plt.title("Sinusoidal regression on water consumption data")
    # plt.plot(xShow, y, label='training data',c='orange')
    # plt.plot(xShow, res['fitfunc'](x), label='', c='black')
    # # print(xShow)
    # plt.legend()
    # plt.xlabel("Time")
    # plt.ylabel("Litres of water")
    # plt.show()

    # vendors=loadVendors()
    # communities=loadCommunities()
    # res=get_res('csvdata/austin_water.csv')
    # for community in communities:
    #     community.assign_function(res)
    #     for vendor in vendors:
    #         if community.vendor_id == vendor.id:
    #             vendor.communities.append(community)

    # y = vendors[0].communities[0].predict(dates)
    # plt.plot(dates, y)
    # plt.show()

    # solutions={}
    # for vendor in vendors:
    #     solutions[vendor]=tsp(vendor, datem)
    #     print(solutions[vendor])
    # return solutions

    # vendor = vendors[0]
    # print(vendor.communities)
    # tanker_num = 0
    # for tanker_route in tsp(vendor, datem):
    #     print(tanker_num)
    #     for community in tanker_route:
    #         print(1*'\t', community)
    #     tanker_num += 1


if __name__ == "__main__":
    main()
