# Border Crossing Analysis

## Approach
1. Loop through each line of the csv file and store the values in two dictictionaries; one is to store the values for every unique border-measure-date with another dictionary as its value with 'Date', 'Value', 'Measure', and 'Border' as its keys, and the other one is two store the values for every unique border-measure pairs; which will be used to calculate the averages. NOTE: All the date entries were converted to date type in order to compare the dates.

2. Loop through the keys of the dictionary with the border-measure keys, and then loop through the keys of each border-measure key, and loop through the keys again to be able to compare the dates, so that only the older months get counted. Once the average is calculated, I concatenate the border-measure pairs with each date to use it as a key to add the value to the dictionary with the rest of the data.

3. Create a list of the different dictionaries.

4. Sort the list of dictionaries using the sorted function.

5. Convert the Date back to a string to have the same format as the original entry.

6. Save the list of borders into a csv file using the DictWriter() and writerow() methods from the csv library.
