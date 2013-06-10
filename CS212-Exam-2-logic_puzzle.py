"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager. ?????
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""
import itertools

def day_after(i, j):
    return j - i == 1

def logic_puzzle():
    order = find_order()
    return sorted(order.keys(), key=lambda x: order[x])

def find_order():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    fellas = ['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']
    #days = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday'}
    days = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5}

    orderings = list(itertools.permutations(days.values()))
    return(next({'Hamming': hamming, 'Knuth': knuth, 'Minsky': minksy, 'Simon': simon, 'Wilkes':wilkes}
                for hamming, knuth, minksy, simon, wilkes in orderings
                #6. Knuth arrived the day after Simon.
                if day_after(simon, knuth)
                for laptop, droid, tablet, iphone, other in orderings
                #1. The person who arrived on Wednesday bought the laptop.
                if days['Wednesday'] == laptop and
                #8. The person who arrived on Friday didn't buy the tablet.
                days['Friday'] != tablet and
                #12. Either the person who bought the iphone or the person who bought the tablet arrived on Tuesday.
                (iphone == days['Tuesday'] or tablet == days['Tuesday'])
                for programmer, writer, manager, designer, otherp in orderings
                #2. The programmer is not Wilkes.
                if programmer != wilkes and
                #4. The writer is not Minsky.
                writer != minksy and
                #3. Of the programmer and the person who bought the droid, one is Wilkes and the other is Hamming.
                ((droid == wilkes and programmer == hamming) or (droid == hamming and programmer == wilkes)) and
                #5. Neither Knuth nor the person who bought the tablet is the manager.
                manager != knuth and manager != tablet and
                #7. The person who arrived on Thursday is not the designer.
                days['Thursday'] != designer and
                #9. The designer didn't buy the droid.
                designer != droid and
                #11. Of the person who bought the laptop and Wilkes, one arrived on Monday and the other is the writer.
                ((laptop == days['Monday'] and wilkes == writer) or (laptop == writer and days['Monday'] == wilkes)) and
                #10. Knuth arrived the day after the manager.
                day_after(manager, knuth)
            ))
    
print logic_puzzle()