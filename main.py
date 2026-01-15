import json
import os 


solde_dict = {
    "solde" : 50000,
    "liste_transfert" : []

}

fichier_solde = "data_solde.json"
# fichier_transfert = "data_transfert.json"
if not os.path.exists(fichier_solde) :
    with open(fichier_solde,'w+') as file :
        json.dump(solde_dict,file,indent = 4)

# if not os.path.exists(fichier_transfert):
#     with open(fichier_transfert, 'w') as file:
#         json.dump([], file, indent=4)

mot_de_passe = 1234



def mis_a_jour_fichier(fichier,contenu) :
    try :
        with open (fichier,'w') as file :
            json.dump(contenu,file,indent = 4)
    except :
        print("Erreur d'ecriture")

def lire_fichier(fichier):
    global solde_dict
    try :
        with open(fichier,'r') as file :
            contenu = json.load(file)
    except (json.JSONDecodeError):
        # print("Erreur de lecture")
        mis_a_jour_fichier(fichier,solde_dict) 
        with open(fichier,'r') as file :
            contenu = json.load(file)
            # print(contenu)

    return contenu
donnee = lire_fichier(fichier_solde)
liste_transfert = donnee['liste_transfert']

solde = lire_fichier(fichier_solde)


#Menu principal qui permet d'acceder au portail OrangeMoney en tapant #144# ou 0 pour quitter
def menu_principal():
    while True :
        print('*' * 70)
        print("\n"
            "\tBienvenue dans le portail de ORANGE\n"
            "\n")
        print('*' * 70)
        choix = input("Veuillez taper :\n\t #144# pour acceder a OrangeMoney" \
                    "\n\t 0 pour quitter\n")
        
        match choix :
            case "#144#" :
                print("Beinvenue")
                menu_principal_OrangeMoney(mot_de_passe)

            case '0' :
                exit()

            case _ :
                print("Choix invalide") 

def menu_principal_OrangeMoney(mot_de_passe) :
    
    
    print("*******************************************************\n" \
        "\tBienvenue dans le portail OrangeMoney\n"
        "*******************************************************\n")
    
    while True :
        choix = input("veuillez taper : \n1 pour Consulter le solde\n" \
            "2 pour acheter du credit\n" \
            "3 pour acheter un forfait\n"
            "4 pour effectuer un transfert\n" \
            "5 pour annuler le dernier transfert\n"
            "6 pour afficher l'historique des transferts\n"
            "0 pour retourner au menu principal\n" \
            "9 pour arreter le programme")
        
        
        match choix :
            case '1' :
                solde_compte(mot_de_passe)
                redirection()
            case '2' :
                achat_credit(mot_de_passe)
                solde = lire_fichier(fichier_solde)
                print(f"Nouveau solde : {solde['solde']}FCFA")
                redirection()
            case '3' :
                achat_forfait(mot_de_passe)
                solde = lire_fichier(fichier_solde)
                print(f"Nouveau solde : {solde['solde']}FCFA")
                redirection()
            case '4' :
                transert_argent(mot_de_passe)
                solde = lire_fichier(fichier_solde)
                print(f"Nouveau solde : {solde['solde']}FCFA")
                redirection()
            case '5' :
                donnee = lire_fichier(fichier_solde)
                liste_transfert = donnee['liste_transfert']
                
                if len(liste_transfert) > 0 :
                    annuler_transfert(mot_de_passe)
                    donnee = lire_fichier(fichier_solde)
                    liste_transfert = donnee['liste_transfert']
                    print(f"Nouveau solde : {donnee['solde']}FCFA")
                else :
                    print("Pas d'annulation")
                redirection()

            case '6' :
                historique_transfert()

            case '0' :
                menu_principal()
                break
            case '9' :
                exit()
            case _ :
                print("choix invalide!")
                    
        


def redirection ():
    choix = input("0 Accueil\n" \
        "9 Quitter")
    match choix :
        case '0':
            
            menu_principal_OrangeMoney(mot_de_passe)
        case '9':
            exit()
        case _ :
            print("choix invalide!!!")


def verifier_mot_de_passe(mot_de_passe) :
    verif = False
    tentative = 3
    while tentative != 0 :
        mot_passe_saisi = input("veuillez saisir votre code secret : ")
        if mot_passe_saisi.isdigit() and int(mot_passe_saisi) == mot_de_passe :
            verif = True
            break
        else :
            tentative -= 1
            print("Code incorrecte!")
            if tentative > 0 :
                print(f"Il vous reste {tentative} tentative.s")
            else :
                print("Trop de tentatives!!!")
                print('*' * 50)
                exit()
    return verif

def verifier_numero() :
    while True :
        verif = False
        numero = input("Veuillez saisir le numero du destinaire : ")
        if numero.isdigit() and int(numero) > 0 :
            if len(numero) == 9 and numero.startswith('7') :
                verif = True
                return verif,numero
                break
            else :
                print("Le numero doit etre compose de 9 chiffres!")
        else :
            print("Erreur de saisie! Veuillez saisir un nombre")

            return verif
        


