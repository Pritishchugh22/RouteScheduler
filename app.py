from __future__ import print_function

import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask, render_template

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import pandas as pd 
import numpy as np

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
    

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result)

    print("\n\n\n\n\n")
    #location = list(result.values()) # Printing the new dictionary
    location=[]
    for i in result:
        location.append(i["input"])
    no_of_vechicles = int(location[0])
    print(no_of_vechicles)
    print(type(no_of_vechicles))
    location = location[1:]
    print(location)#this shows the json converted as a python dictionary
    print("\n\n\n\n\n")

    SERVICE_ACCOUNT_FILE = 'keys.json'
    credentials = None
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)



    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1nRQee6z7vbJZD4HphXKMPXbrhozjBF9_mder_TihRkY'

    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    def distanceCalculator(To,From):
        # writing to a file
        aoa = [[To,From]]
        if To!=From: 
            request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                            range="Sheet1!A1", valueInputOption="USER_ENTERED", body={"values":aoa}).execute()
            #print(request)
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                range="Sheet1!C2").execute()
            #print("yahan tak theek hai")
            values = result.get('values', [])
            #print(values)
            return int(int(values[0][0])/60)
        else:
            return 0

    def timeCalculator(To,From):
        # writing to a file
        aoa = [[To,From]]
        if To!=From: 
            request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                            range="Sheet1!A1", valueInputOption="USER_ENTERED", body={"values":aoa}).execute()
            #print(request)
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                range="Sheet1!C1").execute()
            #print("yahan tak theek hai")
            values = result.get('values', [])
    #        print(values)
            return int(int(values[0][0])/60)
        else:
            return 0
    #timeCalculator("Chandigarh","mohali")

    #function to create the time matrix
    def time_matrix(location):
        matrix=[]
        no_of_locations = len(location)
        for i in location:
            #print("hi")
            temp =[]
            for j in location:
                #print("Heloo")
                #print(i,j)
                temp.append(timeCalculator(i,j))
                #print("1")
            matrix.append(temp)
            #print(matrix)
        #print("hogya")
        for i in range(1,len(location)):
            j =0
            while j<i:
                matrix[i][j]=matrix[j][i]
                j+=1
        #print(matrix)
        return matrix 

    def distance_matrix(location):
        matrix=[]
        no_of_locations = len(location)
        for i in location:
            #print("hi")
            temp =[]
            for j in location:
                #print("Heloo")
                #print(i,j)
                temp.append(distanceCalculator(i,j))
                #print("1")
            matrix.append(temp)
            #print(matrix)
        #print("hogya")
        for i in range(1,len(location)):
            j =0
            while j<i:
                matrix[i][j]=matrix[j][i]
                j+=1
        #print(matrix)
        return matrix 

    def time(location):
        def create_data_model(location):
            """Stores the data for the problem."""
            data = {}
            data['time_matrix'] = time_matrix(location)
            print(data['time_matrix'])
            data['time_windows'] = [
                (0, 17),  # depot
                (7, 20),  # 1
                (10, 17),  # 2
            ]
            data['num_vehicles'] = no_of_vechicles
            data['depot'] = 0
            return data


        def print_solution(data, manager, routing, solution):
            """Prints solution on console."""
    #        print(f'Objective: {solution.ObjectiveValue()}')
            time_dimension = routing.GetDimensionOrDie('Time')
            total_time = 0
            route=[]
            for vehicle_id in range(data['num_vehicles']):
                arr=[]
                index = routing.Start(vehicle_id)
                plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
                while not routing.IsEnd(index):
                    time_var = time_dimension.CumulVar(index)
                    plan_output += '{0} Time({1},{2}) -> '.format(
                        manager.IndexToNode(index), solution.Min(time_var),
                        solution.Max(time_var))
