import ast
import math
import operator


class Calculadora:

    def __init__(self):
        self.operadores = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

    # ==================================================
    # EVALUAR EXPRESIÓN DE FORMA SEGURA
    # ==================================================

    def calcular(self, expresion):

        try:
            expresion = expresion.replace(",", ".")
            expresion = expresion.strip()

            arbol = ast.parse(
                expresion,
                mode="eval"
            )

            resultado = self._evaluar(arbol.body)

            if isinstance(resultado, float):

                if resultado.is_integer():
                    resultado = int(resultado)

                else:
                    resultado = round(resultado, 10)

            return resultado

        except ZeroDivisionError:
            raise ValueError(
                "No se puede dividir entre cero."
            )

        except Exception:
            raise ValueError(
                "No pude entender esa operación."
            )

    # ==================================================
    # EVALUADOR SEGURO
    # ==================================================

    def _evaluar(self, nodo):

        # Número
        if isinstance(
            nodo,
            ast.Constant
        ):

            if isinstance(
                nodo.value,
                (int, float)
            ):
                return nodo.value

            raise ValueError()

        # Operaciones matemáticas
        if isinstance(
            nodo,
            ast.BinOp
        ):

            operador = self.operadores.get(
                type(nodo.op)
            )

            if operador is None:
                raise ValueError()

            izquierda = self._evaluar(
                nodo.left
            )

            derecha = self._evaluar(
                nodo.right
            )

            return operador(
                izquierda,
                derecha
            )

        # Números negativos
        if isinstance(
            nodo,
            ast.UnaryOp
        ):

            operador = self.operadores.get(
                type(nodo.op)
            )

            if operador is None:
                raise ValueError()

            valor = self._evaluar(
                nodo.operand
            )

            return operador(valor)

        raise ValueError()

    # ==================================================
    # RAÍZ CUADRADA
    # ==================================================

    def raiz(self, numero):

        try:
            numero = float(
                str(numero).replace(",", ".")
            )

            if numero < 0:
                raise ValueError()

            resultado = math.sqrt(numero)

            return self._formatear(resultado)

        except Exception:
            raise ValueError(
                "No puedo calcular la raíz de ese número."
            )

    # ==================================================
    # FORMATEAR RESULTADO
    # ==================================================

    def _formatear(self, resultado):

        if isinstance(resultado, float):

            if resultado.is_integer():
                return int(resultado)

            return round(resultado, 10)

        return resultado