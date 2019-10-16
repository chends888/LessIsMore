## Less (Less symbols, more programming)

Language presentation:
https://docs.google.com/presentation/d/1-h7ggldzPTUR2f3mnbVbR7cG_QsvAlcn5wy-FymNHJM/edit?usp=sharing


## EBNF

stmts = {stmt};
stmt = vardec | assig | print | funcdec | while | if ;

vardec = "int" | "bool", ident ;
assig = varname, "is", relexpr ;
print = "print", relexpr ;
funcdec = "int" | "bool", "func", ident, "(", ")", "is", stmts, "endfunc" ;
while = "while", relexpr, "do", stmts, "endloop" ;
if = "if", relexpr, "do", stmts, ["else", stmts], "endif" ;

relexpr = expr ["greater", expr | "less", expr | "equals", expr] ;
expr = expr ["+", term | "-", term | "or", term] ;
term = expr ["*", factor | "/", factor | "and", factor] ;
factor = int | ident | "true" | "false" | "+", factor | "-", factor | "(", relexpr, ")" | "input", "(", ")"

ident = {a-zA-Z_}{a-zA-Z0-9_} ;
int = {("-2⁶³" | ... | "2⁶³")} ;
