import math 
import sys 
import tkinter as tk 
from tkinter import scrolledtext
import struct 

# Create main window
root = tk.Tk() 
root.title("Fixed-Point & IEEE754 Forward/Reverse Calculator") 
root.geometry("700x650") 

# --- REVERSE CONVERSION LOGIC ---

def binary_to_float(bin_str):
    """Converts a binary string like '-101.11' or '101.11' back to a decimal float."""
    try:
        bin_str = bin_str.strip()
        if not bin_str or bin_str == "0.0":
            return 0.0
        
        sign = 1
        if bin_str.startswith("-"):
            sign = -1
            bin_str = bin_str[1:]
            
        if "." in bin_str:
            integer_part, fractional_part = bin_str.split(".")
        else:
            integer_part, fractional_part = bin_str, ""
            
        decimal_val = int(integer_part, 2) if integer_part else 0
        
        for idx, bit in enumerate(fractional_part):
            if bit == '1':
                decimal_val += 2 ** -(idx + 1)
                
        return decimal_val * sign
    except Exception:
        return "Invalid Binary Format"

def single_hex_to_dec(hex_str):
    """Converts a 32-bit IEEE754 hex string (8 hex chars) back to a float."""
    try:
        hex_str = hex_str.strip().replace("0x", "")
        return struct.unpack('>f', bytes.fromhex(hex_str))[0]
    except Exception:
        return "Invalid Hex Format (Requires 8 hex characters)"

def double_hex_to_dec(hex_str):
    """Converts a 64-bit IEEE754 hex string (16 hex chars) back to a float."""
    try:
        hex_str = hex_str.strip().replace("0x", "")
        return struct.unpack('>d', bytes.fromhex(hex_str))[0]
    except Exception:
        return "Invalid Hex Format (Requires 16 hex characters)"

def hex_to_int_dec(hex_str):
    """Converts a standard integer hex string back to a decimal integer."""
    try:
        hex_str = hex_str.strip()
        return int(hex_str, 16)
    except Exception:
        return "Invalid Hex Format"

# --- FORWARD CONVERSION LOGIC ---

def decimal_string_to_binary(decimal_value): 
    temp = 0 
    input_size = len(decimal_value) 
    for i in range(0, input_size): 
        index = (input_size-1) - i 
        if (decimal_value[index] == '1'): 
            temp = temp | (1 << i) 
    return temp 

def float_to_binary(n, precision): 
    if n == 0: 
        return "0.0" 
    sign = "" 
    if n < 0: 
        sign = "-" 
        n = abs(n) 
    integer_part = int(n) 
    fractional_part = n - integer_part 
    integer_binary = bin(integer_part)[2:] 
    
    fractional_binary = [] 
    while fractional_part > 0 and len(fractional_binary) < precision: 
        fractional_part *= 2 
        bit = int(fractional_part) 
        fractional_binary.append(str(bit)) 
        fractional_part -= bit 
        
    fractional_string = "".join(fractional_binary) 
    single_number_str = "".join(fractional_binary) 
    
    if (len(fractional_binary) > 1): 
        raw_binary = str(integer_binary) + str(single_number_str) 
    else: 
        raw_binary = str(integer_binary) 
        
    return sign + integer_binary + "." + fractional_string 

def dec_to_double(decimal_value): 
    packed_bytes = struct.pack('>d', decimal_value) 
    return packed_bytes.hex() 

def dec_to_single(decimal_value): 
    packed_bytes = struct.pack('>f', decimal_value) 
    return packed_bytes.hex() 

def dec_to_hex(integer_value): 
    return int(integer_value) 

# --- LOG PRINT CONTROLLER ---
def print_to_log(title, val_name, input_val, result_name, result_val):
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"=== {title.upper()} ===\n\n")
    output_box.insert(tk.END, f"Input {val_name}: {input_val}\n\n")
    output_box.insert(tk.END, f"Result {result_name}: {result_val}\n")
    output_box.config(state=tk.DISABLED)

# --- BUTTON EVENT HANDLERS ---

# Forward Buttons
def click_fwd_bin():
    if dec_to_bin_var.get():
        val = float(dec_to_bin_var.get())
        res = float_to_binary(val, 64)
        print_to_log("Forward: Decimal to Binary", "Decimal", val, "Binary", res)

def click_fwd_single():
    if dec_to_single_var.get():
        val = float(dec_to_single_var.get())
        res = dec_to_single(val)
        print_to_log("Forward: Decimal to IEEE754 Single", "Decimal", val, "Hex", res)

def click_fwd_double():
    if dec_to_double_var.get():
        val = float(dec_to_double_var.get())
        res = dec_to_double(val)
        print_to_log("Forward: Decimal to IEEE754 Double", "Decimal", val, "Hex", res)

