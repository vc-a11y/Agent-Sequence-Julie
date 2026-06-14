"""
Gabarits de fiches eleves - Assistant Sequences Cycle 2
========================================================
Deux chartes visuelles pretes a l'emploi, en HTML/CSS -> PDF (weasyprint).

  - CHARTE A "bandeau d'angle"  : bandeau colore en coin + titre tampon
                                  + bulle d'objectifs + mascotte (facon modele maths).
  - CHARTE B "encadre a ombre"  : grand bandeau-titre arrondi a ombre portee
                                  + decor (etoile, illustration debordante).

Dependances : weasyprint  (pip install weasyprint --break-system-packages)
Polices a installer dans ~/.fonts : PatrickHand-Regular.ttf, Baloo2.ttf,
        Fredoka.ttf, Nunito.ttf  (fournies dans kit/polices).

REGLES IMPORTANTES (rappel) :
  * Tout element a decouper -> page separee en fin de fiche (page_decoupe()).
  * Illustrations vectorielles uniquement (cf. generateurs/illustrations.py).
  * Titre toujours travaille, jamais de sous-titre creux.
"""
import os, base64
from weasyprint import HTML

FONTS_DIR = os.environ.get("KIT_FONTS", os.path.abspath("../polices"))

def _font_face():
    return f"""
    @font-face {{ font-family:'Patrick'; src:url('file://{FONTS_DIR}/PatrickHand-Regular.ttf'); }}
    @font-face {{ font-family:'Baloo';   src:url('file://{FONTS_DIR}/Baloo2.ttf'); }}
    @font-face {{ font-family:'Fred';    src:url('file://{FONTS_DIR}/Fredoka.ttf'); }}
    @font-face {{ font-family:'Nun';     src:url('file://{FONTS_DIR}/Nunito.ttf'); }}
    """

def img_b64(path):
    """Encode une image PNG en data-URI pour l'embarquer dans le HTML."""
    b = base64.b64encode(open(path, "rb").read()).decode()
    return f"data:image/png;base64,{b}"

# =====================================================================
#  CHARTE A — bandeau d'angle + titre tampon + bulle + mascotte
# =====================================================================
def charte_a(discipline, titre, objectifs, corps_html,
             couleur="#5BC0DE", mascotte_datauri=None, sortie="fiche.pdf"):
    """
    objectifs : liste de chaines (affichees avec une coche verte).
    corps_html: le HTML des exercices (utiliser exercice_head(), etc.).
    """
    obj = "".join(f'<div class="g"><span class="v">&#10004;</span>{o}</div>' for o in objectifs)
    masc = f'<img class="mascotte" src="{mascotte_datauri}">' if mascotte_datauri else ""
    css = _font_face() + f"""
    @page {{ size:A4; margin:0; }}
    * {{ box-sizing:border-box; margin:0; padding:0; }}
    body {{ font-family:'Nun'; color:#3A3A3A; font-size:13px; }}
    .wrap {{ padding:0 16mm 14mm; }}
    .corner {{ position:relative; height:78px; margin-bottom:6px; }}
    .corner .blob {{ position:absolute; top:0; left:0; width:230px; height:88px;
        background:{couleur}; border-radius:0 0 60px 0; }}
    .corner .disc {{ position:absolute; top:22px; left:24px; font-family:'Baloo'; font-size:19px; color:#13414d; }}
    .corner .nameblock {{ position:absolute; top:14px; right:0; font-family:'Patrick'; font-size:14px; }}
    .corner .nameblock u {{ text-decoration:none; border-bottom:1.5px dotted #aaa; padding:0 40px; }}
    .stamp {{ font-family:'Baloo'; font-style:italic; font-size:30px; color:#2b2b2b; letter-spacing:1px;
        transform:skewX(-9deg); border-bottom:4px solid {couleur}; display:inline-block;
        padding-bottom:2px; margin:2px 0 12px; text-transform:uppercase; }}
    .goalrow {{ position:relative; min-height:120px; margin-bottom:8px; }}
    .bubble {{ background:#fff; border:2.5px solid #3A3A3A; border-radius:16px; padding:11px 16px;
        width:74%; box-shadow:3px 3px 0 rgba(91,192,222,.25); position:relative; }}
    .bubble:after {{ content:''; position:absolute; right:-16px; top:38px; border:9px solid transparent; border-left-color:#3A3A3A; }}
    .bubble .gt {{ font-family:'Baloo'; font-size:14px; color:#3D5A80; margin-bottom:5px; }}
    .bubble .g {{ font-family:'Patrick'; font-size:14px; margin:3px 0; }}
    .bubble .g .v {{ color:#7FB069; font-family:'Baloo'; margin-right:5px; }}
    .mascotte {{ position:absolute; right:6px; top:0; width:96px; }}
    {COMMON_EX_CSS}
    """
    html = f"""<html><head><meta charset='utf-8'><style>{css}</style></head><body>
    <div class="corner"><div class="blob"></div>
      <div class="disc">{discipline}</div>
      <div class="nameblock">Pr&eacute;nom : <u>&nbsp;</u><br><br>Date : <u>&nbsp;</u></div>
    </div>
    <div class="wrap">
      <div class="stamp">{titre}</div>
      <div class="goalrow">
        <div class="bubble"><div class="gt">Voici les objectifs des exercices :</div>{obj}</div>
        {masc}
      </div>
      {corps_html}
    </div></body></html>"""
    HTML(string=html).write_pdf(sortie)
    return sortie

