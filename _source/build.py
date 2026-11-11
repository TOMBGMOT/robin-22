"""Génère index.html (le menu des 22 ans de Robin) à partir des données ci-dessous."""
import hashlib
import os
import html
import urllib.parse

# ---------------------------------------------------------------- photos
# Fichiers Wikimedia Commons (licences libres) : nom exact, auteur, licence
PHOTOS = {
    "halles": ("Mercado, Narbona, Francia, 2023-01-08, DD 116.jpg", "Diego Delso", "CC BY-SA 4.0"),
    "cathedrale": ("Catedral, Narbona, Francia, 2023-01-08, DD 135-137 HDR.jpg", "Diego Delso", "CC BY-SA 4.0"),
    "donjon": ("Narbonne panorama.jpg", "Benh Lieu Song", "CC BY-SA 3.0"),
    "domitia": ("Via Domitia (Narbonne).jpg", "Didier Descouens", "CC BY-SA 4.0"),
    "horreum": ("Roman Horreum, Narbonne (18731509574).jpg", "auteur indiqué sur la page du fichier", "licence libre"),
    "narbovia": ("Le musée Narbo Via.jpg", "Anthony Morel", "CC BY-SA 4.0"),
    "pont": ("Narbonne - Le pont des marchands.jpg", "Didier Descouens", "CC BY-SA 4.0"),
    "apero": ("Canal de la Robine - Narbonne.jpg", "Soj", "CC BY-SA 3.0"),
    "gruissan": ("Gruissan 12.jpg", "Jcb-caz-11", "CC BY-SA 4.0"),
    "plage": ("Mer et plage - Narbonne-Plage.JPG", "Florian Pépellin", "CC BY-SA 3.0"),
    "littorale": ("Étang de Gruissan 2010.JPG", "Wikinade", "CC BY-SA 3.0"),
    "fontfroide": ("Cloitre abbaye de Fontfroide.jpg", "Christophe Martin", "domaine public"),
    "sigean": ("File by Alexander Baranov - Жирафы (14018664602).jpg", "Alexander Baranov", "CC BY 2.0"),
    "clape": ("Massif de la Clape03.JPG", "Krzysztof Golik", "CC BY-SA 4.0"),
    "bowling": ("Sawmill Lanes Bowling Alley.JPG", "Giesige.27", "CC BY-SA 4.0"),
}

# Galerie des Grands Buffets : (fichier, auteur, légende au stylo, largeur d'origine si < 960)
GALERIE = [
    ("Fontaine de homards aux Grands Buffets.jpg", "voir la page du fichier", "la fontaine de homards. Oui, une fontaine.", None),
    ("Grands Buffets plateau de fromages.jpg", "voir la page du fichier", "111 fromages. On a dit qu’on essayait.", 600),
    ("Buffets, restaurant Les Grands Buffets.jpg", "Madroune", "la salle des entrées (juste les entrées)", None),
    ("Les grands buffets salon jean de la Fontaine.jpg", "Adrien Privat", "le salon doré. On mange là-dedans.", None),
]


def commons_urls(filename, width=960, original=False):
    name = filename.replace(" ", "_")
    h = hashlib.md5(name.encode("utf-8")).hexdigest()
    q = urllib.parse.quote(name, safe=",()'")
    if original:
        img = f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{q}"
    else:
        img = f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/{width}px-{q}"
    page = f"https://commons.wikimedia.org/wiki/File:{q}"
    return img, page


def credit(fichier, auteur, licence=""):
    return f"Photo : {auteur}{', ' + licence if licence else ''} (Wikimedia Commons)"


