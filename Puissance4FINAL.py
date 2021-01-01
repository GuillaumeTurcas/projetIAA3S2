#############################################################################
#                                                                           #
#                               Puissance 4                                 #
#                                                                           #
#############################################################################	

import random as rd
import numpy as np
import math

def CreationMatrice(): #Créer une matrice vide de 12 par 7
	Mat = []
	for i in range(12):
		matprov = []
		for j in range(6):
			matprov.append(0)
		Mat.append(matprov)
	return Mat

def AfficherMatrice(mat): #Afficher le jeux du puissance 4 en fonction de ce qui a déjà été joué
	print('\n')
	for j in range(6):
		for i in range(12):
			print('|', end = '')
			if(mat[i][j] == 0):
				print(' ', end = '')
			else:
				if(mat[i][j] == 1):
					print('X', end = '') #afficher X pour le joueur 1
				else:
					print('O', end = '') #afficher O pour le joueur 2
		print('|')
	for i in range(12):
		print('|-', end = '')
	print('|')
	for i in range(1,13):
		print('|', end = '')
		print(i%10, end = '')
	print('|')

def Jouable(col, mat): 
	if(mat[col][0] == 0):
		return 1
	else:
		return 0

def Jeux(mat, col): #Renvoie la coordonnée de la ligne où il faut jouer en fonction de la colonne
	i = 5
	while(mat[col][i] != 0 and i >= 0):
		i -= 1
	if(0 <= i and i < 12): #verifie la valeur la moins haute qui n'ait pas déjà été joué
		return i
	else:
		return niveau1(mat) #n'est jamais renvoyé

def AGagne(mat): #verifie toutes les combinaisons possibles pour savoir si un joueur a gagné, peut importe s'il est le 1 ou le 2
	for i in range(12):
		for j in range(6):
			if(i-3>= 0):
				if(pow(mat[i][j]+mat[i-1][j]+mat[i-2][j]+mat[i-3][j],2) == 16):
					return True
				elif(j-3 >= 0):
					if(pow(mat[i][j]+mat[i-1][j-1]+mat[i-2][j-2]+mat[i-3][j-3],2) == 16):
						return True
				elif(j+3<6):
					if(pow(mat[i][j]+mat[i-1][j+1]+mat[i-2][j+2]+mat[i-3][j+3],2) == 16):
						return True				
			if(i+3 < 12):
				if(pow(mat[i][j]+mat[i+1][j]+mat[i+2][j]+mat[i+3][j],2) == 16):
					return True
				elif(j-3 >= 0):
					if(pow(mat[i][j]+mat[i+1][j-1]+mat[i+2][j-2]+mat[i+3][j-3],2) == 16):
						return True
				elif(j+3<6):
					if(pow(mat[i][j]+mat[i-1][j+1]+mat[i-2][j+2]+mat[i-3][j+3],2) == 16):
						return True				
			if(j-3 >= 0):
				if(pow(mat[i][j]+mat[i][j-1]+mat[i][j-2]+mat[i][j-3],2) == 16):
					return True
			if(j+3<6):
				if(pow(mat[i][j]+mat[i][j+1]+mat[i][j+2]+mat[i][j+3],2) == 16):
					return True
	return False

def EstNul(mat): #verifie si la grille est remplie, et donc s'il y a match nul
	for i in range(12):
		if(Jouable(i, mat) == 1):
			return False
	return True

#############################################################################
#                                                                           #
#                               Joueur 1V1                                  #
#                                                                           #
#############################################################################	

def TourJVJ(mat): #sert pour le jeux en joueur contre joueur, ne sert jamais dans l'IA
	Fin = False
	Joueur = 1
	while(Fin == False):
		print('\nC\'est au tour du jouer', Joueur, ' de jouer !')
		print('\nChoisissez la colonne où vous voulez mettre votre pion ', end ='')
		col = int(input())
		if(col < 0 or col > 11 or Jouable(col, mat) == 0):
			while(col < 0 or col > 11 or type(col) != int or Jouable(col, mat) == 0):
				print('Vous ne pouvez pas choisir cette colonne, choisissez une colonne valide !')
				col = int(input())
		('Vous avez joué la colonne', col, '\n')
		mat[col][Jeux(mat, col)] = pow(-1, Joueur+1)
		AfficherMatrice(mat)
		if(AGagne(mat)):
			print('Le joueur', Joueur, 'a gagné ! \nVoulez-vous rejouer ? (y/n)')
			rejouer = str(input())
			Fin = True
		elif(EstNul(mat)):
			print('Match nul, voulez vous rejouer ? (y/n)', end = '')
			rejouer = str(input())
			Fin = True
		if(Joueur == 1):
			Joueur = 2
		else :
			Joueur = 1
	return rejouer

#############################################################################
#                                                                           #
#                                   [IA]                                    #
#                                                                           #
#############################################################################	
 