# =====================================================================
#  CHARTE B — encadre-titre a ombre portee + decor
# =====================================================================
def charte_b(discipline, titre_html, fiche_num, corps_html,
             deco_datauris=None, sortie="fiche.pdf"):
    """
    titre_html : peut contenir <span class="amp">&amp;</span> pour colorer un mot.
    deco_datauris : dict optionnel {'star':datauri, 'apple':datauri}.
    """
    deco = deco_datauris or {}
    star  = f'<img class="deco-star" src="{deco["star"]}">' if "star" in deco else ""
    apple = f'<img class="deco-apple" src="{deco["apple"]}">' if "apple" in deco else ""
    css = _font_face() + f"""
    @page {{ size:A4; margin:10mm 9mm; }}
    * {{ box-sizing:border-box; margin:0; padding:0; }}
    body {{ font-family:'Nun'; color:#3A3A3A; font-size:12px; }}
    .banner {{ position:relative; background:#FCF3D6; border:3px solid #3A3A3A;
        border-radius:22px 20px 24px 18px; padding:13px 20px 15px 20px; margin-bottom:16px;
        box-shadow:4px 4px 0 rgba(61,90,128,.18); }}
    .banner .disc {{ font-family:'Baloo'; font-size:10px; color:#b08a3a; letter-spacing:2px; }}
    .banner h1 {{ font-family:'Baloo'; font-size:32px; color:#3D5A80; line-height:1.05; margin-top:1px; }}
    .banner h1 .amp {{ color:#E8615A; }}
    .banner .ul {{ display:block; height:8px; width:240px; margin-top:4px; background:#7FB069;
        border-radius:7px; transform:rotate(-1deg); }}
    .fiche-badge {{ position:absolute; top:16px; right:20px; font-family:'Baloo'; font-size:13px;
        background:#5B9BD5; color:#fff; padding:5px 13px; border-radius:13px; transform:rotate(3deg);
        box-shadow:2px 2px 0 rgba(0,0,0,.15); }}
    .deco-apple {{ position:absolute; bottom:-10px; right:118px; width:44px; transform:rotate(9deg); }}
    .deco-star  {{ position:absolute; top:-13px; left:-7px; width:34px; transform:rotate(-12deg); }}
    .namebar {{ font-family:'Patrick'; font-size:15px; margin-bottom:12px; }}
    .namebar u {{ text-decoration:none; border-bottom:2px dotted #bbb; }}
    {COMMON_EX_CSS}
    """
    html = f"""<html><head><meta charset='utf-8'><style>{css}</style></head><body>
    <div class="banner">{star}
      <div class="disc">{discipline}</div>
      <h1>{titre_html}</h1><span class="ul"></span>
      <span class="fiche-badge">Fiche n&deg; {fiche_num}</span>{apple}
    </div>
    <div class="namebar">Mon pr&eacute;nom : <u>{"&nbsp;"*34}</u></div>
    {corps_html}
    </body></html>"""
    HTML(string=html).write_pdf(sortie)
    return sortie

