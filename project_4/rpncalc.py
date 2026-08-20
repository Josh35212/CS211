"""
Name: Josh Gilliam
Info: CS211 Project 4, 1/3/2026
Credit: Chatgpt helped work out which parts from old calc
function (provided in the skeleton code) needed to be moved 
to the rpn_parse function when factoring.

Reverse Polish calculator.

This RPN calculator creates an expression tree from
the input.  It prints the expression in algebraic
notation and then prints the result of evaluating it.
"""

import lex
import expr
import io


def calc(text: str):
    """Read and evaluate a single line formula."""
    try:
        stack = rpn_parse(text)
        if len(stack) == 0:
            print("(No expression)")
        else:
            # For a balanced expression there will be one Expr object
            # on the stack, but if there are more we'll just print
            # each of them
            for exp in stack:
                print(f"{exp} => {exp.eval()}")
    except Exception as e: 
        print(e)

def rpn_parse(text: str) -> list[expr.Expr]:
    """Parse text in reverse Polish notation
    into a list of expressions (exactly one if
    the expression is balanced).
    Example:
        rpn_parse("5 3 + 4 * 7")
          => [ Times(Plus(IntConst(5), IntConst(3)), IntConst(4)))),
               IntConst(7) ]
    May raise:  ValueError for lexical or syntactic error in input 
    """
    tokens = lex.TokenStream(io.StringIO(text))
    stack = [ ]

    BINOPS = { lex.TokenCat.PLUS : expr.Plus,   # Table (dict) of all binary operations 
           lex.TokenCat.TIMES: expr.Times,
           lex.TokenCat.DIV: expr.Div,
           lex.TokenCat.MINUS:  expr.Minus
        }
    
    UNOPS = {                                   # Table (dict) of all unary operations 
        lex.TokenCat.NEG: expr.Neg,
        lex.TokenCat.ABS: expr.Abs,
    }

    try: 
        while tokens.has_more():
            tok = tokens.take()
            if tok.kind == lex.TokenCat.INT:
                stack.append(expr.IntConst(int(tok.value)))
            elif tok.kind in BINOPS:                    # Handle binary operations
                binop_class = BINOPS[tok.kind]
                right = stack.pop()
                left = stack.pop()
                stack.append(binop_class(left, right))
            elif tok.kind in UNOPS:                     # Handle unary operations 
                value = stack.pop()
                stack.append(UNOPS[tok.kind](value))
            elif tok.kind == lex.TokenCat.VAR:          # Handle variables
                stack.append(expr.Var(tok.value))
            elif tok.kind == lex.TokenCat.ASSIGN:
                right = stack.pop()
                left = stack.pop()
                # Reverse left and right 
                stack.append(expr.Assign(right, left))    
            else:
                raise ValueError(f"Unknown token {tok.value}")
    
    except lex.LexicalError as e:
    # Lexer choked on input; re-raise the exception with its original message
        raise
    except IndexError:
    # Stack underflow means the expression was imbalanced
        raise ValueError(f"Imbalanced RPN expression, missing operand at {tok.value}")
      
    return stack


def rpn_calc():
    txt = input("Expression (return to quit):")
    while len(txt.strip()) > 0:
        calc(txt)
        txt = input("Expression (return to quit):")
    print("Bye! Thanks for the math!")


if __name__ == "__main__":
    """RPN Calculator as main program"""
    rpn_calc()






