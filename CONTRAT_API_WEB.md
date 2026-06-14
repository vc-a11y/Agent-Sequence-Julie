import React, { useState, useMemo } from "react";

// ============================================================
//  Assistant Séquences Cycle 2 — Console connectée à ton API
//  Catalogue + parcours + aperçu de séquence + bouton Générer
// ============================================================

// ⚙️  CONFIG API — à renseigner avec ton endpoint.
//     L'interface envoie un POST JSON et attend des URLs de fichiers en retour.
const API_CONFIG = {
  url: "https://ton-api.exemple.fr/generer", // <-- REMPLACE par ton endpoint
  headers: { "Content-Type": "application/json" }, // ajoute ton auth ici plus tard
};
// Contrat :
//   Requête (POST JSON) : { discipline, sequence, niveau, seances, produits[],
//                           format, typographie, detail, differenciation, demande }
//   Réponse (JSON)      : { fichiers: [ { nom, url, type } ] }

const DISCIPLINES = [
  { id: "qlm", nom: "Questionner le monde", accent: "#3D7A6B", sequences: [
    { titre: "Le jour et la nuit", niveaux: ["CE1", "CE2"], note: "Rythmes cycliques du temps",
      attendus: ["Se repérer dans le temps et mesurer des durées.", "Repérer et situer quelques événements dans un temps long."],
      domaines: ["Se situer dans l'espace et dans le temps — d.5", "Pratiquer des démarches scientifiques — d.4", "Pratiquer des langages — d.1"],
      cca: ["Identifier les rythmes cycliques du temps.", "L'alternance jour / nuit.", "Le caractère cyclique des jours, des semaines, des saisons."],
      prog: "En CE1 : alternance jour/nuit et caractère cyclique, première explication par la rotation de la Terre. Réservé au CE2 : Terre dans l'univers (astres, position Terre-Soleil, lunaisons), mesure fine des durées." },
    { titre: "L'alimentation et les dents", niveaux: ["CP"], note: "Comportements favorables à la santé",
      attendus: ["Connaître des caractéristiques du monde vivant, ses interactions, sa diversité.", "Reconnaître des comportements favorables à sa santé."],
      domaines: ["Pratiquer des démarches scientifiques — d.4", "Pratiquer des langages — d.1", "Adopter un comportement éthique et responsable — d.3, 5"],
      cca: ["Quelques règles d'hygiène de vie (variété alimentaire, propreté des dents).", "Catégories d'aliments, leur origine.", "Modifications de la dentition."],
      prog: "En CP : catégories d'aliments, variété, hygiène et dentition. Réservé au CE1-CE2 : apports énergétiques (« manger pour bouger »), équilibre alimentaire sur la journée/semaine." },
    { titre: "Les trois états de la matière", niveaux: ["CE2"], note: "Changements d'états de l'eau",
      attendus: ["Identifier les trois états de la matière et observer des changements d'états.", "Identifier un changement d'état de l'eau dans un phénomène de la vie quotidienne."],
      domaines: ["Pratiquer des démarches scientifiques — d.4", "S'approprier des outils et des méthodes — d.2"],
      cca: ["Propriétés des solides, liquides et gaz.", "Changements d'états (solidification, condensation, fusion).", "Les états de l'eau (liquide, glace, vapeur)."],
      prog: "Tout ce qui est lié à l'état gazeux est abordé en CE2." },
    { titre: "Le monde vivant : animal, végétal", niveaux: ["CP", "CE1"], note: "Caractéristiques du vivant",
      attendus: ["Connaître des caractéristiques du monde vivant, ses interactions, sa diversité."],
      domaines: ["Pratiquer des démarches scientifiques — d.4", "Pratiquer des langages — d.1"],
      cca: ["Identifier ce qui est animal, végétal, minéral.", "Le cycle de vie des êtres vivants.", "Régimes alimentaires de quelques animaux."],
      prog: "Observation du proche puis du plus lointain ; petits écosystèmes en classe." },
    { titre: "Se repérer dans l'espace", niveaux: ["CP", "CE1", "CE2"], note: "Repères et représentations",
      attendus: ["Se repérer dans l'espace et le représenter.", "Situer un lieu sur une carte, un globe ou un écran."],
      domaines: ["Se situer dans l'espace et dans le temps — d.5"],
      cca: ["Vocabulaire des positions et des déplacements.", "Modes de représentation de l'espace.", "Éléments constitutifs d'une carte."],
      prog: "De l'espace proche et connu vers l'espace lointain au fil du cycle." },
    { titre: "Les objets techniques", niveaux: ["CE1", "CE2"], note: "Fonction et fonctionnement",
      attendus: ["Comprendre la fonction et le fonctionnement d'objets fabriqués.", "Réaliser quelques objets et circuits électriques simples."],
      domaines: ["Imaginer, réaliser — d.5", "S'approprier des outils et des méthodes — d.2"],
      cca: ["Observer et utiliser des objets techniques.", "Constituants d'un circuit électrique simple.", "Rôle de l'interrupteur, règles de sécurité."],
      prog: "Les démarches varient selon l'âge ; circuits travaillés avec les règles de sécurité." },
  ]},
  { id: "math", nom: "Mathématiques", accent: "#2E5B9E", sequences: [
    { titre: "Lire l'heure", niveaux: ["CE1", "CE2"], note: "Se repérer dans le temps, durées",
      attendus: ["Se repérer dans le temps et mesurer des durées.", "Comparer, estimer, mesurer des durées."],
      domaines: ["Représenter — d.1, 5", "Modéliser — d.1, 2, 4"],
      cca: ["Lire l'heure sur une horloge à aiguilles.", "Unités usuelles de durées et relations.", "Caractère cyclique des jours, des saisons."],
      prog: "Lien étroit avec « Questionner le monde » pour les repères temporels." },
    { titre: "Les nombres jusqu'à 100", niveaux: ["CP", "CE1"], note: "Nommer, lire, écrire, comparer",
      attendus: ["Comprendre et utiliser des nombres entiers pour dénombrer, ordonner, comparer.", "Nommer, lire, écrire, représenter des nombres entiers."],
      domaines: ["Représenter — d.1, 5", "Calculer — d.4"],
      cca: ["Unités de numération (unités, dizaines).", "Comparer, ranger, encadrer avec =, ≠, <, >.", "Diverses représentations des nombres."],
      prog: "Champ numérique élargi progressivement ; CP centré sur les petits nombres." },
    { titre: "Addition et soustraction posées", niveaux: ["CE1", "CE2"], note: "Calcul posé",
      attendus: ["Calculer avec des nombres entiers.", "Résoudre des problèmes en utilisant le calcul."],
      domaines: ["Calculer — d.4", "Modéliser — d.1, 2, 4"],
      cca: ["Algorithme de calcul posé (addition, soustraction).", "Mémoriser tables et compléments.", "Sens des opérations."],
      prog: "La technique posée s'appuie sur le calcul mental et la numération." },
    { titre: "Les solides et les figures planes", niveaux: ["CP", "CE1", "CE2"], note: "Reconnaître, décrire, reproduire",
      attendus: ["Reconnaître, nommer, décrire, reproduire quelques solides.", "Reconnaître, nommer, décrire, reproduire quelques figures géométriques."],
      domaines: ["Représenter — d.1, 5", "Raisonner — d.2, 3, 4"],
      cca: ["Vocabulaire des solides (cube, pavé, boule…).", "Figures usuelles (carré, rectangle, triangle, cercle).", "Alignement, angle droit, égalité de longueurs."],
      prog: "Manipulations et reproductions, difficulté croissante selon les instruments." },
    { titre: "Mesurer des longueurs", niveaux: ["CE1", "CE2"], note: "Grandeurs et mesures",
      attendus: ["Comparer, estimer, mesurer des longueurs.", "Résoudre des problèmes impliquant des longueurs."],
      domaines: ["Modéliser — d.1, 2, 4", "Calculer — d.4"],
      cca: ["Unités usuelles (m, dm, cm, mm, km) et relations.", "Utiliser règle graduée, mètre.", "Encadrer une mesure par deux entiers."],
      prog: "Lien avec « Questionner le monde » et l'EPS." },
  ]},
  { id: "fr", nom: "Français", accent: "#8E3B6B", sequences: [
    { titre: "Correspondances graphème-phonème", niveaux: ["CP"], note: "Identifier des mots",
      attendus: ["Identifier des mots de manière de plus en plus aisée.", "Lire et comprendre des textes adaptés."],
      domaines: ["Comprendre le fonctionnement de la langue — d.1, 2"],
      cca: ["Établir les correspondances graphophonologiques.", "Combinatoire (syllabes simples et complexes).", "Mémoriser mots fréquents et irréguliers."],
      prog: "Automatisation du code alphabétique complète à la fin du CP." },
    { titre: "La phrase simple", niveaux: ["CE1", "CE2"], note: "Se repérer dans la phrase",
      attendus: ["Comprendre le fonctionnement de la langue.", "Se repérer dans la phrase simple."],
      domaines: ["Comprendre le fonctionnement de la langue — d.1, 2"],
      cca: ["Identifier sujet, verbe, compléments.", "Classes de mots (nom, article, adjectif, verbe).", "Types de phrases et ponctuation."],
      prog: "Observation et manipulation avant la formulation de règles." },
    { titre: "Écrire un texte court", niveaux: ["CP", "CE1", "CE2"], note: "S'approprier une démarche",
      attendus: ["Écrire des textes en commençant à s'approprier une démarche.", "Réviser et améliorer l'écrit produit."],
      domaines: ["Écrire — d.1"],
      cca: ["Démarche d'écriture (trouver, organiser, écrire).", "Écrits courts porteurs de sens.", "Vigilance orthographique."],
      prog: "Des écrits courts quotidiens vers des projets d'écriture plus longs." },
    { titre: "Accords dans le groupe nominal", niveaux: ["CE1", "CE2"], note: "Orthographe grammaticale",
      attendus: ["Maîtriser l'orthographe grammaticale de base.", "Raisonner pour réaliser les accords."],
      domaines: ["Comprendre le fonctionnement de la langue — d.1, 2"],
      cca: ["Chaîne d'accords déterminant/nom/adjectif.", "Marques d'accord en nombre (-s) et genre (-e).", "Notion de groupe nominal."],
      prog: "Cas simples d'abord ; dictées et activités ritualisées." },
  ]},
  { id: "emc", nom: "Enseignement moral et civique", accent: "#B5532A", sequences: [
    { titre: "Respecter autrui", niveaux: ["CP", "CE1", "CE2"], note: "Accepter les différences",
      attendus: ["Respecter autrui : accepter et respecter les différences.", "Identifier et partager des émotions et des sentiments."],
      domaines: ["Culture de la sensibilité", "Culture de la règle et du droit"],
      cca: ["Le respect des adultes et des pairs.", "Le respect des autres dans leur diversité.", "Reconnaissance des émotions de base."],
      prog: "À partir de situations concrètes et de discussions réglées." },
    { titre: "Les symboles de la République", niveaux: ["CE1", "CE2"], note: "Valeurs et principes",
      attendus: ["Connaître les valeurs, principes et symboles de la République.", "Accéder à une première connaissance d'une société démocratique."],
      domaines: ["Culture de la règle et du droit", "Culture du jugement"],
      cca: ["Symboles : drapeau, hymne, devise, fête nationale.", "Liberté, Égalité, Fraternité, laïcité.", "L'égalité filles-garçons."],
      prog: "Notions abordées régulièrement tout au long du cycle." },
    { titre: "Les règles de la classe", niveaux: ["CP"], note: "Vivre ensemble",
      attendus: ["Respecter les règles de la vie collective."],
      domaines: ["Culture de la règle et du droit"],
      cca: ["Règles de vie de la classe et de l'école.", "Vocabulaire de la règle et du droit.", "La règle peut interdire, obliger, autoriser."],
      prog: "Dans la continuité du cycle 1." },
  ]},
  { id: "arts", nom: "Arts plastiques", accent: "#C18A2E", sequences: [
    { titre: "La représentation du monde", niveaux: ["CP", "CE1", "CE2"], note: "Dessiner, représenter",
      attendus: ["Réaliser et donner à voir des productions plastiques.", "Comparer quelques œuvres d'art."],
      domaines: ["Expérimenter, produire, créer — d.1, 2, 4, 5"],
      cca: ["Le dessin comme moyen d'expression.", "Employer divers outils, dont numériques.", "Influence des outils et supports."],
      prog: "Toutes les questions abordées chaque année, en spirale." },
    { titre: "L'expression des émotions", niveaux: ["CP", "CE1", "CE2"], note: "Couleurs et matières",
      attendus: ["Proposer des réponses inventives dans un projet.", "S'exprimer sur sa production, celle de ses pairs, sur l'art."],
      domaines: ["Expérimenter, produire, créer — d.1, 2, 4, 5"],
      cca: ["S'emparer des éléments du langage plastique.", "Expérimenter les effets des couleurs et matières.", "Confronter sa perception à celle des autres."],
      prog: "Se nourrit de la lecture de contes et de mythes." },
  ]},
  { id: "eps", nom: "Éducation physique et sportive", accent: "#4A7A2E", sequences: [
    { titre: "Courir, sauter, lancer", niveaux: ["CP", "CE1", "CE2"], note: "Produire une performance",
      attendus: ["Courir, sauter, lancer à des intensités et durées variables.", "Accepter de viser une performance mesurée."],
      domaines: ["Développer sa motricité — d.1"],
      cca: ["Transformer sa motricité spontanée.", "Mobiliser ses ressources pour des efforts variés.", "Respecter les règles de sécurité."],
      prog: "Agir sur sa motricité pour améliorer la performance au fil du cycle." },
    { titre: "Jeux collectifs", niveaux: ["CP", "CE1", "CE2"], note: "Affrontement collectif",
      attendus: ["S'engager dans un affrontement en respectant les règles.", "Connaître le but du jeu, reconnaître partenaires et adversaires."],
      domaines: ["Partager des règles, assumer des rôles — d.3"],
      cca: ["Rechercher le gain du jeu.", "Accepter l'opposition et la coopération.", "S'informer, prendre des repères pour agir."],
      prog: "De la reconnaissance des rôles vers des stratégies d'attaque/défense." },
  ]},
];

