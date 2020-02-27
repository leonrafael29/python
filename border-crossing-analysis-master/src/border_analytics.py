import csv
import datetime
import math
from operator import itemgetter



#Load Border_Crossing_Entry_Data
line_count = 0
 
borders_set = set() #Use this set to store borders
borders_measure_set = set() #Use this set to store border-measure pairs
border = {}
border_me = {} #to store the dates and values of pairs border-measure to find average
dates = set()

with open('./input/Border_Crossing_Entry_data.csv') as file:
	csv_file = csv.reader(file, delimiter = ',')
	for row in csv_file:
		if line_count == 0: #to skip header
			line_count += 1
			pass
		else:
			border_measure_date= row[3] + "_" + row[5] + "_" + row[4]
			border_measure = row[3] + "_" + row[5]
			if border_measure_date in borders_set:
				border[border_measure_date]['Value'] += int(row[6])
 

			else:
				border[border_measure_date] = {}
				border[border_measure_date]['Border'] = row[3]
				border[border_measure_date]['Date'] = datetime.datetime.strptime(row[4], '%m/%d/%Y %I:%M:%S %p')
				border[border_measure_date]['Measure'] = row[5]
				border[border_measure_date]['Value'] = int(row[6])

				borders_set.add(border_measure_date)

			if border_measure in border_me:
				if row[4] in border_me[border_measure]:
					border_me[border_measure][row[4]] += int(row[6]) 
				else:
					border_me[border_measure][row[4]] = int(row[6]) #the border-measure pair is in the dicitionary, but the date is not

			else:
				border_me[border_measure] = {}
				border_me[border_measure][row[4]] = int(row[6])

			
#print(border_me['US-Canada Border_Buses']['06/01/2019 12:00:00 AM'])
#print(border_me)			

#Find the average for every border-measure pair


border_measure_average = {}
for measure in border_me.keys():
	for date in border_me[measure].keys():
		sum_values = 0
		count = 0
		for i in border_me[measure].keys():
			if datetime.datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p') > datetime.datetime.strptime(i, '%m/%d/%Y %I:%M:%S %p'):
				sum_values += border_me[measure][i]
				count += 1
		if count == 0:
			average = 0
		else:
			average = math.ceil(sum_values / count)
		border_measure_average[measure + "_" + date] = average

#print(border_measure_average)

#Add the average to the border dictionary
for i in border:
	border[i]['Average'] = border_measure_average[i]

#rint(border)

#list of borders
border_list = [border[x] for x in border.keys()]

#sort the list of borders by Date, Border, Measure, and Value
sorted_borders = sorted(border_list, key = itemgetter('Date', 'Value', 'Measure', 'Border'), reverse = True)

#Change the format of the dates
for i in sorted_borders:
	i['Date'] = datetime.datetime.strftime(i['Date'], '%m/%d/%Y %I:%M:%S %p') 

print(border_list)

#save border_list to a csv file
csv_columns = ['Border', 'Date', 'Measure', 'Value', 'Average']
with open("./output/report.csv", 'w') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
	writer.writeheader()
	for border in sorted_borders:
		writer.writerow(border)









			#border_mean[row[3] + "_" + row[5]].append(row[6])



	
			
			