def solde_compte(mot_passe) :
    print("******* Solde du compte *******")
    
    if verifier_mot_de_passe(mot_passe) :
        
        solde = lire_fichier(fichier_solde)
        print(f"Le solde de vore compte est de {solde['solde']}FCFA.")


def achat_credit(mot_de_passe) :
    print("******* Achat de credit *******")
    while True :
        montant = input("Veuillez saisir le montant de recharge : ")
        if montant.isdigit() and int(montant) > 0 :
            montant = int(montant)
            if verifier_mot_de_passe(mot_de_passe) :
                solde = lire_fichier(fichier_solde)
                if montant <= solde['solde'] :
                    solde['solde'] -= montant
                    print(f"Recharge credit : {montant}FCFA")
                    mis_a_jour_fichier(fichier_solde,solde)
                    print('*' * 50)
                    break
                else :
                    print("Le solde de votre compte est insuffisant")
                    break
            else :
                exit()
        else :
            print("Le montant doit etre un nombre positif!")


def transert_argent(password):
    transfert = {}
    verif_num,numero = verifier_numero()
    if verif_num:
        while True :
            montant = input("Veuillez saisir le montant de transfert : ")
            if montant.isdigit() and int(montant) > 0 :
                if verifier_mot_de_passe(password) :
                    solde = lire_fichier(fichier_solde)
                    if int(montant) <= solde['solde'] :

                        montant = int(montant)
                        
                        
                        solde['solde'] -= montant
                    
                        mis_a_jour_fichier(fichier_solde,solde)
                        donnee = lire_fichier(fichier_solde)
                        liste = donnee['liste_transfert']
                        
                        transfert['id'] = len(liste) + 1
                        transfert['numero'] = numero
                        transfert['montant'] = montant
                        transfert['etat'] = "Effectue"
                        liste.append(transfert)
                        mis_a_jour_fichier(fichier_solde,donnee)
                        print(f"Transfert de {montant}FCFA effectue avec succes")
                        print('*' * 50)
                        break
                    else :
                        print("Le solde de votre compte est insuffisant")
                        print('*' * 50)

                        break
                else :
                    break
            else :
                print("Le montant doit etre un nombre positif!")


def annuler_transfert(lmot_depasse) :
    donnee = lire_fichier(fichier_solde)
    liste = donnee['liste_transfert']
    if liste[-1]['etat'] == "Annule" :
        print("Le dernier transfert a deja ete annule")
    else :
        choix = input("1 : confirmer\n2 : Annuler")
        match choix :
            case '1' :
                if verifier_mot_de_passe(mot_de_passe) :
                    # solde = lire_fichier(fichier_solde)
                    donnee['solde'] += liste[-1]['montant']
                    print(donnee)
                    # mis_a_jour_fichier(fichier_solde,solde)
                    print(f"Le transfert de {liste[-1]['montant']}FCFA a ete annuler avec succes!")
                    liste[-1]['etat'] = "Annule"
                    mis_a_jour_fichier(fichier_solde,donnee)
                    for transfert in liste :
                        print(f"{transfert['id']} | montant : {transfert['montant']} | destinataire : {transfert['numero']}")
                        
            case '2' :
                print("Retour au menu")


        return solde

def historique_transfert():
    donnee = lire_fichier(fichier_solde)
    liste = donnee['liste_transfert']
    if len(liste) == 0 :
        print("La liste de transfert est vide")
    else:
        for transfert in liste :
            print(f"Numero : {transfert['numero']}")
            print(f"Montant : {transfert['montant']}")
            print(f"Etat : {transfert['etat']}")
            print('*' * 50)
                





def achat_forfait(mot_depasse):
    liste_forfait =[{
        "id" : 1,
        "taille" : "100 Mo",
        "prix" : 500
    },
    {
        "id" : 2,
        "taille" : "500 Mo",
        "prix" : 1000
    },
    {
        "id" : 3,
        "taille" : "1 Go",
         "prix" : 2000
    }]

    print("**********Achat de forfait**********")
    print("Voici la liste des forfaits disponibles :")
    while True :
        indice = 0
        for forfait in liste_forfait :
            indice += 1
            print(f"{forfait['id']} . {forfait['taille']} a {forfait['prix']}FCFA")

        choix = input("Veuillez choisir un forfait")
        if choix.isdigit():
            if int(choix) <= len(liste_forfait):
                choix = int(choix)
                taille = liste_forfait[choix-1]["taille"]
                prix = liste_forfait[choix-1]['prix']
                print(f"Vous allez acheter un forfait de {taille} a {prix}FCFA")
                if verifier_mot_de_passe(mot_depasse) :
                    solde = lire_fichier(fichier_solde)
                    solde['solde'] -= prix
                    mis_a_jour_fichier(fichier_solde,solde)
                    print(f"Votre achat de {prix}FCFA a ete effectuer avec succes!\n")
                    break
                else:
                    exit()
            else :
                print("Veuillez saisir un nombre dans la liste de forfaits")
        else :
            print("Le choix doit etre un nombre!!!")










menu_principal()