const PRODUITS = [
  { id: "prep", label: "Fiche de préparation" },
  { id: "exercices", label: "Exercices élèves" },
  { id: "evaluation", label: "Évaluation" },
  { id: "images", label: "Images-supports" },
];
const SEANCES = [3, 4, 5, 6];
const FORMATS = ["PDF", "Word"];
const TYPOS = ["Script École", "Cursive standard"];
const DETAILS = ["Synthétique", "Détaillé"];
const DIFFS = ["Légère", "Complète"];

function Chip({ active, disabled, onClick, children, accent }) {
  return (
    <button onClick={onClick} disabled={disabled}
      style={{ fontFamily: "'Baloo 2', system-ui, sans-serif", fontSize: 14.5,
        padding: "6px 15px", borderRadius: 13,
        border: active ? `2.5px solid ${accent}` : "2px solid #d8d2c4",
        background: active ? accent : "#fffdf8", color: active ? "#fff" : "#4a4636",
        cursor: disabled ? "default" : "pointer", opacity: disabled ? 0.4 : 1,
        transition: "all .12s ease", boxShadow: active ? `2px 2px 0 ${accent}40` : "none" }}>
      {children}
    </button>
  );
}
function Field({ label, hint, children }) {
  return (
    <div style={{ marginBottom: 18 }}>
      <div style={{ display: "flex", alignItems: "baseline", gap: 8, marginBottom: 8 }}>
        <span style={{ fontFamily: "'Baloo 2', sans-serif", fontSize: 12.5, fontWeight: 600,
          letterSpacing: ".8px", textTransform: "uppercase", color: "#6b6450" }}>{label}</span>
        {hint && <span style={{ fontFamily: "'Patrick Hand', cursive", fontSize: 13.5, color: "#a39d88" }}>{hint}</span>}
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 7 }}>{children}</div>
    </div>
  );
}
function Section({ titre, items, accent }) {
  return (
    <div style={{ marginBottom: 9 }}>
      <div style={{ fontFamily: "'Baloo 2', sans-serif", fontSize: 11.5, fontWeight: 700, color: accent,
        textTransform: "uppercase", letterSpacing: ".5px", marginBottom: 3 }}>{titre}</div>
      <ul style={{ margin: 0, paddingLeft: 17 }}>
        {items.map((it, i) => (<li key={i} style={{ fontFamily: "'Nunito', sans-serif", fontSize: 13,
          color: "#4a4636", lineHeight: 1.4, marginBottom: 2 }}>{it}</li>))}
      </ul>
    </div>
  );
}

