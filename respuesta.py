from ia.ia import IA

from datetime import datetime, timedelta

from herramientas.calculadora import Calculadora

import re


class Respuesta:

    def __init__(self):
        self.ia = IA()
        self.calculadora = Calculadora()

    # ==================================================
    # DETECTAR ACCIONES DE SPOTIFY
    # ==================================================

    def detectar_accion_spotify(self, mensaje):

        texto = mensaje.lower().strip()

        # ----------------------------------------------
        # ABRIR SPOTIFY
        # ----------------------------------------------

        patrones_abrir = [
            "abre spotify",
            "abrir spotify",
            "abre mi spotify",
            "abrir mi spotify",
            "quiero abrir spotify",
            "pon spotify",
            "abrir la aplicación de spotify"
        ]

        if any(patron in texto for patron in patrones_abrir):
            return {
                "tipo": "spotify_abrir",
                "datos": {
                    "url": "https://open.spotify.com/"
                }
            }

        # ----------------------------------------------
        # BUSCAR EN SPOTIFY
        # ----------------------------------------------

        patrones_buscar = [
            "busca ",
            "buscar ",
            "búscame ",
            "buscame ",
            "encuentra ",
            "quiero buscar "
        ]

        for patron in patrones_buscar:

            if texto.startswith(patron):

                consulta = mensaje[len(patron):].strip()

                if consulta:

                    # Quitar "en spotify" del final
                    consulta = re.sub(
                        r"\s+en spotify\s*$",
                        "",
                        consulta,
                        flags=re.IGNORECASE
                    ).strip()

                    if consulta:

                        return {
                            "tipo": "spotify_buscar",
                            "datos": {
                                "consulta": consulta
                            }
                        }

        # ----------------------------------------------
        # BUSCAR MÚSICA
        # ----------------------------------------------

        patrones_musica = [
            "busca música de ",
            "busca musica de ",
            "buscar música de ",
            "buscar musica de ",
            "quiero escuchar ",
            "quiero oír ",
            "quiero oir ",
            "pon música de ",
            "pon musica de ",
            "reproduce ",
            "reproducir "
        ]

        for patron in patrones_musica:

            if texto.startswith(patron):

                consulta = mensaje[len(patron):].strip()

                if consulta:

                    consulta = re.sub(
                        r"\s+en spotify\s*$",
                        "",
                        consulta,
                        flags=re.IGNORECASE
                    ).strip()

                    if consulta:

                        return {
                            "tipo": "spotify_buscar",
                            "datos": {
                                "consulta": consulta
                            }
                        }

        # ----------------------------------------------
        # PLAYLIST
        # ----------------------------------------------

        patrones_playlist = [
            "busca una playlist de ",
            "busca playlist de ",
            "buscar una playlist de ",
            "buscar playlist de ",
            "quiero una playlist de ",
            "pon una playlist de ",
            "reproduce una playlist de "
        ]

        for patron in patrones_playlist:

            if texto.startswith(patron):

                consulta = mensaje[len(patron):].strip()

                if consulta:

                    consulta = re.sub(
                        r"\s+en spotify\s*$",
                        "",
                        consulta,
                        flags=re.IGNORECASE
                    ).strip()

                    if consulta:

                        return {
                            "tipo": "spotify_playlist",
                            "datos": {
                                "consulta": consulta
                            }
                        }

        return None

    # ==================================================
    # DETECTAR ACCIONES DE CALENDARIO
    # ==================================================

    def detectar_accion_calendario(self, mensaje):

        texto = mensaje.lower().strip()

        # ----------------------------------------------
        # CREAR EVENTO
        # ----------------------------------------------

        patrones_crear = [
            "agenda ",
            "agéndame ",
            "agendame ",
            "crea un evento",
            "crear un evento",
            "añade un evento",
            "anota en mi calendario",
            "anota ",
            "pon en mi calendario"
        ]

        es_creacion = any(
            patron in texto
            for patron in patrones_crear
        )

        if not es_creacion:
            return None

        # ----------------------------------------------
        # DETECTAR HORA
        # ----------------------------------------------

        coincidencia_hora = re.search(
            r'(\d{1,2})(?::(\d{2}))?\s*(?:de la\s*)?(am|pm)?',
            texto
        )

        if not coincidencia_hora:
            return None

        hora = int(coincidencia_hora.group(1))

        minutos = int(
            coincidencia_hora.group(2) or 0
        )

        periodo = coincidencia_hora.group(3)

        if periodo == "pm" and hora < 12:
            hora += 12

        if periodo == "am" and hora == 12:
            hora = 0

        # ----------------------------------------------
        # DETECTAR FECHA
        # ----------------------------------------------

        ahora = datetime.now()

        if "mañana" in texto:
            fecha = ahora + timedelta(days=1)

        elif "hoy" in texto:
            fecha = ahora

        else:
            fecha = ahora + timedelta(days=1)

        inicio = fecha.replace(
            hour=hora,
            minute=minutos,
            second=0,
            microsecond=0
        )

        # ----------------------------------------------
        # DURACIÓN POR DEFECTO: 1 HORA
        # ----------------------------------------------

        fin = inicio + timedelta(hours=1)

        # ----------------------------------------------
        # OBTENER TÍTULO
        # ----------------------------------------------

        titulo = "Evento"

        if "reunión" in texto or "reunion" in texto:
            titulo = "Reunión"

        elif "cumpleaños" in texto or "cumpleanos" in texto:
            titulo = "Cumpleaños"

        elif "cita" in texto:
            titulo = "Cita"

        elif "clase" in texto:
            titulo = "Clase"

        return {
            "tipo": "crear_evento",
            "datos": {
                "titulo": titulo,
                "inicio": inicio.isoformat(),
                "fin": fin.isoformat(),
                "descripcion": ""
            }
        }

        # ==================================================
    # DETECTAR CALCULADORA
    # ==================================================

    def detectar_calculadora(self, mensaje):

        texto = mensaje.lower().strip()

        # ----------------------------------------------
        # QUITAR PALABRAS INNECESARIAS
        # ----------------------------------------------

        expresion = texto

        prefijos = [
            "calcula ",
            "calcular ",
            "cuánto es ",
            "cuanto es ",
            "cuánto da ",
            "cuanto da ",
            "resuelve ",
            "resuelve la operación ",
            "resuelve la operacion ",
        ]

        for prefijo in prefijos:

            if expresion.startswith(prefijo):

                expresion = expresion[
                    len(prefijo):
                ].strip()

                break

        # ----------------------------------------------
        # RAÍZ CUADRADA
        # ----------------------------------------------

        patrones_raiz = [
            "raíz cuadrada de ",
            "raiz cuadrada de ",
            "raíz de ",
            "raiz de ",
        ]

        for patron in patrones_raiz:

            if expresion.startswith(patron):

                numero = expresion[
                    len(patron):
                ].strip()

                if numero:

                    try:
                        resultado = self.calculadora.raiz(
                            numero
                        )

                        return {
                            "tipo": "calculadora",
                            "datos": {
                                "operacion": f"√{numero}",
                                "resultado": resultado
                            }
                        }

                    except ValueError:
                        return {
                            "tipo": "calculadora_error",
                            "datos": {}
                        }

        # ----------------------------------------------
        # CONVERTIR OPERACIONES ESCRITAS
        # ----------------------------------------------

        expresion = expresion.replace(
            " por ",
            "*"
        )

        expresion = expresion.replace(
            " multiplicado por ",
            "*"
        )

        expresion = expresion.replace(
            " dividido entre ",
            "/"
        )

        expresion = expresion.replace(
            " dividido por ",
            "/"
        )

        # ----------------------------------------------
        # PORCENTAJE
        # ----------------------------------------------

        coincidencia = re.fullmatch(
            r"(\d+(?:[.,]\d+)?)\s*%\s*de\s*(\d+(?:[.,]\d+)?)",
            expresion
        )

        if coincidencia:

            porcentaje = float(
                coincidencia.group(1).replace(",", ".")
            )

            numero = float(
                coincidencia.group(2).replace(",", ".")
            )

            resultado = (
                porcentaje / 100
            ) * numero

            return {
                "tipo": "calculadora",
                "datos": {
                    "operacion": expresion,
                    "resultado": self.calculadora._formatear(
                        resultado
                    )
                }
            }

        # ----------------------------------------------
        # OPERACIÓN MATEMÁTICA
        # ----------------------------------------------

        if not re.fullmatch(
            r"[0-9+\-*/().%\s]+",
            expresion
        ):
            return None

        # Tiene que contener al menos
        # un operador matemático

        if not re.search(
            r"[+\-*/%]",
            expresion
        ):
            return None

        try:

            resultado = self.calculadora.calcular(
                expresion
            )

            return {
                "tipo": "calculadora",
                "datos": {
                    "operacion": expresion,
                    "resultado": resultado
                }
            }

        except ValueError:

            return {
                "tipo": "calculadora_error",
                "datos": {}
            }

    # ==================================================
    # GENERAR RESPUESTA
    # ==================================================

    def generar(
        self,
        mensaje,
        personalidad,
        emociones,
        memoria
    ):

        mensaje_lower = mensaje.lower().strip()

                # ==================================================
        # CALCULADORA
        # ==================================================

        accion_calculadora = self.detectar_calculadora(
            mensaje
        )

        if accion_calculadora:

            tipo = accion_calculadora["tipo"]

            if tipo == "calculadora":

                operacion = accion_calculadora[
                    "datos"
                ]["operacion"]

                resultado = accion_calculadora[
                    "datos"
                ]["resultado"]

                return {
                    "respuesta": (
                        f"El resultado de {operacion} "
                        f"es {resultado}."
                    ),
                    "accion": accion_calculadora,
                    "requiere_confirmacion": False
                }

            if tipo == "calculadora_error":

                return {
                    "respuesta": (
                        "No pude realizar esa operación. "
                        "Revisa los números e inténtalo nuevamente."
                    ),
                    "accion": accion_calculadora,
                    "requiere_confirmacion": False
                }

        # ==================================================
        # SPOTIFY
        # ==================================================

        accion_spotify = self.detectar_accion_spotify(
            mensaje
        )

        if accion_spotify:

            tipo = accion_spotify["tipo"]

            if tipo == "spotify_abrir":

                return {
                    "respuesta": "Claro. Abriendo Spotify.",
                    "accion": accion_spotify,
                    "requiere_confirmacion": False
                }

            if tipo == "spotify_buscar":

                consulta = accion_spotify["datos"]["consulta"]

                return {
                    "respuesta": (
                        f"Claro. Voy a buscar "
                        f"'{consulta}' en Spotify."
                    ),
                    "accion": accion_spotify,
                    "requiere_confirmacion": False
                }

            if tipo == "spotify_playlist":

                consulta = accion_spotify["datos"]["consulta"]

                return {
                    "respuesta": (
                        f"Claro. Voy a buscar "
                        f"una playlist de '{consulta}' en Spotify."
                    ),
                    "accion": accion_spotify,
                    "requiere_confirmacion": False
                }

        # ==================================================
        # CALENDARIO
        # ==================================================

        accion_calendario = self.detectar_accion_calendario(
            mensaje
        )

        if accion_calendario:

            inicio = datetime.fromisoformat(
                accion_calendario["datos"]["inicio"]
            )

            fecha_texto = inicio.strftime("%d/%m/%Y")
            hora_texto = inicio.strftime("%H:%M")
            titulo = accion_calendario["datos"]["titulo"]

            return {
                "respuesta": (
                    f"¿Quieres que cree el evento "
                    f"'{titulo}' el {fecha_texto} "
                    f"a las {hora_texto}?"
                ),
                "accion": accion_calendario,
                "requiere_confirmacion": True
            }

        # ==================================================
        # OBTENER USUARIO
        # ==================================================

        usuario = memoria.obtener_usuario()

        nombre = usuario.get("nombre")
        pronombres = usuario.get("pronombres")

        # ==================================================
        # DETECTAR EMOCIÓN DEL MENSAJE
        # ==================================================

        emocion_detectada = emociones.detectar(
            mensaje
        )

        # ==================================================
        # OBTENER EMOCIÓN ACTUAL
        # ==================================================

        emocion_actual = emociones.emocion_actual()

        print(
            f"[LUMY] Emoción detectada: {emocion_detectada}"
        )

        print(
            f"[LUMY] Emoción actual: {emocion_actual}"
        )

        print(
            f"[LUMY] Estado: {emociones.obtener_estado()}"
        )

        # ==================================================
        # IDENTIDAD — CAMBIAR NOMBRE
        # ==================================================

        patrones_nombre = [
            "me llamo ",
            "mi nombre es ",
            "quiero que me llames ",
            "quiero que me digas "
        ]

        for patron in patrones_nombre:

            if mensaje_lower.startswith(patron):

                nuevo_nombre = mensaje[len(patron):].strip()

                if nuevo_nombre:

                    memoria.establecer_usuario(
                        nombre=nuevo_nombre
                    )

                    emociones.modificar(
                        "felicidad",
                        5
                    )

                    return (
                        f"Entendido. A partir de ahora te llamaré "
                        f"{nuevo_nombre}."
                    )

        # ==================================================
        # IDENTIDAD — CAMBIAR PRONOMBRES
        # ==================================================

        patrones_masculinos = [
            "mis pronombres son masculinos",
            "mis pronombres son masculino",
            "mis pronombres son él",
            "mis pronombres son el",
            "quiero que uses pronombres masculinos conmigo",
            "quiero que uses pronombres masculino conmigo",
            "quiero que uses pronombres él conmigo",
            "quiero que uses pronombres el conmigo"
        ]

        if any(
            patron in mensaje_lower
            for patron in patrones_masculinos
        ):

            memoria.establecer_usuario(
                pronombres="masculinos"
            )

            return (
                "Entendido. Usaré pronombres masculinos "
                "contigo a partir de ahora."
            )

        patrones_femeninos = [
            "mis pronombres son femeninos",
            "mis pronombres son femenino",
            "mis pronombres son ella",
            "quiero que uses pronombres femeninos conmigo",
            "quiero que uses pronombres femenino conmigo",
            "quiero que uses pronombres ella conmigo"
        ]

        if any(
            patron in mensaje_lower
            for patron in patrones_femeninos
        ):

            memoria.establecer_usuario(
                pronombres="femeninos"
            )

            return (
                "Entendido. Usaré pronombres femeninos "
                "contigo a partir de ahora."
            )

        patrones_neutros = [
            "mis pronombres son neutros",
            "mis pronombres son neutro",
            "mis pronombres son elle",
            "quiero que uses pronombres neutros conmigo",
            "quiero que uses pronombres neutro conmigo",
            "quiero que uses pronombres elle conmigo"
        ]

        if any(
            patron in mensaje_lower
            for patron in patrones_neutros
        ):

            memoria.establecer_usuario(
                pronombres="neutros"
            )

            return (
                "Entendido. Usaré pronombres neutros "
                "contigo a partir de ahora."
            )

        if mensaje_lower.startswith(
            "mis pronombres son "
        ):

            inicio = (
                mensaje_lower.find(
                    "mis pronombres son "
                )
                + len("mis pronombres son ")
            )

            nuevos_pronombres = mensaje[inicio:].strip()

            if nuevos_pronombres:

                memoria.establecer_usuario(
                    pronombres=nuevos_pronombres
                )

                return (
                    f"Entendido. Tus pronombres son "
                    f"{nuevos_pronombres}. "
                    "Los tendré en cuenta."
                )

        # ==================================================
        # GUARDAR PREFERENCIA: COLOR FAVORITO
        # ==================================================

        if (
            "mi color favorito es" in mensaje_lower
            or "mi color preferido es" in mensaje_lower
        ):

            if "mi color favorito es" in mensaje_lower:

                inicio = (
                    mensaje_lower.find(
                        "mi color favorito es"
                    )
                    + len("mi color favorito es")
                )

            else:

                inicio = (
                    mensaje_lower.find(
                        "mi color preferido es"
                    )
                    + len("mi color preferido es")
                )

            color = mensaje[inicio:].strip()

            if color:

                memoria.guardar_preferencia(
                    "color_favorito",
                    color
                )

                emociones.modificar(
                    "felicidad",
                    5
                )

                return (
                    f"¡Entendido! "
                    f"Tu color favorito es {color}. "
                    "Lo recordaré."
                )

        # ==================================================
        # PREGUNTAR COLOR FAVORITO
        # ==================================================

        if (
            "cuál es mi color favorito" in mensaje_lower
            or "cual es mi color favorito" in mensaje_lower
            or "qué color me gusta" in mensaje_lower
            or "que color me gusta" in mensaje_lower
        ):

            color = memoria.obtener_preferencia(
                "color_favorito"
            )

            if color:

                return (
                    f"Tu color favorito es {color}. "
                    "Lo recuerdo."
                )

            return (
                "Todavía no sé cuál es tu color favorito. "
                "Puedes decírmelo diciendo: "
                "'Mi color favorito es...'"
            )

        # ==================================================
        # GUARDAR RECUERDO: PROYECTO LUMY
        # ==================================================

        if (
            "estoy construyendo a lumy" in mensaje_lower
            or "estoy construyendo lumy" in mensaje_lower
        ):

            recuerdo = (
                "El usuario está construyendo a LUMY."
            )

            memoria.guardar_recuerdo(
                recuerdo
            )

            emociones.modificar(
                "felicidad",
                5
            )

            return (
                "Sí. Recordaré que estás "
                "construyendo a LUMY."
            )

        # ==================================================
        # GUARDAR GUSTOS / PREFERENCIAS
        # ==================================================

        patrones_gusto = [
            "me gusta ",
            "me gustan ",
            "me encanta ",
            "me encantan ",
            "mi hobby es ",
            "mi pasatiempo es ",
            "me interesa "
        ]

        for patron in patrones_gusto:

            if mensaje_lower.startswith(patron):

                contenido = mensaje[len(patron):].strip()

                if contenido:

                    recuerdo = (
                        f"Al usuario le gusta {contenido}."
                    )

                    memoria.guardar_recuerdo(
                        recuerdo
                    )

                    emociones.modificar(
                        "felicidad",
                        5
                    )

                    return (
                        f"Lo tendré en cuenta. "
                        f"Recuerdo que te gusta {contenido}."
                    )

        # ==================================================
        # GUARDAR COSAS QUE NO LE GUSTAN
        # ==================================================

        patrones_no_gusta = [
            "no me gusta ",
            "no me gustan ",
            "odio "
        ]

        for patron in patrones_no_gusta:

            if mensaje_lower.startswith(patron):

                contenido = mensaje[len(patron):].strip()

                if contenido:

                    recuerdo = (
                        f"Al usuario no le gusta {contenido}."
                    )

                    memoria.guardar_recuerdo(
                        recuerdo
                    )

                    return (
                        f"Entendido. "
                        f"Recordaré que no te gusta {contenido}."
                    )

        # ==================================================
        # PREGUNTAR POR RECUERDOS
        # ==================================================

        if (
            "qué recuerdas de mí" in mensaje_lower
            or "que recuerdas de mi" in mensaje_lower
            or "qué recuerdas sobre mí" in mensaje_lower
            or "que recuerdas sobre mi" in mensaje_lower
        ):

            recuerdos = memoria.obtener_recuerdos()

            if recuerdos:

                lista = "\n".join(
                    f"• {recuerdo}"
                    for recuerdo in recuerdos
                )

                return (
                    "Esto es lo que recuerdo de ti:\n\n"
                    f"{lista}"
                )

            return (
                "Todavía no tengo recuerdos permanentes "
                "sobre ti."
            )

        # ==================================================
        # PREGUNTAR NOMBRE
        # ==================================================

        if (
            "cómo me llamo" in mensaje_lower
            or "como me llamo" in mensaje_lower
            or "cuál es mi nombre" in mensaje_lower
            or "cual es mi nombre" in mensaje_lower
        ):

            if nombre:

                return f"Te llamas {nombre}."

            return (
                "Todavía no sé cómo te llamas. "
                "Puedes decírmelo diciendo: "
                "'Me llamo...'"
            )

        # ==================================================
        # PREGUNTAR PRONOMBRES
        # ==================================================

        if (
            "qué pronombres uso" in mensaje_lower
            or "que pronombres uso" in mensaje_lower
            or "cuáles son mis pronombres" in mensaje_lower
            or "cuales son mis pronombres" in mensaje_lower
        ):

            if pronombres:

                return (
                    f"Tus pronombres registrados son "
                    f"{pronombres}."
                )

            return (
                "Todavía no me has indicado tus pronombres."
            )

        # ==================================================
        # AGRADECIMIENTO
        # ==================================================

        if "gracias" in mensaje_lower:

            emociones.modificar(
                "felicidad",
                5
            )

            return (
                "De nada. "
                "Me alegra poder ayudarte."
            )

        # ==================================================
        # SALUDOS
        # ==================================================

        saludos = [
            "hola",
            "holi",
            "hey",
            "buenas",
            "buenos días",
            "buenas tardes",
            "buenas noches"
        ]

        if any(
            mensaje_lower == saludo
            or mensaje_lower.startswith(
                saludo + " "
            )
            for saludo in saludos
        ):

            if nombre:

                return (
                    f"Hola, {nombre}. "
                    "Qué bueno escucharte. ¿Qué hacemos hoy?"
                )

            return (
                "Hola. "
                "Qué bueno escucharte. ¿Qué hacemos hoy?"
            )

        # ==================================================
        # DESPEDIDAS
        # ==================================================

        despedidas = [
            "adiós",
            "adios",
            "hasta luego",
            "nos vemos",
            "me voy",
            "chao",
            "chau"
        ]

        if any(
            despedida in mensaje_lower
            for despedida in despedidas
        ):

            return (
                "Hasta luego. "
                "Estaré aquí cuando vuelvas."
            )

        # ==================================================
        # IA REAL
        # ==================================================

        respuesta = self.ia.generar(
            mensaje,
            personalidad,
            emociones,
            memoria
        )

        return respuesta