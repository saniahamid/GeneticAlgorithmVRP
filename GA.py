# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 14:40:02 2018

@author: sania hamid

This code optimizes the routing using Genetic Algorithm startergy
"""

import numpy as np
import random
import math
import datetime
from sklearn.utils import shuffle

tournament_size = 3
num_parents  = 0
crossover_probability = 0.9
mutation_probability = 0.5

def create_initial_pop(request,pop_size=400):
    #print("In GA.py")
    global num_parents 
    num_parents = (int(pop_size*0.30))
    request_list = []
    for i in (request.keys()):
        request_list.append(i)

 
    #generating the population
    initial_pop = []
    for i in range(pop_size):
        temp = request_list.copy()
        random.shuffle(temp)
        initial_pop.append(temp)
    return initial_pop

def run_num_generations(pop_list, request, num_generations):
    #print("In run_num_generations")
    x = datetime.datetime.now()
    a = x.strftime("%X")
    b = a.replace(":","") 
    fh = open("Log\data"+str(b)+".txt","a")
    for i in range(num_generations):
        fitness = calc_fitness(pop_list,request)
        #print("Population before calling best chromosome:")
        #for q in pop_list:
            #print(q)
        #print("Fitness of that population:")
        #for e in fitness:
            #print(e)
        best_ind = calc_best_chromosome(pop_list,fitness)
        print("The best individual in {}th generation is:\n{}".format(i,best_ind))
        fh.write(str(i)+" "+ str(best_ind['best']['fitness'])+"\n")
        temp_pop_list = pop_list.copy()
        temp_fitness = fitness.copy()
        parent = []
        pt = []
        #print("Population for the {}th generation is:".format(i))
        #for k in pop_list:
            #print(k)
        #print("The number of parents are:",num_parents)
        for j in range(num_parents):
            
            parent.append(parent_selection(temp_pop_list,request,temp_fitness,tournament_size))
            if parent[j] in pop_list:
                index = temp_pop_list.index(parent[j])
                del temp_pop_list[index]
                del temp_fitness[index]
                
        #print("\nThe selected parents are: \n")
        #for b in parent:
            #print(b)
                
        #print("\nPopulation after deleting parents: \n")
        #for m in temp_pop_list:
            #print(m)
        
        rand_crossover = random.uniform(0,1)
        if (rand_crossover <= crossover_probability):
            #print("crossover")
            for i in parent:
                temp = i.copy()
                pt.append(temp)
            offsprings =  crossover(pt, request)
            #print("\nThe offsprings are: \n")
            #for d in offsprings:
            #print(d)
            rand_mutation = random.uniform(0,1)
            if(rand_mutation <= mutation_probability):
                #print("mutation")
                mutated_offsprings = mutation(offsprings)
            else:
                mutated_offsprings = []
        else:
            offsprings = []
            mutated_offsprings = []
        #print("new population")
        #offsprings = []
        #mutated_offsprings = []
        pop_list = new_population_selection(pop_list,parent,parent,offsprings,mutated_offsprings)
    fh.close()
    return best_ind

def calc_fitness(pop_list,request):
    #print("In calculate fitness")

    total_distance_individual = []
    for i in pop_list:
        sum_route = euclidean_distance(i,request)
        total_distance_individual.append(sum_route)
               
    return total_distance_individual

def euclidean_distance(individual,request):
  
    sum_dist = 0
    for j in range(len(individual)-1):
       
        x1 = request[individual[j]]['pickup'][1]
        y1 = request[individual[j]]['pickup'][0]
        x2 = request[individual[j+1]]['pickup'][1]
        y2 = request[individual[j+1]]['pickup'][0]
        
        sum_dist += math.sqrt(((x2-x1))**2+((y2-y1))**2)

    return sum_dist

def parent_selection(pop_list,request,fitness,tournament_size):
   
    parent = []
    #print("Population Length:",range(len(pop_list)))
    #print("Tounament_size:",tournament_size)
    if(len(pop_list) <= tournament_size):
        return (pop_list[0])
    else:
        select_tour = random.sample(range(len(pop_list)), tournament_size)
   
        selected_chromosomes = []
        fitness_selected_chromosome = []
        for i in select_tour:
            selected_chromosomes.append(pop_list[i])
            fitness_selected_chromosome.append(fitness[i])
        ranked_selected_chromosomes = [x for _,x in sorted(zip(fitness_selected_chromosome,selected_chromosomes))]
        ranked_fitness_selected_chromosome = [y for y,_ in sorted(zip(fitness_selected_chromosome,selected_chromosomes))]
        return ranked_selected_chromosomes[0]
    
def create_pop():
    return pop

def fitness():
    return fitness



def crossover(par,request):
    #print("In crossover")
    #print("The parents are.{}".format(parents))
    #print("The requests are. {}".format(request))
    parents = []
    offsprings = []
    for r in range(len(par)-1):
        a = par[r].copy()
        b = par[r+1].copy()
        parents.append(a)
        parents.append(b)
  
    length = len(parents)
    if (length%2 == 1):
        length -=1
    for i in range(0,(length-1),2):
        
        fitness_append_parent1_ele1 = []
        fitness_append_parent2_ele1 = []
        fitness_append_parent1_ele2 = []
        fitness_append_parent2_ele2 = []
        
        length_parent = len(parents[i])
       
        rand_1 = random.randint(0,length_parent-2)
        rand_2 = random.randint(0,length_parent-2)
        
              
        del_parent1_1 = parents[i+1][rand_2]
        del_parent1_2 = parents[i+1][rand_2+1]
        del_parent2_1 = parents[i][rand_1]
        del_parent2_2 = parents[i][rand_1+1]
        
        #print("deleting {} and {} from parent {}".format(del_parent1_1,del_parent1_2,parents[i]))
        parents[i].remove(del_parent1_1)
        parents[i].remove(del_parent1_2)
        parents[i+1].remove(del_parent2_1)
        parents[i+1].remove(del_parent2_2)
        
        
        for j in range(len(parents[i])+1):
            parents[i].insert(j,del_parent1_1)
            parents[i+1].insert(j,del_parent2_1)
            
            fitp1_1 = euclidean_distance(parents[i],request)
            
            fitness_append_parent1_ele1.append(fitp1_1)
            
            fitp2_1 = euclidean_distance(parents[i+1],request)
           
            fitness_append_parent2_ele1.append(fitp2_1)
            
            parents[i].remove(del_parent1_1)
            parents[i+1].remove(del_parent2_1)
            
        
        indp1_1 = np.argmin(fitness_append_parent1_ele1)
 
     
        indp2_1 = np.argmin(fitness_append_parent2_ele1)
        
        
        parents[i].insert(indp1_1,del_parent1_1)
        parents[i+1].insert(indp2_1,del_parent2_1)
        
        #print("after appending\n {} \n {}".format(parents[i],parents[i+1]))
        
        for j in range(len(parents[i])+1):
            parents[i].insert(j,del_parent1_2)
            parents[i+1].insert(j,del_parent2_2)
           
            fitp1_2 = euclidean_distance(parents[i],request)
          
            fitness_append_parent1_ele2.append(fitp1_2)
            
            fitp2_2 = euclidean_distance(parents[i+1],request)
       
            fitness_append_parent2_ele2.append(fitp2_2)
            
            parents[i].remove(del_parent1_2)
            parents[i+1].remove(del_parent2_2)
            
    
        indp1_2 = np.argmin(fitness_append_parent1_ele2)

        indp2_2 = np.argmin(fitness_append_parent2_ele2)

        
        parents[i].insert(indp1_2,del_parent1_2)
        parents[i+1].insert(indp2_2,del_parent2_2)
        
    offsprings = parents
    
    return offsprings

def mutation(offsprings):
    #print("In mutation")

    for i in range(len(offsprings)):
       
        rand_1 = random.randint(0,len(offsprings[i]))
        rand_2 = random.randint(0,len(offsprings[i]))
        while(rand_2 == rand_1):
            rand_2 = random.randint(0,len(offsprings))
        if(rand_1>rand_2):
            a = rand_2
            b = rand_1
        else:
            a = rand_1
            b = rand_2
        b+=1
        #print("The indexes selected are {} and {}".format(a,b))
        #print("Mutating the offspring: {}".format(offsprings[i]))
        #offsprings[0][a:b] = a[0][a:b][::-1]
        #print("After Mutatiion:{}".format(offsprings[0][3:7]))
        #print("After Mutatiion:{}".format(offsprings[0][3:7:][::-1]))
        offsprings[i][a:b] = offsprings[i][a:b:][::-1]
        #print("Offspring after mutation is: {}".format(offsprings[i]))
    return offsprings

def new_population_selection(pop_list,parent,parents,offsprings,mutated_offsprings):
    #print("In new population")
    #print("Population is:")
    #for a in pop_list:
        #print(a)
    #print("Parents are:")
    #for p in parents:
        #print(p)
    #print("Offsprings are:")
    #for b in offsprings:
        #print(b)
    #print("Mutated offsprings are:")
    #for c in mutated_offsprings:
        #print(c)
    #print("Creating new population:")
    temp_pop_list = []
    for k in pop_list:
        if(k not in parents):
            temp_pop_list.append(k)
    #print("The population without the parents is:")
    #for e in temp_pop_list:
        #print(e)
    new_pop = []
    for p1 in parents:
        new_pop.append(p1)
    for b1 in offsprings:
        new_pop.append(b1)
    for c1 in mutated_offsprings:
        new_pop.append(c1)
    for i in range(int(len(temp_pop_list)*0.6)):
        new_pop.append(temp_pop_list[i])
    #print("The new poplulation is:")
    #for u in new_pop:
        #print(u)
    return new_pop

def calc_best_chromosome(pop_list,fitness):
    #print("In Calculate best chromosome.")
    best_fitness_index = np.argmin(fitness)
    #print("The best fitness is {} at index {}:".format(fitness[best_fitness_index],best_fitness_index))
    #print("The tour for this fitness is:\n{}".format(pop_list[best_fitness_index]))
    best_chromosome = {"best":{"tour":pop_list[best_fitness_index],"fitness":fitness[best_fitness_index]}}
    #print(best_chromosome)
    return best_chromosome