def TourJVIA(mat, Joueur, niveau): #Joueur contre IA, la même chose que Joueur contre joueur, mais en appelant la fonction IA lorsque c'est à son tour
	Fin = False 
	J = 1
	while(Fin == False):
		if(Joueur == J):
			col = JeuxJ(mat, Joueur)
		else:
			col = int(JeuxIA(mat, niveau, J))
			print('\n\nL\'IA joue la colonne', col+1)
		mat[col][Jeux(mat, col)] = pow(-1, J + 1)
		AfficherMatrice(mat)
		if(AGagne(mat)):
			print('\nLe joueur', J, 'a gagné ! \nVoulez-vous rejouer ? (y/n) ', end = '')
			rejouer = str(input())
			Fin = True
		elif(EstNul(mat)):
			print('\nMatch nul, voulez vous rejouer ? (y/n) ', end = '')
			rejouer = str(input())
			Fin = True
		if(J == 1):
			J = 2
		else :
			J = 1
	return rejouer

def JeuxJ(mat, Joueur): #renvoie ce que le joueur veut jouer lorsque c'est son tour
	print('\nC\'est au tour du joueur', Joueur, ' de jouer !')
	print('\nChoisissez la colonne où vous voulez mettre votre pion ', end ='')
	col = int(input())-1
	if(col < 0 or col > 11 or Jouable(col, mat) == 0):
		while(col < 0 or col > 11 or type(col) != int or Jouable(col, mat) == 0):
			print('Vous ne pouvez pas choisir cette colonne, choisissez une colonne valide !')
			col = int(input())
	print('Vous avez joué la colonne', col, '\n')
	return col	


def JeuxIA(mat, niv, J): #renvoie ce que l'IA veut joueur, en fonction de son niveau
	print('\nC\'est au tour de l\'IA de jouer')
	if niv == 1:
		return niveau1(mat)
	if niv == 2:
		return niveau2(mat, J)
	if niv >= 3:
		return niveau3(list_minmax(mat,niv,niv,[]))
	return -1

def niveau1(mat): #renvoie une valeure aléatoire possible
	col = rd.randint(0,11)
	while(Jouable(col, mat) == 0):
		col = rd.randint(0,11)
	return col
 
def niveau2(mat, J): #Se défend s'il est en train de perdre, attaque s'il peut gagner, sinon joue au hasard
	col = -1
	for j in range(12):
		if Jouable(j, mat) == 1:
			i = Jeux(mat, j)
			mat[j][i] = pow(-1, J + 1)
			if AGagne(mat):
				col = j
			mat[j][i] = 0
	if col == -1:
		for j in range(12):
			if Jouable(j, mat) == 1:
				i = Jeux(mat, j)
				mat[j][i] = pow(-1, J)
				if AGagne(mat):
					col = j
				mat[j][i] = 0
		if col == -1:
			return niveau1(mat)
		else:
			return col
	else:
		return col


def niveau3(liste): #Appel au MinMax
	if type(liste[0]) != list:
		return liste.index(vrai_max(liste)) 
	else:
		for i in range(len(liste)):
			liste[i] = min_spec(liste[i])
		return liste.index(vrai_max(liste))



#############################################################################
#                                                                           #
#                                  MinMax                                   #
#                                                                           #
#############################################################################


def heuristique2(state): #ça traverse partiellement la matrice (en passant quand meme par toutes les cases) et ça compte toutes les combinaisons possibles
						 #+-1000 s'il y a possibilité de gagner ou perdre
	somme = 0
	for i in range(12):  #verifie les colonnes
		for j in range(3):  
			zone =[state[i][j], state[i][j+1], state[i][j+2], state[i][j+3]]
			if not(1 in zone) :
				if zone.count(-1) == 4:
					somme += (1000)
				else :
					somme += zone.count(-1)
			if not (-1 in zone) :
				if zone.count(1) == 4:
					somme -= (1000)
				else :
					somme -= zone.count(1)
	for i in range(9): #verifie les lignes
		for j in range(6):
			zone = [state[i][j], state[i+1][j], state[i+2][j], state[i+3][j]]
			if not(1 in zone) :
				if zone.count(-1) == 4:
					somme += (1000)
				else :
					somme += zone.count(-1)
			if not (-1 in zone) :
				if zone.count(1) == 4:
					somme -= (1000)
				else :
					somme -= zone.count(1)
	for i in range(9): #verfie les diagonales
		for j in range(3):
			zone = [state[i][j+3], state[i+1][j+2], state[i+2][j+1], state[i+3][j]]
			if not(1 in zone) :
				if zone.count(-1) == 4:
					somme += (1000)
				else :
					somme += zone.count(-1)
			if not (-1 in zone) :
				if zone.count(1) == 4:
					somme -= (1000)
				else :
						somme -= zone.count(1)
	for i in range(9): #verifie les diagonales de l'autre sens
		for j in range(3):
			zone = [state[i+3][j+3], state[i+2][j+2], state[i+1][j+1], state[i][j]]
			if not(1 in zone) :
				if zone.count(-1) == 4:
					somme += (1000)
				else :
					somme += zone.count(-1)
			if not (-1 in zone) :
				if zone.count(1) == 4:
					somme -= (1000)
				else :
					somme -= zone.count(1)
	return somme

