from graphviz import Digraph

class NodoAST:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo  # Tipo del nodo, e.g., 'For', 'Operador', etc.
        self.valor = valor  # Valor específico del nodo, si aplica
        self.hijos = []  # Lista de hijos del nodo

    def agregar_hijo(self, nodo_hijo):
        """Agrega un nodo hijo."""
        if nodo_hijo != None: self.hijos.append(nodo_hijo)

    def graficar(self):
        dot = Digraph(comment="AST")

        def agregar_nodos_aristas(nodo, dot, parent_id=None):
            if nodo is None:  # Verificar que el nodo no sea None
                return
            
            node_id = id(nodo)
            label = f"{nodo.tipo}: {nodo.valor}" if nodo.valor else nodo.tipo
            dot.node(str(node_id), label)
            
            if parent_id:
                dot.edge(str(parent_id), str(node_id))

            for hijo in nodo.hijos:
                agregar_nodos_aristas(hijo, dot, node_id)

        agregar_nodos_aristas(self, dot)
        return dot

    def exportar_ast_grafico(self, filename="AST_Grafico", formato="png"):
        """Exporta el AST como un gráfico a un archivo de imagen."""
        dot = self.graficar()
        dot.format = formato
        dot.render(filename, view=False)  # view=True abre la imagen automáticamente
        print(f"AST exportado como {filename}.{formato}")

class NodoDeclaracion(NodoAST):
    def __init__(self, tipovar, nombre_variable):
        super().__init__("Declaracion")
        self.tipovar = tipovar
        self.nombre_variable = nombre_variable

class NodoFunctionAt(NodoAST):
    def __init__(self, izquierdo=None, derecho=None):
        super().__init__("Function")
        self.izquierdo = izquierdo
        self.derecho = derecho
        if izquierdo: self.agregar_hijo(izquierdo)
        if derecho: self.agregar_hijo(derecho)

class NodoTypeCor(NodoAST):
    def __init__(self, izquierdo=None, derecho=None):
        super().__init__("literal []")
        self.izquierdo = izquierdo
        self.derecho = derecho
        if izquierdo: self.agregar_hijo(izquierdo)
        if derecho: self.agregar_hijo(derecho)

class NodoUnary(NodoAST):
    def __init__(self, nombre, hijo=None):
        super().__init__("unary")
        self.nombre = nombre
        self.hijo = hijo
        if hijo: self.agregar_hijo(hijo)

class NodoFactor(NodoAST):
    def __init__(self):
        super().__init__("Factor")


class NodoLeaf(NodoAST):
    def __init__(self, name):
        super().__init__("")
        self.name = name

class NodoFunction(NodoAST):
    def __init__(self, nombre, izquierdo=None, derecho=None):
        super().__init__("Unary")
        self.nombre = nombre
        self.izquierdo = izquierdo
        self.derecho = derecho
        if izquierdo: self.agregar_hijo(izquierdo)
        if derecho: self.agregar_hijo(derecho)



class NodoOperador(NodoAST):
    def __init__(self, operador, izquierdo=None, derecho=None):
        super().__init__("Operador", operador)
        self.izquierdo = izquierdo
        self.derecho = derecho
        if izquierdo: self.agregar_hijo(izquierdo)
        if derecho: self.agregar_hijo(derecho)

class NodoLiteral(NodoAST):
    def __init__(self, valor, derecho=None):
        super().__init__("literal")
        self.valor = valor
        self.derecho = derecho
        if derecho: self.agregar_hijo(derecho)

class NodoArray(NodoAST):
    def __init__(self, izquierdo=None, derecho=None):
        super().__init__("Array")
        self.izquierdo = izquierdo
        self.derecho = derecho
        if izquierdo: self.agregar_hijo(izquierdo)
        if derecho: self.agregar_hijo(derecho)

class NodoExprFact(NodoAST):
    def __init__(self, izquierdo=None, derecho=None):
        super().__init__("ExprFact")
        self.izquierdo = izquierdo
        self.derecho = derecho
        if izquierdo: self.agregar_hijo(izquierdo)
        if derecho: self.agregar_hijo(derecho)

class NodoIf(NodoAST):
    def __init__(self, condicion):
        super().__init__("If")
        self.condicion = condicion
        self.cuerpo_if = []
        self.cuerpo_else = []

class NodoWhile(NodoAST):
    def __init__(self, condicion):
        super().__init__("While")
        self.condicion = condicion
        self.cuerpo = []

class NodoFor(NodoAST):
    def __init__(self, inicializacion, condicion, incremento):
        super().__init__("For")
        self.inicializacion = inicializacion
        self.condicion = condicion
        self.incremento = incremento
        self.cuerpo = []