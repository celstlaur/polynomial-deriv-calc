def derivative(polynomial):
    """
    :string polynomial:
    :return string derivative:
    """

    # TODO: simplify ^, check for redundancies

    ops = ["+", "-", "–"]
    assume_neg = ["(", "^"]
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    split_poly = []
    split_ops = []

    power_map = dict()

    # check whether input is acceptable

    acceptable_characters = ops + assume_neg + nums + [" ", ")"]
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    var = ""
    empty_string = True
    for x in range(0, len(polynomial)):
        if polynomial[x] not in acceptable_characters and polynomial[x].lower() not in alphabet:
            raise Exception("Format unacceptable. Cannot parse character '" + polynomial[x] + "' Please see list of accepted characters.")
        elif var == "" and polynomial[x].lower() in alphabet:
            var = polynomial[x]
        elif polynomial[x].lower() in alphabet:
            if var.lower() != polynomial[x].lower():
                raise Exception("Only one variable is allowed. Expected '" + var + "', found '" + polynomial[x] + "'.")
            if polynomial[x - 1].lower() in alphabet:
                raise Exception("Format unacceptable. Please ensure that you're choosing a single letter to represent your variables.")




        # flag whether derivable characters are available
        if empty_string and polynomial[x] in (alphabet + nums):
            empty_string = False

    if empty_string:
        raise Exception("Please enter a polynomial.")

    # split polynomial by terms
    last_term = ""
    for x in range(0, len(polynomial)):

        # ignore spacing
        if polynomial[x] == " " or polynomial[x] == "(" or polynomial[x] == ")":
            continue

        # found new operator
        if polynomial[x] in ops and last_term != "" and last_term[-1] not in assume_neg:

            # if found operation, add last term to split
            # then add the operation itself

            # terms should begin with a number or a variable
            if last_term[0] in ops:
                if len(last_term) == 1:
                    raise Exception("Improperly formatted operators.")
                if last_term[1] != var and last_term[1] not in nums:
                    raise Exception("Improperly formatted operators.")
            elif last_term[0] != var and last_term[0] not in nums:
                raise Exception("Improperly formatted operators.")


            split_poly.append(last_term)
            split_ops.append(polynomial[x])
            last_term = ""
        elif last_term != "" and last_term[-1] == var and polynomial[x] not in ops + assume_neg:
            raise Exception("Ensure polynomial is formatted correctly. Cannot parse term '" + last_term + polynomial[x]
                            + "'")
        elif polynomial[x] == "^" and last_term != "" and last_term[-1] not in var:
            raise Exception("Ensure polynomial is formatted correctly. It may be missing a variable.")
        elif polynomial[x] == "^" and last_term == "":
            raise Exception("Ensure polynomial is formatted correctly. It may be missing a variable.")
        else:
            last_term += polynomial[x]

    if last_term != "":
        split_poly.append(last_term)

    if len(split_ops) == len(split_poly):

        raise Exception("Ensure polynomial is formatted correctly. Too many operators parsed.")

    #print(split_ops)
    #print(split_poly)

    deriv = ""
    for term in range(0, len(split_poly)):

        # remove parenthesis surrounding whole term
        while split_poly[term][0] == "(" and split_poly[term][-1] == ")":
            split_poly[term] = split_poly[term][1:-1]

        i = split_poly[term].find("^")

        # scenario in which no exponent
        # second case checks whether x^0 was input
        if i == -1 or split_poly[term][i + 1:] == "0":

            # constant term! goodbye
            if split_poly[term][-1] in nums:
                continue

            # power of 1 -- remove variable and add to derivative

            num = split_poly[term][:-1]

            # add missing 1
            if num == "-" or num == "":
                num += "1"

            if "0" not in power_map.keys():
                if term > 0 and split_ops[term - 1] == "-":
                    power_map["0"] = -int(num)
                else:

                    power_map["0"] = int(num)
            else:

                if term > 0 and split_ops[term - 1] == "-":
                    power_map["0"] -= int(num)
                else:
                    power_map["0"] += int(num)


        else:
            # scenario in which exponent exists
            num = split_poly[term][0:i - 1]

            # add missing 1
            if num == "-" or num == "":
                num += "1"
            """
            # check for parenthesis
            if num[0] == "(":
                num = num[1:]
            if num[-1] == ")":
                num = num[:-1]
            """

            num = int(num)

            exp = split_poly[term][i + 1:]

            """
            # check for parenthesis
            if exp[0] == "(":
                exp = exp[1:]
            if exp[-1] == ")":
                exp = exp[:-1]
                
            """

            # check for variable
            if var in exp:
                raise Exception("Polynomial terms cannot be raised to the power of a variable. Please enter a polynomial.")
            if exp == "" or exp in ops:
                raise Exception("Please ensure all exponents are associated with a numeric value.")

            exp = int(exp)

            # perform arithmetic
            num = num * exp
            exp = str(exp - 1)

            if exp not in power_map.keys():
                if term > 0 and split_ops[term - 1] == "-":
                    power_map[exp] = -int(num)
                else:
                    power_map[exp] = int(num)
            else:
                if term > 0 and split_ops[term - 1] == "-":
                    power_map[exp] -= int(num)
                else:
                    power_map[exp] += int(num)

    # create derivative string

    keys = [x for x in power_map.keys()]
    keys.sort(reverse=True)

    if not keys:
        return "0"

    if power_map[keys[0]] != 0:

        if power_map[keys[0]] != 1 or keys[0] == "0":
            deriv += str(power_map[keys[0]])

        if keys[0] != "0":
            deriv += var
            if keys[0] != "1":
                deriv = deriv + "^(" + keys[0] + ")"

    for power in keys[1:]:

        num = power_map[power]

        if num == 0:
            continue
        elif num < 0 and deriv != "":
            deriv += " - "
            num = num * -1
        elif deriv != "":
            deriv += " + "

        deriv += str(num)

        if power != "0":
            deriv += var
            if power != "1":
                deriv = deriv + "^(" + power + ")"


    # check if deriv is empty, if so, return 0
    if deriv == "":
        return "0"

    return deriv