# =====================================================================
#  Briques d'exercices communes
# =====================================================================
COMMON_EX_CSS = """
    .exhead { margin:14px 0 8px; }
    .pill { font-family:'Baloo'; color:#fff; font-size:15px; display:inline-block; width:30px;
        height:30px; line-height:30px; text-align:center; border-radius:50%; }
    .extit { font-family:'Patrick'; font-size:16px; vertical-align:6px; margin-left:8px; }
    .tag { font-family:'Baloo'; font-size:10px; color:#fff; padding:2px 8px; border-radius:9px;
        vertical-align:8px; margin-left:6px; display:inline-block; transform:rotate(2deg); }
    .sub { font-family:'Patrick'; font-size:14px; color:#555; margin:3px 0 8px 38px; }
    .ex { margin-bottom:14px; }
    .card { display:inline-block; width:118px; border:2.5px solid #3A3A3A;
        border-radius:18px 15px 20px 14px; padding:7px 5px; text-align:center; margin:0 6px 0 0; vertical-align:top; }
    .card img { height:58px; } .card .l { font-family:'Patrick'; font-size:15px; }
    .chip { display:inline-block; width:80px; border:2px solid #3A3A3A; border-radius:12px;
        padding:4px; text-align:center; margin:0 5px 4px 0; vertical-align:top; }
    .chip img { height:42px; } .chip .l { font-family:'Patrick'; font-size:12px; }
    /* page a decouper */
    .cut-banner { border:2.5px dashed #E89BB0; border-radius:16px; padding:10px 14px;
        margin-bottom:16px; background:#FBE7EC; }
    .cut-banner .ico { font-family:'Baloo'; font-size:20px; color:#E8615A; }
    .cut-banner .ct  { font-family:'Baloo'; font-size:20px; color:#3D5A80; margin-left:8px; vertical-align:3px; }
    .cut-banner .cn  { font-family:'Patrick'; font-size:13px; color:#666; display:block; margin-top:4px; }
    .cut-grid { text-align:center; }
    .cut-grid .chip { width:120px; border:2px dashed #3A3A3A; padding:10px 6px; margin:8px; }
    .cut-grid .chip img { height:66px; } .cut-grid .chip .l { font-size:15px; }
"""

PILL_COLORS = ["#7FB069", "#5B9BD5", "#E89BB0", "#F2A65A", "#9B72AA"]

def exercice_head(num, consigne, tag=None):
    color = PILL_COLORS[(num-1) % len(PILL_COLORS)]
    t = f'<span class="tag" style="background:{color};">{tag}</span>' if tag else ""
    return (f'<div class="exhead"><span class="pill" style="background:{color};">{num}</span>'
            f'<span class="extit">{consigne}</span>{t}</div>')

def page_decoupe(titre_consigne, vignettes_html):
    """
    Genere la PAGE SEPAREE de decoupage (saut de page automatique).
    vignettes_html : suite de blocs .chip a decouper.
    """
    return f"""
    <div style="page-break-before:always;"></div>
    <div class="cut-banner"><span class="ico">&#9986;</span>
      <span class="ct">Mat&eacute;riel &agrave; d&eacute;couper</span>
      <span class="cn">{titre_consigne}</span></div>
    <div class="cut-grid">{vignettes_html}</div>
    """

def vignette(datauri, label):
    return f'<div class="chip"><img src="{datauri}"><div class="l">{label}</div></div>'
