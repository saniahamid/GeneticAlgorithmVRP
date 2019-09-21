# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 14:57:08 2018

@author: sania hamid

This code is the scheduler for the system
"""
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np

import GA

#number of new requests every timestep
#no_new_requests = 0

#total number of rewquests so far
#total_requests = 0

num_generations = 200

class Vehicle:
    def __init__(self,name,no,capacity,tour):
        self.name = name+" "+str(no)
        self.capacity = 4
        self.tour = tour
        self.vacancy = self.capacity - len(tour)
               
        
    def details(self):
        print(self.name)
        print("Capacity is: ",self.capacity)
        print("It's tour is: ",self.tour)
        print("Vacancy is: ",self.vacancy)
        return 0
    
    def set_stops(self,request):
        print("Setting the stops for {} tour".format(self.tour))
        nodes = []
        for t in self.tour:
            #print("The pick up and drop-off location for node {} is:\n {}".format(t,request[t]))
            nodes.append(request[t]['pickup'])
            nodes.append(request[t]['dropoff'])
        #print("The nodes are:{}".format(nodes))
        print(t)
        return 0
      
    def get_stops(self):
        return self.tour
        
    
def read_data(file_name):
    print("Reading Data")
    df = pd.read_csv(file_name)
    data = df.as_matrix()
    #print(data)
    return data

def extract_new_requests(data,no_new_requests ,total_requests):
    new_requests = data[total_requests:no_new_requests]
    #print('{} newly added requests:\n {}'.format(no_new_requests,new_requests))
    #print(new_requests[0][0])
    #put the requests in a dictionary 
    request = {}
    for i in range(len(new_requests)):
        request[i] = {"pickup":(new_requests[i][0],new_requests[i][1]),"dropoff":(new_requests[i][2],new_requests[i][3])}
    #print("The dictionary of requests is: ", request)
    #for i in request:
        #print(request[i],"\n")
    call_GA(request)
    return 0 

def call_GA(request):
    

    request_list = GA.create_initial_pop(request)
    best_tour = GA.run_num_generations(request_list, request, num_generations)
    print("The best tour generated after {} generations is:\n{}".format(num_generations,best_tour))

    #GA.rank_fitness(request_list,request)
    
    appoint_taxi(best_tour,request)
    return 0

def appoint_taxi(best_tour,request):
    print("Appointing taxis:")
    num_taxi = math.ceil(len(best_tour['best']['tour'])/4)
    print("No. of taxis required is: {}".format(num_taxi))
    vehicle_list = []
    for i in range(num_taxi):
        veh = Vehicle("Vehicle",i+1,4,best_tour['best']['tour'][i*4:i*4+4])
        vehicle_list.append(veh)
    for_meanX = []
    for_meanY = []
    for r in range(len(request)):
        for_meanX.append(request[r]['pickup'][0])
        for_meanY.append(request[r]['pickup'][1])
    temp_meanX =np.array(for_meanX)
    temp_meanY =np.array(for_meanY)
    mean_X = np.mean(temp_meanX)
    mean_Y = np.mean(temp_meanY)
    for i in range(num_taxi):
        #vehicle_list[i].set_stops(request)
        #vehicle_list[i].details()
        to = vehicle_list[i].get_stops()
        print("The points for {}th taxis are:".format(i))
        pltX = []
        pltY = []
        pltX.append(mean_X)
        pltY.append(mean_Y)
        for t in to:
            print(request[t])
            pltX.append(request[t]['pickup'][0])
            pltY.append(request[t]['pickup'][1])
        pltX.append(mean_X)
        pltY.append(mean_Y)
        print("PLTX is:{}".format(pltX))
        print("PLTY is:{}".format(pltY))
        plt.plot(pltX,pltY,marker='o')
           
    return 0