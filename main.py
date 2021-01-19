import csv
import sys
from itertools import combinations
import operator

is_for_gen = None

def apriori_algorithm(all_transactions, num_of_transactions, min_supp, output_file):
    #  From the paper:
    #  "The first pass of the algorithm simply counts item occurrences to determine the large 1-items."
    first_itemset, desired_itemset = {}, {}
    l1 = []  # large 1-itemsets
    k = 2
    for transaction in all_transactions:
        for t in transaction:
            if t not in first_itemset and len(t) > 0:
                first_itemset[t] = 1  # initialize
            elif t in first_itemset and len(t) > 0:
                first_itemset[t] += 1  # counting item sets

    #  now, we need to get the item sets that are higher than or equal to the threshold defined by the user
    for element in list(first_itemset):
        if min_supp > float(first_itemset[element]) / num_of_transactions:  # if smaller than the threshold
            first_itemset.pop(element)
        else:
            desired_itemset[(element,)] = float(first_itemset[element]) / num_of_transactions
            l1.append((element,))

    #  now, we initialized the first list, we'll be increasing k for each time we implement the
    #  apriori_gen algorithm. We apply an iterative approach or level-wise search where k-frequent item sets
    #  are used to find k+1 item sets.
    #  From the paper: "The apriori-gen function takes as argument Lk-1,
    #  the set of all large (k - 1)-item sets. It returns a superset of the set of all large k-items.

    is_empty_flag = False
    while not is_empty_flag:
        candidate_itemsets = []
        temp_set = set(l1)  # remove duplicates

        #  now, we need to do the join step: "First, in the join step, we join Lk-1 with Lk-1"
        for i, j in combinations(l1, 2):
            # TODO: THERE MAY BE A BETTER GENERATION METHOD FOR THE DATASET
            # The paper: i.item1 == j.item1, ..., i.itemk-2 = j.itemk-2, i.itemk-1 < j.itemk-1
            if i[:k - 3] == j[:k - 3]:
                # print("i: " + str(i))
                # print("j: " + str(j))
                # convert tuple to a list
                temp_item = list(i)
                temp_item.append(j[k - 2])
                # change back to tuple and add it to ck
                temp_item = tuple(sorted(temp_item))
                candidate_itemsets.append(temp_item)


        # "Next, in the prune step, we delete all item sets c E ck such that some (k-1)-subset of c is not in Lk-1"
        # If a transaction doesn't contain any candidate k-itemset, then Ck will not have an entry for this transaction.
        for candidate in candidate_itemsets:
            for subset in combinations(candidate, k - 1):
                if subset not in temp_set:
                    candidate_itemsets.remove(candidate)
                    break

        # Now, "we determine which of the candidate item sets are actually large, and they become the seed for the
        # next pass. This process continues until no new large item sets are found" (when l1 is empty)
        temp_desired = dict()
        temp_set = set(candidate_itemsets)
        for transaction in all_transactions:
            candidate_transaction = set()
            for i in combinations(transaction, k):
                candidate_transaction.add(tuple(sorted(i)))
            for candidate in candidate_transaction.intersection(temp_set):  # we're counting the frequency
                if candidate in temp_desired:
                    temp_desired[candidate] += 1
                else:
                    temp_desired[candidate] = 1

        # build l1 again
        temp_l1 = []
        for candidate in sorted(temp_desired.keys()):
            if min_supp < temp_desired[candidate] / num_of_transactions:
                temp_l1.append(candidate)
                desired_itemset[candidate] = temp_desired[candidate] / num_of_transactions

        l1 = temp_l1
        if len(l1) == 0:
            is_empty_flag = True

        # increment k and loop again
        k += 1

    global is_for_gen
    is_for_gen = desired_itemset

    return sorted(desired_itemset.items(), key=lambda elem: elem[1], reverse=True)


def main():
    csv_name = sys.argv[1]  # your INTEGRATED-DATASET file
    min_supp = float(sys.argv[2])  # between 0 and 1
    min_conf = float(sys.argv[3])  # between 0 and 1
    output_file = open('output.txt', 'w')
    all_transactions = set()

    with open(csv_name, mode='r') as csv_file:  # open the INTEGRATED-DATASET file in read mode
        file_reader = csv.reader(csv_file)  # make a reader object which will iterate over lines in the given csvfile.
        for row in file_reader:  # Each row read from the csv file is returned as a list of strings
            all_transactions.add(tuple(row))  # add transactions to a set to get rid of duplicates

    # From Piazza: Your code has to generate a file named output.txt every time you run it, no matter the database you use.
    supp_str = str(min_supp * 100)
    conf_str = str(min_conf * 100)
    output_file.write('==Frequent itemsets (min_sup =' + supp_str + '%)' + '\n')

    num_of_transactions = len(all_transactions)
    first_part = apriori_algorithm(all_transactions, num_of_transactions, min_supp, output_file)
    for first in first_part:
        supp_str_of_element = str("{:.2f}".format(first[1] * 100))
        output_file.write('[' + ', '.join(first[0]) + '], ' + supp_str_of_element + '%' + '\n')

    output_file.write('==High-confidence association rules (min_conf =' + conf_str + '%)' + '\n')

    # generate rules
    associated_rules = {}
    for i_set in is_for_gen.keys():
        if len(i_set) != 1:
            for i in i_set:
                l = list(i_set)  #lefthand side
                l.remove(i)
                if is_for_gen[tuple(l)] > 0:
                    r = [i]
                    cur_conf = is_for_gen[i_set] / is_for_gen[tuple(l)]
                    if cur_conf >= min_conf:
                        tmp = dict()
                        tmp['supp'] = is_for_gen[i_set]
                        tmp['conf'] = cur_conf
                        key = '[' + ', '.join(l) + '] => ' + '[' + str(r[0]) + ']'
                        # DONE!
                        associated_rules[key] = tmp

    associated_rules = sorted(associated_rules.items(), key=lambda x: operator.getitem(x[1], 'conf'), reverse=True)
    for rule in associated_rules:
        str_supp_rule = str("{:.2f}".format(rule[1]['supp'] * 100))
        str_conf_rule = str("{:.2f}".format(rule[1]['conf'] * 100))
        output_file.write(rule[0] + ' (Conf:' + str_conf_rule + '%  Supp:' + str_supp_rule + '%)\n')

    output_file.close()


if __name__ == "__main__":
    main()