export default function App() {
  const [discId, setDiscId] = useState("qlm");
  const [seqTitre, setSeqTitre] = useState("Le jour et la nuit");
  const [niveau, setNiveau] = useState("CE1");
  const [seances, setSeances] = useState(5);
  const [produits, setProduits] = useState(["prep", "exercices", "evaluation"]);
  const [format, setFormat] = useState("PDF");
  const [typo, setTypo] = useState("Script École");
  const [detail, setDetail] = useState("Détaillé");
  const [diff, setDiff] = useState("Complète");

  const [modeReel, setModeReel] = useState(false);
  const [apiUrl, setApiUrl] = useState(API_CONFIG.url);
  const [statut, setStatut] = useState("idle");
  const [fichiers, setFichiers] = useState([]);
  const [erreur, setErreur] = useState("");

  const disc = DISCIPLINES.find((d) => d.id === discId);
  const accent = disc.accent;
  const seqObj = disc.sequences.find((s) => s.titre === seqTitre) || disc.sequences[0];
  const niveauxDispo = seqObj.niveaux;

  const resetSortie = () => { setStatut("idle"); setFichiers([]); setErreur(""); };
  const choisirDiscipline = (d) => { setDiscId(d.id); const f = d.sequences[0]; setSeqTitre(f.titre); setNiveau(f.niveaux[0]); resetSortie(); };
  const choisirSequence = (s) => { setSeqTitre(s.titre); if (!s.niveaux.includes(niveau)) setNiveau(s.niveaux[0]); resetSortie(); };
  const toggleProduit = (id) => { setProduits((p) => (p.includes(id) ? p.filter((x) => x !== id) : [...p, id])); resetSortie(); };

  const demande = useMemo(() => {
    const lp = produits.length === PRODUITS.length ? "tous les supports"
      : produits.map((id) => PRODUITS.find((p) => p.id === id)?.label.toLowerCase()).join(", ");
    return `Crée une séquence « ${seqTitre} » en ${niveau} (${disc.nom}), sur ${seances} séances. `
      + `Produis ${lp || "la séquence seule"} au format ${format}. Typographie : ${typo}. `
      + `Déroulé ${detail.toLowerCase()}. Différenciation ${diff.toLowerCase()}.`;
  }, [seqTitre, niveau, disc, seances, produits, format, typo, detail, diff]);

  const payload = useMemo(() => ({
    discipline: disc.nom, sequence: seqTitre, niveau, seances,
    produits, format, typographie: typo, detail, differenciation: diff, demande,
  }), [disc, seqTitre, niveau, seances, produits, format, typo, detail, diff, demande]);

  async function generer() {
    setStatut("loading"); setErreur(""); setFichiers([]);
    if (!modeReel) {
      await new Promise((r) => setTimeout(r, 1100));
      const base = seqTitre.replace(/[^a-zA-Z0-9]+/g, "_");
      const demo = [];
      if (produits.includes("prep")) demo.push({ nom: `Fiche_preparation_${base}_${niveau}.pdf`, url: "#" });
      if (produits.includes("exercices")) demo.push({ nom: `Exercices_${base}_${niveau}.pdf`, url: "#" });
      if (produits.includes("evaluation")) demo.push({ nom: `Evaluation_${base}_${niveau}.pdf`, url: "#" });
      setFichiers(demo); setStatut("done"); return;
    }
    try {
      const res = await fetch(apiUrl, { method: "POST", headers: API_CONFIG.headers, body: JSON.stringify(payload) });
      if (!res.ok) throw new Error(`Réponse ${res.status}`);
      const data = await res.json();
      setFichiers(data.fichiers || []); setStatut("done");
    } catch (e) { setErreur(String(e.message || e)); setStatut("error"); }
  }

  return (
    <div style={{ minHeight: "100vh", background: "#f3efe4",
      backgroundImage: "repeating-linear-gradient(#f3efe4, #f3efe4 27px, #e4ddc9 28px)",
      fontFamily: "'Nunito', system-ui, sans-serif" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700&family=Patrick+Hand&family=Nunito:wght@400;600;700&display=swap');
        * { box-sizing: border-box; }
        button:focus-visible, input:focus-visible { outline: 3px solid #2E5B9E; outline-offset: 2px; }
        @media (max-width: 900px){ .grid3 { grid-template-columns: 1fr !important; } }
      `}</style>

      <div style={{ position: "relative", borderBottom: "3px solid #d8d2c4", background: "#fffdf8", padding: "24px 40px 20px 64px" }}>
        <div style={{ position: "absolute", left: 40, top: 0, bottom: 0, width: 2, background: "#d98b8b" }} />
        <div style={{ fontFamily: "'Patrick Hand', cursive", fontSize: 15, color: "#a39d88", letterSpacing: 1 }}>Assistant pédagogique · Cycle 2</div>
        <h1 style={{ fontFamily: "'Baloo 2', sans-serif", fontSize: 32, fontWeight: 700, color: "#2b2b40", margin: "2px 0 0" }}>Préparer une séquence</h1>
      </div>

      <div className="grid3" style={{ display: "grid", gridTemplateColumns: "0.85fr 1fr 1.1fr", maxWidth: 1240, margin: "0 auto" }}>

        <div style={{ padding: "24px 20px 24px 40px" }}>
          <Field label="Discipline">
            {DISCIPLINES.map((d) => (<Chip key={d.id} active={d.id === discId} accent={d.accent} onClick={() => choisirDiscipline(d)}>{d.nom}</Chip>))}
          </Field>
          <div style={{ marginBottom: 8, fontFamily: "'Baloo 2', sans-serif", fontSize: 12.5, fontWeight: 600, letterSpacing: ".8px", textTransform: "uppercase", color: "#6b6450" }}>Séquence</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
            {disc.sequences.map((s) => {
              const active = s.titre === seqTitre;
              return (
                <button key={s.titre} onClick={() => choisirSequence(s)}
                  style={{ textAlign: "left", cursor: "pointer", padding: "10px 13px", borderRadius: 13,
                    border: active ? `2.5px solid ${accent}` : "2px solid #e0dac9", background: active ? `${accent}12` : "#fffdf8", transition: "all .12s ease" }}>
                  <div style={{ fontFamily: "'Baloo 2', sans-serif", fontSize: 15, color: active ? accent : "#3a3a40", fontWeight: 600 }}>{s.titre}</div>
                  <div style={{ display: "flex", justifyContent: "space-between", marginTop: 2 }}>
                    <span style={{ fontFamily: "'Patrick Hand', cursive", fontSize: 13, color: "#9a937e" }}>{s.note}</span>
                    <span style={{ fontFamily: "'Patrick Hand', cursive", fontSize: 12.5, color: accent }}>{s.niveaux.join(" · ")}</span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        <div style={{ padding: "24px 22px", borderLeft: "2px dashed #d8d2c4" }}>
          <Field label="Niveau" hint="selon la séquence">
            {["CP", "CE1", "CE2"].map((n) => (<Chip key={n} active={n === niveau && niveauxDispo.includes(n)} disabled={!niveauxDispo.includes(n)} accent={accent} onClick={() => { setNiveau(n); resetSortie(); }}>{n}</Chip>))}
          </Field>
          <Field label="Nombre de séances">
            {SEANCES.map((n) => (<Chip key={n} active={n === seances} accent={accent} onClick={() => { setSeances(n); resetSortie(); }}>{n}</Chip>))}
          </Field>
          <Field label="Que produire ?" hint="plusieurs choix">
            {PRODUITS.map((p) => (<Chip key={p.id} active={produits.includes(p.id)} accent={accent} onClick={() => toggleProduit(p.id)}>{p.label}</Chip>))}
          </Field>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
            <Field label="Format">{FORMATS.map((f) => (<Chip key={f} active={f === format} accent={accent} onClick={() => { setFormat(f); resetSortie(); }}>{f}</Chip>))}</Field>
            <Field label="Typographie">{TYPOS.map((t) => (<Chip key={t} active={t === typo} accent={accent} onClick={() => { setTypo(t); resetSortie(); }}>{t}</Chip>))}</Field>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
            <Field label="Déroulé">{DETAILS.map((d) => (<Chip key={d} active={d === detail} accent={accent} onClick={() => { setDetail(d); resetSortie(); }}>{d}</Chip>))}</Field>
            <Field label="Différenciation">{DIFFS.map((d) => (<Chip key={d} active={d === diff} accent={accent} onClick={() => { setDiff(d); resetSortie(); }}>{d}</Chip>))}</Field>
          </div>
        </div>

        <div style={{ padding: "24px 40px 24px 22px", borderLeft: "2px dashed #d8d2c4" }}>
          <div style={{ background: "#fffdf8", border: `2.5px solid ${accent}`, borderRadius: 18, padding: "18px 20px", boxShadow: `4px 4px 0 ${accent}25` }}>
            <div style={{ fontFamily: "'Patrick Hand', cursive", fontSize: 14, color: "#a39d88" }}>Aperçu · {disc.nom} · {niveau}</div>
            <div style={{ fontFamily: "'Baloo 2', sans-serif", fontSize: 22, fontWeight: 700, color: "#2b2b40", lineHeight: 1.1, marginBottom: 10 }}>{seqTitre}</div>
            <Section accent={accent} titre="Attendus de fin de cycle" items={seqObj.attendus} />
            <Section accent={accent} titre="Compétences & domaines du socle" items={seqObj.domaines} />
            <Section accent={accent} titre="Connaissances & compétences associées" items={seqObj.cca} />
            <div style={{ marginTop: 12, background: "#FFF4D6", borderLeft: "5px solid #E0A800", borderRadius: 6, padding: "9px 12px" }}>
              <div style={{ fontFamily: "'Baloo 2', sans-serif", fontSize: 12, fontWeight: 700, color: "#7A5C00", textTransform: "uppercase", letterSpacing: ".5px", marginBottom: 3 }}>Dosage selon la progressivité</div>
              <div style={{ fontFamily: "'Nunito', sans-serif", fontSize: 13, color: "#7A5C00", lineHeight: 1.45 }}>{seqObj.prog}</div>
            </div>
          </div>

          <div style={{ marginTop: 16 }}>
            <label style={{ display: "flex", alignItems: "center", gap: 8, fontFamily: "'Patrick Hand', cursive", fontSize: 14, color: "#6b6450", marginBottom: 8, cursor: "pointer" }}>
              <input type="checkbox" checked={modeReel} onChange={(e) => { setModeReel(e.target.checked); resetSortie(); }} />
              Appeler mon API réelle (sinon : démonstration)
            </label>
            {modeReel && (
              <input value={apiUrl} onChange={(e) => setApiUrl(e.target.value)} placeholder="https://ton-api…/generer"
                style={{ width: "100%", padding: "8px 11px", borderRadius: 10, border: "2px solid #d8d2c4", fontFamily: "monospace", fontSize: 13, marginBottom: 10, background: "#fffdf8" }} />
            )}
            <button onClick={generer} disabled={statut === "loading" || produits.length === 0}
              style={{ width: "100%", fontFamily: "'Baloo 2', sans-serif", fontSize: 17, fontWeight: 700, padding: "13px", borderRadius: 14, border: "none",
                cursor: produits.length === 0 ? "default" : "pointer", background: produits.length === 0 ? "#c9c3b2" : accent, color: "#fff",
                boxShadow: produits.length === 0 ? "none" : `3px 3px 0 ${accent}55`, transition: "all .15s ease" }}>
              {statut === "loading" ? "Génération en cours…" : "Générer les documents"}
            </button>

            {statut === "done" && (
              <div style={{ marginTop: 14 }}>
                <div style={{ fontFamily: "'Baloo 2', sans-serif", fontSize: 13, color: "#3D7A6B", marginBottom: 8 }}>
                  {modeReel ? "Fichiers reçus :" : "Démo — fichiers qui seraient produits :"}
                </div>
                {fichiers.map((f, i) => (
                  <a key={i} href={f.url} download
                    style={{ display: "flex", alignItems: "center", justifyContent: "space-between", textDecoration: "none",
                      background: "#fffdf8", border: "2px solid #e0dac9", borderRadius: 11, padding: "10px 13px", marginBottom: 7 }}>
                    <span style={{ fontFamily: "'Nunito', sans-serif", fontSize: 14, color: "#3a3a40", fontWeight: 600 }}>{f.nom}</span>
                    <span style={{ fontFamily: "'Baloo 2', sans-serif", fontSize: 13, color: accent }}>{modeReel ? "Télécharger" : "—"}</span>
                  </a>
                ))}
              </div>
            )}
            {statut === "error" && (
              <div style={{ marginTop: 12, background: "#FBE7EC", border: "2px solid #E89BB0", borderRadius: 11, padding: "10px 13px", fontFamily: "'Nunito', sans-serif", fontSize: 13.5, color: "#8E3B4A" }}>
                L'appel API a échoué : {erreur}. Vérifie l'URL, l'authentification et que CORS autorise cette origine.
              </div>
            )}
          </div>

          <details style={{ marginTop: 14 }}>
            <summary style={{ fontFamily: "'Patrick Hand', cursive", fontSize: 14, color: "#8a8470", cursor: "pointer" }}>Voir les données envoyées (POST JSON)</summary>
            <pre style={{ background: "#2b2b40", color: "#eef2fb", borderRadius: 12, padding: "12px 14px", fontSize: 12, overflowX: "auto", marginTop: 8 }}>{JSON.stringify(payload, null, 2)}</pre>
          </details>
        </div>
      </div>
    </div>
  );
}
