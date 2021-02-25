## About The Project

Analyze your user research to find the most attractive functionnalities

[![Kano Chart][kano.png]]

### Built With

* [Python](https://www.python.org/)
* [numpy](https://numpy.org/)
* [matplotlib](https://matplotlib.org/stable/index.html)

## Getting Started

To get a local copy up and running follow these steps.


1. Clone the repo
   ```sh
   git clone https://github.com/astranchet/kano.git
   ```
2. Edit result.csv with your own results

3. Edit kano.py with your own data:
	- file: result file name
	- functionnal_dict and disfunctionnal_dict: label used in your form
	- features: name and columns for each feature

4. Run the script	
   ```sh
   python kano.py
   ```

5. Enjoy the graph and the results
   ```
1 - « Nommer les conférences » : D 1.06   F 2.26   Catégorie Attractive
2 - « Réserver un numéro récurrent » : D 1.47   F 2.69   Catégorie Attractive
3 - « Inviter des personnes » : D 0.61   F 1.78   Catégorie Inutile
4 - « Ajouter à votre agenda » : D 1.03   F 2.01   Catégorie Attractive
5 - « Rendre des personnes silencieuses » : D -0.37   F 2.51   Catégorie Attractive
6 - « Savoir qui est présent » : D -0.46   F 2.95   Catégorie Attractive
7 - « Avoir accès à un tableau de bord pendant la conférence » : D 0.11   F 2.45   Catégorie Attractive
8 - « Recevoir un rapport après la conférence » : D -0.18   F 1.45   Catégorie Inutile
   ```

## License

Distributed under the MIT License. 


<!-- CONTACT -->
## Contact

Anne-Sophie Tranchet - [@annso_](https://twitter.com/annso_)

Project Link: [https://github.com/astranchet/kano](https://github.com/astranchet/kano)