def click_fwd_hex():
    if dec_to_hex_var.get():
        val = float(dec_to_hex_var.get())
        res = hex(dec_to_hex(val))
        print_to_log("Forward: Decimal to Hex", "Decimal", val, "Hex", res)

# Reverse Buttons
def click_rev_bin():
    if bin_to_dec_var.get():
        val = bin_to_dec_var.get()
        res = binary_to_float(val)
        print_to_log("Reverse: Binary to Decimal", "Binary String", val, "Decimal Float", res)

def click_rev_single():
    if single_to_dec_var.get():
        val = single_to_dec_var.get()
        res = single_hex_to_dec(val)
        print_to_log("Reverse: IEEE754 Single to Decimal", "Hex String", val, "Decimal Float", res)

def click_rev_double():
    if double_to_dec_var.get():
        val = double_to_dec_var.get()
        res = double_hex_to_dec(val)
        print_to_log("Reverse: IEEE754 Double to Decimal", "Hex String", val, "Decimal Float", res)

def click_rev_hex():
    if hex_to_dec_var.get():
        val = hex_to_dec_var.get()
        res = hex_to_int_dec(val)
        print_to_log("Reverse: Hex to Decimal", "Hex String", val, "Decimal Integer", res)

# --- GUI LAYOUT ASSEMBLY ---

# Column 1 Layout: Forward Conversions (Left Side)
tk.Label(root, text="FORWARD CONVERSIONS (Dec ? Bin/Hex)", font=("Arial", 10, "bold")).place(x=30, y=15)

tk.Label(root, text="Convert decimal to binary:").place(x=30, y=45)
dec_to_bin_var = tk.StringVar()
tk.Entry(root, textvariable=dec_to_bin_var, width=18).place(x=30, y=65)
tk.Button(root, text="Convert", command=click_fwd_bin).place(x=160, y=61)

tk.Label(root, text="Convert decimal to single:").place(x=30, y=105)
dec_to_single_var = tk.StringVar()
tk.Entry(root, textvariable=dec_to_single_var, width=18).place(x=30, y=125)
tk.Button(root, text="Convert", command=click_fwd_single).place(x=160, y=121)

tk.Label(root, text="Convert decimal to double:").place(x=30, y=165)
dec_to_double_var = tk.StringVar()
tk.Entry(root, textvariable=dec_to_double_var, width=18).place(x=30, y=185)
tk.Button(root, text="Convert", command=click_fwd_double).place(x=160, y=181)

tk.Label(root, text="Convert decimal to hex:").place(x=30, y=225)
dec_to_hex_var = tk.StringVar()
tk.Entry(root, textvariable=dec_to_hex_var, width=18).place(x=30, y=245)
tk.Button(root, text="Convert", command=click_fwd_hex).place(x=160, y=241)


# Column 2 Layout: Reverse Conversions (Right Side)
tk.Label(root, text="REVERSE CONVERSIONS (Bin/Hex ? Dec)", font=("Arial", 10, "bold")).place(x=380, y=15)

tk.Label(root, text="Convert binary to decimal:").place(x=380, y=45)
bin_to_dec_var = tk.StringVar()
tk.Entry(root, textvariable=bin_to_dec_var, width=18).place(x=380, y=65)
tk.Button(root, text="Convert", command=click_rev_bin).place(x=510, y=61)

tk.Label(root, text="Convert single hex to decimal:").place(x=380, y=105)
single_to_dec_var = tk.StringVar()
tk.Entry(root, textvariable=single_to_dec_var, width=18).place(x=380, y=125)
tk.Button(root, text="Convert", command=click_rev_single).place(x=510, y=121)

tk.Label(root, text="Convert double hex to decimal:").place(x=380, y=165)
double_to_dec_var = tk.StringVar()
tk.Entry(root, textvariable=double_to_dec_var, width=18).place(x=380, y=185)
tk.Button(root, text="Convert", command=click_rev_double).place(x=510, y=181)

tk.Label(root, text="Convert hex to decimal integer:").place(x=380, y=225)
hex_to_dec_var = tk.StringVar()
tk.Entry(root, textvariable=hex_to_dec_var, width=18).place(x=380, y=245)
tk.Button(root, text="Convert", command=click_rev_hex).place(x=510, y=241)


# Centralized Shared Output Box (Bottom)
tk.Label(root, text="Calculation Results Log:", font=("Arial", 10, "bold")).place(x=30, y=300)
output_box = scrolledtext.ScrolledText(root, width=78, height=16, font=("Courier New", 10))
output_box.place(x=30, y=325)
output_box.config(state=tk.DISABLED)

root.mainloop()
