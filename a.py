import os
import time
import lookup as lu

lookup_table = lu.lookup

# Blending code
def blending(col1, col2, alpha):
    new_red = lookup_table[col1[0]][col2[0]][alpha]
    new_green = lookup_table[col1[1]][col2[1]][alpha]
    new_blue = lookup_table[col1[2]][col2[2]][alpha]
    if "Kill" in [new_red, new_green, new_blue]: return "Kill"
    else: return new_red, new_green, new_blue

# Convert hex code to int to store in json
def tuple_to_int(tuple):
    return tuple[0] * 256 ** 2 + tuple[1] * 256 + tuple[2]

print("Initializing lists...")
standard_colors = [
    (255,255,255),(248,248,248),(234,234,234),(221,221,221),(192,192,192),(178,178,178),(150,150,150),(128,128,128),(119,119,119),(95,95,95),(77,77,77),(51,51,51),(41,41,41),(28,28,28),(17,17,17),(8,8,8),(0,0,0),(0,51,102),(51,102,153),(51,102,204),(0,51,153),(0,0,153),(0,0,204),(0,0,102),(0,102,102),(0,102,153),(0,153,204),(0,102,204),(0,51,204),(0,0,255),(51,51,255),(51,51,153),(0,128,128),(0,153,153),(51,204,204),(0,204,255),(0,153,255),(0,102,255),(51,102,255),(51,51,204),(102,102,153),(51,153,102),(0,204,153),(0,255,204),(0,255,255),(51,204,255),(51,153,255),(102,153,255),(102,102,255),(102,0,255),(102,0,204),(51,153,51),(0,204,102),(0,255,153),(102,255,204),(102,255,255),(102,204,255),(153,204,255),(153,153,255),(153,102,255),(153,51,255),(153,0,255),(0,102,0),(0,204,0),(0,255,0),(102,255,153),(153,255,204),(204,255,255),(204,236,255),(204,204,255),(204,153,255),(204,102,255),(204,0,255),(153,0,204),(0,51,0),(0,128,0),(51,204,51),(102,255,102),(153,255,153),(204,255,204),(255,204,255),(255,153,255),(255,102,255),(255,0,255),(204,0,204),(102,0,102),(51,102,0),(0,153,0),(102,255,51),(153,255,102),(204,255,153),(255,255,204),(255,204,204),(255,153,204),(255,102,204),(255,51,204),(204,0,153),(128,0,128),(51,51,0),(102,153,0),(153,255,51),(204,255,102),(255,255,153),(255,204,153),(255,153,153),(255,102,153),(255,51,153),(204,51,153),(153,0,153),(102,102,51),(153,204,0),(204,255,51),(255,255,102),(255,204,102),(255,153,102),(255,124,128),(255,0,102),(214,0,147),(153,51,102),(128,128,0),(204,204,0),(255,255,0),(255,204,0),(255,153,51),(255,102,0),(255,80,80),(204,0,102),(102,0,51),(153,102,51),(204,153,0),(255,153,0),(204,102,0),(255,51,0),(255,0,0),(204,0,0),(153,0,51),(102,51,0),(153,102,0),(204,51,0),(153,51,0),(153,0,0),(128,0,0),(165,0,33)
]
new_colors = []
alphas = [0.15, 0.3, 0.5, 0.65, 0.8, 0.95]
number_of_colors = len(standard_colors)
marks = [0 for i in range(16777216)]

for i in standard_colors:
    marks[tuple_to_int(i)] = -1

# -1 corresponds to a base color
# For all other colors, use the first element as the base, the second element as the top, and set the top to the third element
# To read this color format, convert the decimal number into hexidecimal, you should get the hex code 

"""
layers = int(input("How many step colors do you want to construct? (<3 recommended) ")) + 1

while layers > 4:
    print("waitwaitwait you don't wanna kill your computer do you?")
    layers = int(input("How many step colors do you want to construct? (<3 recommended) ")) + 1
"""
"""
update_freq = int(input("How many colors do you want constructed between progress updates? (10k recommended) "))
"""
update_freq = 200
start_time = time.time()

layer = 1
print("Code is running!")
while True:

    options = len(standard_colors) * len(standard_colors) * 6
    option_count = 0
    percentage = 0
    time_start_layer = time.time()

    # For every color
    for color in standard_colors:
        c_int = tuple_to_int(color)
        # Try to blend it with every other color
        for mix in standard_colors:
            # And blend it with every alpha
            for alpha in alphas:
                option_count += 1
                new_color = blending(color, mix, alpha)

                if new_color == "Kill":
                    continue

                n_int = tuple_to_int(new_color)

                if marks[n_int] == 0:
                    marks[n_int] = [tuple_to_int(color), tuple_to_int(mix), alpha]
                    number_of_colors += 1
                    new_colors.append(new_color)
                    """
                    if number_of_colors >= 16000000:
                        print(f"Color #{number_of_colors} {new_color} has been constructed! ({int((time.time() - start_time) * 1000) / 1000}s)")
                    elif number_of_colors >= 15500000:
                        if number_of_colors % (update_freq // 100) == 0:
                            print(f"{number_of_colors} colors have been constructed! ({int((time.time() - start_time) * 1000) / 1000}s)")
                    elif number_of_colors >= 14500000:
                        if number_of_colors % (update_freq // 10) == 0:
                            print(f"{number_of_colors} colors have been constructed! ({int((time.time() - start_time) * 1000) / 1000}s)")
                    elif number_of_colors % update_freq == 0:
                        print(f"{number_of_colors} colors have been constructed! ({int((time.time() - start_time) * 1000) / 1000}s)")
                    """
                    
                if layer >= 2:
                    if option_count >= options * (percentage + 1) / (update_freq * 100):
                        print(f"The color search for layer {layer} is {(percentage + 1) / update_freq}% completed!")
                        print(f"{number_of_colors} colors constructed. ")
                        print(f"{option_count} options searched.")
                        print(f"{int((time.time() - start_time) * 1000) / 1000} seconds elapsed.")
                        print(f"ETA: {int((time.time() - time_start_layer) * ((update_freq * 100) / (percentage + 1)) * 1000) / 1000}s")
                        percentage += 1
                           
                if number_of_colors >= 16777216:
                    break
            if number_of_colors >= 16777216:
                break
        if number_of_colors >= 16777216:
            break
    if number_of_colors >= 16777216:
        break

    print("\033c")
    print(f"Layer {layer} completed with {number_of_colors} colors! ({int((time.time() - start_time) * 1000) / 1000}s)")
    standard_colors = new_colors
    new_colors = []
    layer += 1

percent = 0
with open("methods.json", "w") as f:
    f.write("{")  # start JSON array

    for i in range(16777216):  # or just marks[i] depending on structure
        f.write(f'"{i}": {marks[i]}')

        if i != 16777215:
            f.write(",")  # comma between elements

        # progress bar
        new_percent = int(i / 16777216 * 100)
        if new_percent >= percent + 1:
            percent = new_percent
            print(f"[{'#'*percent}{'-'*(100-percent)}] {percent}% ({i}/{16777216}) ({int((time.time() - start_time) * 1000) / 1000}s)")

    f.write("}")

print(f"The program ended with {number_of_colors} colors constructed ({int(number_of_colors / 16777216 * 100) / 100}% of the total!) ({int((time.time() - start_time) * 1000) / 1000}s)")
