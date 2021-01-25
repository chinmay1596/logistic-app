from geopy.distance import great_circle

def calculate_distance_using_lat_lng(lat1, lng1, lat2, lng2):
    order_coordinates = (lat1, lng1)
    warehouse_coordinates = (lat2, lng2)
    distance = great_circle(order_coordinates, warehouse_coordinates).kilometers  # returning distance in km
    return distance

def fetch_all_the_orders_of_warehouse_within_georadius(request, orders, geo_radius):
    order_list = []
    georadius = geo_radius
    for order in orders:
        orders_distance = calculate_distance_using_lat_lng(order.latitude, order.longitude, order.warehouse.latitude,
                                                           order.warehouse.longitude)
        if orders_distance <= georadius:
            orders = {
                "order_id": order.id,
                "distance": orders_distance
            }
            order_list.append(orders)
    return order_list


def sort_and_fetch_orders(request, orders):
    order_list = []
    for order in orders:
        orders_distance = calculate_distance_using_lat_lng(order.latitude, order.longitude,
                                                           order.warehouse.latitude,
                                                           order.warehouse.longitude)
        orders = {
            "order_id": order.id,
            "distance": orders_distance,
            "points": [order.warehouse.longitude, order.warehouse.latitude, order.longitude, order.latitude]
        }
        order_list.append(orders)
    return sorted(order_list, key=lambda i: (i['distance']))


def bundle_orders(sorted_orders, threshold):
    start = int(sorted_orders[0]['distance'])
    curent_group_number = 1
    groups = {curent_group_number: [sorted_orders[0], ]}
    threshold = threshold
    order_ids = []
    for order in sorted_orders[1:]:
        order_ids.append(int(order['order_id']))
        distance = int(order['distance'])
        if distance in range(start, start + threshold + 1):
            if curent_group_number not in groups.keys():
                curent_group_number += 1
                groups[curent_group_number] = [order]
            else:
                groups[curent_group_number].append(order)
        else:
            start = distance
            curent_group_number += 1
            groups[curent_group_number] = [order]
    return groups
