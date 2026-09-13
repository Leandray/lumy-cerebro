from ia.ia import IA
from datetime import datetime, timedelta
import re


class Respuesta:

   def __init__(self, notificar=None):

    self.notificar = notificar

    self.ia = IA()

    # ======================================================
    # TEMPORIZADOR
    # ======================================================

    try:
        from herramientas.temporizador import Temporizador

        self.temporizador = Temporizador(
            al_terminar=self.notificar_temporizador
        )

    except Exception as error:

        print(
            "[LUMY] ⚠️ No se pudo inicializar "
            "el temporizador:"
        )

        print(error)

        self.temporizador = None
        
    # ==========================================================
# NOTIFICAR CUANDO TERMINA EL TEMPORIZADOR
# ==========================================================

def notificar_temporizador(self):

    print(
        "[LUMY] 🔔 El temporizador ha terminado."
    )

    if self.notificar:

        self.notificar({
            "tipo": "temporizador",
            "titulo": "Temporizador terminado",
            "mensaje": "¡Tu temporizador ha terminado!",
            "icono": "⏱️"
        })
    # ==========================================================
    # DETECTAR ACCIONES DE MÚSICA
    # ==========================================================

    def detectar_accion_musica(self, mensaje):

        texto = mensaje.lower().strip()

        # ======================================================
        # ABRIR YOUTUBE MUSIC
        # ======================================================

        patrones_youtube = [
            "abre youtube music",
            "abrir youtube music",
            "abre youtube",
            "abrir youtube"
        ]

        for patron in patrones_youtube:

            if texto.startswith(patron):

                return {
                    "tipo": "musica_abrir",
                    "datos": {
                        "servicio": "youtube"
                    }
                }

        # ======================================================
        # ABRIR SPOTIFY
        # ======================================================

        patrones_spotify = [
            "abre spotify",
            "abrir spotify"
        ]

        for patron in patrones_spotify:

            if texto.startswith(patron):

                return {
                    "tipo": "musica_abrir",
                    "datos": {
                        "servicio": "spotify"
                    }
                }

        # ======================================================
        # REPRODUCIR UNA CANCIÓN
        # ======================================================

        patrones_reproducir = [
            "reproduce ",
            "reproducir ",
            "pon ",
            "poner ",
            "quiero escuchar ",
            "quiero oír ",
            "quiero oir ",
            "escucha ",
            "escuchar "
        ]

        for patron in patrones_reproducir:

            if texto.startswith(patron):

                consulta = mensaje[len(patron):].strip()

                if not consulta:
                    return None

                # ----------------------------------------------
                # QUITAR SERVICIO DEL FINAL
                # ----------------------------------------------

                sufijos = [
                    " en youtube music",
                    " en youtube",
                    " en spotify"
                ]

                for sufijo in sufijos:

                    if consulta.lower().endswith(sufijo):

                        consulta = consulta[
                            : -len(sufijo)
                        ].strip()

                        break

                if not consulta:
                    return None

                return {
                    "tipo": "musica_reproducir",
                    "datos": {
                        "consulta": consulta
                    }
                }

        # ======================================================
        # BUSCAR MÚSICA
        # ======================================================

        patrones_buscar = [
            "busca música ",
            "buscar música ",
            "busca musica ",
            "buscar musica ",
            "busca la canción ",
            "buscar la canción ",
            "busca la cancion ",
            "buscar la cancion "
        ]

        for patron in patrones_buscar:

            if texto.startswith(patron):

                consulta = mensaje[len(patron):].strip()

                if not consulta:
                    return None

                return {
                    "tipo": "musica_buscar",
                    "datos": {
                        "consulta": consulta
                    }
                }

        # ======================================================
        # PLAYLIST
        # ======================================================

        patrones_playlist = [
            "abre mi playlist ",
            "abrir mi playlist ",
            "abre la playlist ",
            "abrir la playlist ",
            "reproduce mi playlist ",
            "reproducir mi playlist "
        ]

        for patron in patrones_playlist:

            if texto.startswith(patron):

                playlist = mensaje[len(patron):].strip()

                if not playlist:
                    return None

                return {
                    "tipo": "musica_playlist",
                    "datos": {
                        "consulta": playlist
                    }
                }

        return None

    # ==========================================================
    # DETECTAR ACCIONES DE CALENDARIO
    # ==========================================================

    def detectar_accion_calendario(self, mensaje):

        texto = mensaje.lower().strip()

        # ------------------------------------------------------
        # CREAR EVENTO
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # DETECTAR HORA
        # ------------------------------------------------------

        coincidencia_hora = re.search(
            r'(\d{1,2})(?::(\d{2}))?\s*(?:de la\s*)?(am|pm)?',
            texto
        )

        if not coincidencia_hora:
            return None

        hora = int(
            coincidencia_hora.group(1)
        )

        minutos = int(
            coincidencia_hora.group(2) or 0
        )

        periodo = coincidencia_hora.group(3)

        if periodo == "pm" and hora < 12:
            hora += 12

        if periodo == "am" and hora == 12:
            hora = 0

        # ------------------------------------------------------
        # DETECTAR FECHA
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # DURACIÓN POR DEFECTO
        # ------------------------------------------------------

        fin = inicio + timedelta(hours=1)

        # ------------------------------------------------------
        # OBTENER TÍTULO
        # ------------------------------------------------------

        titulo = "Evento"

        if (
            "reunión" in texto
            or "reunion" in texto
        ):

            titulo = "Reunión"

        elif (
            "cumpleaños" in texto
            or "cumpleanos" in texto
        ):

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

    # ==========================================================
    # DETECTAR CALCULADORA
    # ==========================================================

    def detectar_calculadora(self, mensaje):

        texto = mensaje.lower().strip()

        patrones = [
            "cuánto es ",
            "cuanto es ",
            "calcula ",
            "calcular ",
            "resuelve ",
            "resolver "
        ]

        for patron in patrones:

            if texto.startswith(patron):

                expresion = mensaje[
                    len(patron):
                ].strip()

                if expresion:

                    return {
                        "tipo": "calcular",
                        "datos": {
                            "expresion": expresion
                        }
                    }

        return None

    # ==========================================================
    # DETECTAR TEMPORIZADOR
    # ==========================================================

    def detectar_temporizador(self, mensaje):

        texto = mensaje.lower().strip()

        patrones = [
            "pon un temporizador de ",
            "poner un temporizador de ",
            "crea un temporizador de ",
            "crear un temporizador de ",
            "temporizador de ",
            "temporizador "
        ]

        for patron in patrones:

            if texto.startswith(patron):

                tiempo_texto = mensaje[
                    len(patron):
                ].strip()

                if not tiempo_texto:
                    return None

                coincidencia = re.search(
                    r'(\d+(?:\.\d+)?)\s*(segundos?|s|minutos?|m|horas?|h)',
                    tiempo_texto.lower()
                )

                if not coincidencia:
                    return None

                cantidad = float(
                    coincidencia.group(1)
                )

                unidad = coincidencia.group(2)

                if unidad.startswith("s"):

                    segundos = cantidad

                elif unidad.startswith("m"):

                    segundos = cantidad * 60

                elif unidad.startswith("h"):

                    segundos = cantidad * 3600

                else:

                    return None

                return {
                    "tipo": "temporizador",
                    "datos": {
                        "segundos": segundos
                    }
                }

        return None

    # ==========================================================
    # GENERAR RESPUESTA
    # ==========================================================

    def generar(
        self,
        mensaje,
        personalidad,
        emociones,
        memoria
    ):

        mensaje_lower = mensaje.lower().strip()

        # ======================================================
        # CALCULADORA
        # ======================================================

        accion_calculadora = self.detectar_calculadora(
            mensaje
        )

        if accion_calculadora:

            expresion = accion_calculadora[
                "datos"
            ][
                "expresion"
            ]

            try:

                # Importamos aquí para evitar problemas
                # si Calculadora cambia de ubicación.

                from herramientas.calculadora import Calculadora

                calculadora = Calculadora()

                resultado = calculadora.calcular(
                    expresion
                )

                return {
                    "respuesta": (
                        f"El resultado es {resultado}."
                    ),
                    "accion": accion_calculadora,
                    "requiere_confirmacion": False
                }

            except Exception as error:

                print(
                    "[LUMY] Error en calculadora:"
                )

                print(error)

                return {
                    "respuesta": (
                        f"No pude calcular "
                        f"'{expresion}'."
                    ),
                    "accion": None,
                    "requiere_confirmacion": False
                }

        # ======================================================
        # TEMPORIZADOR
        # ======================================================

        accion_temporizador = self.detectar_temporizador(
            mensaje
        )

        if accion_temporizador:

            segundos = accion_temporizador[
                "datos"
            ][
                "segundos"
            ]

            return {
                "respuesta": (
                    f"De acuerdo. Pondré un temporizador "
                    f"de {segundos:g} segundos."
                ),
                "accion": accion_temporizador,
                "requiere_confirmacion": False
            }

        # ======================================================
        # MÚSICA
        # ======================================================

        accion_musica = self.detectar_accion_musica(
            mensaje
        )

        if accion_musica:

            tipo = accion_musica["tipo"]

            # --------------------------------------------------
            # REPRODUCIR
            # --------------------------------------------------

            if tipo == "musica_reproducir":

                consulta = accion_musica[
                    "datos"
                ][
                    "consulta"
                ]

                return {
                    "respuesta": (
                        f"Claro. Voy a reproducir "
                        f"'{consulta}'."
                    ),
                    "accion": accion_musica,
                    "requiere_confirmacion": False
                }

            # --------------------------------------------------
            # ABRIR SERVICIO
            # --------------------------------------------------

            if tipo == "musica_abrir":

                servicio = accion_musica[
                    "datos"
                ][
                    "servicio"
                ]

                if servicio == "youtube":

                    return {
                        "respuesta": (
                            "Voy a abrir YouTube."
                        ),
                        "accion": accion_musica,
                        "requiere_confirmacion": False
                    }

                if servicio == "spotify":

                    return {
                        "respuesta": (
                            "Voy a abrir Spotify."
                        ),
                        "accion": accion_musica,
                        "requiere_confirmacion": False
                    }

            # --------------------------------------------------
            # BUSCAR
            # --------------------------------------------------

            if tipo == "musica_buscar":

                consulta = accion_musica[
                    "datos"
                ][
                    "consulta"
                ]

                return {
                    "respuesta": (
                        f"Voy a buscar "
                        f"'{consulta}'."
                    ),
                    "accion": accion_musica,
                    "requiere_confirmacion": False
                }

            # --------------------------------------------------
            # PLAYLIST
            # --------------------------------------------------

            if tipo == "musica_playlist":

                consulta = accion_musica[
                    "datos"
                ][
                    "consulta"
                ]

                return {
                    "respuesta": (
                        f"Voy a abrir la playlist "
                        f"'{consulta}'."
                    ),
                    "accion": accion_musica,
                    "requiere_confirmacion": False
                }

        # ======================================================
        # CALENDARIO
        # ======================================================

        accion_calendario = self.detectar_accion_calendario(
            mensaje
        )

        if accion_calendario:

            inicio = datetime.fromisoformat(
                accion_calendario[
                    "datos"
                ][
                    "inicio"
                ]
            )

            fecha_texto = inicio.strftime(
                "%d/%m/%Y"
            )

            hora_texto = inicio.strftime(
                "%H:%M"
            )

            titulo = accion_calendario[
                "datos"
            ][
                "titulo"
            ]

            return {
                "respuesta": (
                    f"¿Quieres que cree el evento "
                    f"'{titulo}' el {fecha_texto} "
                    f"a las {hora_texto}?"
                ),
                "accion": accion_calendario,
                "requiere_confirmacion": True
            }

        # ======================================================
        # OBTENER USUARIO
        # ======================================================

        usuario = memoria.obtener_usuario()

        nombre = usuario.get(
            "nombre"
        )

        pronombres = usuario.get(
            "pronombres"
        )

        # ======================================================
        # DETECTAR EMOCIÓN
        # ======================================================

        emocion_detectada = emociones.detectar(
            mensaje
        )

        emocion_actual = emociones.emocion_actual()

        print(
            f"[LUMY] Emoción detectada: "
            f"{emocion_detectada}"
        )

        print(
            f"[LUMY] Emoción actual: "
            f"{emocion_actual}"
        )

        print(
            f"[LUMY] Estado: "
            f"{emociones.obtener_estado()}"
        )

        # ======================================================
        # IDENTIDAD — CAMBIAR NOMBRE
        # ======================================================

        patrones_nombre = [
            "me llamo ",
            "mi nombre es ",
            "quiero que me llames ",
            "quiero que me digas "
        ]

        for patron in patrones_nombre:

            if mensaje_lower.startswith(patron):

                nuevo_nombre = mensaje[
                    len(patron):
                ].strip()

                if nuevo_nombre:

                    memoria.establecer_usuario(
                        nombre=nuevo_nombre
                    )

                    emociones.modificar(
                        "felicidad",
                        5
                    )

                    return {
                        "respuesta": (
                            f"Entendido. "
                            f"A partir de ahora te llamaré "
                            f"{nuevo_nombre}."
                        ),
                        "accion": None,
                        "requiere_confirmacion": False
                    }

        # ======================================================
        # IDENTIDAD — PRONOMBRES MASCULINOS
        # ======================================================

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

            return {
                "respuesta": (
                    "Entendido. Usaré pronombres "
                    "masculinos contigo a partir de ahora."
                ),
                "accion": None,
                "requiere_confirmacion": False
            }

        # ======================================================
        # IDENTIDAD — PRONOMBRES FEMENINOS
        # ======================================================

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

            return {
                "respuesta": (
                    "Entendido. Usaré pronombres "
                    "femeninos contigo a partir de ahora."
                ),
                "accion": None,
                "requiere_confirmacion": False
            }

        # ======================================================
        # IDENTIDAD — PRONOMBRES NEUTROS
        # ======================================================

        patrones_neutros = [
            "mis pronombres son neutros",
            "mis pronombres son neutro",
            "quiero que uses pronombres neutros conmigo",
            "quiero que uses pronombres neutro conmigo"
        ]

        if any(
            patron in mensaje_lower
            for patron in patrones_neutros
        ):

            memoria.establecer_usuario(
                pronombres="neutros"
            )

            return {
                "respuesta": (
                    "Entendido. Usaré lenguaje neutro "
                    "contigo a partir de ahora."
                ),
                "accion": None,
                "requiere_confirmacion": False
            }

        # ======================================================
        # GUARDAR COLOR FAVORITO
        # ======================================================

        if (
            "mi color favorito es" in mensaje_lower
            or "mi color preferido es" in mensaje_lower
        ):

            if "mi color favorito es" in mensaje_lower:

                inicio = mensaje_lower.find(
                    "mi color favorito es"
                ) + len(
                    "mi color favorito es"
                )

            else:

                inicio = mensaje_lower.find(
                    "mi color preferido es"
                ) + len(
                    "mi color preferido es"
                )

            color = mensaje[
                inicio:
            ].strip()

            if color:

                memoria.guardar_preferencia(
                    "color_favorito",
                    color
                )

                emociones.modificar(
                    "felicidad",
                    5
                )

                return {
                    "respuesta": (
                        f"Entendido. "
                        f"Tu color favorito es {color}. "
                        f"Lo recordaré."
                    ),
                    "accion": None,
                    "requiere_confirmacion": False
                }

        # ======================================================
        # PREGUNTAR COLOR FAVORITO
        # ======================================================

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

                return {
                    "respuesta": (
                        f"Tu color favorito es {color}. "
                        f"Lo recuerdo."
                    ),
                    "accion": None,
                    "requiere_confirmacion": False
                }

            return {
                "respuesta": (
                    "Todavía no sé cuál es tu color favorito. "
                    "Puedes decírmelo diciendo: "
                    "'Mi color favorito es...'"
                ),
                "accion": None,
                "requiere_confirmacion": False
            }

        # ======================================================
        # GUARDAR RECUERDO — PROYECTO LUMY
        # ======================================================

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

            return {
                "respuesta": (
                    "Sí. Recordaré que estás "
                    "construyendo a LUMY."
                ),
                "accion": None,
                "requiere_confirmacion": False
            }

        # ======================================================
        # GUARDAR GUSTOS / PREFERENCIAS
        # ======================================================

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

                contenido = mensaje[
                    len(patron):
                ].strip()

                if contenido:

                    recuerdo = (
                        f"Al usuario le gusta "
                        f"{contenido}."
                    )

                    memoria.guardar_recuerdo(
                        recuerdo
                    )

                    emociones.modificar(
                        "felicidad",
                        5
                    )

                    return {
                        "respuesta": (
                            f"Lo tendré en cuenta. "
                            f"Recuerdo que te gusta "
                            f"{contenido}."
                        ),
                        "accion": None,
                        "requiere_confirmacion": False
                    }

        # ======================================================
        # GUARDAR COSAS QUE NO LE GUSTAN
        # ======================================================

        patrones_no_gusta = [
            "no me gusta ",
            "no me gustan ",
            "odio "
        ]

        for patron in patrones_no_gusta:

            if mensaje_lower.startswith(patron):

                contenido = mensaje[
                    len(patron):
                ].strip()

                if contenido:

                    recuerdo = (
                        f"Al usuario no le gusta "
                        f"{contenido}."
                    )

                    memoria.guardar_recuerdo(
                        recuerdo
                    )

                    return {
                        "respuesta": (
                            f"Entendido. "
                            f"Recordaré que no te gusta "
                            f"{contenido}."
                        ),
                        "accion": None,
                        "requiere_confirmacion": False
                    }

        # ======================================================
        # PREGUNTAR RECUERDOS
        # ======================================================

        if (
            "qué recuerdas de mí" in mensaje_lower
            or "que recuerdas de mi" in mensaje_lower
            or "qué recuerdas de mi" in mensaje_lower
            or "que recuerdas de mí" in mensaje_lower
        ):

            recuerdos = memoria.obtener_recuerdos()

            if recuerdos:

                lista = "\n".join(
                    f"• {recuerdo}"
                    for recuerdo in recuerdos
                )

                return {
                    "respuesta": (
                        "Esto es lo que recuerdo de ti:\n\n"
                        f"{lista}"
                    ),
                    "accion": None,
                    "requiere_confirmacion": False
                }

            return {
                "respuesta": (
                    "Todavía no tengo recuerdos "
                    "permanentes sobre ti."
                ),
                "accion": None,
                "requiere_confirmacion": False
            }

        # ======================================================
        # PREGUNTAR NOMBRE
        # ======================================================

        if (
            "cómo me llamo" in mensaje_lower
            or "como me llamo" in mensaje_lower
            or "cuál es mi nombre" in mensaje_lower
            or "cual es mi nombre" in mensaje_lower
        ):

            if nombre:

                return {
                    "respuesta": (
                        f"Te llamas {nombre}."
                    ),
                    "accion": None,
                    "requiere_confirmacion": False
                }

            return {
                "respuesta": (
                    "Todavía no sé cómo te llamas. "
                    "Puedes decírmelo diciendo: "
                    "'Me llamo...'"
                ),
                "accion": None,
                "requiere_confirmacion": False
            }

        # ======================================================
        # PREGUNTAR PRONOMBRES
        # ======================================================

        if (
            "qué pronombres uso" in mensaje_lower
            or "que pronombres uso" in mensaje_lower
            or "cuáles son mis pronombres" in mensaje_lower
            or "cuales son mis pronombres" in mensaje_lower
        ):

            if pronombres:

                return {
                    "respuesta": (
                        f"Usas {pronombres}."
                    ),
                    "accion": None,
                    "requiere_confirmacion": False
                }

            return {
                "respuesta": (
                    "Todavía no me has indicado "
                    "tus pronombres."
                ),
                "accion": None,
                "requiere_confirmacion": False
            }

        # ======================================================
        # AGRADECIMIENTO
        # ======================================================

        if "gracias" in mensaje_lower:

            emociones.modificar(
                "felicidad",
                5
            )

            return {
                "respuesta": (
                    "De nada. "
                    "Me alegra poder ayudarte."
                ),
                "accion": None,
                "requiere_confirmacion": False
            }

        # ======================================================
        # SALUDOS
        # ======================================================

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

                return {
                    "respuesta": (
                        f"Hola, {nombre}. "
                        "Qué bueno escucharte. "
                        "¿Qué hacemos hoy?"
                    ),
                    "accion": None,
                    "requiere_confirmacion": False
                }

            return {
                "respuesta": (
                    "Hola. "
                    "Qué bueno escucharte. "
                    "¿Qué hacemos hoy?"
                ),
                "accion": None,
                "requiere_confirmacion": False
            }

        # ======================================================
        # DESPEDIDAS
        # ======================================================

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

            return {
                "respuesta": (
                    "Hasta luego. "
                    "Estaré aquí cuando vuelvas."
                ),
                "accion": None,
                "requiere_confirmacion": False
            }

        # ======================================================
        # IA REAL
        # ======================================================

        respuesta = self.ia.generar(
            mensaje,
            personalidad,
            emociones,
            memoria
        )

        return {
            "respuesta": respuesta,
            "accion": None,
            "requiere_confirmacion": False
        }