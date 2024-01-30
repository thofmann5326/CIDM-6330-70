# Defining Function for Numbers to Roman with some input number
def number_roman(num):
    # Mapping numbers to there Roman counterparts
    num_to_Roman = {
        1000: 'M',
        900: 'CM',
        500: 'D',
        400: 'CD',
        100: 'C',
        90: 'XC',
        50: 'L',
        40: 'XL',
        10: 'X',
        9: 'IX',
        5: 'V',
        4: 'IV',
        1: 'I'
    }

    # Creating a string variable called result and setting it to be blank
    result = ""

    # Creating a for loop to cycle though the Number mappings and adding the symbol to the result
    for value, symbol in sorted(num_to_Roman .items(), key=lambda x: x[0], reverse=True):
        while num >= value:
            result += symbol
            num -= value
    # Returning the result string for the function
    return result

# Defining Function for Romans to Numbers with some input Roman Charectors


def Roman_number(roman):
    # Mapping roman charectors to there numerical counterparts
    roman_to_num = {
        'I': 1,
        'IV': 4,
        'V': 5,
        'IX': 9,
        'X': 10,
        'XL': 40,
        'L': 50,
        'XC': 90,
        'C': 100,
        'CD': 400,
        'D': 500,
        'CM': 900,
        'M': 1000
    }

    # Creating a intiger variable called result and setting it 0
    result = 0

    # Creating a interger vaiable called I to store the loop count
    i = 0

    # creating a loop to process the input charector back to number
    while i < len(roman):
        if i + 1 < len(roman) and roman[i:i+2] in roman_to_num:
            result += roman_to_num[roman[i:i+2]]
            i += 2
        else:
            result += roman_to_num[roman[i]]
            i += 1

    # Returning the result string for the function
    return result


# Ask the user for numerical input
user_number = int(input("Enter a number: "))

# Convert the numerical input to Roman numeral form
convert_roman = number_roman(user_number)

# Print the result of the conversion
print(f"The Roman charectors of {user_number} is: {convert_roman}")

# Ask the user for input of Roman number
user_roman = input("Enter a Roman Number: ")

# Convert the Roman numeral to numerical form
Convert_number = Roman_number(user_roman)

# Print the result of the conversion
print(f"The numerical conversion of {user_roman} is: {Convert_number}")