# ---------------------------------------------------------------- propositions
GROUPES = [
    ("Au centre, à pied", [
        ("halles", "Les Halles", "Les Halles", "à pied",
         "Le marché couvert de Narbonne. On y mange dès le matin, au comptoir, avec les habitués. L’échauffement idéal.",
         "L’intérieur des Halles de Narbonne et ses étals"),
        ("cathedrale", "La cathédrale Saint-Just", "La cathédrale Saint-Just", "à pied",
         "Commencée en 1272, jamais terminée. Les bâtisseurs sont sûrement partis déjeuner et ne sont jamais revenus. On les comprend.",
         "La nef de la cathédrale Saint-Just de Narbonne"),
        ("donjon", "Le donjon du palais des Archevêques", "Le donjon des Archevêques", "à pied",
         "On grimpe tout en haut pour la vue sur la ville. Et pour faire un peu de place.",
         "Narbonne et sa cathédrale vues depuis le donjon"),
        ("domitia", "La Via Domitia", "La Via Domitia", "à pied",
         "Un morceau de vraie voie romaine, en plein milieu de la place de l’Hôtel-de-Ville. Gratuit, rapide, et ça fait cultivé.",
         "Les pavés de la Via Domitia sur la place de l’Hôtel-de-Ville"),
        ("horreum", "L’Horreum", "L’Horreum", "à pied",
         "Des galeries romaines sous la ville. Fraîches, un peu mystérieuses, parfaites pour digérer.",
         "Une galerie souterraine de l’Horreum"),
        ("narbovia", "Le musée Narbo Via", "Narbo Via", "à pied",
         "Le grand musée romain de Narbonne, avec un mur entier de pierres sculptées. Un peu excentré, mais ça se fait à pied.",
         "Le bâtiment du musée Narbo Via"),
        ("pont", "Balade sur la Robine et le pont des Marchands", "La Robine et le pont des Marchands", "à pied",
         "Balade le long du canal, puis passage sur l’un des derniers ponts habités de France. Il y a des maisons dessus. Si, si.",
         "Le pont des Marchands au-dessus du canal de la Robine"),
        ("apero", "L’apéro en terrasse", "L’apéro en terrasse", "à pied",
         "Au soleil, au bord de la Robine. Activité techniquement facultative, moralement obligatoire.",
         "Le canal de la Robine en plein centre de Narbonne"),
    ]),
    ("Juste à côté du buffet", [
        ("bowling", "Le Private Bowling Pub", "Le Private Bowling Pub", "voisin du buffet",
         "Dans le même complexe que les Grands Buffets&nbsp;: un pub avec bowling, billard, cocktails et parfois des concerts. Le plan parfait pour digérer. Attention, après 111 fromages, la boule va te paraître légère.",
         "Des pistes de bowling"),
    ]),
    ("Un bus et c’est réglé", [
        ("gruissan", "Gruissan", "Gruissan", "bus 8",
         "Un village construit en rond autour d’une vieille tour, des étangs, et la plage des chalets sur pilotis. Pratique pour se perdre deux fois.",
         "Le village de Gruissan"),
        ("plage", "Narbonne-Plage", "Narbonne-Plage", "bus 8",
         "La mer, sur la même ligne de bus. Au printemps, l’eau sera fraîche. Ce sera ton problème, pas le mien.",
         "La plage de Narbonne-Plage"),
        ("littorale", "La Littorale à vélo", "La Littorale à vélo", "vélo",
         "L’itinéraire qui relie Narbonne à la mer en passant par Gruissan. Pour mériter le buffet avant, ou pour l’éliminer après.",
         "L’étang de Gruissan"),
    ]),
    ("L’expédition (sans voiture, faut le vouloir)", [
        ("fontfroide", "L’abbaye de Fontfroide", "L’abbaye de Fontfroide", "bus + marche",
         "La plus belle abbaye du coin, en pleine garrigue, avec une roseraie d’environ 2&nbsp;500 rosiers. Les moines y ont vécu des siècles sans buffet à volonté&nbsp;: respect. Bus 407 jusqu’à Saint-Julien puis 30 minutes de marche, ou un taxi.",
         "Le cloître de l’abbaye de Fontfroide"),
        ("sigean", "La Réserve africaine de Sigean", "La Réserve africaine de Sigean", "voiture",
         "Des lions, des girafes et des rhinocéros, dans l’Aude. On en parle&nbsp;?",
         "Des girafes à la Réserve africaine de Sigean"),
        ("clape", "Une dégustation dans le massif de la Clape", "Une dégustation dans la Clape", "voiture",
         "Le massif juste à côté de Narbonne est couvert de vignes. On goûte, on recrache. En théorie.",
         "Le massif de la Clape"),
    ]),
]

CERCLE = ('<svg class="cercle" viewBox="0 0 200 60" preserveAspectRatio="none" aria-hidden="true">'
          '<path vector-effect="non-scaling-stroke" d="M16 9 C60 2 150 2 189 8 C198 22 197 40 188 52 '
          'C140 59 60 59 12 53 C3 40 4 21 15 8 C32 4 52 3 72 4"/></svg>')


def item(cle, data_nom, nom, prix, desc, alt):
    fichier, auteur, licence = PHOTOS[cle]
    thumb, _ = commons_urls(fichier)
    titre = html.escape(credit(fichier, auteur, licence))
    return f'''      <li><button class="plat" type="button" aria-pressed="false" data-nom="{html.escape(data_nom)}">
        <span class="vignette" data-lieu="{html.escape(nom)}"><img src="{thumb}" alt="{html.escape(alt)}" title="{titre}" loading="lazy" decoding="async" width="960" height="480"></span>
        <span class="ligne"><span class="nom">{nom}{CERCLE}</span><span class="coche" aria-hidden="true">✓</span><span class="points" aria-hidden="true"></span><span class="prix">{prix}</span></span>
        <span class="desc">{desc}</span>
      </button></li>'''


def chariot():
    out = []
    for titre, items in GROUPES:
        out.append(f'    <h3>{titre}</h3>\n    <ul class="chariot-groupe">')
        out.extend(item(*it) for it in items)
        out.append('    </ul>\n')
    return "\n".join(out)


def galerie():
    out = []
    for fichier, auteur, legende, largeur in GALERIE:
        src, _ = commons_urls(fichier, original=bool(largeur))
        titre = html.escape(credit(fichier, auteur))
        out.append(f'''      <figure class="galerie-photo">
        <span class="vignette" data-lieu="Les Grands Buffets"><img src="{src}" alt="{html.escape(legende)}" title="{titre}" loading="lazy" decoding="async"></span>
        <figcaption class="bic">{legende}</figcaption>
      </figure>''')
    return "\n".join(out)


def credits_readme():
    lignes = ["## Crédits photos", "", "Toutes les photos viennent de Wikimedia Commons (licences libres).", ""]
    for fichier, auteur, _, _ in GALERIE:
        _, page = commons_urls(fichier)
        lignes.append(f"- Les Grands Buffets : {auteur} — {page}")
    for titre, items in GROUPES:
        for cle, _, nom, *_ in items:
            fichier, auteur, licence = PHOTOS[cle]
            _, page = commons_urls(fichier)
            lignes.append(f"- {nom} : {auteur}, {licence} — {page}")
    return "\n".join(lignes) + "\n"


ICI = os.path.dirname(os.path.abspath(__file__))
template = open(os.path.join(ICI, "template.html"), encoding="utf-8").read()
page = template.replace("<!--CHARIOT-->", chariot()).replace("<!--GALERIE-->", galerie())
open(os.path.join(ICI, "..", "index.html"), "w", encoding="utf-8").write(page)
open(os.path.join(ICI, "CREDITS.md"), "w", encoding="utf-8").write(credits_readme())
print("index.html généré :", len(page), "caractères")
