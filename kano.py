import csv
from numpy import mean

file = 'results_27012021.csv'

csv_dict = {
    'id': 0, # N°Obs

    'feature1_on': 1, # ;1. Et si AudioConf vous permettait de donner un nom à l’objet de la _réunion, pour que vous et vos invités vous y retrouviez plus facilement ?
    'feature1_off': 2, # ;2. Actuellement, AudioConf ne me permet pas de donner un nom à une conférence. Je peux seulement l'identifier par sa date et son heure.
    
    'feature2_on': 3, # ;3. Et si AudioConf vous permettait de conserver le même numéro pour un rendez-vous hebdomadaire ?
    'feature2_off': 4, # ;4. Actuellement, AudioConf permet de réserver un numéro de conférence à la fois. Il n'est pas possible de réserver de numéros à l'avance.
}

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
        'functionnal_score' : [],
        'disfunctionnal_score' : []
    }
}


def read_answers(row):
    # Calculer le score fonctionnel de la feature 1
    reponse_func = row[csv_dict['feature1_on']]
    if reponse_func:
        score = functionnal_score(reponse_func)
        features[1]['functionnal_score'].append(score)

    # Calculer le score fonctionnel de la feature 2
    reponse_disfunc = row[csv_dict['feature1_off']]
    if reponse_disfunc:
        score = disfunctionnal_score(reponse_disfunc)
        features[1]['disfunctionnal_score'].append(score)

def functionnal_score(choice):
    # TODO vérifier que choice n'est pas vide
    if choice in functionnal_dict:
        return functionnal_dict[choice]
    else:
        print('"{}" manque dans le dictionnaire fonctionnel'.format(choice))

def disfunctionnal_score(choice):
    # TODO vérifier que choice n'est pas vide
    if choice in disfunctionnal_dict:
        return disfunctionnal_dict[choice]
    else:
        print('"{}" manque dans le dictionnaire disfonctionnel'.format(choice))


with open(file) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            # Skipline
            line_count += 1
        else:
            line_count += 1
            read_answers(row)




    # Calculer la moyenne de tous les scores fonctionnels de la feature 1
    # print("Score feature1 : {}".format(feature1))
    print("Score feature1 : F {} D {} ".format(mean(features[1]['functionnal_score']), mean(features[1]['disfunctionnal_score'])))

    print('Processed {:d} lines.'.format(line_count-1))
