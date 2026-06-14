import sys, os
sys.path.insert(0, os.path.abspath("../generateurs"))
os.environ["KIT_FONTS"] = os.path.abspath("../polices")
import illustrations as ill
from gabarits import charte_a, charte_b, exercice_head, page_decoupe, vignette, img_b64

# Generer les illustrations necessaires
os.makedirs("_tmp", exist_ok=True); os.chdir("_tmp")
ill.save_png("pomme", ill.aliment_pomme(), 120,120)
ill.save_png("poisson", ill.aliment_poisson() if hasattr(ill,'aliment_poisson') else ill.aliment_pomme(), 150,120)
ill.save_png("mascotte", ill.mascotte_renard(), 120,130)
ill.save_png("h3", ill.horloge(3,0), 150,150)
ill.save_png("hempty", ill.horloge(0,0,hands=False), 150,150)
ill.save_png("star", ill.etoile(), 50,50)

# --- Test CHARTE A (bandeau d'angle + mascotte) ---
corps = exercice_head(1, "Relie chaque horloge a la bonne heure.")
corps += f'<div style="text-align:center;"><img src="{img_b64("h3.png")}" style="height:90px;"> &nbsp; <img src="{img_b64("hempty.png")}" style="height:90px;"></div>'
charte_a("Math&eacute;matiques", "Lire l'heure", 
         ["Lire les heures de la journ&eacute;e.", "Dessiner les aiguilles."],
         corps, mascotte_datauri=img_b64("mascotte.png"), sortie="testA.pdf")

# --- Test CHARTE B (encadre a ombre + page a decouper) ---
corps_b = exercice_head(1, "Le jeu des familles", tag="&agrave; trier")
corps_b += '<div class="sub">Range chaque aliment. Vignettes en derni&egrave;re page.</div>'
corps_b += page_decoupe("D&eacute;coupe puis colle dans l'exercice 1.",
                        vignette(img_b64("pomme.png"),"pomme"))
charte_b("QUESTIONNER LE MONDE", "L'alimentation <span class='amp'>&amp;</span> les dents",
         "1", corps_b, deco_datauris={"star":img_b64("star.png"), "apple":img_b64("pomme.png")},
         sortie="testB.pdf")

print("OK - testA.pdf et testB.pdf generes")
print("Pages testA:", os.path.getsize("testA.pdf"), "bytes ; testB:", os.path.getsize("testB.pdf"), "bytes")
