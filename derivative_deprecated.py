def derivative(polynomial):
    """
    :string polynomial:
    :return string derivative:
    """
    # questions: NO INBUILT FUNCTIONS? including len, int, etc?
    # currently i'm considering only the first term after an exponent to be part of the exponent
    # do i need to evaluate within parenthesis?

    ops = ["+", "-", "–"]
    assume_neg = ["(", "^"]
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    split_poly = []
    split_ops = []

    # check whether input is acceptable

    acceptable_characters = ops + assume_neg + nums + [" ", ")"]
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    var = ""
    empty_string = True
    for x in range(0, len(polynomial)):
        if polynomial[x] not in acceptable_characters and polynomial[x].lower() not in alphabet:
            raise Exception("Format unacceptable. Cannot parse character '" + polynomial[
                x] + "' Please see list of accepted characters.")
        elif var == "" and polynomial[x].lower() in alphabet:
            var = polynomial[x]
        elif polynomial[x].lower() in alphabet and var.lower() != polynomial[x].lower():
            raise Exception("Only one variable is allowed. Expected '" + var + "', found '" + polynomial[x] + "'.")

        # flag whether derivable characters are available
        if empty_string and polynomial[x] in (alphabet + nums):
            empty_string = False

    if empty_string:
        raise Exception("Please enter a polynomial.")

    # split polynomial by terms
    last_term = ""
    for x in range(0, len(polynomial)):

        # ignore spacing
        if polynomial[x] == " ":
            continue

        # found new operator
        if polynomial[x] in ops and last_term != "" and last_term[-1] not in assume_neg:
            # if found operation, add last term to split
            # then add the operation itself
            split_poly.append(last_term)
            split_ops.append(polynomial[x])
            last_term = ""
        else:
            last_term += polynomial[x]

    split_poly.append(last_term)

    deriv = ""
    # print(split_ops)
    # print(split_poly)

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

            # add operation
            if deriv != "" and term > 0:
                deriv = deriv + " " + split_ops[term - 1] + " "

            to_add = split_poly[term][:-1]
            if to_add == "":
                deriv += "1"
            else:
                deriv += to_add

        else:
            # scenario in which exponent exists
            num = split_poly[term][0:i - 1]

            # add missing 1
            if num == "-" or num == "":
                num += "1"

            # check for parenthesis
            if num[0] == "(":
                num = num[1:]
            if num[-1] == ")":
                num = num[:-1]

            """
            Better code here would be:
            if num[0] == "(":
                num = num[1:-1]

            But I can't guarantee that parenthesis are matching, so I'm just going to remove them. Bleh.
            //TODO// Parse for matching parenthesis only at the beginning and raise an exception if they're
            encountered? 
            """

            num = int(num)

            var = split_poly[term][i - 1]

            exp = split_poly[term][i + 1:]

            # check for parenthesis
            if exp[0] == "(":
                exp = exp[1:]
            if exp[-1] == ")":
                exp = exp[:-1]

            exp = int(exp)

            # perform arithmetic
            num = num * exp
            exp = exp - 1

            # add operation
            if deriv != "" and term > 0:
                deriv = deriv + " " + split_ops[term - 1] + " "

            # add to derivative
            if exp == 1:
                deriv = deriv + str(num) + var
            elif exp == 0:
                deriv = deriv + str(num)
            else:
                deriv = deriv + str(num) + var + "^(" + str(exp) + ")"

    # check if deriv is empty, if so, return 0
    if deriv == "":
        return "0"

    return deriv


def play_derivative():
    playing = "Y"

    print("Welcome to the derivative calculator!")
    while playing.upper() == "Y":
        poly = input("Please enter a polynomial:")
        print("The derivative of " + poly + " is: " + derivative(poly))

        playing = input("\nWould you like to derive another polynomial? (Y/N)")


if __name__ == "__main__":
    # play_derivative()


    poly = "-2x^3 +x^-5"
    print("The derivative of " + poly + " is: " + derivative(poly))

    # –
    poly2 = "4x^3 - 2x^-2 -x"
    print("The derivative of " + poly2 + " is: " + derivative(poly2))

    poly3 = "x^ 5 + 10 x^3 + 2x + 100"
    print("The derivative of " + poly3 + " is: " + derivative(poly3))

    poly4 = "8x^2 –5x^(-3) -3x"
    print("The derivative of " + poly4 + " is: " + derivative(poly4))

    poly5 = "2"
    print("The derivative of " + poly5 + " is: " + derivative(poly5))

    poly6 = "-10x^0"
    print("The derivative of " + poly6 + " is: " + derivative(poly6))



