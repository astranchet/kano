import csv
import numpy as num
import matplotlib.pyplot as plt
import matplotlib.patches as patches

file = 'results.csv'

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
        'present_column_number': 1, 
        'absent_column_number': 2, 
    },
    2: {
        'name' : 'Réserver un numéro récurrent',
        'present_column_number': 3,
        'absent_column_number': 4,
    },
    3: {
        'name' : 'Inviter des personnes',
        'present_column_number': 5, 
        'absent_column_number': 6,
    },
    4: {
        'name' : 'Ajouter à votre agenda',
        'present_column_number': 7, 
        'absent_column_number': 8,
    },
    5: {
        'name' : 'Rendre des personnes silencieuses',
        'present_column_number': 9, 
        'absent_column_number': 10,
    },
    6: {
        'name' : 'Savoir qui est présent',
        'present_column_number': 11, 
        'absent_column_number': 12,
    },
    7: {
        'name' : 'Avoir accès à un tableau de bord pendant la conférence',
        'present_column_number': 13, 
        'absent_column_number': 14,
    },
    8: {
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
        return "Inutile"
    elif d_score >= -1 and d_score < 2 and f_score >= 2:
        return "Attractive"
    elif d_score >= 2 and f_score >= -1 and f_score < 2:
        return "Indispensable"
    elif d_score >= 2 and f_score >= 2:
        return "Performante"
    elif d_score <= 2 or f_score <= 2:
        return "Répulsive"
    return "Q - questionnable "


plots_x = []
plots_y = []
errors_x = []
errors_y = []
plots_colors = []

def compute_avg():
    # Compute average of scores for each feature
    for i in features:
        feature_scores = scores[i]
        name = features[i]["name"]
        f_score = num.mean(feature_scores['functionnal_scores'])
        d_score = num.mean(feature_scores['disfunctionnal_scores'])
        feature_category = category(f_score, d_score)
        print("{} - « {} » : D {:4.2f}   F {:4.2f}   Catégorie {}".format(
            i,
            name,
            d_score, 
            f_score,
            feature_category
        ))
        plots_x.append(d_score)
        errors_x.append(num.var(feature_scores['disfunctionnal_scores']))
        plots_y.append(f_score)
        errors_y.append(num.var(feature_scores['functionnal_scores']))

        plots_colors.append('deeppink')


def draw_chart():
    fig, ax = plt.subplots()

    # titres
    ax.set(xlabel='Sans la feature', ylabel='Avec la feature',
       title='Quelles features sont attendues par les utilisateurs')
    # axes
    ax.plot([-2, 4], [0, 0], color = 'grey', linestyle = 'solid', linewidth=2)
    ax.plot([0, 0], [-2, 4], color = 'grey', linestyle = 'solid', linewidth=2)   
    # cadrant
    ax.plot([-2, 4], [2, 2], color = 'grey', linestyle = 'dashed')
    ax.plot([2, 2], [-2, 4], color = 'grey', linestyle = 'dashed')
    # cadrant labels
    ax.annotate("Performantes", (2.25,3))
    ax.annotate("Indispensables", (2.25,1))
    ax.annotate("Attractives", (0.5,3))
    ax.annotate("Inutiles", (0.5,1))
    ax.annotate("Repoussantes", (-2,-1))
    # zones
    rect = patches.Rectangle((0,0),4,4,linewidth=2,edgecolor='green',facecolor='mintcream', alpha = 0.5, zorder=1)
    ax.add_patch(rect)

    # plots
    ax.scatter(plots_x, plots_y, s=40,c=plots_colors, edgecolors='none', zorder=2)
    # plot labels
    for i in features:
        # ax.errorbar(x=plots_x[i-1], y=plots_y[i-1], xerr=errors_x[i-1], yerr=errors_y[i-1], ecolor='grey')
        ax.annotate(i, xy=(plots_x[i-1], plots_y[i-1]))

    fig.savefig("kano.png")

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

    draw_chart()

    # Thanks, bye
    print('{:d} lines processed.'.format(line_count-1))
