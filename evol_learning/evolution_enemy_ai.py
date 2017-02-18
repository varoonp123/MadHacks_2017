# @Author: Varoon Pazhyanur <varoon>
# @Date:   18-02-2017
# @Filename: evolution_enemy_ai.py
# @Last modified by:   varoon
# @Last modified time: 18-02-2017

from random import Random
from time import time
from time import sleep
import inspyred
import itertools

##Goal: create enemy attributes that adapy

#generator function. enemy attribues that add up to 100. Only for Generation 0.
def generate_enemy(random,args):
    SUM_OF_TRAITS = 100
    enemy_feature_vector = []
    #fire rate
    enemy_feature_vector.append(random.uniform(1,20))
    #health = random.uniform(1,20)
    #aggression=random.uniform(1,20)
    #dodge_likelihood = random.uniform(1,20)
    #shot_speed = random.uniform(1,20)
    speed = SUM_OF_TRAITS - fire_rate - health - aggression - dodge_likelihood - shot_speed
    enemy_feature_vector.append(speed)
    print(enemy_feature_vector)
    print(sum(enemy_feature_vector))
    return enemy_feature_vector


#gives segments, calculates area of polygon
def survival(enemy):
    ## TODO: FIX THIS TO BE OBJECTIVE FUNCTION
    return max(enemy)

#evaluator function. returns list of survival scores of entire generation.
def evaluate_enemy(candidates):
    fitness=[]
    for cs in candidates:
        fit = survival(cs)
        fitness.append(fit)
    return fitness

#need to bound each parameter. 0<=EACH_TRAIT<=100
"""
def bound_enemy(enemy,args):
    #amount still left to be allocated/overallocated. Positive if can add more traits.
    while (sum(enemy) is not 100):
        unallocated = 100-sum(enemy)
        for i in range(0,size(enemy))
            if enemy[i] + unallocated/size(enemy) > 0:      #if adding portion of unallocated keeps trait positive
                enemy[i] = enemy[i] + unallocated/size(enemy)
    return enemy

def bound_enemy(candidate, args):
    for i in range(0,size(candidate)):
        candidate[i] = max(min(candidate[i], 100), 0)
    return candidate
bound_polygon.lower_bound = itertools.repeat(-1)
bound_polygon.upper_bound = itertools.repeat(1)
"""
#ACTUAL EVOLUTION
def mutate_enemy(random,candidates,args):
    #gaussian distrubtion for random mutation
    mut_rate = args.setdefault('mutation_rate', 0.1)
    #bounder = args['_ec'].bounder
    for i, cs in candidates:
        for j, (c, lo, hi) in enumerate(zip(cs, bounder.lower_bound, bounder.upper_bound)):
            if random.random() < mut_rate:
                x = c[0] + random.gauss(0, 1) * (hi - lo)
                y = c[1] + random.gauss(0, 1) * (hi - lo)
                candidates[i][j] = (x, y)
        candidates[i] = bounder(candidates[i], args)
    return candidates

#ACTUAL SCRIPT:
rand = Random()
rand.seed(int(time()))
my_ec = inspyred.ec.EvolutionaryComputation(rand)
my_ec.selector = inspyred.ec.selectors.tournament_selection
my_ec.variator = [inspyred.ec.variators.uniform_crossover, mutate_enemy]
my_ec.replacer = inspyred.ec.replacers.steady_state_replacement

my_ec.terminator = [inspyred.ec.terminators.evaluation_termination, inspyred.ec.terminators.average_fitness_termination]


final_pop = my_ec.evolve(generator=generate_enemy,
                         evaluator=evaluate_enemy,
                         pop_size=10,
                         bounder=bound_enemy,
                         max_evaluations=5000,
                         num_selected=2,
                         mutation_rate=0.25,
                         canvas=can)
# Sort and print the best individual, who will be at index 0.
final_pop.sort(reverse=True)
print('Terminated due to {0}.'.format(my_ec.termination_cause))
print(final_pop[0])
sleep(10)
