"""
Génération du PDF de correction du Contrôle final de Génétique SVI-S4
(Année 2017-2018, Université Sidi Mohamed Ben Abdellah - FSDM Fès).
"""

from pdf_writer import PDF


def build():
    pdf = PDF()
    pdf.set_title("Correction Controle final Genetique SVI-S4 2017-2018")

    # ===== EN-TETE =====
    pdf.heading("Correction du Contrôle final de Génétique SVI - S4", level=1)
    pdf.paragraph(
        "Université Sidi Mohamed Ben Abdellah - Faculté des Sciences Dhar El Mahraz - "
        "Département de Biologie. Année 2017-2018. Durée 1 H 30 min.",
        size=10, font="F1"
    )
    pdf.space(8)

    # =========================================================================
    # EXERCICE I
    # =========================================================================
    pdf.heading("Exercice I", level=2)
    pdf.paragraph(
        "Données : 3 couples d'allèles d'un organisme diploïde. Les couples a/a+ et c/c+ "
        "sont liés au sexe et distants de 30 cMg. Le couple b/b+ est autosomal."
    )
    pdf.space(4)

    # ----- Q1 -----
    pdf.heading("1) Croisements pour prouver la liaison au sexe et l'autosomie", level=3)
    pdf.paragraph(
        "Principe : on réalise des croisements réciproques. Si les résultats du croisement "
        "direct et du croisement réciproque sont différents (notamment selon le sexe de la "
        "descendance), le gène est lié au sexe. S'ils sont identiques, le gène est autosomal."
    )
    pdf.space(4)

    pdf.paragraph("a) Test du couple a/a+ (idem pour c/c+) :", font="F2")
    pdf.bullet("Croisement direct  : femelle a/a (récessive)  ×  mâle a+/Y (sauvage).")
    pdf.code(
        "    P :  ♀ a/a   ×   ♂ a+/Y\n"
        "  F1 :  ♀ a+/a  ->  [a+]\n"
        "        ♂ a/Y   ->  [a]"
    )
    pdf.bullet("Croisement réciproque : femelle a+/a+ (sauvage)  ×  mâle a/Y.")
    pdf.code(
        "    P :  ♀ a+/a+ ×   ♂ a/Y\n"
        "  F1 :  ♀ a+/a  ->  [a+]\n"
        "        ♂ a+/Y  ->  [a+]"
    )
    pdf.paragraph(
        "Conclusion : les résultats des deux croisements diffèrent (les mâles F1 changent de "
        "phénotype selon le sens du croisement) ==> a/a+ (et de même c/c+) est lié au sexe.",
        font="F2"
    )
    pdf.space(4)

    pdf.paragraph("b) Test du couple b/b+ :", font="F2")
    pdf.bullet("Croisement direct  : ♀ b/b  ×  ♂ b+/b+.")
    pdf.code(
        "    P :  ♀ b/b   ×   ♂ b+/b+\n"
        "  F1 :  ♀ et ♂  b+/b  ->  [b+]"
    )
    pdf.bullet("Croisement réciproque : ♀ b+/b+  ×  ♂ b/b.")
    pdf.code(
        "    P :  ♀ b+/b+ ×   ♂ b/b\n"
        "  F1 :  ♀ et ♂  b+/b  ->  [b+]"
    )
    pdf.paragraph(
        "Conclusion : les deux croisements donnent le même résultat dans les deux sexes "
        "==> b/b+ est autosomal.",
        font="F2"
    )
    pdf.space(6)

    # ----- Q2 -----
    pdf.heading("2) Descendance F1 × F1 issue de ♂ [AC] × ♀ [ac]", level=3)
    pdf.paragraph(
        "a et c sont portés par le chromosome X et distants de 30 cMg "
        "(taux de recombinaison r = 30 %)."
    )
    pdf.paragraph("Génotypes parentaux :")
    pdf.code(
        "  P :  ♂ [AC] = a+ c+ / Y         ×    ♀ [ac] = a c / a c"
    )
    pdf.paragraph("Obtention de F1 :")
    pdf.code(
        "  ♀ F1 :  a+ c+ / a c   ->  [AC]   (toutes les femelles)\n"
        "  ♂ F1 :  a c   / Y     ->  [ac]   (tous les mâles)"
    )
    pdf.space(4)
    pdf.paragraph("Croisement F1 × F1 :  ♀ a+c+/ac  ×  ♂ ac/Y.", font="F2")
    pdf.paragraph(
        "La femelle F1 est dihybride pour deux gènes liés à 30 cM ; elle produit 4 types "
        "de gamètes :"
    )
    pdf.code(
        "  Parentaux  (1-r)/2  =  35 %  :  a+ c+    et   a c\n"
        "  Recombines    r/2   =  15 %  :  a+ c     et   a c+"
    )
    pdf.paragraph(
        "Le mâle F1 (ac/Y) produit deux types de gamètes en proportions égales : "
        "ac (50 %) et Y (50 %)."
    )
    pdf.space(4)

    pdf.paragraph("Descendance FEMELLE (X paternel = a c) :", font="F2")
    pdf.code(
        "  Gamete mere   %     Genotype          Phenotype\n"
        "  ----------------------------------------------------\n"
        "    a+ c+      35%    a+c+ / ac           [AC]\n"
        "    a  c       35%    ac   / ac           [ac]\n"
        "    a+ c       15%    a+c  / ac           [Ac]\n"
        "    a  c+      15%    ac+  / ac           [aC]"
    )
    pdf.space(2)
    pdf.paragraph("Descendance MÂLE (Y paternel, hémizygote) :", font="F2")
    pdf.code(
        "  Gamete mere   %     Genotype          Phenotype\n"
        "  ----------------------------------------------------\n"
        "    a+ c+      35%    a+c+ / Y            [AC]\n"
        "    a  c       35%    ac   / Y            [ac]\n"
        "    a+ c       15%    a+c  / Y            [Ac]\n"
        "    a  c+      15%    ac+  / Y            [aC]"
    )
    pdf.space(4)
    pdf.paragraph(
        "Remarque : les deux sexes présentent ici la même répartition phénotypique, parce "
        "que la femelle F1 est l'unique « informative » (le père F1 ne donne qu'un seul type "
        "de gamète X = ac). Les mâles F1 révèlent donc directement les gamètes maternels."
    )

    # =========================================================================
    # EXERCICE II
    # =========================================================================
    pdf.space(10)
    pdf.heading("Exercice II", level=2)
    pdf.paragraph(
        "Quatre souches haploïdes de levure (arg1, arg2, arg3, arg4), incapables de "
        "synthétiser l'arginine. Elles complémentent toutes deux à deux : chacune est "
        "donc mutée dans un gène différent."
    )
    pdf.space(2)
    pdf.paragraph("Récapitulatif des résultats expérimentaux :")
    pdf.code(
        "  Croisement       Resultats sur les spores en vrac\n"
        "  arg1 x arg2      85 % arg-   et   15 % arg+\n"
        "  arg1 x arg4      75 % arg-   et   25 % arg+\n"
        "  arg3 x arg4      90 % arg-   et   10 % arg+\n"
        "  arg2 x arg4      20 asques 2:2 (arg+ : arg-)\n"
        "                   30 asques 1:3 (1 arg+, 3 arg-)\n"
        "                   50 asques 0:4 (4 arg-)\n"
        "  arg2 x sauvage   35 % de post-reduction\n"
        "  arg4 x sauvage   35 % de post-reduction\n"
        "  arg2 x arg3      50 % de recombinaison (donne)"
    )
    pdf.space(6)

    # ----- Q1 -----
    pdf.heading("1) Composition en spores : souche × sauvage", level=3)
    pdf.paragraph(
        "Chaque souche n'est mutée que dans un seul gène. Le croisement avec la souche "
        "sauvage met en jeu un seul couple d'allèles arg-/arg+ qui se sépare en "
        "ségrégation 2:2 (méiose normale)."
    )
    pdf.paragraph("Donc, pour chaque souche (arg1, arg2, arg3, arg4) × sauvage :", font="F2")
    pdf.code(
        "  Chaque asque contient :  2 spores arg+   et   2 spores arg-\n"
        "  En vrac (toutes spores melangees) :  50 % arg+  et  50 % arg-"
    )
    pdf.space(6)

    # ----- Q2 -----
    pdf.heading("2) Composition en spores en vrac : arg2 × arg4", level=3)
    pdf.paragraph("Calcul à partir des 100 asques observés (= 400 spores) :")
    pdf.code(
        "  20 asques 2 arg+ : 2 arg-   ->  20 x 2 =  40 arg+   et  40 arg-\n"
        "  30 asques 1 arg+ : 3 arg-   ->  30 x 1 =  30 arg+   et  90 arg-\n"
        "  50 asques 0 arg+ : 4 arg-   ->            0 arg+   et 200 arg-\n"
        "  --------------------------------------------------------------\n"
        "  Totaux                              :    70 arg+   et 330 arg-"
    )
    pdf.boxed(
        "==> En vrac : 70/400 = 17,5 % de spores arg+   et   330/400 = 82,5 % de spores arg-."
    )
    pdf.space(6)

    # ----- Q3 -----
    pdf.heading("3) Établissement de la carte factorielle", level=3)
    pdf.paragraph("a) Calcul des distances entre gènes (à partir des % arg+ en vrac) :", font="F2")
    pdf.paragraph(
        "Pour deux gènes liés (en levure haploïde), les spores recombinantes représentent "
        "2 fois la fréquence des spores arg+ (les recombinants donnent moitié arg+, moitié "
        "double-mutants arg-). On en déduit :"
    )
    pdf.code(
        "  D(arg1 ; arg2)  = 2 x 15 % = 30 cM            (lies)\n"
        "  D(arg1 ; arg4)  = 2 x 25 % = 50 % (sature)    (non lies en pratique)\n"
        "  D(arg3 ; arg4)  = 2 x 10 % = 20 cM            (lies)\n"
        "  D(arg2 ; arg4)  = 2 x 17,5 % = 35 cM          (lies)\n"
        "  D(arg2 ; arg3)  = 50 % (donne)               (non lies en pratique)"
    )
    pdf.space(2)
    pdf.paragraph("b) Identification des asques pour arg2 × arg4 :", font="F2")
    pdf.paragraph(
        "Parents : arg2- arg4+   x   arg2+ arg4-. Les asques se classent ainsi :"
    )
    pdf.code(
        "  Asque                           Spores                Type   Nb\n"
        "  -------------------------------------------------------------------\n"
        "  4 arg- (0 arg+)                 2 (arg2- arg4+)\n"
        "                                  2 (arg2+ arg4-)        DP    50\n"
        "  2 arg+ : 2 arg-                 2 (arg2+ arg4+)\n"
        "                                  2 (arg2- arg4-)        DR    20\n"
        "  1 arg+ : 3 arg-                 1 de chacun des 4      T     30"
    )
    pdf.paragraph(
        "DP = 50 > DR = 20  ==>  arg2 et arg4 sont bien liés (sur le même chromosome)."
    )
    pdf.space(2)
    pdf.paragraph("c) Distance gène-centromère (test de post-réduction) :", font="F2")
    pdf.paragraph(
        "La fraction de post-réduction (PR) est liée à la distance gène-centromère par "
        "D = (% PR) / 2."
    )
    pdf.code(
        "  D(arg2 ; centromere) = 35 / 2 = 17,5 cM\n"
        "  D(arg4 ; centromere) = 35 / 2 = 17,5 cM"
    )
    pdf.space(2)
    pdf.paragraph("d) Justification de l'ordre des gènes :", font="F2")
    pdf.bullet(
        "D(arg2;C) + D(arg4;C) = 17,5 + 17,5 = 35 = D(arg2;arg4)  ==>  arg2 et arg4 sont "
        "de part et d'autre du centromère."
    )
    pdf.bullet(
        "D(arg1;arg2) + D(arg2;arg4) = 30 + 35 = 65 cM théoriques, alors que la mesure "
        "donne 50 % (saturé) : cohérent, car arg1 est encore plus loin de arg4 que arg2 "
        "==> arg1 est à l'opposé de arg4 par rapport à arg2."
    )
    pdf.bullet(
        "D(arg3;arg4) = 20 cM ; D(arg2;arg3) = 50 % (saturé). Si arg3 prolongeait arg4 du "
        "même côté : D(arg2;arg3) = 35 + 20 = 55 cM théoriques (saturé à 50 %), ce qui "
        "concorde ==> arg3 est dans le prolongement de arg4."
    )
    pdf.space(2)
    pdf.paragraph("e) Carte factorielle (un seul groupe de liaison) :", font="F2")
    pdf.code(
        "  arg1 ----30 cM---- arg2 --17,5-- (C) --17,5-- arg4 ----20 cM---- arg3\n"
        "                                    o\n"
        "  D(arg1 ; C) = 30 + 17,5 = 47,5 cM\n"
        "  D(arg3 ; C) = 17,5 + 20 = 37,5 cM"
    )
    pdf.space(6)

    # ----- Q4 -----
    pdf.heading("4) Proportions DP, DR, T pour arg1 × arg3", level=3)
    pdf.paragraph(
        "D'après la carte précédente, arg1 et arg3 sont aux extrémités du chromosome :"
    )
    pdf.code(
        "  D(arg1 ; arg3) = 30 + 17,5 + 17,5 + 20 = 85 cM (theorique)\n"
        "                  -> sature a 50 % en spores en vrac"
    )
    pdf.paragraph(
        "Les deux gènes se comportent comme NON liés ==> on attend DP = DR (signature de "
        "l'indépendance en analyse de tétrades)."
    )
    pdf.paragraph(
        "Comme les deux gènes sont éloignés du centromère (PR(arg1) = 95 %, PR(arg3) = 75 %, "
        "saturés à ~ 67 %), les tétratypes T sont majoritaires : on tend vers le cas limite "
        "DP = DR = 1/6 et T = 2/3."
    )
    pdf.boxed(
        "Resultat attendu :  DP = DR ≈ 16,7 %   et   T ≈ 66,7 %."
    )
    pdf.paragraph(
        "Vérification du % d'arg+ : (DR×4 + T×2)/(4×Total) = (66,7 + 33,3)/4 ≈ 25 %, "
        "soit 50 % de spores recombinées, conforme à des gènes non liés."
    )
    pdf.space(6)

    # ----- Q5 -----
    pdf.heading("5) Phénotype du zygote arg- (DR de arg2 × arg3) × arg3", level=3)
    pdf.paragraph(
        "Croisement de départ arg2 × arg3 : parents arg2- arg3+   et   arg2+ arg3-."
    )
    pdf.paragraph("Composition d'un asque DR :", font="F2")
    pdf.code(
        "  2 spores arg2+ arg3+   ->  arg+\n"
        "  2 spores arg2- arg3-   ->  arg-     (double mutant)"
    )
    pdf.paragraph(
        "Donc la spore arg- d'un asque DR a forcément le génotype  arg2- arg3-."
    )
    pdf.paragraph("Croisement avec la souche arg3 (= arg2+ arg3-) :", font="F2")
    pdf.code(
        "        arg2- arg3-     x     arg2+ arg3-\n"
        "                |\n"
        "                v\n"
        "  Diploide :   arg2- arg3-  /  arg2+ arg3-\n"
        "    locus arg2 :  arg2- / arg2+   ->  arg2+   (sauvage)\n"
        "    locus arg3 :  arg3- / arg3-   ->  arg3-   (homozygote mute)"
    )
    pdf.boxed(
        "==> Phénotype du zygote : arg-   (incapable de synthétiser l'arginine, "
        "car le gène arg3 est non fonctionnel à l'état homozygote)."
    )

    return pdf


if __name__ == "__main__":
    import os
    pdf = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "correction_genetique_SVI_S4_2017_2018.pdf")
    pdf.save(out)
    print(f"PDF written: {out} ({os.path.getsize(out)} bytes)")
