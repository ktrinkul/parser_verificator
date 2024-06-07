from parser import check, parse, Node

axiom_name = {}
axiom_name[str(parse("p>(q>p)"))] = "K"
axiom_name[str(parse("(s>(p>q))>((s>p)>(s>q))"))] = "S"
axiom_name[str(parse("p>f>f>p"))] = "notE"

axiomas = [str(parse("p>(q>p)")),
           str(parse("(s>(p>q))>((s>p)>(s>q))")),
           str(parse("p>f>f>p"))]

formulas = []

def pred_beta_rule(fstr):
    for formula in formulas:
        if beta_rule(fstr, formula, "формулы"):
            return True
    for axioma in axiomas:
        if beta_rule(fstr, axioma, "аксиомы"):
            return True
    return False

def beta_rule(fstr_beta, formula_beta, from_what):
    # print(str(parse(str(parse(formula).left)).left), str(parse(formula).left))
    value_fstr = []
    fstr_copy = str(parse(fstr_beta))
    valuer(value_fstr, str(parse(fstr_copy)))
    #print(value_fstr)

    value_formula = []
    formula_copy = str(parse(formula_beta))
    alphabet = [chr(i) for i in range(97, 123)]
    for c in formula_copy:
        if c in alphabet and c != 'f' and c not in value_formula:
            value_formula.append(c)
    #print(formula_copy, value_formula)

    for old in value_formula:
        for new in value_fstr:
            if str(parse(formula_beta.replace(old, new))) == str(parse(fstr_beta)):
                print(f"формула {fstr_beta} выводима из {from_what}", end = " ")
                if from_what == "аксиомы":
                    print(axiom_name[str(parse(formula_beta))], end = " ")
                else:
                    print(formula_beta, end=" ")
                print(f"путем замены переменной {old} на выражение {new}")
                return True

    return False

def valuer(value_form, form):
    if parse(form).left is not None:
        if str(parse(form).left) not in value_form:
            value_form.append(str(parse(form).left))
        valuer(value_form, str(parse(form).left))
        #print(value_form, "left")
    if parse(form).right is not None:
        if str(parse(form).right) not in value_form:
            value_form.append(str(parse(form).right))
        valuer(value_form, str(parse(form).right))
        #print(value_form, "right")
    return

def MP_rule(fstr):
    AST = str(parse(fstr)) #B
    for formula in formulas: #ищем выводимый AB
        if AST == str(parse(formula).right):
            for axioma in axiomas: #ищем выводимую A
                if str(parse(axioma)) == str(parse(formula).left):
                    #print(formula)
                    #print(str(parse(str(parse(formula).left)).left), str(parse(formula).left))
                    #print(AST)
                    print(f"{AST} выводима из формулы {formula} и аксиомы {axiom_name[str(parse(axioma))]} "
                          f"по правилу modus ponens")
                    #formulas.append(AST)
                    return True

    for axioma in axiomas: #ищем выводимый AB
        if AST == str(parse(axioma).right):
            for formula in formulas: #ищем выводимую A
                if str(parse(formula)) == str(parse(axioma).left):
                        #print(formula)
                        #print(axioma, axiom_name[str(parse(axioma))])
                        #print(AST)
                    print(f"{AST} выводима из аксиомы {axiom_name[str(parse(axioma))]} и формулы {formula} "
                          f"по правилу modus ponens")
                    #formulas.append(AST)
                    return True

    for formula_1 in formulas: #ищем выводимый AB
        if AST == str(parse(formula_1).right):
            for formula_2 in formulas: #ищем выводимую A
                if str(parse(formula_2)) == str(parse(formula_1).left):
                        #print(formula)
                        #print(axioma, axiom_name[str(parse(axioma))])
                        #print(AST)
                    print(f"{AST} выводима из формул {formula_1} и {formula_2} "
                          f"по правилу modus ponens")
                    #formulas.append(AST)
                    return True
    return False

def main():
    while True:
        formula_str0 = input()
        if formula_str0 == "stop":
            break
        else:
            formula_str = formula_str0.replace(' ', '')
            if check(formula_str):
                ASTree_curr = str(parse(formula_str))
                if ASTree_curr in axiomas:
                    print(f"Формула {ASTree_curr} является аксиомой {axiom_name[ASTree_curr]}")
                elif ASTree_curr in formulas:
                    print(f"Формула {ASTree_curr} была выведена ранее")
                else:
                    if MP_rule(ASTree_curr):
                        formulas.append(ASTree_curr)
                        #print(formulas)
                    elif pred_beta_rule(ASTree_curr):
                        formulas.append(ASTree_curr)
                        #print(formulas)
                    else:
                        print(f"Формула {ASTree_curr} не выводима из аксиом и имеющихся формул")
                        #print(formulas)
            else:
                print("Ошибка в написании формулы")

if __name__ == "__main__":
    main()