def play_derivative():
    playing = "Y"

    print("Welcome to the polynomial derivative calculator!\nThis is a simple calculator intended to find the",
          "derivative of basic polynomials. Inputs should include a single letter a-z denoting a variable,\nintegers,",
          "and any of +/-/^ to denote addition, subtraction, and exponentiation respectively. ")
    mode = input("Would you like to run preset commands? (Y/N)")

    if mode.upper() == "Y":

        print("--")

        poly3 = "5x^ 5 + 10 x^3 + 2x + 100"
        print("The derivative of " + poly3 + " is: " + derivative(poly3))

        poly = "-2x^3 +x^-5"
        print("The derivative of " + poly + " is: " + derivative(poly))

        poly2 = "4x^3 – 2x^-2 -x"
        print("The derivative of " + poly2 + " is: " + derivative(poly2))

        poly4 = "8x^2 –5x^(-3) -3x"
        print("The derivative of " + poly4 + " is: " + derivative(poly4))


        print("--")
        cont = input("Would you like to enter your own polynomials? (Y/N)")

        if cont.upper() != "Y":
            return

    while playing.upper() == "Y":
        poly = input("Please enter a polynomial:")

        try:
            print("--\nThe derivative of " + poly + " is: " + derivative(poly))
            if "(" in poly or ")" in poly:
                print("**Please note that this calculator ignores parenthesis. Only the first term after an exponent",
                      "will be considered part of said exponent.\nIf you attempted to perform a calculation within an",
                      "exponent, your output is likely incorrect.**")
            print("--")
        except Exception as e:
            print(e)


        #playing = input("\nWould you like to derive another polynomial? (Y/N)")






if __name__ == "__main__":

    play_derivative()



    