def Result(state, a, J): #renvoie une nouvelle matrice provisoire avec la colonne jouée provisoirement dans 
	newState = [[],[],[],[],[],[],[],[],[],[],[],[]]
	for i in range(12):
		newState[i] = state[i][:]
	newState[a][Jeux(newState, a)] = pow(-1, J + 1)
	return newState

def Actions(state): #renvoie toutes les colonnes où ont peut joueur (si une colonne est rempli, ne la rajoute pas dans la liste)
	actions = []
	for a in range(12):
		if Jouable(a, state)==1:
			actions.append(a)
	return actions

#Algorithme Min Max
#Crée une liste des différentes valeurs, et choisis le maximum

def list_minmax(M,profondeur,profondeur_initiale,liste): 
	if profondeur == 1:
		for col in Actions(M):
			if Jouable(col, M)==1:
				liste.append(heuristique2(M))
			else:
				liste.append(np.nan)
	else:
		liste_ce_niveau = list(liste)
		for col in Actions(M):
			if Jouable(col, M)==1:
				liste.append(list_minmax(Result(M,col,(profondeur_initiale - profondeur + 1)%2 +1),profondeur-1,profondeur_initiale,list(liste_ce_niveau)))
			else:
				liste.append(list_nan(Result(M,col,(profondeur_initiale - profondeur + 1)%2 +1),profondeur-1,profondeur_initiale,list(liste_ce_niveau)))
	return liste

def list_nan(M,profondeur,profondeur_initiale,liste):#renvoie une liste vide de taille fixe (en fonction du nombre de coup possible dans ce niveau)
	if profondeur == 1:
		for col in range(12):
			liste.append(np.nan)
	else:
		liste_ce_niveau = list(liste) 
		for col in range(12):
			liste.append(list_nan(M,profondeur-1,profondeur_initiale,list(liste_ce_niveau))) #fonction recursive
	return liste




def max_spec(liste):
	#partie max recursive de l'algorithme min max
	if type(liste[0]) != list:
		return vrai_max(liste)
	else:
		for i in range(len(liste)):
			liste[i] = min_spec(liste[i])
	return max_spec(liste)


def min_spec(liste): 
	#partie min recursive de l'algorithme
	if type(liste[0]) != list:
		return vrai_min(liste)
	else:
		for i in range(len(liste)):
			liste[i] = max_spec(liste[i])
			return min_spec(liste)

def vrai_max(liste):
	#retourne le maximum d'une liste avec des nan
	if liste == 12 * [np.nan]:
		return np.nan
	n = len(liste)
	maximum = -math.inf
	for i in range(n):
		element = liste[i]
		if type(element) == int and element>maximum:
			maximum = element
	return maximum

def vrai_min(liste):
	#retourne le minimum d'une liste avec des nan'''
	if liste == 12 * [np.nan]:
		return np.nan 
	n = len(liste)
	minimum = math.inf
	for i in range(n):
		element = liste[i]
		if type(element) == int and element<minimum:
			minimum = element
	return minimum      



#############################################################################
#                                                                           #
#                                  [MAIN]                                   #
#                                                                           #
#############################################################################

rejouer = 'y'
while(rejouer == 'y' or rejouer == 'Y'):
	print('\n\n------------------------------------------------------')
	print('|                                                    |')
	print('|                     Puissance 4                    |')
	print('|                                                    |')
	print('|                        par                         |')
	print('|                                                    |')
	print('|                    Hugo Schultz                    |')
	print('|                    Loïs Sorinas                    |')
	print('|                  Jules Thuillier                   |')
	print('|                et Guillaume Turcas                 |')
	print('|                                                    |')
	print('------------------------------------------------------\n')

	mat = CreationMatrice()
	AfficherMatrice(mat)

	choix = 2

	#ma1 = MHeuristique();
	#print('\n',np.transpose(ma1))

	while(choix != 0 and choix != 1):
		print('\nVoulez-vous jouer à deux (0) ou contre l IA (1) ? ', end ='')
		choix = int(input())
		
	if(choix == 1):
		Joueur = 0
		niveau = 0
		while(Joueur != 1 and Joueur != 2):
			print('\nVoulez-vous être le joueur 1 (1) ou le joueur 2 (2) ? ', end = '')
			Joueur = int(input())
		while(niveau != 1 and niveau != 2 and niveau != 3 and niveau !=4 and niveau !=5):
			print('\nChoisisez un niveau de difficulté entre 1 et 4 ? ', end = '')
			niveau = int(input())
		if Joueur == 1:
			col = JeuxJ(mat, Joueur)
			mat[col][Jeux(mat, col)] = -1
			AfficherMatrice(mat)
		rejouer = TourJVIA(mat, 2, niveau)
	if(choix == 0):
		print('\nMatch 1 Vs 1\n')
		rejouer = TourJVJ(mat)
