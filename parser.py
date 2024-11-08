from treeAST import *
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
    KEYS_C = 'KEYS_C'
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

errores = 0
recoveri = False
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
        global recoveri
        if self.current_token and self.current_token.type == token_type:
            recoveri = False
            self.get_next_token()
        else:
            self.error(f"Expected {token_type}, found {self.current_token.type}")
            self.recover()
            
            recoveri =True

    def error(self, message):
        global errores
        errores += 1
        print(f"Error {errores}: {message} at token {self.tokens[self.current_token_index-1].line}:{self.tokens[self.current_token_index-1].column+1}")
        self.recover()

    def recover(self):
        # Recupera el flujo hasta el próximo punto seguro (;)
        while self.current_token and self.current_token.type != TokenType.FIN_L:
            self.get_next_token()
        

    def parse(self):
        global errores
        return self.Program(), errores

    def Program(self):
        ret = NodoAST("Program")
        ret.agregar_hijo(self.Declaration())
        ret.agregar_hijo(self.ProgramPrime())
        return ret

    # Program' ::= Declaration Program' | ''
    def ProgramPrime(self):
        ret = NodoAST("ProgramP")
        if self.current_token and self.current_token.type in {TokenType.INTEGER, TokenType.BOOL_D, TokenType.CHAR_D,
                                                               TokenType.STRING_D, TokenType.VOID_D}:
            ret.agregar_hijo(self.Declaration())
            ret.agregar_hijo(self.ProgramPrime())
            return ret
        if self.current_token_index<len(self.tokens)-1:
            self.error("se esperaba tipo de var")
        return None
        


        
        # Empty production

    # Declaration ::= AUX PRAG
    def Declaration(self):
        ret = NodoAST("Declaration")
        izq = self.AUX()
        der = self.PRAG()
        if der:
            der.hijos= [izq] + der.hijos
            ret.agregar_hijo(der)
            return ret
        return ret.agregar_hijo(izq)
        

    # AUX ::= Type Identifier
    def AUX(self):
        global recoveri
        ret = NodoAST("Aux")
        ret.agregar_hijo(self.Type())
        ret.agregar_hijo(NodoAST(self.current_token.value))
        self.expect(TokenType.IDENTIFIER)
        if recoveri == True:
            return None
        return ret

    # Type ::= BaseType Type'
    def Type(self):
        ret = NodoAST("Type")
        ret.agregar_hijo(self.BaseType())
        ret.agregar_hijo(self.TypePrime())
        return ret

    # BaseType ::= IntType | BoolType | CharType | StringType | Void
    def BaseType(self):
        if self.current_token.type == TokenType.INTEGER:
            self.expect(TokenType.INTEGER)
            return NodoAST("integer")
        elif self.current_token.type == TokenType.BOOL_D:
            self.expect(TokenType.BOOL_D)
            return NodoAST("boolean")
        elif self.current_token.type == TokenType.CHAR_D:
            self.expect(TokenType.CHAR_D)
            return NodoAST("char")
        elif self.current_token.type == TokenType.STRING_D:
            self.expect(TokenType.STRING_D)
            return NodoAST("string")
        elif self.current_token.type == TokenType.VOID_D:
            self.expect(TokenType.VOID_D)
            return NodoAST("void")
        else:
            self.error("Expected base type")
            return None

    # Type' ::= [ ] Type' | ''
    def TypePrime(self):
        typ = NodoAST("typePrime")
        ret = None
        global recoveri
        if self.current_token and self.current_token.type == TokenType.OPEN_CHE:
            ret = NodoAST("[]")
            self.expect(TokenType.OPEN_CHE)
            self.expect(TokenType.CLOSE_CHE)
            if recoveri == True:
                recoveri =False
                return None
            ret.agregar_hijo(self.TypePrime())
            return NodoAST.agregar_hijo(ret)
        return None
        # Empty production

    # PRAG ::= VarDecl | Function
    # PRAG ::= VarDecl | Function | ';'
    def PRAG(self):
        global recoveri
        if self.current_token and self.current_token.type == TokenType.ASSIGN_OP:
            return NodoOperador("=",None, self.VarDecl())
        elif self.current_token and self.current_token.type == TokenType.OPEN_PAR:
            return self.Function()
        elif self.current_token and self.current_token.type == TokenType.FIN_L:  # Detectar fin de línea
            self.expect(TokenType.FIN_L)
            return None
        else:
            self.error(f"Expected =, ( or ;  found {self.current_token.type}")
            self.expect(TokenType.FIN_L)
            return None


    # VarDecl ::= = Expression ; | ;
    def VarDecl(self):
        if self.current_token and self.current_token.type == TokenType.ASSIGN_OP:
            self.expect(TokenType.ASSIGN_OP)
            ret = self.Expression()
            self.expect(TokenType.FIN_L)
            return ret
        self.expect(TokenType.FIN_L)
        return None

    # Function ::= ( Params ) { StmtList }
    def Function(self):
        global recoveri
        ret = NodoAST("funcion")
        self.expect(TokenType.OPEN_PAR)
        if recoveri == True:
            recoveri =False
            return None
        ret.agregar_hijo(self.Params())
        self.expect(TokenType.CLOSE_PAR)
        if recoveri == True:
            recoveri =False
            return None
        self.expect(TokenType.KEYS_O)
        if recoveri == True:
            recoveri =False
            return None
        ret.agregar_hijo(self.StmtList())
        self.expect(TokenType.KEYS_C)
        if recoveri == True:
            recoveri =False
            return None
        return ret

    # Params ::= Type Identifier Params' | ''
    def Params(self):
        if self.current_token and self.current_token.type in {TokenType.INTEGER, TokenType.BOOL_D, TokenType.CHAR_D,
                                                               TokenType.STRING_D, TokenType.VOID_D}:
            ret = NodoAST("Params")
            ret.agregar_hijo(self.Type())
            id = self.current_token.value
            self.expect(TokenType.IDENTIFIER)
            ret.agregar_hijo(NodoAST(id))
            ret.agregar_hijo(self.ParamsPrime())
            return ret
        return None
        # Empty production

    # Params' ::= , Params | ''
    def ParamsPrime(self):
        if self.current_token and self.current_token.type == TokenType.COMA:
            ret = NodoArray("ParamsP")
            self.expect(TokenType.COMA)
            ret.agregar_hijo(self.Params())
            return ret
        return None
        # Empty production

    # StmtList ::= Statement StmtList' | ''
    def StmtList(self):
        if self.current_token and self.current_token.type in {TokenType.IF_D, TokenType.FOR_D, TokenType.RETURN_D,
                                                              TokenType.PRINT_KEY, TokenType.IDENTIFIER, TokenType.KEYS_O,TokenType.INTEGER,
                                                              TokenType.CHAR_D, TokenType.STRING_D, TokenType.BOOL_D}:
            ret = NodoAST("StmList")
            ret.agregar_hijo(self.Statement())
            ret.agregar_hijo(self.StmtListPrime())
            return ret
        return None
        # Empty production

    # StmtList' ::= Statement StmtList' | ''
    def StmtListPrime(self):

        if self.current_token and self.current_token.type in {TokenType.IF_D, TokenType.FOR_D, TokenType.RETURN_D,
                                                              TokenType.PRINT_KEY, TokenType.IDENTIFIER, TokenType.KEYS_O, TokenType.INTEGER,
                                                              TokenType.CHAR_D, TokenType.STRING_D, TokenType.BOOL_D}:
            ret = NodoAST("StmListP")
            ret.agregar_hijo(self.Statement())
            ret.agregar_hijo(self.StmtListPrime())
            return ret
        return None
        # Empty production

    # Statement ::= VarDecl | IfStmt | ForStmt | ReturnStmt | ExprStmt | PrintStmt | { StmtList }
    def Statement(self):
        ret = NodoAST("Statement")
        if self.current_token and self.current_token.type == TokenType.IF_D:
            ret.agregar_hijo(self.IfStmt())
            return ret
        elif self.current_token and self.current_token.type == TokenType.FOR_D:
            ret.agregar_hijo(self.ForStmt())
            return ret
        elif self.current_token and self.current_token.type == TokenType.RETURN_D:
            ret.agregar_hijo(self.ReturnStmt())
            return ret
        elif self.current_token and self.current_token.type == TokenType.PRINT_KEY:
            ret.agregar_hijo(self.PrintStmt())
            return ret
        elif self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            ret.agregar_hijo(self.ExprStmt())
            return ret
        elif self.current_token and self.current_token.type == TokenType.KEYS_O:
            self.expect(TokenType.KEYS_O)
            ret.agregar_hijo(self.StmtList())
            self.expect(TokenType.KEYS_C)
            return ret
        else:
            ret.agregar_hijo(self.Declaration())
            return ret

    # IfStmt ::= if ( Expression ) Statement else Statement
    def IfStmt(self):
        global recoveri
        ret = NodoAST("if")
        self.expect(TokenType.IF_D)
        self.expect(TokenType.OPEN_PAR)
        if recoveri == True:
            recoveri = False
            return None
        ret.agregar_hijo(self.Expression())
        self.expect(TokenType.CLOSE_PAR)
        if recoveri == True:
            recoveri = False
            return None
        ret.agregar_hijo(self.Statement())
        self.expect(TokenType.ELSE_D)
        if recoveri == True:
            recoveri = False
            return None
        ret.agregar_hijo(self.Statement())
        return ret

    # ForStmt ::= for ( ExprStmt Expression ; ExprStmt ) Statement
    def ForStmt(self):
        ret = NodoAST("for")
        global recoveri
        self.expect(TokenType.FOR_D)
        self.expect(TokenType.OPEN_PAR)
        if recoveri == True:
            recoveri = False
            return None
        ret.agregar_hijo(self.ExprStmt())
        ret.agregar_hijo(self.Expression())
        self.expect(TokenType.FIN_L)
        if recoveri == True:
            recoveri = False
            return None
        ret.agregar_hijo(self.ExprStmt())
        self.expect(TokenType.CLOSE_PAR)
        if recoveri == True:
            recoveri = False
            return None
        self.expect(TokenType.KEYS_O)
        if recoveri == True:
            recoveri = False
            return None
        ret.agregar_hijo(self.Statement())
        self.expect(TokenType.KEYS_C)
        if recoveri == True:
            recoveri = False
            return None
        return ret

    # ReturnStmt ::= return Expression ;
    def ReturnStmt(self):
        ret = NodoAST("ReturnStmt")
        self.expect(TokenType.RETURN_D)
        ret.agregar_hijo(NodoAST("return"))
        ret.agregar_hijo(self.Expression())
        self.expect(TokenType.FIN_L)
        return ret

    # PrintStmt ::= print ( ExprList ) ;
    def PrintStmt(self):
        global recoveri
        printst = NodoAST("PrintStmt")
        self.expect(TokenType.PRINT_KEY)
        printst.agregar_hijo(NodoAST("print"))
        self.expect(TokenType.OPEN_PAR)
        if recoveri == True:
            self.expect(TokenType.FIN_L)
            recoveri =False
            return
        printst.agregar_hijo(self.ExprList())
        self.expect(TokenType.CLOSE_PAR)
        if recoveri == True:
            self.expect(TokenType.FIN_L)
            recoveri =False
            return
        self.expect(TokenType.FIN_L)
        if recoveri == True:
            recoveri =False
            return
        return printst
    # ExprStmt ::= Expression ;
    def ExprStmt(self):
        global recoveri
        assig = False
        exstmt = NodoAST("ExprStmt")
        
        izq = self.Expression()
        if self.current_token and self.current_token.type == TokenType.ASSIGN_OP:
            assig = True
            der = self.AssignExpr()
            asig = NodoOperador("=",izq,der)
            exstmt.agregar_hijo(asig)
        else:
            exstmt.agregar_hijo(izq)

        if assig == True:
            self.expect(TokenType.FIN_L)
            if recoveri==True:
                self.expect(TokenType.FIN_L)
        return exstmt
    
    def AssignExpr(self):
        self.expect(TokenType.ASSIGN_OP) 
        
        return self.Expr()
        
    # ExprList ::= Expression ExprList'
    def ExprList(self):
        ret = NodoAST("ExprLis")
        ret.agregar_hijo(self.Expression())
        ret.agregar_hijo(self.ExprListPrime())
        return ret

    # ExprList' ::= , ExprList | ''
    def ExprListPrime(self):
        if self.current_token and self.current_token.type == TokenType.COMA:
            ret = NodoAST("ExprListPrime")
            self.expect(TokenType.COMA)
            ret.agregar_hijo(NodoAST(","))
            ret.agregar_hijo(self.ExprList())
            return ret
        return None
        # Empty production

    # Expression ::= OrExpr
    def Expression(self):
        expre = NodoAST("Expression")
        expre.agregar_hijo(self.OrExpr())
        return expre

    # OrExpr ::= AndExpr OrExpr'
    def OrExpr(self):
        orxpr=NodoAST("orExpr")
        orxpr.agregar_hijo(self.AndExpr())
        orxpr.agregar_hijo(self.OrExprPrime())
        return orxpr

    # OrExpr' ::= || AndExpr OrExpr' | ''
    def OrExprPrime(self):
        if self.current_token and self.current_token.type == TokenType.OR_LOG:
            self.expect(TokenType.OR_LOG)
            andxpr = self.AndExpr()
            return NodoOperador("||",andxpr.agregar_hijo(self.OrExprPrime()))
        # Empty production
        return None

    # AndExpr ::= EqExpr AndExpr'
    def AndExpr(self):
        andxpr=NodoAST("Andxpr")
        andxpr.agregar_hijo(self.EqExpr())
        andxpr.agregar_hijo(self.AndExprPrime())
        return andxpr

    # AndExpr' ::= && EqExpr AndExpr' | ''
    def AndExprPrime(self):
        if self.current_token and self.current_token.type == TokenType.ANDLOG:
            self.expect(TokenType.ANDLOG)
            eqexpr = self.EqExpr()
            return NodoOperador("&&",eqexpr.agregar_hijo(self.AndExprPrime()))
        return None
        # Empty production

    # EqExpr ::= RelExpr EqExpr'
    def EqExpr(self):
        eqxpr=NodoAST("Eqxpr")
        eqxpr.agregar_hijo(self.RelExpr())
        eqxpr.agregar_hijo(self.EqExprPrime())
        return eqxpr

    # EqExpr' ::= == RelExpr EqExpr' | != RelExpr EqExpr' | ''
    def EqExprPrime(self):
        if self.current_token and self.current_token.type == TokenType.COMPARE_OP:
            self.expect(TokenType.COMPARE_OP)
            rele=self.RelExpr()
            return NodoOperador("==",rele.agregar_hijo(self.EqExprPrime()))
        elif self.current_token and self.current_token.type == TokenType.DIFF_OP:
            self.expect(TokenType.DIFF_OP)
            rele=self.RelExpr()
            return NodoOperador("!=",rele.agregar_hijo(self.EqExprPrime()))
        # Empty production
        return None

    # RelExpr ::= Expr RelExpr'
    def RelExpr(self):
        rexpr=NodoAST("RelExpr")
        izq =self.Expr()
        der = self.RelExprPrime()
        if der:
            der.hijos= [izq] + der.hijos
            rexpr.agregar_hijo(der)
            return rexpr
        
        else:
            rexpr.agregar_hijo(izq)
            return rexpr

    # RelExpr' ::= < Expr RelExpr' | > Expr RelExpr' | <= Expr RelExpr' | >= Expr RelExpr' | ''
    def RelExprPrime(self):
        oper = self.current_token.value
        if self.current_token and self.current_token.type in {TokenType.MINOR_OP, TokenType.GREAT_OP,
                                                               TokenType.MINOREQ_OP, TokenType.GREATEQ_OP}:
            
            self.expect(self.current_token.type)
            expr = self.Expr()
            expr.agregar_hijo(self.RelExprPrime())
            op = NodoOperador(oper,None,expr)
            return op
        
        return None
        # Empty production

    # Expr ::= Term Expr'
    def Expr(self):
        expr=NodoAST("Expr")
        izq = self.Term()
        der = self.ExprPrime()
        if der:
            der.hijos= [izq] + der.hijos
            expr.agregar_hijo(der)
            return expr
        
        else:
            expr.agregar_hijo(izq)
            return expr
        r

    # Expr' ::= + Term Expr' | - Term Expr' | ''
    def ExprPrime(self):
        if self.current_token and self.current_token.type == TokenType.ADD_OP:
            self.expect(TokenType.ADD_OP)
            ter = self.Term()
            ter.agregar_hijo(self.ExprPrime())
            op = NodoOperador("+",None,ter)
            return op
            
        elif self.current_token and self.current_token.type == TokenType.SUB_OP:
            self.expect(TokenType.SUB_OP)
            ter = self.Term()
            ter.agregar_hijo(self.ExprPrime())
            op = NodoOperador("-",None,ter)
            return op
        return None

    # Term ::= Unary Term'
    def Term(self):
        ter=NodoAST("Term")
        izq = self.Unary()
        der = self.TermPrime()
        if der:
            der.hijos= [izq] + der.hijos
            ter.agregar_hijo(der)
            return ter
        
        else:
            ter.agregar_hijo(izq)
            return ter

    # Term' ::= * Unary Term' | / Unary Term' | % Unary Term' | ''
    def TermPrime(self):
        if self.current_token and self.current_token.type == TokenType.MULT:
            self.expect(TokenType.MULT)
            un = self.Unary()  
            un.agregar_hijo(self.TermPrime())
            op = NodoOperador("*",None,un)
            return op
        elif self.current_token and self.current_token.type == TokenType.DIV:
            self.expect(TokenType.DIV)
            un = self.Unary()
            un.agregar_hijo(self.TermPrime())
            op = NodoOperador("/",None,un)
            return op
        elif self.current_token and self.current_token.type == TokenType.MOD:
            self.expect(TokenType.MOD)
            un =self.Unary()
            un.agregar_hijo(self.TermPrime())
            op = NodoOperador("%",None,un)
            return op
        # Empty production
        return None

    # Unary ::= ! Unary | - Unary | Factor
    def Unary(self):
        if self.current_token and self.current_token.type == TokenType.NEG_OP:
            self.expect(TokenType.NEG_OP)
            return NodoOperador('!',None,self.Unary())
        elif self.current_token and self.current_token.type == TokenType.SUB_OP:
            self.expect(TokenType.SUB_OP)
            return NodoOperador('-',None,self.Unary())
        else:
            return self.Factor()

    # Factor ::= Identifier FactorR | IntegerLiteral Factor' | CharLiteral Factor' | StringLiteral Factor' | BooleanLiteral Factor' | ( Expression ) Factor'
    def Factor(self):
        if self.current_token.type == TokenType.IDENTIFIER:
            id = self.current_token.value
            self.expect(TokenType.IDENTIFIER)
            nf = NodoFactor()
            nf.agregar_hijo(NodoAST(id))
            nf.agregar_hijo(self.FactorR())
            return nf
        elif self.current_token.type == TokenType.L_INTEGER:
            id = self.current_token.value
            self.expect(TokenType.L_INTEGER)
            nf = NodoFactor()
            nf.agregar_hijo(NodoAST(id))
            nf.agregar_hijo(self.FactorPrime())
            return nf
        elif self.current_token.type == TokenType.L_CHAR:
            id = self.current_token.value
            self.expect(TokenType.L_CHAR)
            nf = NodoFactor()
            nf.agregar_hijo(NodoAST(id))
            nf.agregar_hijo(self.FactorPrime())
            return nf
        elif self.current_token.type == TokenType.L_STRING:
            id = self.current_token.value
            self.expect(TokenType.L_STRING)
            nf = NodoFactor()
            nf.agregar_hijo(NodoAST(id))
            nf.agregar_hijo(self.FactorPrime())
            return nf
        elif self.current_token.type == TokenType.L_BOOLEAN:
            id = self.current_token.value
            self.expect(TokenType.L_BOOLEAN)
            nf = NodoFactor()
            nf.agregar_hijo(NodoAST(id))
            nf.agregar_hijo(self.FactorPrime())
            return nf
        elif self.current_token.type == TokenType.OPEN_PAR:
            nf = NodoFactor()
            self.expect(TokenType.OPEN_PAR)
            nf.agregar_hijo(self.Expression())
            self.expect(TokenType.CLOSE_PAR)
            nf.agregar_hijo(self.FactorPrime())
            return nf

    # FactorR ::= Factor' | ( ExprList ) Factor'
    def FactorR(self):
        global recoveri
        if self.current_token and self.current_token.type == TokenType.OPEN_PAR:
            facR = NodoAST("FactorR")
            self.expect(TokenType.OPEN_PAR)
            facR.agregar_hijo(self.ExprList())
            self.expect(TokenType.CLOSE_PAR)
            global recoveri
            if recoveri == True:
                recoveri =False
                return
            facR.agregar_hijo(self.FactorPrime())
            return facR
        else:
            facR = NodoAST("FactorR")
            hj=self.FactorPrime()
            if hj != None:
                facR.agregar_hijo()
                return facR
            return None

    # Factor' ::= [ Expression ] Factor' | ''
    def FactorPrime(self):
        global recoveri
        if self.current_token and self.current_token.type == TokenType.OPEN_CHE:
            factpri = NodoAST("FactorPrime")
            self.expect(TokenType.OPEN_CHE)
            factpri.agregar_hijo(self.Expression())
            self.expect(TokenType.CLOSE_CHE)
            if recoveri == True:
                recoveri =False
                return
            factpri.agregar_hijo(self.FactorPrime())
            return factpri
        return None
