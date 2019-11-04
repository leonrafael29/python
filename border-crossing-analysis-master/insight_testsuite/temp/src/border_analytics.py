import csv
import datetime
from operator import itemgetter
from itertools import groupby


#Load Border_Crossing_Entry_Data
headers = ['Border', 'Date', 'Measure', 'Value', 'Average']
line_count = 0
borders_list = []
#create one dictionary for every needed information to store the values
border_value = {}
border_border = {}
border_date = {}
border_date_string = {}
border_measure = {}
data = [] #to store all dictionaries grouped by border, measure, and date
unique_borders = set() #to keep only unique border-measure elements
dict_bor_and_meas = {}
dict_bor_and_values = {}

with open('/users/leongutierrez/Documents/python/border-crossing-analysis-master/input/Border_Crossing_Entry_data.csv') as file:
	csv_file = csv.reader(file, delimiter = ',')
	for row in csv_file:
		if line_count == 0: #to skip header
			line_count += 1
			pass
		else:
			new_item = row[3] + "-" + str(row[4]) + "-" + row[5] #this is going to be the key for the dictionaries, to aggregate values by border-measure-date
			if new_item not in borders_list:
				border_value[new_item] = int(row[6])
				border_border[new_item] = row[3]
				border_date[new_item] = datetime.datetime.strptime(row[4], '%m/%d/%Y %I:%M:%S %p')
				border_date_string[new_item] = row[4]
				border_measure[new_item] = row[5]


				# find the most current date for every unique border-measure 
				border_and_measure = row[3] + "-" + row[5]
				max_date = datetime.datetime.strptime(row[4], '%m/%d/%Y %I:%M:%S %p')
				
				if border_and_measure in unique_borders:
					if max_date > dict_bor_and_meas[border_and_measure]:
						dict_bor_and_meas[border_and_measure] = max_date		
				else:
					dict_bor_and_meas[border_and_measure] = max_date
					unique_borders.add(border_and_measure)

			else:
				border_value[new_item] += int(row[6])

#create lists of the values of dictionaries to be able to iterate through them
border = list(border_border.values())
date = list(border_date.values())
date_string = list(border_date_string.values())
date_string = list(border_date_string.values())
measure = list(border_measure.values())
value = list(border_value.values())
new_value = {} #in this dictionary I'm going to store the values of all borde

#print(border[1])
#print(value[1])
#get the values for every set of border-measure, excluding the most current date
for i in range(len(border_value.keys())):
	new_border = border[i] + "-" + measure[i]

	if date[i] != dict_bor_and_meas[new_border]:
		new_value.setdefault(new_border,[]).append(value[i])

#print(new_value)	
#print(new_value.keys())


#find the average for every border-measure
avgDict = {}
for k, v in new_value.items():
	avgDict[k] = round(sum(v)/ len(v))

#print(avgDict)

#assign their respective averages to dictionaries with most current date, and 0 to the others.
border_average = border_value.copy()
border_average_keys = list(border_value.keys())
for i in range(len(border_value.keys())):
	new_border = border[i] + "-" + measure[i]

	if date[i] != dict_bor_and_meas[new_border]:
		border_average[border_average_keys[i]] = 0
	else:
		border_average[border_average_keys[i]] = avgDict[new_border]

#print(border_average)
#Join all dictionaries into one
#data['Border'] = list(border_border.values())
#data['Date'] = list(border_date.values())
#data['Measure'] = list(border_measure.values())
#data['Value'] = list(border_value.values())

#def filterDict(dictObj, callback):
#	newDict = dict()
#	for (key, value) in dictObj.items():
#		if callback((key, value)):
#			newDict[key] = value
#	return newDict

#create a dictionary for every border-measure-date entry, and append them to the data list.
average = list(border_average.values())
for i in range(len(border_value.keys())):
	new_border = {}
	new_border['Border'] = border[i]
	new_border['Date'] = date[i]
	new_border['Measure'] = measure[i]
	new_border['Value'] = value[i]
	new_border['Average'] = average[i]
	data.append(new_border)




#Sort data dictionary
data.sort(key = itemgetter('Date', 'Value', 'Measure', 'Border'), reverse = True)

#change format of data entries
for i in data:
	i['Date'] = i['Date'].strftime('%m/%d/%Y %I:%M%:%S %p')

#print(data[1:5])

#Save the data dictionary as a csv file.
with open('./output/report.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for data in data:
            writer.writerow(data)


#Calculate average of every Border and Measure
#for border, measure, items in groupby(data, key= itemgetter('Border', 'Measure')):
#	print(border)
#	print(measure)
#	for i in items:
#		print(' ', i)





				#elif i['Border'] == row[3] & i['Date'] == row[4] & i['Measure'] == row[5]:
				#	i['Value'] += float(row[6])
#
#				elif i['Border'] == row[3] & i['Date'] != row[4] & i['Measure'] == row[5]:
#					border['Border'] = row[3]
#					border['Date'] = row[4]
#					border['Measure'] = row[5]
#					border['Value'] = float(row[6])
#					data.append(border)
#
#				elif i['Border'] == row[3] & i['Date'] == row[4] & i['Measure'] != row[5]:
#					border['Border'] = row[3]
#					border['Date'] = row[4]
#					border['Measure'] = row[5]
#					border['Value'] = float(row[6])
#					data.append(border)






