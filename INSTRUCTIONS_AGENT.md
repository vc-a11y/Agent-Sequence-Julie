# Kit de démarrage — Assistant Séquences Cycle 2

Ce kit rend l'agent **immédiatement opérationnel** : il contient les instructions
de l'agent, les générateurs d'illustrations, les deux gabarits de fiches, les
polices et des exemples. L'agent n'a plus à « reconstruire le décor » à chaque fois.

## Contenu du dossier

```
kit/
├── agent/
│   └── INSTRUCTIONS_AGENT.md      → À COLLER dans les instructions système de l'agent
├── generateurs/
│   └── illustrations.py           → Illustrations vectorielles "fait main" (aliments,
│                                     horloges, mascotte, étoile, assiette…)
├── gabarits/
│   └── gabarits.py                → 2 chartes de fiche (A: bandeau d'angle + mascotte ;
│                                     B: encadré-titre à ombre) + briques d'exercices
│                                     + page de découpe séparée
├── polices/
│   ├── PatrickHand-Regular.ttf    → manuscrite (consignes)
│   ├── Baloo2.ttf                 → titres ronds
│   ├── Fredoka.ttf                → variante ronde
│   └── Nunito.ttf                 → texte courant lisible
└── exemples/
    └── (PDF de démonstration)
```

## Mise en place (3 étapes)

### 1. Coller les instructions
Ouvre `agent/INSTRUCTIONS_AGENT.md` et colle tout son contenu dans le champ
**instructions / system prompt** de ton agent.

### 2. Activer les capacités côté plateforme
L'agent a besoin de :
- **exécution de code** (Python) et **création de fichiers** ;
- **weasyprint** (`pip install weasyprint --break-system-packages`) pour HTML→PDF ;
- **cairosvg** (`pip install cairosvg --break-system-packages`) pour SVG→PNG ;
- **LibreOffice** pour DOCX→PDF (si format Word demandé) ;
- les **polices** : copier les .ttf de `kit/polices/` dans `~/.fonts/` puis `fc-cache -f`.

> Sans ces capacités, l'agent rédige la séquence et décrit les supports,
> mais ne produit pas les PDF designés.

### 3. Fournir les ressources à l'agent
Mets `generateurs/illustrations.py` et `gabarits/gabarits.py` à disposition de
l'agent (base de connaissances / fichiers du projet). Il les importe pour produire
les fiches sans repartir de zéro.

## Police cursive scolaire (Script École / Cursive standard)
Ces polices ne sont pas libres et **ne sont pas incluses**. Pour les modèles
d'écriture en cursive normée :
- soit Julie **fournit son fichier .ttf** Script École → l'agent l'installe et
  produit des PDF en cursive parfaite ;
- soit l'agent produit le support en **Word** (la police s'applique chez Julie si
  elle l'a installée) ;
- à défaut, il utilise une cursive de substitution et le signale.

## Rappel des règles de conception (déjà dans les instructions)
1. **Cadrage par cases à choix** avant production (niveau, séances, format, typo…).
2. **Vocabulaire B.O. exact** + bloc « dosage selon la progressivité » visible.
3. **Supports élèves jolis** : couleurs variées, manuscrit, illustrations crayonnées,
   titre travaillé, manipulations/jeux (pas seulement des exercices sur table).
4. **Tout élément à découper → page séparée** en fin de fiche (`page_decoupe()`).
5. **PDF séparés** : prép / exercices / évaluation.

## Démarrage rapide (exemple de code pour l'agent)
```python
import sys, os
sys.path.insert(0, "generateurs"); os.environ["KIT_FONTS"] = "polices"
import illustrations as ill
from gabarits.gabarits import charte_a, exercice_head, img_b64

ill.save_png("h3", ill.horloge(3,0), 150,150)
corps = exercice_head(1, "Relie chaque horloge a la bonne heure.")
corps += f'<img src="{img_b64("h3.png")}" style="height:90px;">'
charte_a("Mathématiques", "Lire l'heure",
         ["Lire les heures de la journée.", "Dessiner les aiguilles."],
         corps, sortie="ma_fiche.pdf")
```
