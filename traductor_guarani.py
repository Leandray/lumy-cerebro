
# traductor_guarani.py
# Diccionario manual: guaraní boliviano <-> español

DICCIONARIO = {
    # Formato: "palabra en español": "palabra en guaraní"
    
    "Máscara": "agüero",
    "Comprar": "agua",
    "Despiojar": "aikiu",
    "Apreciar": "akatua",
    "Derecha": "akatu",
    "Flojera": "aki",
    "duermo": "ake",
    "quebrar": "akio",
    "cabeza": "aka",
    "almohada": "akandita",
    "ardilla": "akutiguai",
    "nube": "amapitu",
    "trueno": "amariapu",
    "ajeno": "ambue",
    "moco": "ambi",
    "suspiro": "angu",
    "diablo": "aña",
    "verdad": "añete",
    "Tiempo": "ara",
    "calor": "jakuvo",
    "tormenta": "arapochi",
    "costilla": "aruka",
    "lovizna": "araivi",
    "lunes": "araviki",
    "martes": "arapá",
    "miercoles": "arapoa",
    "jueves": "arakavi",
    "viernes": "arakuera",
    "sabado": "arapi",
    "domingo": "aratú",
    "hora": "arajai",
    "minuto": "arajaimi",
    "reloj": "arajaika",
    "universo": "araipi",
    "fiesta": "arete",
    "cuello": "ayu",
    "corbata": "ayuregua",
    "leer": "amongüeta",
    "ruido": "ambu",
    "ratón": "anguya",
    "no": "ani",
    "mentira": "apu",
    "oido": "apisa",
    "maíz": "avati",
    "lluvia": "ama",
    "uno": "metei",
    "dos": "mokoi",
    "tres": "mboapi",
    "cuatro": "irundi",
    "cinco": "pandepo",
    "seis": "ova",
    "siete": "chiu",
    "ocho": "juri",
    "nueve": "chau",
    "diez": "pañandepo",
    "me llamo": "cheré",
    "miel": "ie",
    "abeja": "eiru",
    "lamer": "eére",
    "oir": "endu",
    "hablar": "ere",
    "kilo": "etakure",
    "kilometro": "etañejäata",
    "caminar": "guata",
    "vomitar": "güeé",
    "maicena": "güiraprpoasa",
    "si": "jare",
    "dolor": "jasi",
    "azul":"joviáü",
    "mono": "machi",
    "flor": "mbaepoti",
    "libro": "mbaekuatia riru",
    "mosca": "mberu",
    "oreja": "nambi",
    "tu": "nde",
    "plato": "ñae",
    "mosquito": "ñeti",
    "abrazo": "ñokuava",
    "patio": "oka",
    "techo": "ovapia",
    "mariposa": "panapana",
    "herida": "pere",
    "piel": "pire",
    "tocar": "poko",
    "ombligo": "purua",
    "pie": "pi",
    "estómago": "pia",
    "nuevo": "piau",
    "tobillo": "piñoa",
    "hermoso": "pora",
    "delgado": "poi-pireri",
    "frente": "rovai",
    "cara": "rova",
    "cuñado": "rovaya",
    "frio": "roi",
    "huevo": "rupia",
    "carne": "so-ó",
    "picante": "tai",
    "gallo": "takareo",
    "vida": "tekove",
    "alma": "tekove",
    "comida": "tembiú",
    "ojo": "tesa",
    "iglesia": "tupao",
    "centavo": "vopoparai",
    "caracol": "yatita",
    "luna": "yasi",
    "casa": "o",
    "perro": "ñaguaimba",
    "abuelo": "ramii",
    "abuela": "yari",
    "tío": "tuti",
    "tía": "yaiche",
    "hermano mayor": "rikei",
    "hermano menor": "rivi",
    "esposo": "mee",
    "esposa": "tembireko",
    "novia": "tembirekora",
    "niño": "michia",
    "hijo": "membi",
    "hija": "rayi",
    "madre": "sií",
    "madrastra": "sianga",
    "padrastro": "ruanga",
    "amor": "aiu",
}

def normalizar(texto):
    """Normaliza mayúsculas y espacios sin modificar las tildes."""
    return " ".join(texto.strip().casefold().split())


def traducir(palabra, destino="guarani"):
    palabra = normalizar(palabra)

    if destino == "guarani":
        diccionario = {
            normalizar(espanol): guarani
            for espanol, guarani in DICCIONARIO.items()
        }

    elif destino == "espanol":
        diccionario = {
            normalizar(guarani): espanol
            for espanol, guarani in DICCIONARIO.items()
            if guarani.strip()
        }

    else:
        return None

    resultado = diccionario.get(palabra)

    if not resultado or resultado == "ESCRIBE_AQUI":
        return None

    return resultado