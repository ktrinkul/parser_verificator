def check(fstr):
    if fstr[0] in ['>', ")"] or fstr[-1] in ['>', "("]:
        #print("if str[0]")
        return False

    count_brackets = 0
    for i in range(0, len(fstr)):
        if fstr[i] == '(':
            count_brackets+=1
        elif fstr[i] == ')':
            count_brackets -= 1
    if count_brackets != 0:
        #print("count_brackets")
        return False

    alphabet = [chr(i) for i in range(97, 123)]
    ALPHABET0 = [chr(i) for i in range(65, 91)]
    for i in range(1, len(fstr)):
        if fstr[i] == '(' and (fstr[i-1] in alphabet or fstr[i-1] == ')'): #p( and )(
            #print("p( and )(", i, fstr[i-1], fstr[i])
            return False
        elif fstr[i] == ')' and fstr[i-1] in ['>', '(']: #() and >)
            #print("() and >)")
            return False
        elif fstr[i].isalpha() and fstr[i] in ALPHABET0: #FGHDH
            #print("FGHDH")
            return False
        elif fstr[i].isdigit(): #24543
            #print("24543")
            return False
        elif fstr[i] in alphabet and (fstr[i-1].isalpha() or fstr[i-1] == ')'): #pp and )p
            #print("pp and )p")
            return False
        elif fstr[i] == '>' and fstr[i-1] in ["(", ">"]: #(> and  >>
            #print("(> and  >>")
            return False
    return True

class Node:
    def __init__(self, symbol):
        self.symbol = symbol
        self.left = None
        self.right = None

    def add_child(self, child):
        if self.left is None:
            self.left = child
        else: #уже есть левый ребенок
            self.right = child

    def __str__(self): #вывод
        if self.left and self.right:
            return f"({self.left} > {self.right})"
        else:
            return str(self.symbol)

def parse(fstr):
    if len(fstr) == 0:
        return None

    brackets_pos = [0] * len(fstr)
    st = []
    for i in range(len(fstr)):
        if fstr[i] == '(':
            st.append(i)
        elif fstr[i] == ')':
            if len(st) == 0:
                return None
            brackets_pos[st.pop()] = i
            #на i месте - ( / а на brackets_pos[i] - )

    tokens = []
    operators = []
    prev_is_operand = False

    i = 0
    while i < len(fstr):
        token = None

        if fstr[i] == '(':
            token = parse(fstr[i + 1:brackets_pos[i]]) #()-всю скобку внутри
            i = brackets_pos[i] #переходим на )
            if token is None:
                return None

        if fstr[i] == '>':
            if not prev_is_operand: #не параметр а )
                return None

            prev_is_operand = False
            operators.append(i)

        alphabet = [chr(i) for i in range(97, 123)]
        if fstr[i] in alphabet:
            token = Node(fstr[i])

        if token and prev_is_operand:
            return None

        if token:
            prev_is_operand = True
            tokens.append(token)

        i += 1

    if len(operators) + 1 != len(tokens):
        return None

    curr = tokens[0]
    for i in range(1, len(tokens)):
        new_root = Node("")
        new_root.add_child(curr)
        new_root.add_child(tokens[i])
        curr = new_root

    return curr

def main():
    while True:
        formula_str0 = input()
        if formula_str0 == "stop":
            break
        else:
            formula_str = formula_str0.replace(' ', '')
            if check(formula_str):
                ASTree =  parse(formula_str)
                print(ASTree)
            else:
                print("Ошибка в написании формулы")


if __name__ == "__main__":
    main()

