"""
Count names with more than seven letters
"""

LETTER_COUNT_THRESHOLD = 7


def count_names_with_more_than_threshold_letters(prenoms: list[str]) -> int:
    names_above_threshold = 0
    for prenom in prenoms:
        if len(prenom) > LETTER_COUNT_THRESHOLD:
            names_above_threshold += 1
            print(prenom + " est un prénom avec un nombre de lettres supérieur à 7")
        else:
            print(prenom + " est un prénom avec un nombre de lettres inférieur ou égal à 7")
    return names_above_threshold


prenoms = ["Guillaume", "Gilles", "Juliette", "Antoine", "François", "Cassandre"]
print("Nombre de prénoms dont le nombre de lettres est supérieur à 7 : " + str(count_names_with_more_than_threshold_letters(prenoms=prenoms)))
