# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 14:49:11 2018

@author: sania
"""
import numpy
import pandas as pd
import GA
import Scheduler

#defining the size of the population

def main():
    print("In main")
    #file to read data from
    data = Scheduler.read_data('SampleRides.csv')
    total_requests = 0
    no_new_requests = 32
    Scheduler.extract_new_requests(data,no_new_requests,total_requests)
    return 0

if __name__ == '__main__':
    main()
