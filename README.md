## TEAMMATES: 

Pelin Cetin [pc2807] and Justin Andrew Zwick [jaz2130]

## FILES:

1. main.py
2. INTEGRATED-DATASET.csv
3. example-run.txt 

## HOW TO RUN OUR PROGRAM:

python3 main.py INTEGRATED-DATASET.csv <min_support> <min_confidence>

## OUR DATASET:

a) We started off with this dataset: https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j 
It is the department of health's inspection results for different NYC restaurants.

b) To make INTEGRATED-DATASET.csv, we iterated over the original dataset line by line using the Python csv module, 
filter out all rows that have a critical flag value of 'A' = 'Not applicable', 
filter out all rows that have a 'N', 'Z', or 'P' value in the grade column (meaning 'Not yet graded' and 'grade pending'),
and then we wrote the columns "borough", "inspection date", "violation code", and "grade" to the new csv file. At first, we were filtering out all rows where the inspection did not occur in 2018, but after a conversation with Professor Gravano, we decided that inspecting results from all years would lead to more compelling results, so we stopped filtering based on the year.

c) Our choice of dataset is compelling because there could be some interesting correlations between a borough and a certain health grade, or a borough and a certain health violation that seems to be common there. As an example from our output, 

[A, Manhattan], 21.02%
[Staten Island] => [A] (Conf:78.68%  Supp:4.41%)

Although Manhattan and the grade A appear the most frequently together out of all the other boroughs, the confidence that the grade will be A if the restaurant is in Staten Island is higher than all the other boroughs.

[10F, Bronx] => [A] (Conf:79.93%  Supp:1.00%)

10F refers to the following violation code: "Non-food contact surface improperly constructed. Unacceptable material used. Non-food contact surface or equipment improperly maintained and/or not properly sealed, raised, spaced or movable to allow accessibility for cleaning on all sides, above and underneath the unit.". If a restaurant has the 10F violation code and is in Bronx, it's highly likely that its grade is A. This is compelling because although most people would probably not prefer to go to a restaurant with hygiene issues, the fact that it has a grade "A" would make people prefer to go there. 


## INTERNAL DESIGN:

We start off by extracting the csv_filename, min_support and min_conf from the command line. We iterate over every line of the csv file, adding all transactions to a set to remove duplicates. Then we count item occurrences to determine the large 1-items. We iterate over the tuples we extracted from the csv file, count the initial occurrences. At this point, there is only one element in the tuples. Then, we get the item sets that are higher than or equal to the threshold defined by the user. If the tuple occurs less than the threshold, we pop that from the first_itemset we created in the previous step. If not, we append the tuple and its occurrence in the desired_itemset dictionary with the tuple being the key and the occurrence the value. We also append the tuple to the list l1 (large 1-itemset). 

After initializing the first list, we'll be increasing k for each time we implement the apriori_gen algorithm. We apply an iterative approach or level-wise search where k-frequent item sets are used to find k+1 item sets. While l1 is not empty, we look at the combinations of l1 and 2 and append the candidate to our candidate_itemset. In the paper, the authors followed the following approach: i.item1 == j.item1, ..., i.itemk-2 = j.itemk-2, i.itemk-1 < j.itemk-1. However, after playing around for a while, we decided to tweak the generation algorithm a little bit too better suit our dataset. Professor Gravano said we were allowed to do that on Piazza. After we select the initial candidates, we arrive to the prune step. 
In the prune step, we delete all item sets c E ck such that some (k-1)-subset of c is not in Lk-1. If a transaction doesn't contain any candidate k-itemset, then Ck will not have an entry for this transaction. Next, we determine which of the candidate item sets are actually large, and they become the seed for the next pass. Again, we do that by counting the frequencies of the tuples. In the paper, this is done by using a hashset but Professor Gravano said that we were allowed to follow other approaches for this part of the code, so we decided to use the same (iterate and count frequencies) approach that we started the code with. Now that we found our candidates, we then build l1 again and append the candidates to desired_itemset dictionary. This process continues until no new large item sets are found. At the end, the dictionary contains all tuples, whose frequencies are higher than the threshold set by the user. So, we sort this dictionary based on the key (which contains the frequency) to find the highest frequency item sets and to print them in the output file. We decided to keep the two decimals after the comma to give a more accurate result to the user. 

Lastly, we generate association rules using those items in the item sets. We do this by using the algorithm the professor explained in the 9th lecture. We first find all large item sets (by iterating over the desired_itemset dictionary's keys and making sure that the frequency is bigger than zero) and then for each large itemset, we find all association rules with sufficient confidence (by calculating the confidence of each tuple and comparing that to min_confidence). 

## SAMPLE RUN:

This was called using "python3 main.py INTEGRATED-DATASET.csv 0.01 0.01"
The results are compelling because it shows the user compelling relations between violations and grades and boroughs. We eat food everyday and a large fraction of the population eat outside. We may go somewhere thinking that because it's grade A, it must be clean. However, the restaurant might have violated several codes and still received a good grade. 

