import grpc
import sys
from proto import restaurant_pb2
from proto import restaurant_pb2_grpc
from concurrent import futures

RESTAURANT_ITEMS_FOOD = ["chips", "fish", "burger", "pizza", "pasta", "salad"]
RESTAURANT_ITEMS_DRINK = ["water", "fizzy drink", "juice", "smoothie", "coffee", "beer"]
RESTAURANT_ITEMS_DESSERT = ["ice cream", "chocolate cake", "cheese cake", "brownie", "pancakes", "waffles"]

def CheckIngredients(items, stock):

    status = 0
    for ingredient in items:
        if ingredient not in stock:
            status = 1
            break
    return status

class Restaurant(restaurant_pb2_grpc.RestaurantServicer):
    
    def FoodOrder(self, request, context):
        stat = CheckIngredients(request.items, RESTAURANT_ITEMS_FOOD)
        return restaurant_pb2.RestaurantResponse(orderID=request.orderID, status=stat)
    
    def DrinkOrder(self, request, context):
        stat = CheckIngredients(request.items, RESTAURANT_ITEMS_DRINK)
        return restaurant_pb2.RestaurantResponse(orderID=request.orderID, status=stat)
    
    def DessertOrder(self, request, context):
        stat = CheckIngredients(request.items, RESTAURANT_ITEMS_DESSERT)
        return restaurant_pb2.RestaurantResponse(orderID=request.orderID, status=stat)
    # Logic goes here

def serve():
    
    PORT = str(9999)
    '''
    if(sys.argv < 1):
        print("Please give the port number.")
    else:
        PORT = str(sys.argv[0])
    ''' 
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    restaurant_pb2_grpc.add_RestaurantServicer_to_server(Restaurant(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

    # Logic goes here
    # Remember to start the server on localhost and a port defined by the first command line argument


if __name__ == '__main__':
    serve()