#                    arr.append(manager.IndexToNode(index))
                    index = solution.Value(routing.NextVar(index))
                time_var = time_dimension.CumulVar(index)
                plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),
                                                            solution.Min(time_var),
                                                            solution.Max(time_var))
                plan_output += 'Time of the route: {}min\n'.format(
                    solution.Min(time_var))
                arr.append(manager.IndexToNode(index))
                route.append(arr)
                print(plan_output)
                total_time += solution.Min(time_var)
            print('Total time of all routes: {}min'.format(total_time))
            return route


        def time_solution(location):
            """Solve the VRP with time windows."""
            #hard coding the locations of the appointment
            
            # Instantiate the data problem.
            data = create_data_model(location)

            # Create the routing index manager.
            manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']),
                                                   data['num_vehicles'], data['depot'])

            # Create Routing Model.
            routing = pywrapcp.RoutingModel(manager)


            # Create and register a transit callback.
            def time_callback(from_index, to_index):
                """Returns the travel time between the two nodes."""
                # Convert from routing variable Index to time matrix NodeIndex.
                from_node = manager.IndexToNode(from_index)
                to_node = manager.IndexToNode(to_index)
                return data['time_matrix'][from_node][to_node]

            transit_callback_index = routing.RegisterTransitCallback(time_callback)

            # Define cost of each arc.
            routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

            # Add Time Windows constraint.
            time = 'Time'
            routing.AddDimension(
                transit_callback_index,
                30,  # allow waiting time
                30,  # maximum time per vehicle
                False,  # Don't force start cumul to zero.
                time)
            time_dimension = routing.GetDimensionOrDie(time)
            # Add time window constraints for each location except depot.
            for location_idx, time_window in enumerate(data['time_windows']):
                if location_idx == data['depot']:
                    continue
                index = manager.NodeToIndex(location_idx)
                time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
            # Add time window constraints for each vehicle start node.
            depot_idx = data['depot']
            for vehicle_id in range(data['num_vehicles']):
                index = routing.Start(vehicle_id)
                time_dimension.CumulVar(index).SetRange(
                    data['time_windows'][depot_idx][0],
                    data['time_windows'][depot_idx][1])

            # Instantiate route start and end times to produce feasible times.
            for i in range(data['num_vehicles']):
                routing.AddVariableMinimizedByFinalizer(
                    time_dimension.CumulVar(routing.Start(i)))
                routing.AddVariableMinimizedByFinalizer(
                    time_dimension.CumulVar(routing.End(i)))

            # Setting first solution heuristic.
            search_parameters = pywrapcp.DefaultRoutingSearchParameters()
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

            # Solve the problem.
            solution = routing.SolveWithParameters(search_parameters)

            # Print solution on console.
            if solution:
                return print_solution(data, manager, routing, solution)
    #            return 1
            else:
                print("no can't find using time analysis")
                return 0

        return time_solution(location)

        
    
    def distance(location):
        def create_data_model(location):
            """Stores the data for the problem."""
            data = {}
            data['distance_matrix'] = distance_matrix(location)
            data['num_vehicles'] = no_of_vechicles
            data['depot'] = 0
            return data


        def print_solution(data, manager, routing, solution):
            """Prints solution on console."""
    #        print(f'Objective: {solution.ObjectiveValue()}')
            max_route_distance = 0
            route=[]
            for vehicle_id in range(data['num_vehicles']):
                arr =[]
                index = routing.Start(vehicle_id)
                plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
                route_distance = 0
                while not routing.IsEnd(index):
                    plan_output += ' {} -> '.format(manager.IndexToNode(index))
                    arr.append(manager.IndexToNode(index))
                    previous_index = index
                    index = solution.Value(routing.NextVar(index))
                    route_distance += routing.GetArcCostForVehicle(
                        previous_index, index, vehicle_id)
                plan_output += '{}\n'.format(manager.IndexToNode(index))
#                arr.append(manager.IndexToNode(index))
                route.append(arr)
                plan_output += 'Distance of the route: {}m\n'.format(route_distance)
                print(plan_output)
                max_route_distance = max(route_distance, max_route_distance)
            print('Maximum of the route distances: {}m'.format(max_route_distance))
            return route



        def distance_solution(location):
            """Entry point of the program."""
            # Instantiate the data problem.
            data = create_data_model(location)

            # Create the routing index manager.
            manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                                   data['num_vehicles'], data['depot'])

            # Create Routing Model.
            routing = pywrapcp.RoutingModel(manager)


            # Create and register a transit callback.
            def distance_callback(from_index, to_index):
                """Returns the distance between the two nodes."""
                # Convert from routing variable Index to distance matrix NodeIndex.
                from_node = manager.IndexToNode(from_index)
                to_node = manager.IndexToNode(to_index)
                return data['distance_matrix'][from_node][to_node]

            transit_callback_index = routing.RegisterTransitCallback(distance_callback)

            # Define cost of each arc.
            routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

            # Add Distance constraint.
            dimension_name = 'Distance'
            routing.AddDimension(
                transit_callback_index,
                0,  # no slack
                3000,  # vehicle maximum travel distance
                True,  # start cumul to zero
                dimension_name)
            distance_dimension = routing.GetDimensionOrDie(dimension_name)
            distance_dimension.SetGlobalSpanCostCoefficient(100)

            # Setting first solution heuristic.
            search_parameters = pywrapcp.DefaultRoutingSearchParameters()
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

            # Solve the problem.
            solution = routing.SolveWithParameters(search_parameters)

            # Print solution on console.
            if solution:
                return print_solution(data, manager, routing, solution)
    #            return 1
            else:
                print('No solution found !')
                return 0
        return distance_solution(location)
        
    
#    location = ["sector 70 Mohali","sector 80 Mohali", "sector 72 Mohali","sector 75 Mohali","sector 40 Mohali"]
    #route = time(location)
    #if route ==0:
    route = distance(location)
    print(route)

    # converting locations into lat long ---------------------------------------------------------------------------------------

    data = {'City':location} 
    
    #  Convert the dictionary into DataFrame 
    df = pd.DataFrame(data) 

    longitude = []
    latitude = []

    # function to find the coordinate
    # of a given city
    def findGeocode(city):

        # try and catch is used to overcome
        # the exception thrown by geolocator
        # using geocodertimedout
        try:

            # Specify the user_agent as your
            # app name it should not be none
            geolocator = Nominatim(user_agent="your_app_name")

            return geolocator.geocode(city)

        except GeocoderTimedOut:

            return findGeocode(city)	

    # each value from city column
    # will be fetched and sent to
    # function find_geocode
    for i in (df["City"]):

        if findGeocode(i) != None:

            loc = findGeocode(i)

            # coordinates returned from
            # function is stored into
            # two separate list
            latitude.append(loc.latitude)
            longitude.append(loc.longitude)

        # if coordinate for a city not
        # found, insert "NaN" indicating
        # missing value
        else:
            latitude.append(np.nan)
            longitude.append(np.nan)

    lat_long=[]
    for i in route:
        l =[]
        for j in i:
            temp = []
            temp.append(latitude[j])
            temp.append(longitude[j])
            l.append(temp)
        lat_long.append(l)
    print(lat_long)

# ---------------------------------------------------------------------------------------------------------------

    lat_long =jsonify(lat_long)
    return lat_long
#    return render_template('map.html')    

