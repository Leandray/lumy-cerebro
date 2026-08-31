from ia.ia import IA


class Respuesta:

    def __init__(self):
        self.ia = IA()

    def generar(
        self,
        mensaje,
        personalidad,
        emociones,
        memoria
    ):

        mensaje_lower = mensaje.lower().strip()

        usuario = memoria.obtener_usuario()

        nombre = usuario.get("nombre")
        pronombres = usuario.get("pronombres")

        # ==================================================
        # DETECTAR EMOCIÓN DEL MENSAJE
        # ==================================================

        emocion_detectada = emociones.detectar(mensaje)

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

        # --------------------------------------------------
        # PRONOMBRES MASCULINOS
        # --------------------------------------------------

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

        # --------------------------------------------------
        # PRONOMBRES FEMENINOS
        # --------------------------------------------------

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

        # --------------------------------------------------
        # PRONOMBRES NEUTROS
        # --------------------------------------------------

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

        # --------------------------------------------------
        # FORMATO PERSONALIZADO
        # --------------------------------------------------

        if mensaje_lower.startswith(
            "mis pronombres son "
        ):

            inicio = mensaje_lower.find(
                "mis pronombres son "
            ) + len("mis pronombres son ")

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

                inicio = mensaje_lower.find(
                    "mi color favorito es"
                ) + len("mi color favorito es")

            else:

                inicio = mensaje_lower.find(
                    "mi color preferido es"
                ) + len("mi color preferido es")

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

                return f"Tus pronombres registrados son {pronombres}."

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