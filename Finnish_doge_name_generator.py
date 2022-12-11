# Markov chain Finnish doge name generator. 
# Can of course be used to generate any kinds of names by simply changing the source material.

# source_names.txt must be included, containing one name per line. These will be used as source for generating new names.
# excluded_names.txt must be included but may be empty. These will be excluded from both source and generated names. (For example human names can be excluded from doge names.)

import os
import random

# ze configurazióne
number_of_generated_names = 200 
minimum_name_length = 4         # ignore source names shorter than this
maximum_name_length = 13        # truncate generated names if they exceed this length
sample_length = 4               # number of characters used for each step in the Markov chain


os.system('cls')
print("Markov chain Finnish doge name generator")
print("----------------------------------------\n")


try:
    file = open("source_names.txt", "r", encoding="utf-8")
except:
    print("\nERROR!!!!!!!!!!!!!!!!!!!111111111111111111 unable to open source_names.txt.")
    quit()
names_on_file = [line.rstrip().lower() for line in file]
file.close()
print(str(len(names_on_file)) + " doge names found.")

try:
    file = open("excluded_names.txt", "r", encoding="utf-8")
except:
    print("\nERROR!!!!!!!!!!!!!!!!!!!111111111111111111 unable to open excluded_names.txt.")
    quit()
excluded_names = [line.rstrip().lower() for line in file]
file.close()


excluded_amount = 0
for name in names_on_file:
    if name in excluded_names:
        excluded_amount += 1
        names_on_file.remove(name)
print("-> " + str(excluded_amount) + " boring human names removed from the list, woof.")

# The list "names" will include start and end characters, e.g. "^^^^Doggy$"
# ^^^^ marks the start of the name and is padding for the generator so the name begins with a single random character instead of a fixed character sequence. $ marks the end of the name, stopping the generator when encountered. 
names = []
padding = ""
excluded_amount = 0
for x in range(0,sample_length):
    padding = padding + "^"
for name in names_on_file:
    if len(name) >= minimum_name_length:
        names.append(padding + name + "$")
    else: 
        excluded_amount += 1
print("-> " + str(excluded_amount) + " short names removed from the list (has to be at least " + str(minimum_name_length) + " characters).")
print("= " + str(len(names)) + " names used as source.")


parts = {}   # dictionary of each 4-character sample of a name, and the character that follows it. E.g. "Dogg": "y"
for name in names:
    for x in range (len(name)-sample_length):
        key = name[x:x+sample_length]
        value = name[x+sample_length]
        # One key can contain multiple values. Hence the first value is a list of strings with one item instead of being just a string. (Otherwise it'd have to be converted from string to list later.)
        if key in parts:
            parts[key].append(value)
        elif key not in parts:
            parts[key] = [value]


# This section selects segments the name can start with. 
# With the ^^^^ padding it just selects all names and doesn't change anything in the way the generator works. 
# However, it will be needed if the padding is not used. In this case each name should begin with one ^ as the starting character.
starting_segments = []
for part in parts:
    if part[0] == "^":
        starting_segments.append(part)


print("\nYour next dogs will be called:\n")
number_of_new_names = 0
new_names = []
tab = 0
while number_of_new_names < number_of_generated_names:
    new_name = starting_segments[random.randint(0,len(starting_segments) - 1)]
    for x in range (0,maximum_name_length):
        key = new_name[-4:]
        value = str(parts[key][random.randint(0, len(parts[key])) - 1])
        new_name = new_name + value
        if "$" in new_name:
            break
    # remove ending character $ and all initial characters ^ from generated name
    new_name = new_name[:-1]
    while new_name[0] == "^":
        new_name = new_name[1:] # remove all initial characters ^ from generated name

    if new_name in names_on_file or new_name in excluded_names or new_name in new_names:   # ignore result if it exists in source, excluded, or already generated names
        pass
    else:
        print(new_name.capitalize() + "\t", end = "")
        if (len(new_name) < 8):
            print("\t", end = "")
        new_names.append(new_name)
        number_of_new_names += 1
        tab += 1
        if tab == 10:
            tab = 0
            print("\n ")

try:
    with open("new_names.txt", 'w') as file:
        for name in new_names:
            file.write(name.capitalize() + "\n")
    print("Written to new_names.txt")
except:
    print("Unable to write new_names.txt")