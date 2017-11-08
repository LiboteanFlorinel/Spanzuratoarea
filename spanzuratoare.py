# Joc Spanzuratoarea

id_student = "Libotean Florinel"
input_file = open("cuvinte_de_verificat.txt", "r", encoding="utf-8")
output_file = open("date_iesire_timestamp.txt", "w", encoding="utf-8")
litere = "aăâiîertțnucosșldpmfvbghjxzkqwy"  #toate literele din lb romana si nu numai


# functie ce verifica daca un cuvant se potriveste unui sablon
def match_pattern(cuvant1, cuvant2):
    if len(cuvant1) != len(cuvant2):
        return False
    for i in range(0, len(cuvant1)):
        if cuvant1[i] != "*":
            if cuvant1[i] != cuvant2[i]:
                return False
    return True


# functie ce returneaza toate cuvintele care se potrivesc unui sablon
def find_all_pattern_matches(cuvant1):
    cuvinte_gasite = []
    # in acest fisier vom putea adauga cuvinte noi
    dictionar = open("ceva.txt", "r", encoding="utf-8")
    cuvinte = dictionar.readlines()
    i = 0
    for cuvant in cuvinte:
        cuvant = cuvant.strip("\n")
        i += 1
        if match_pattern(cuvant1, cuvant):
            cuvinte_gasite.append(cuvant)
    dictionar.close()
    return cuvinte_gasite


def unde_se_potriveste_litera(id_student, id_joc, litera, cuvant):
    pozitii = []
    for i in range(0, len(cuvant)):
        if cuvant[i] == litera:
            pozitii.append(i)
    return pozitii


def verifica_cuvantul(id_student, id_joc, cuvant1, cuvant2):
    if cuvant1 == cuvant2:
        return 1
    return 0


# functie ce returneaza de cate ori apare o litera intr-un cuvant
def nr_litere(litera, cuvant):
    x = 0
    for i in range(0, len(cuvant)):
        if cuvant[i] == litera:
            x += 1
    return x

# functie de rezolvare a problemei in cazul in care cuvantul cautat se afla in dictionar
# metoda pe scurt:
# programul gaseste toate cuvintele de lungimea cautat si care au literele din cuvant1 pe pozitile acestuia
# daca exista in dictionar un singur cuvant care respecta sablonul se va returna direct solutia
# astfel va fi nevoie de 0 incercari pt determinarea ei
# in caz contrar se determina numarul de aparitii ale fiecarei litere din cuvintele care corespund sablonului
# in functie de nr de aparitii ale unei litere(descrescator) se incearca potrivirea ei in cuvant2
def rezolvare(id_student, id_joc, cuvant1, cuvant2):
    cuvinte = find_all_pattern_matches(cuvant1)
    if len(cuvinte) == 1:
        return 0
    litere_care_apar = ""
    nr_aparitii = []
    incercari = 0
    for cuvant in cuvinte:
        for i in range(0, len(cuvant)):
            k = 0
            for j in range(0, len(litere_care_apar)):
                if cuvant[i] == litere_care_apar[j]:
                    k = 1
                    nr_aparitii[j] += 1
            if k == 0:
                litere_care_apar = litere_care_apar + cuvant[i]
                nr_aparitii.append(1)
    for i in range(0, len(nr_aparitii) - 1):
        for j in range(i + 1, len(nr_aparitii)):
            if nr_aparitii[i] < nr_aparitii[j]:
                char1 = litere_care_apar[i]
                char2 = litere_care_apar[j]
                nr_aparitii[i], nr_aparitii[j] = nr_aparitii[j], nr_aparitii[i]
                litere_care_apar = litere_care_apar[:i] + char2 + litere_care_apar[i + 1:]
                litere_care_apar = litere_care_apar[:j] + char1 + litere_care_apar[j + 1:]
    for i in range(0, len(litere_care_apar)):
        pozitii = unde_se_potriveste_litera(id_student, id_joc, litere_care_apar[i], cuvant2)
        k = 0
        for j in pozitii:
            if cuvant1[j] == "*":
                k = 1
                cuvant1 = cuvant1[:j] + litere_care_apar[i] + cuvant1[j + 1:]
        if k:
            incercari += 1
        if verifica_cuvantul(id_student, id_joc, cuvant1, cuvant2):
            return incercari
    return -1  # in cazul in care aceasta metoda nu functioneaza se returneaza -1


# rezolvarea problemei in cazul in care cuvantul nu se afla in dictionar
# metoda de rezolvare:
# se iau pe rand literele cele mai frecvente din lb romana
# dupa care se incerca gasirea cuvantului litera cu litera
def rezolvare_v2(id_student, id_joc, cuvant1, cuvant2):
    litere_ordonate_dupa_frecventa = "aăâiîertțnucosșldpmfvbghjxzkqwy"
    incercari = 0
    for i in litere_ordonate_dupa_frecventa:
        pozitii = unde_se_potriveste_litera(id_student, id_joc, i, cuvant2)
        k = 0
        for j in pozitii:
            if cuvant1[j] == "*":
                k = 1
                cuvant1 = cuvant1[:j] + i + cuvant1[j + 1:]
        if k:
            incercari += 1
        if verifica_cuvantul(id_student, id_joc, cuvant1, cuvant2):
            # daca cuvantul gasit nu exista in dictionar acesta va fi adaugat
            # astfel la a doua rulare programul va gasi mai repede solutia
            #dictionar = open("ceva.txt", "a+", encoding="utf-8")
            #dictionar.write('\n')
            #dictionar.write(cuvant2)
            #dictionar.close()
            return incercari


def joc(linie):
    linie.replace("\r\t\n", "")
    l = linie.split(";")
    l[2] = l[2].strip("\n")
    l[1] = l[1].lower()
    l[2] = l[2].lower()
    y = int(l[0])
    x = rezolvare(id_student, y, l[1], l[2])
    z = [y, x]
    if x > -1:
        return z
    else:
        x = rezolvare_v2(id_student, y, l[1], l[2])
        z[1] = x
        return z


def main():
    jocuri = []
    total_incercari = 0
    i = -1
    while True:
        x = input_file.readline()
        if x == "":
            break
        jocuri.append(joc(x))
        i += 1
        output_file.write(str(jocuri[i][0]) + ";" + str(jocuri[i][1]) + "\n")
        total_incercari += jocuri[i][1]
    input_file.close()
    print("Numarul total de jocuri: {}\nTotal incercari: {}\n".format(len(jocuri), total_incercari))
    for i in range(0, len(jocuri)):
        print("idJoc: {}; Nr de incercari: {}\n".format(jocuri[i][0], jocuri[i][1]))
    output_file.close()


if __name__ == "__main__":
    main()

