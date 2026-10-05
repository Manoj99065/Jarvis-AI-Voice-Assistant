def calculate(expression):
    # simple safety: only allow numbers, operators, parentheses, spaces
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        return "I can only compute simple arithmetic expressions."
    try:
        result = eval(expression)
        return f"The answer is {result}"
    except:
        return "Sorry, I couldn't calculate that."