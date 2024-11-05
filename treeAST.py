

class ASTNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.name) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

    def generate_code(self):
        return ""  # Método general a sobreescribir en nodos específicos


# Nodo principal del programa
class ProgramNode(ASTNode):
    def __init__(self):
        super().__init__("Program")


# Nodo para declaraciones generales
class DeclarationNode(ASTNode):
    def __init__(self, name):
        super().__init__(name)


# Nodo para la declaración de variables
class VarDeclNode(ASTNode):
    def __init__(self, identifier, expression=None):
        super().__init__("VarDecl")
        self.identifier = identifier
        self.expression = expression

    def generate_code(self):
        code = f"{self.identifier} = {self.expression.generate_code() if self.expression else ''};"
        return code


# Nodo para la declaración de funciones
class FunctionNode(ASTNode):
    def __init__(self, identifier, params, body):
        super().__init__("Function")
        self.identifier = identifier
        self.params = params  # Nodo Params
        self.body = body      # Nodo StmtList

    def generate_code(self):
        params_code = self.params.generate_code()
        body_code = self.body.generate_code()
        return f"function {self.identifier}({params_code}) {{\n{body_code}\n}}"


# Nodo para parámetros de funciones
class ParamsNode(ASTNode):
    def __init__(self):
        super().__init__("Params")

    def generate_code(self):
        return ", ".join(child.generate_code() for child in self.children)


# Nodo para una lista de sentencias (cuerpo de la función o bloques)
class StmtListNode(ASTNode):
    def __init__(self):
        super().__init__("StmtList")

    def generate_code(self):
        return "\n".join(child.generate_code() for child in self.children)


# Nodo base para sentencias (Statement)
class StatementNode(ASTNode):
    def __init__(self, name):
        super().__init__(name)


# Nodo para sentencias de impresión
class PrintStmtNode(StatementNode):
    def __init__(self, expr_list):
        super().__init__("PrintStmt")
        self.expr_list = expr_list

    def generate_code(self):
        return f"print({self.expr_list.generate_code()});"


# Nodo para sentencias de retorno
class ReturnStmtNode(StatementNode):
    def __init__(self, expression):
        super().__init__("ReturnStmt")
        self.expression = expression

    def generate_code(self):
        return f"return {self.expression.generate_code()};"


# Nodo para expresiones de asignación
class AssignExprNode(ASTNode):
    def __init__(self, identifier, value):
        super().__init__("AssignExpr")
        self.identifier = identifier
        self.value = value

    def generate_code(self):
        return f"{self.identifier} = {self.value.generate_code()};"


# Nodo base para expresiones (Expression)
class ExpressionNode(ASTNode):
    def __init__(self, expr_type, value=None):
        super().__init__(expr_type)
        self.value = value

    def generate_code(self):
        return str(self.value)


# Nodo para expresiones binarias (por ejemplo, +, -, *, /)
class BinaryExprNode(ExpressionNode):
    def __init__(self, left, operator, right):
        super().__init__("BinaryExpr")
        self.left = left
        self.operator = operator
        self.right = right

    def generate_code(self):
        return f"({self.left.generate_code()} {self.operator} {self.right.generate_code()})"


# Nodo para expresiones unarias (por ejemplo, -x, !x)
class UnaryExprNode(ExpressionNode):
    def __init__(self, operator, operand):
        super().__init__("UnaryExpr")
        self.operator = operator
        self.operand = operand

    def generate_code(self):
        return f"({self.operator}{self.operand.generate_code()})"


# Nodo para literales (números, cadenas, booleanos)
class LiteralNode(ExpressionNode):
    def __init__(self, value):
        super().__init__("Literal", value)

    def generate_code(self):
        return str(self.value)


# Nodo para identificadores (variables)
class IdentifierNode(ExpressionNode):
    def __init__(self, name):
        super().__init__("Identifier")
        self.name = name

    def generate_code(self):
        return self.name


# Nodo para listas de expresiones, como en una llamada a print(x, y, z)
class ExprListNode(ASTNode):
    def __init__(self):
        super().__init__("ExprList")

    def generate_code(self):
        return ", ".join(child.generate_code() for child in self.children)


# Nodo para condiciones if
class IfStmtNode(StatementNode):
    def __init__(self, condition, true_stmt, false_stmt=None):
        super().__init__("IfStmt")
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def generate_code(self):
        code = f"if ({self.condition.generate_code()}) {{\n{self.true_stmt.generate_code()}\n}}"
        if self.false_stmt:
            code += f" else {{\n{self.false_stmt.generate_code()}\n}}"
        return code


# Nodo para bucles for
class ForStmtNode(StatementNode):
    def __init__(self, init, condition, increment, body):
        super().__init__("ForStmt")
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body

    def generate_code(self):
        return f"for ({self.init.generate_code()} {self.condition.generate_code()}; {self.increment.generate_code()}) {{\n{self.body.generate_code()}\n}}"
