from ddgs import DDGS


class BusquedaWeb:

    def __init__(self):
        self.max_resultados = 5

    # ==========================================
    # BUSCAR EN INTERNET
    # ==========================================

    def buscar(self, consulta):
        try:
            print("==========================================")
            print("[LUMY WEB] Iniciando búsqueda...")
            print(f"[LUMY WEB] Consulta: {consulta}")

            resultados = DDGS().text(
                consulta,
                region="wt-wt",
                safesearch="moderate",
                max_results=self.max_resultados
            )

            if not resultados:
                print("[LUMY WEB] No se encontraron resultados.")
                return []

            resultados_limpios = []

            for resultado in resultados:

                titulo = resultado.get(
                    "title",
                    ""
                )

                url = resultado.get(
                    "href",
                    ""
                )

                descripcion = resultado.get(
                    "body",
                    ""
                )

                if not titulo and not descripcion:
                    continue

                resultados_limpios.append({
                    "titulo": titulo,
                    "url": url,
                    "descripcion": descripcion
                })

            print(
                f"[LUMY WEB] Resultados encontrados: "
                f"{len(resultados_limpios)}"
            )

            for i, resultado in enumerate(
                resultados_limpios,
                start=1
            ):
                print(
                    f"[LUMY WEB] {i}. "
                    f"{resultado['titulo']}"
                )

            print("==========================================")

            return resultados_limpios

        except Exception as error:

            print("==========================================")
            print("[LUMY WEB] ERROR EN BÚSQUEDA:")
            print(error)
            print("==========================================")

            return []

    # ==========================================
    # FORMATEAR RESULTADOS
    # ==========================================

    def formatear_resultados(self, resultados):

        if not resultados:
            return (
                "No se encontraron resultados "
                "relevantes en Internet."
            )

        texto = []

        for i, resultado in enumerate(
            resultados,
            start=1
        ):

            texto.append(
                f"""
RESULTADO {i}

Título:
{resultado['titulo']}

URL:
{resultado['url']}

Información:
{resultado['descripcion']}
"""
            )

        return "\n".join(texto)


# ==========================================
# PRUEBA DIRECTA
# ==========================================

if __name__ == "__main__":

    print("==========================================")
    print("        PRUEBA DE BÚSQUEDA WEB LUMY")
    print("==========================================")

    buscador = BusquedaWeb()

    resultados = buscador.buscar(
        "¿Qué es la robótica?"
    )

    print("\nRESULTADOS:\n")

    print(
        buscador.formatear_resultados(
            resultados
        )
    )