import csv
import sys
from collections import namedtuple
from collections import defaultdict
from decimal import *
from operator import attrgetter

#Our named tuple will act similar to "objects" in that they have named variables we can set to represent their attributes
Modifier = namedtuple('Modifier' ,'name speed acceleration weight handling traction turbo total')

##FCN -- Reads in csv table data
##arg: string of csv file name
##ret: list of modifers
def import_table(csvName):
    l = [] #list of Modifiers we will eventually return
    r = open(csvName)
    reader = csv.reader(r)
    rowNum = 0
    for row in reader: #loop through rows
        if rowNum !=0: #ignore header row
            tempValues =[] #placeholder list of values before conversion to Modifier
            colNum = 0
            for col in row: #loop through cell by column
                if colNum == 0:
                    tempValues.append(col)
                else:
                    tempValues.append(Decimal(col))
                colNum = colNum + 1
            mod = Modifier(*tempValues) #convert placeholder list to Modifier
            l.append(mod) #add it to the end of the list we are returning
        rowNum = rowNum + 1
    r.close
    return l

##FCN -- takes imported lists, and creates a list of every  Modifier combination, with summed attributes.
##arg: four different lists of Modifiers, representing each type
##ret: list of all possible combinations of Modifiers with updated attributes
def combine_modifiers(characters, karts, wheels, gliders):
    combos = []
    for c in characters:
        for k in karts:
            for w in wheels:
                for g in gliders:
                    tempComb = []
                    tempComb.append(c.name + " + " + k.name + " + " + w.name + " + " + g.name)
                    tempComb.append(c.speed + k.speed + w.speed + g.speed)
                    tempComb.append(c.acceleration + k.acceleration + w.acceleration + g.acceleration)
                    tempComb.append(c.weight + k.weight + w.weight + g.weight)
                    tempComb.append(c.handling + k.handling + w.handling + g.handling)
                    tempComb.append(c.traction + k.traction + w.traction + g.traction)
                    tempComb.append(c.turbo + k.turbo + w.turbo + g.turbo)
                    tempComb.append(c.total + k.total + w.total + g.total)
                    comb = Modifier(*tempComb)
                    combos.append(comb)
    return combos

##FCN -- recursive prioritization of combinations, takes lists of single or grouped/summed attributes
##arg: dictionary with keys of tied values, and values of lists of combinations; list of lists of single or grouped/summed prioritized attributes; counter to know how deep into our recursion we are
##ret: list of lists of tied Modifier combos, in order of the defined priorities
def recursive_priority(tiedCombos, sortedCombos, priorities, layersDeep):
    #BC0: if there are no tied combos, append list to the list
    if len(tiedCombos) == 1:
        sortedCombos.append(tiedCombos)
        return sortedCombos
    #BC1: if we have recursed through all attribute optimizations, append list to the list
    if layersDeep == len(priorities):
        sortedCombos.append(tiedCombos)
        return sortedCombos
    #create dictionary of lists from list, split by ties by making tied value the key
    optDict = defaultdict(list)
    for c in tiedCombos:
        priority = priorities[layersDeep] #key (attribute) we are optimizing
        tempSum = 0
        #sum attributes of tied-priorities
        for p in priority:
            tempSum = tempSum + getattr(c, p)
        optDict[tempSum].append(c)
    #for every key in our split-of-ties dictionary, recurse on the next optimization
    for key in sorted(optDict, reverse=True):
        sortedCombos = recursive_priority(optDict[key], sortedCombos, priorities, layersDeep+1)
    return sortedCombos

##FCN -- Prints data to csv file and/or console
##arg: takes in list of lists of Modifier combos; list of prioritized attributes; name of csv output file; boolean on whether to print data to console
def print_data(combos, priorities, csvName, printConsole):
    w = open(csvName, 'wb')
    writer = csv.writer(w, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    topRow = ['Combination']
    for p in priorities:
        topRow.append(str(p)) ##append appropriate header cells based on what we prioritized
    writer.writerow(topRow)
    for list in combos: # loop through each of list of tied Modifier combos
        for entry in list: # loop through tied Modifier combo
            writeList = [] # placeholder list of strings we will write to a row
            if printConsole:
                print entry.name,
            writeList.append(entry.name) # append combo name
            for priority in priorities: # loop through each list of single/or grouped attributes
                tempSum = 0 # placeholder variable for summed attributes
                for p in priority: # loop through each attribute in the list
                    tempSum = tempSum + getattr(entry, p) #sum attribute
                if printConsole:
                    print " || ", priority, ": ", str(tempSum),
                writeList.append(tempSum) #append single or summed attribute value
            if printConsole:
                print " |"
            writer.writerow(writeList) #write the row
    w.close

##--------------------------------##
#Import data and create list of all combinations
allCombinations = combine_modifiers(import_table('characters.csv'), import_table('karts.csv'), import_table('wheels.csv'), import_table('gliders.csv'))

#TEST: 3 different ordered lists of priorities using recursive function, and then print to csv output files
priorities1 = [['total'],['acceleration'],['weight'],['speed'],['turbo'],['traction'],['handling']]
priorities2 = [['total'],['acceleration'],['weight'],['speed','traction','handling','turbo']]
priorities3 = [['speed','acceleration'],['total'],['weight','turbo','traction','handling']]

sortedCombos1 = recursive_priority(allCombinations, [], priorities1, 0)
sortedCombos2 = recursive_priority(allCombinations, [], priorities2, 0)
sortedCombos3 = recursive_priority(allCombinations, [], priorities3, 0)

print_data(sortedCombos1, priorities1, 'output-priorities1.csv', False)
print_data(sortedCombos2, priorities2, 'output-priorities2.csv',False)
print_data(sortedCombos3, priorities3, 'output-priorities3.csv', False)

##EDGE: test edge cases, then print to csv output files
edge1 = [['speed','acceleration','total','weight','turbo','traction','handling']]
edge2 = [['speed']]
edge3 = [['total'],['speed','acceleration'],['acceleration','weight'],['weight','traction'],['traction','handling'],['handling','turbo']]
edge4 = [['total'],['acceleration'],['weight'],['speed'],['turbo'],['traction'],['handling'],['total'],['acceleration'],['weight'],['speed'],['turbo'],['traction'],['handling']]

edgeCombos1 = recursive_priority(allCombinations, [], edge1, 0)
edgeCombos2 = recursive_priority(allCombinations, [], edge2, 0)
edgeCombos3 = recursive_priority(allCombinations, [], edge3, 0)
edgeCombos4 = recursive_priority(allCombinations, [], edge4, 0)

print_data(edgeCombos1, edge1, 'output-edge1.csv', False)
print_data(edgeCombos2, edge2, 'output-edge2.csv', False)
print_data(edgeCombos3, edge3, 'output-edge3.csv', False)
print_data(edgeCombos4, edge4, 'output-edge4.csv', False)
##--------------------------------##
