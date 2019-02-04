# blend_mol
Ensemble de scripts python permettant de dessiner des molécules et de les animer
# Scénario hydrogénation
T0 : H2 + catalyseur
T1 : H2 se sépare et se fixe sur le catalyseur
T3 : Molécule (dessiner, rigué et orienté correctement : 3 étapes faites en 3 scripts différents)
T4 : Molécule se rapproche du catalyseur et s'hydrogène
T5 : Molécule s'éloigne du catalyseur

# Mol_draw 
Dessine n'importe quelle molécule à partir d'un fichier .mol2 

#################################################################################################

2 chemins différents à partir de la même molécule cis.
	1) Hydrogénation :

		La molécule de base soit elle est : cis ou trans (peu importe)
		Il y a un support métalique (boules les unes à côté des autres non liées)
		Le métal va aider à couper la molécule d'hydrogène pour la mettre sur la double liaison de la partie cis
		a) Activation : molécule di-hydrogène s'approche du métal, se coupe et se fixe (en faire que sur 1)
		b) La molécule cis arrive sur les deux hydrogènes : la double liaison disparaît et l'hydrogène se met sur chaque carbonne ce qui donne la molécule hydrogéno. 
		c) la molécule se détache et part

	2) Passage cis - trans :
		
		Description : on ne sait pas vraiment comment sa se passe au niveau du métal. 
		a) la molécule cis arrive sur le métal
		b) la double liaison disparait
		c) un carbonne de cette double liaison se fixe sur le métal 
		d) la partie non fixée rote pour se mettre en position trans
		e) la liaison carbonne-métal se détache et une double liaison carbonne-carbonne se crée
		f) On obtient ainsi la molécule trans (qui s'éloigne du métal)
