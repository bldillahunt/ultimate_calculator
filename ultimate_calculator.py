import math
import sys
import tkinter as tk
import ieee754
from ieee754 import double
import struct

# Create the box
root = tk.Tk()
root.title("Ultimate Calculator")
root.geometry("640x480")

binary_label = tk.Label(root, text="")
double_label = tk.Label(root, text="")
single_label = tk.Label(root, text="")

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
	# label = tk.label(root, text=input_text)
	# label.config(
	# 	font=("arial", 10),      # set font and size
	# 	fg="blue",               # set foreground color (text color)
	# 	bg="lightgray",          # set background color
	# 	padx=x,                  # add horizontal padding
	# 	pady=y                   # add vertical padding
	# )

	# # place the label within the window using a geometry manager
	# label.pack(padx=xoffset, pady=yoffset) # pack the label with some vertical padding
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

def dec_to_double(decimal_value):
    packed_bytes = struct.pack('>d', decimal_value)
    hex_representation = packed_bytes.hex()
    return hex_representation

def dec_to_single(decimal_value):
    packed_bytes = struct.pack('>f', decimal_value)
    hex_representation = packed_bytes.hex()
    return hex_representation

def bin_button_click():
    global binary_label
    double_value = float(dec_to_bin_var.get())
    binary_value = float_to_binary(double_value, 64)

    if (binary_label.winfo_exists()):
        binary_label.config(text="")

    binary_label = tk.Label(root, text=f"Current Value: {bin(int(binary_value))}", font=("Arial", 12))
    binary_label.pack(pady=0)
    binary_label.place(x=100, y=75)

def double_button_click():
    global double_label
    double_value = float(dec_to_double_var.get())
    double_value = dec_to_double(double_value)

    if (double_label.winfo_exists()):
        double_label.config(text="")

    double_label = tk.Label(root, text=f"Current Value: {double_value}", font=("Arial", 12))
    double_label.pack(pady=0)
    double_label.place(x=225, y=300)

def single_button_click():
    global single_label
    single_value = float(dec_to_single_var.get())
    single_value = dec_to_single(single_value)

    if (single_label.winfo_exists()):
        single_label.config(text="")

    single_label = tk.Label(root, text=f"Current Value: {single_value}", font=("Arial", 12))
    single_label.pack(pady=0)
    single_label.place(x=225, y=180)

# Add widgets for label and button
label_d2b = tk.Label(root, text="Convert decimal to binary")
button_d2b = tk.Button(root, text="Convert")
label_d2b.pack(side="top", pady=0)
button_d2b.pack(side="top", pady=0)
dec_to_bin_var = create_numeric_box("", 0, 0, 0, 10)

label_d2s = tk.Label(root, text="Convert decimal to single")
button_d2s = tk.Button(root, text="Convert")

label_d2d = tk.Label(root, text="Convert decimal to double")
button_d2d = tk.Button(root, text="Convert")

# Create the box for the floating point value
button_d2b.config(command=bin_button_click)

dec_to_single_var = create_numeric_box("", 0, 0, 0, 75)
button_d2s.pack(ipady=0, pady=0)
button_d2s.place(x=290, y=125)

label_d2s.pack(ipady = 0, pady=0)
label_d2s.place(x=250, y=100)
button_d2s.config(command=single_button_click)

dec_to_double_var = create_numeric_box("", 0, 0, 0, 10)
button_d2d.pack(ipady=0, pady=0)
button_d2d.place(x=290, y=225)

label_d2d.pack(ipady = 0, pady=0)
label_d2d.place(x=250, y=200)
button_d2d.config(command=double_button_click)

root.mainloop()

