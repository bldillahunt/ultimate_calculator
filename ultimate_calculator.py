import math
import sys
import tkinter as tk

# Create the box
root = tk.Tk()
root.title("Ultimate Calculator")
root.geometry("640x480")
output_box = tk.Text(root, height=1, width=40, wrap="word")

output_label = tk.Label(root, text="")

def decimal_string_to_binary(decimal_value):
    temp = 0
    input_size = len(decimal_value)
    print("length = ", input_size)
    for i in range(0, input_size):
        index = (input_size-1) - i
        print("index = ", index)
        if (decimal_value[index] == '1'):
            temp = temp | (1 << i)
        print("decimal value = ", decimal_value[index], "temp = ", temp)
    return temp

def validate_numeric_input(P):
   # P is the value of the entry after the change
    print(P)
    return P.isdecimal() or P == "-" or P == "." or P == "" # Allow empty string or digits

def create_numeric_box(input_text, x, y, xoffset, yoffset):
	label = tk.Label(root, text=input_text)
	label.config(
		font=("Arial", 10),      # Set font and size
		fg="blue",               # Set foreground color (text color)
		bg="lightgray",          # Set background color
		padx=x,                  # Add horizontal padding
		pady=y                   # Add vertical padding
	)

	# Place the label within the window using a geometry manager
	label.pack(padx=xoffset, pady=yoffset) # Pack the label with some vertical padding
	entry_var = tk.StringVar() # A variable to hold the entry's content
	numeric_entry = tk.Entry(root, textvariable=entry_var)
	numeric_entry.pack(padx=xoffset, pady=yoffset)
	vcmd = (root.register(validate_numeric_input), '%P')
#	numeric_entry.config(validate="key", validatecommand=vcmd)
	return entry_var

def float_to_binary(n, precision):
    if n == 0:
        return "0.0"

    sign = ""
    if n < 0:
        sign = "-"
        n = abs(n)

    integer_part = int(n)
    fractional_part = n - integer_part

    # Convert integer part to binary
    integer_binary = bin(integer_part)[2:]  # [2:] removes the "0b" prefix
    print(integer_part, fractional_part, integer_binary)

    # Convert fractional part to binary
    fractional_binary = []

    if fractional_part > 0.0:
        while fractional_part > 0.0 and len(fractional_binary) < precision:
            fractional_part *= 2
            bit = int(fractional_part)
            fractional_binary.append(str(bit))
            fractional_part -= bit
#            print(fractional_part)
    else:
        fractional_binary = ['0']
    
    print(f"fractional binary = ", fractional_binary)
    print(f"integer binary = ", integer_binary)

    single_number_str = "".join(fractional_binary)
    single_number = single_number_str
    print("single number = ", single_number)

#    raw_binary = f"{integer_binary}{single_number}"
    if (len(fractional_binary) > 1) or (fractional_binary[0] == '1'):
        raw_binary = str(integer_binary) + str(single_number)
    else:
        raw_binary = str(integer_binary)

    print("raw binary = ", raw_binary)

    raw_binary_int = decimal_string_to_binary(raw_binary)

    if sign == "-":
        twos_complement = (int(raw_binary_int)^(2**32-1)) + 1
    else:
        twos_complement = int(raw_binary_int)

    print(f"{twos_complement:0b}")
    return f"{twos_complement}"

def on_button_click():
    global output_label
    float_value = float(decimal_var.get())
    binary_value = float_to_binary(float_value, 64)

    if (output_label.winfo_exists()):
        output_label.config(text="")

    output_label = tk.Label(root, text=f"Current Value: {bin(int(binary_value))}", font=("Arial", 12))
    output_label.pack(pady=0)
    output_label.place(x=100, y=100)

# Add widgets for label and button
label_d2b = tk.Label(root, text="Convert decimal to binary")
button_d2b = tk.Button(root, text="Convert")
label_d2b.pack(pady=5)
button_d2b.pack()

# Create the box for the floating point value
decimal_var = create_numeric_box('Float Value', 0, 0, 0, 0)
button_d2b.config(command=on_button_click)

root.mainloop()

