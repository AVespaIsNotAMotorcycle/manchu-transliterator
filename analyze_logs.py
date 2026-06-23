import json

def load_logs():
    entries = []
    file = open("training_logs.json", "r")
    lines = file.readlines()
    for line in lines:
        entries.append(json.loads(line))
    return entries

def length_error(entry):
    predicted = entry["predicted"]
    actual = entry["actual"]

    len_p = len(predicted)
    len_a = len(actual)
    diff = abs(len_a - len_p)

    return diff / 30

def fraction_matching_characters(entry):
    predicted = entry["predicted"]
    actual = entry["actual"]

    lmax = max(len(predicted), len(actual))
    lmin = min(len(predicted), len(actual))

    if lmax == 0: return 0

    matches = 0
    for i in range(lmin):
        ch_p = predicted[i]
        ch_a = actual[i]
        if ch_a == ch_p: matches += 1

    return matches / lmax

def percent_string(number):
    return "{0}%".format(int(number * 100)).rjust(3, ' ')

def batch(logs, function):
    results = []
    for entry in logs:
        results.append(function(entry))
    return results

def average(values):
    total = 0
    for value in values: total += value
    return total / len(values)

def analyze(start, end):
    logs = load_logs()[start:end]

    '''
    columns = ["Length error",
               "% correct chars.",
               "Predicted".ljust(30, ' '),
               "Actual"]
    print("{0} | {1} | {2} | {3}".format(columns[0], columns[1], columns[2], columns[3]))
    for entry in logs:
        error = percent_string(length_error(entry))
        matching_chars = percent_string(fraction_matching_characters(entry))
        predicted = entry["predicted"]
        actual = entry["actual"]
        print("{0} | {1} | {2} | {3}".format(error.rjust(len(columns[0]), " "),
                                       matching_chars.rjust(len(columns[1]), " "),
                                       predicted.ljust(30, " "),
                                       actual.ljust(30, " ")))
    print(average(batch(logs, fraction_matching_characters)))
    '''
    print("{0}\t {1}\t {2}\t {3}".format(str(start + 1).rjust(4, " "),
                                   str(end).rjust(4, " "),
                                   percent_string(average(batch(logs, length_error))),
                                   percent_string(average(batch(logs, fraction_matching_characters)))))

print(len(load_logs()))
for i in range(100):
    start = i * 500
    end = (i + 1) * 500
    analyze(start, end)
