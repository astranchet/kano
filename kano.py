import csv
from numpy import mean

file = 'results_27012021.csv'

functionnal_dict = {
    'Je serais ravi·e !': 4,
    'Je trouverais ça bien :)' : 2,
    "Ça ne changerait pas mon usage d'AudioConf" : 0,
    "Live with" : -1,
    "Dislike" : -2,
}

disfunctionnal_dict = {
    'Je suis ravi·e !' : -2,
    'Je trouve ça bien :)': -1,
    "Je ne suis pas concerné·e." : 0,
    "Ça ne m'enchante pas, mais je fais avec." : 2,
    "Je suis mécontent·e." : 4,
}

features = {
    1: {
        'name' : 'Nommer les conférences',
        'present_column_number': 1, # ;1. Et si AudioConf vous permettait de donner un nom à l’objet de la _réunion, pour que vous et vos invités vous y retrouviez plus facilement ?
        'absent_column_number': 2, # ;2. Actuellement, AudioConf ne me permet pas de donner un nom à une conférence. Je peux seulement l'identifier par sa date et son heure.
    }
}

# TODO : construire à la volée plutôt
scores = {
    1: {
        'functionnal_scores' : [],
        'disfunctionnal_scores' : []
    }
}

def read_answers(row):
    # Compute score for each feature
    for i in features:
        config = features[i]

        is_present_response = row[config['present_column_number']]
        if is_present_response:
            score = functionnal_score(is_present_response)
            scores[i]['functionnal_scores'].append(score)

        is_absent_response = row[config['absent_column_number']]
        if is_absent_response:
            score = disfunctionnal_score(is_absent_response)
            scores[i]['disfunctionnal_scores'].append(score)

def functionnal_score(choice):
    # TODO vérifier que choice n'est pas vide ici plutôt
    if choice in functionnal_dict:
        return functionnal_dict[choice]
    else:
        print('"{}" manque dans le dictionnaire fonctionnel'.format(choice))

def disfunctionnal_score(choice):
    # TODO vérifier que choice n'est pas vide ici plutôt
    if choice in disfunctionnal_dict:
        return disfunctionnal_dict[choice]
    else:
        print('"{}" manque dans le dictionnaire disfonctionnel'.format(choice))

def category(f_score, d_score):
    if d_score >= -1 and d_score <= 2 and f_score >= -1 and f_score <= 2:
        return "I - indifferent"
    elif d_score >= -1 and d_score <= 2 and f_score >= 2:
        return "A - attractive"
    elif d_score >= 2 and f_score >= -1 and f_score <= 2:
        return "M - must-be"
    elif d_score >= 2 and f_score >= 2:
        return "P - performance"
    elif d_score <= 2 or f_score <= 2:
        return "R - reverse"
    return "Q - questionnable "

def compute_avg():
    # Compute average of scores for each feature
    for i in features:
        feature_scores = scores[i]
        f_score = mean(feature_scores['functionnal_scores'])
        d_score = mean(feature_scores['disfunctionnal_scores'])
        print("« {} » : F {:4.2f}   D {:4.2f}   Catégorie {})".format(
            features[i]["name"],
            f_score, 
            d_score,
            category(f_score, d_score)
        ))

with open(file) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';')
    line_count = 0

    # Read answears from file
    for row in csv_reader:
        # skip header
        if line_count == 0:
            line_count += 1
        else:
            line_count += 1
            read_answers(row)

    # Compute average for each features
    compute_avg()

    # Thanks, bye
    print('{:d} lines processed.'.format(line_count-1))
