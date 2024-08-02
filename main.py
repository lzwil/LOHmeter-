import tkinter as tk
from tkinter import messagebox

def calculate_vaf_from_tumor_percentage_if_cons(tumor_percentage, loh):
    if loh:
        return (tumor_percentage + (100 - tumor_percentage)) / (tumor_percentage + 2 * (100 - tumor_percentage))
    else:
        return (tumor_percentage + (100 - tumor_percentage)) / ((2 * tumor_percentage) + 2 * (100 - tumor_percentage))

def calculate_tumor_percentage_from_vaf_if_cons(vaf, loh):
    if loh:
        return ((200 * vaf) - 100) / vaf
    else:
        return 0.5

def calculate_vaf_from_tumor_percentage(tumor_percentage, loh, is_constit):
    if is_constit:
        return calculate_vaf_from_tumor_percentage_if_cons(tumor_percentage, loh)
    else:
        if loh:
            return tumor_percentage / (tumor_percentage + (100 - tumor_percentage) * 2)
        else:
            return tumor_percentage / (tumor_percentage * 2 + (100 - tumor_percentage) * 2)

def calculate_tumor_percentage_from_vaf(vaf, loh, is_constit):
    if is_constit:
        return calculate_tumor_percentage_from_vaf_if_cons(vaf, loh)
    else:
        if loh:
            return (200 * vaf) / (1 + vaf)
        else:
            return (200 * vaf) / (2 + vaf)

def calculate_vaf():
    try:
        tumor_percentage = float(tumor_percentage_entry.get())
        loh = loh_var.get()
        is_constit = constit_var.get()
        if not (0 <= tumor_percentage <= 100):
            raise ValueError("Tumor percentage must be between 0 and 100.")

        vaf = calculate_vaf_from_tumor_percentage(tumor_percentage, loh, is_constit)
        result_label.config(text=f"Expected VAF: {vaf:.2f}")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def calculate_tumor_percentage():
    try:
        vaf = float(vaf_entry.get())
        loh = loh_var.get()
        is_constit = constit_var.get()
        if not (0 <= vaf <= 1):
            raise ValueError("VAF must be between 0 and 1.")

        tumor_percentage = calculate_tumor_percentage_from_vaf(vaf, loh, is_constit)
        result_label.config(text=f"Estimated Tumor Cell %: {tumor_percentage:.2f}%")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Tumor Cell and VAF Calculator")

# LOH Checkbox
loh_var = tk.BooleanVar()
loh_checkbox = tk.Checkbutton(root, text="Loss of Heterozygosity (LOH) Present", variable=loh_var)
loh_checkbox.grid(row=0, column=0, columnspan=2, pady=10)

# Constitutive Variant Checkbox
constit_var = tk.BooleanVar()
constit_checkbox = tk.Checkbutton(root, text="Constitutive Variant", variable=constit_var)
constit_checkbox.grid(row=0, column=1, columnspan=2, pady=10)

# VAF Entry
tk.Label(root, text="Observed VAF (as decimal):").grid(row=1, column=0, sticky=tk.E)
vaf_entry = tk.Entry(root)
vaf_entry.grid(row=1, column=1, padx=10, pady=5)

# Tumor Percentage Entry
tk.Label(root, text="Known Tumor Cell %:").grid(row=2, column=0, sticky=tk.E)
tumor_percentage_entry = tk.Entry(root)
tumor_percentage_entry.grid(row=2, column=1, padx=10, pady=5)

# Calculate Buttons
calc_vaf_button = tk.Button(root, text="Calculate VAF", command=calculate_vaf)
calc_vaf_button.grid(row=3, column=0, pady=10)

calc_tumor_percentage_button = tk.Button(root, text="Calculate Tumor %", command=calculate_tumor_percentage)
calc_tumor_percentage_button.grid(row=3, column=1, pady=10)

# Result Label
result_label = tk.Label(root, text="Result will be shown here")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
