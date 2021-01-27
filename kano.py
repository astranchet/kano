import csv
from numpy import mean
import matplotlib.pyplot as plt

file = 'results_27012021.csv'

functionnal_dict = {
    'Je serais ravi·e !': 4,
    'Je trouverais ça bien :)' : 2,
    "Ça ne changerait pas mon usage d'AudioConf" : 0,
    "Ça ne m'enchenterait pas, mais je ferais avec." : -1,
    "Je serais mécontent·e." : -2,
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
    },
    2: {
        'name' : 'Réserver un numéro récurrent',
        'present_column_number': 3, # ;3. Et si AudioConf vous permettait de conserver le même numéro pour un rendez-vous hebdomadaire ?
        'absent_column_number': 4, # ;4. Actuellement, AudioConf permet de réserver un numéro de conférence à la fois. Il n'est pas possible de réserver de numéros à l'avance.
    },
    3: {
        'name' : 'Inviter des personnes',
        'present_column_number': 5, 
        'absent_column_number': 6,
    },
    3: {
        'name' : 'Ajouter à votre agenda',
        'present_column_number': 7, 
        'absent_column_number': 8,
    },
    4: {
        'name' : 'Rendre des personnes silencieuses',
        'present_column_number': 9, 
        'absent_column_number': 10,
    },
    5: {
        'name' : 'Savoir qui est présent',
        'present_column_number': 11, 
        'absent_column_number': 12,
    },
    6: {
        'name' : 'Avoir accès à un tableau de bord pendant la conférence',
        'present_column_number': 13, 
        'absent_column_number': 14,
    },
    7: {
        'name' : 'Recevoir un rapport après la conférence',
        'present_column_number': 15, 
        'absent_column_number': 16,
    }
}

scores = {}

def init_score_results():
    for i in features:
        name = features[i]["name"]
        scores[i] = {
            'name':  name,
            'functionnal_scores' : [],
            'disfunctionnal_scores' : []
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
    if d_score > -1 and d_score < 2 and f_score > -1 and f_score < 2:
        return "I - indifferent"
    elif d_score >= -1 and d_score < 2 and f_score >= 2:
        return "A - attractive"
    elif d_score >= 2 and f_score >= -1 and f_score < 2:
        return "M - must-be"
    elif d_score >= 2 and f_score >= 2:
        return "P - performance"
    elif d_score <= 2 or f_score <= 2:
        return "R - reverse"
    return "Q - questionnable "


plots_x = []
plots_y = []
plots_colors = []

def compute_avg():
    # Compute average of scores for each feature
    for i in features:
        feature_scores = scores[i]
        name = features[i]["name"]
        f_score = mean(feature_scores['functionnal_scores'])
        d_score = mean(feature_scores['disfunctionnal_scores'])
        feature_category = category(f_score, d_score)
        print("{} - « {} » : D {:4.2f}   F {:4.2f}   Catégorie {}".format(
            i,
            name,
            d_score, 
            f_score,
            feature_category
        ))
        plots_x.append(d_score)
        plots_y.append(f_score)
        plots_colors.append("aabbcc")


def draw_chart():
    # axes
    plt.plot([-2, 4], [0, 0], color = 'grey', linestyle = 'solid')
    plt.plot([0, 0], [-2, 4], color = 'grey', linestyle = 'solid')    
    # cadrant
    plt.plot([0, 4], [2, 2], color = 'grey', linestyle = 'dashed')
    plt.plot([2, 2], [0, 4], color = 'grey', linestyle = 'dashed')
    # cadrant labels
    plt.annotate("Performance", (3,3))
    plt.annotate("Must-be", (3,1))
    plt.annotate("Attractive", (1,3))
    plt.annotate("Indifferent", (1,1))

    # plots
    plt.scatter(plots_x, plots_y)

    # plot labels
    for i in features:
        name = features[i]["name"]
        plt.annotate(i, (plots_x[i-1], plots_y[i-1]))

    plt.show()



with open(file) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';')
    line_count = 0

    init_score_results()

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

    # TODO : sort features

    # TODO draw plots
    draw_chart()

    # Thanks, bye
    print('{:d} lines processed.'.format(line_count-1))
