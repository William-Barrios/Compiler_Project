class TokenType:
    IDENTIFIER = 'IDENTIFIER'
    L_INTEGER = 'L_INTEGER'
    L_CHAR = 'L_CHAR'
    L_STRING = 'L_STRING'
    L_BOOLEAN = 'L_BOOLEAN'
    INTEGER = 'integer'
    ASSIGN_OP = 'ASSIGN_OP'
    ADD_OP = 'ADD_OP'
    OR_LOG = 'OR_LOG'
    SUB_OP = 'SUB_OP'
    MULT = 'MULT'
    DIV = 'DIV'
    PRINT_KEY = 'PRINT_KEY'
    OPEN_PAR = 'OPEN_PAR'
    OPEN_CHE = 'OPEN_CHE'
    CLOSE_PAR = 'CLOSE_PAR'
    CLOSE_CHE = 'CLOSE_CHE'
    EOP = 'EOP'
    KEYS_O = 'KEYS_O'
    KEYS_C = 'KEYS_'
    POW = 'POW'
    FIN_L = 'FIN_L'
    INCR_OP = 'INCR_OP'
    DECR_OP = 'DECR_OP'
    UNKNOWN = 'UNKNOWN'
    COMMENT = 'COMMENT'
    ARRAY_D = "ARRAY_D"
    BOOL_D = 'BOOL_D'
    CHAR_D ='CHAR_D'
    ELSE_D = 'ELSE_D'
    FOR_D = 'FOR_D'
    MOD = 'MOD'
    DECLA_OP = 'DECLA_OP'
    STRING_D = 'STRING'
    VOID_D = 'VOID'
    IF_D = 'IF'
    RETURN_D = 'RETURN'
    WHILE_D = 'WHILE'
    FUNCTION_D = 'FUNCTION'
    COMPARE_OP = 'COMPARE_OP'
    DIFF_OP = 'DIFF_OP'
    NEG_OP = 'NEG_OP'
    ANDLOG = 'ANDLOG'
    MINOR_OP = 'MINOR_OP'
    MINOREQ_OP = 'MINOREQ_OP'
    GREAT_OP = 'GREAT_OP'
    GREATEQ_OP = 'GREATEQ_OP'
    COMA = "COMA"
    FIN_L = 'FIN_L'
    
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def get_next_token(self):
        if self.current_token_index < len(self.tokens) - 1:
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None  # End of input

    def expect(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.get_next_token()
        else:
            self.error(f"Expected {token_type}, found {self.current_token.type}")

    def error(self, message):
        raise Exception(f"Parse error: {message}")

    def parse(self):
        return self.Program()

    # Program ::= Declaration Program'
    def Program(self):
        self.Declaration()
        self.ProgramPrime()

    # Program' ::= Declaration Program' | ''
    def ProgramPrime(self):
        if self.current_token and self.current_token.type in {TokenType.INTEGER, TokenType.BOOL_D, TokenType.CHAR_D,
                                                               TokenType.STRING_D, TokenType.VOID_D}:
            self.Declaration()
            self.ProgramPrime()
        # Empty production

    # Declaration ::= AUX PRAG
    def Declaration(self):
        self.AUX()
        self.PRAG()

    # AUX ::= Type Identifier
    def AUX(self):
        self.Type()
        self.expect(TokenType.IDENTIFIER)

    # Type ::= BaseType Type'
    def Type(self):
        self.BaseType()
        self.TypePrime()

    # BaseType ::= IntType | BoolType | CharType | StringType | Void
    def BaseType(self):
        if self.current_token.type == TokenType.INTEGER:
            self.expect(TokenType.INTEGER)
        elif self.current_token.type == TokenType.BOOL_D:
            self.expect(TokenType.BOOL_D)
        elif self.current_token.type == TokenType.CHAR_D:
            self.expect(TokenType.CHAR_D)
        elif self.current_token.type == TokenType.STRING_D:
            self.expect(TokenType.STRING_D)
        elif self.current_token.type == TokenType.VOID_D:
            self.expect(TokenType.VOID_D)
        else:
            self.error("Expected base type")

    # Type' ::= [ ] Type' | ''
    def TypePrime(self):
        if self.current_token and self.current_token.type == TokenType.OPEN_CHE:
            self.expect(TokenType.OPEN_CHE)
            self.expect(TokenType.CLOSE_CHE)
            self.TypePrime()
        # Empty production

    # PRAG ::= VarDecl | Function
    # PRAG ::= VarDecl | Function | ';'
    def PRAG(self):
        if self.current_token and self.current_token.type == TokenType.ASSIGN_OP:
            self.VarDecl()
        elif self.current_token and self.current_token.type == TokenType.OPEN_PAR:
            self.Function()
        elif self.current_token and self.current_token.type == TokenType.FIN_L:  # Detectar fin de línea
            self.expect(TokenType.FIN_L)
        else:
            self.error("Expected VarDecl, Function, or ';'")


    # VarDecl ::= = Expression ; | ;
    def VarDecl(self):
        if self.current_token and self.current_token.type == TokenType.ASSIGN_OP:
            self.expect(TokenType.ASSIGN_OP)
            self.Expression()
        self.expect(TokenType.FIN_L)

    # Function ::= ( Params ) { StmtList }
    def Function(self):
        self.expect(TokenType.OPEN_PAR)
        self.Params()
        self.expect(TokenType.CLOSE_PAR)
        self.expect(TokenType.KEYS_O)
        self.StmtList()
        self.expect(TokenType.KEYS_C)

    # Params ::= Type Identifier Params' | ''
    def Params(self):
        if self.current_token and self.current_token.type in {TokenType.INTEGER, TokenType.BOOL_D, TokenType.CHAR_D,
                                                               TokenType.STRING_D, TokenType.VOID_D}:
            self.Type()
            self.expect(TokenType.IDENTIFIER)
            self.ParamsPrime()
        # Empty production

    # Params' ::= , Params | ''
    def ParamsPrime(self):
        if self.current_token and self.current_token.type == TokenType.COMA:
            self.expect(TokenType.COMA)
            self.Params()
        # Empty production

    # StmtList ::= Statement StmtList' | ''
    def StmtList(self):
        if self.current_token and self.current_token.type in {TokenType.IF_D, TokenType.FOR_D, TokenType.RETURN_D,
                                                              TokenType.PRINT_KEY, TokenType.IDENTIFIER, TokenType.KEYS_O,TokenType.INTEGER,
                                                              TokenType.CHAR_D, TokenType.STRING_D, TokenType.BOOL_D}:
            self.Statement()
            self.StmtListPrime()
        # Empty production

    # StmtList' ::= Statement StmtList' | ''
    def StmtListPrime(self):
        if self.current_token and self.current_token.type in {TokenType.IF_D, TokenType.FOR_D, TokenType.RETURN_D,
                                                              TokenType.PRINT_KEY, TokenType.IDENTIFIER, TokenType.KEYS_O, TokenType.INTEGER,
                                                              TokenType.CHAR_D, TokenType.STRING_D, TokenType.BOOL_D}:
            self.Statement()
            self.StmtListPrime()
        # Empty production

    # Statement ::= VarDecl | IfStmt | ForStmt | ReturnStmt | ExprStmt | PrintStmt | { StmtList }
    def Statement(self):
            
        if self.current_token and self.current_token.type == TokenType.IF_D:
            self.IfStmt()
        elif self.current_token and self.current_token.type == TokenType.FOR_D:
            self.ForStmt()
        elif self.current_token and self.current_token.type == TokenType.RETURN_D:
            self.ReturnStmt()
        elif self.current_token and self.current_token.type == TokenType.PRINT_KEY:
            self.PrintStmt()
        elif self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            self.ExprStmt()
        elif self.current_token and self.current_token.type == TokenType.KEYS_O:
            self.expect(TokenType.KEYS_O)
            self.StmtList()
            self.expect(TokenType.KEYS_C)
        else:
            self.Declaration()

    # IfStmt ::= if ( Expression ) Statement else Statement
    def IfStmt(self):
        self.expect(TokenType.IF_D)
        self.expect(TokenType.OPEN_PAR)
        self.Expression()
        self.expect(TokenType.CLOSE_PAR)
        self.Statement()
        self.expect(TokenType.ELSE_D)
        self.Statement()

    # ForStmt ::= for ( ExprStmt Expression ; ExprStmt ) Statement
    def ForStmt(self):
        self.expect(TokenType.FOR_D)
        self.expect(TokenType.OPEN_PAR)
        self.ExprStmt()
        self.Expression()
        self.expect(TokenType.FIN_L)
        self.ExprStmt()
        self.expect(TokenType.CLOSE_PAR)
        self.Statement()

    # ReturnStmt ::= return Expression ;
    def ReturnStmt(self):
        self.expect(TokenType.RETURN_D)
        self.Expression()
        self.expect(TokenType.FIN_L)

    # PrintStmt ::= print ( ExprList ) ;
    def PrintStmt(self):
        self.expect(TokenType.PRINT_KEY)
        self.expect(TokenType.OPEN_PAR)
        self.ExprList()
        self.expect(TokenType.CLOSE_PAR)
        self.expect(TokenType.FIN_L)

    # ExprStmt ::= Expression ;
    def ExprStmt(self):
        self.Expression()
        self.expect(TokenType.FIN_L)

    # ExprList ::= Expression ExprList'
    def ExprList(self):
        self.Expression()
        self.ExprListPrime()

    # ExprList' ::= , ExprList | ''
    def ExprListPrime(self):
        if self.current_token and self.current_token.type == TokenType.COMA:
            self.expect(TokenType.COMA)
            self.ExprList()
        # Empty production

    # Expression ::= OrExpr
    def Expression(self):
        self.OrExpr()

    # OrExpr ::= AndExpr OrExpr'
    def OrExpr(self):
        self.AndExpr()
        self.OrExprPrime()

    # OrExpr' ::= || AndExpr OrExpr' | ''
    def OrExprPrime(self):
        if self.current_token and self.current_token.type == TokenType.OR_LOG:
            self.expect(TokenType.OR_LOG)
            self.AndExpr()
            self.OrExprPrime()
        # Empty production

    # AndExpr ::= EqExpr AndExpr'
    def AndExpr(self):
        self.EqExpr()
        self.AndExprPrime()

    # AndExpr' ::= && EqExpr AndExpr' | ''
    def AndExprPrime(self):
        if self.current_token and self.current_token.type == TokenType.ANDLOG:
            self.expect(TokenType.ANDLOG)
            self.EqExpr()
            self.AndExprPrime()
        # Empty production

    # EqExpr ::= RelExpr EqExpr'
    def EqExpr(self):
        self.RelExpr()
        self.EqExprPrime()

    # EqExpr' ::= == RelExpr EqExpr' | != RelExpr EqExpr' | ''
    def EqExprPrime(self):
        if self.current_token and self.current_token.type == TokenType.COMPARE_OP:
            self.expect(TokenType.COMPARE_OP)
            self.RelExpr()
            self.EqExprPrime()
        elif self.current_token and self.current_token.type == TokenType.DIFF_OP:
            self.expect(TokenType.DIFF_OP)
            self.RelExpr()
            self.EqExprPrime()
        # Empty production

    # RelExpr ::= Expr RelExpr'
    def RelExpr(self):
        self.Expr()
        self.RelExprPrime()

    # RelExpr' ::= < Expr RelExpr' | > Expr RelExpr' | <= Expr RelExpr' | >= Expr RelExpr' | ''
    def RelExprPrime(self):
        if self.current_token and self.current_token.type in {TokenType.MINOR_OP, TokenType.GREAT_OP,
                                                               TokenType.MINOREQ_OP, TokenType.GREATEQ_OP}:
            self.expect(self.current_token.type)
            self.Expr()
            self.RelExprPrime()
        # Empty production

    # Expr ::= Term Expr'
    def Expr(self):
        self.Term()
        self.ExprPrime()

    # Expr' ::= + Term Expr' | - Term Expr' | ''
    def ExprPrime(self):
        if self.current_token and self.current_token.type == TokenType.ADD_OP:
            self.expect(TokenType.ADD_OP)
            self.Term()
            self.ExprPrime()
        elif self.current_token and self.current_token.type == TokenType.SUB_OP:
            self.expect(TokenType.SUB_OP)
            self.Term()
            self.ExprPrime()
        # Empty production

    # Term ::= Unary Term'
    def Term(self):
        self.Unary()
        self.TermPrime()

    # Term' ::= * Unary Term' | / Unary Term' | % Unary Term' | ''
    def TermPrime(self):
        if self.current_token and self.current_token.type == TokenType.MULT:
            self.expect(TokenType.MULT)
            self.Unary()
            self.TermPrime()
        elif self.current_token and self.current_token.type == TokenType.DIV:
            self.expect(TokenType.DIV)
            self.Unary()
            self.TermPrime()
        elif self.current_token and self.current_token.type == TokenType.MOD:
            self.expect(TokenType.MOD)
            self.Unary()
            self.TermPrime()
        # Empty production

    # Unary ::= ! Unary | - Unary | Factor
    def Unary(self):
        if self.current_token and self.current_token.type == TokenType.NEG_OP:
            self.expect(TokenType.NEG_OP)
            self.Unary()
        elif self.current_token and self.current_token.type == TokenType.SUB_OP:
            self.expect(TokenType.SUB_OP)
            self.Unary()
        else:
            self.Factor()

    # Factor ::= Identifier FactorR | IntegerLiteral Factor' | CharLiteral Factor' | StringLiteral Factor' | BooleanLiteral Factor' | ( Expression ) Factor'
    def Factor(self):
        if self.current_token.type == TokenType.IDENTIFIER:
            self.expect(TokenType.IDENTIFIER)
            self.FactorR()
        elif self.current_token.type == TokenType.L_INTEGER:
            self.expect(TokenType.L_INTEGER)
            self.FactorPrime()
        elif self.current_token.type == TokenType.L_CHAR:
            self.expect(TokenType.L_CHAR)
            self.FactorPrime()
        elif self.current_token.type == TokenType.L_STRING:
            self.expect(TokenType.L_STRING)
            self.FactorPrime()
        elif self.current_token.type == TokenType.L_BOOLEAN:
            self.expect(TokenType.L_BOOLEAN)
            self.FactorPrime()
        elif self.current_token.type == TokenType.OPEN_PAR:
            self.expect(TokenType.OPEN_PAR)
            self.Expression()
            self.expect(TokenType.CLOSE_PAR)
            self.FactorPrime()

    # FactorR ::= Factor' | ( ExprList ) Factor'
    def FactorR(self):
        if self.current_token and self.current_token.type == TokenType.OPEN_PAR:
            self.expect(TokenType.OPEN_PAR)
            self.ExprList()
            self.expect(TokenType.CLOSE_PAR)
            self.FactorPrime()
        else:
            self.FactorPrime()

    # Factor' ::= [ Expression ] Factor' | ''
    def FactorPrime(self):
        if self.current_token and self.current_token.type == TokenType.OPEN_CHE:
            self.expect(TokenType.OPEN_CHE)
            self.Expression()
            self.expect(TokenType.CLOSE_CHE)
            self.FactorPrime()
        # Empty production
