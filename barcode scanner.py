import tkinter as tk
from tkinter import filedialog
import requests
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk

def scan_barcode(image_path):
    with open(image_path, 'rb') as image_file:
        image = Image.open(image_file)
        barcode = decode(image)
        if barcode:
            return barcode[0].data.decode('utf-8'), image
        else:
            return None, None

def get_nutritional_info(barcode, product_name):
    url = f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'product' in data:
            product = data['product']
            return {
                'product_name': product_name,
                'proteins': product.get('nutriments', {}).get('proteins', 'N/A'),
                'calories': product.get('nutriments', {}).get('energy-kcal_100g', 'N/A'),
                'sugar': product.get('nutriments', {}).get('sugars_100g', 'N/A')
            }
    return None

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def process_product():
    image_path = entry_file.get()
    product_name = entry_product_name.get()

    if not product_name:
        result_text.set("Please enter the product name.")
        return

    barcode, input_image = scan_barcode(image_path)
    if barcode:
        nutritional_info = get_nutritional_info(barcode, product_name)
        if nutritional_info:
            result_text.set(f"Product: {nutritional_info['product_name']}\n"
                            f"Proteins: {nutritional_info['proteins']}\n"
                            f"Calories: {nutritional_info['calories']}\n"
                            f"Sugar: {nutritional_info['sugar']}")
            if input_image:
                input_image.thumbnail((250, 250))  
                input_photo = ImageTk.PhotoImage(input_image)
                input_label.config(image=input_photo)
                input_label.image = input_photo  
        else:
            result_text.set("No nutritional information found for this product.")
    else:
        result_text.set("No barcode detected in the image.")

root = tk.Tk()
root.title("Grocery Item Scanner")
root.configure(bg="#f0f0f0")

frame_input = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
frame_input.grid(row=0, column=0, sticky="ew")

tk.Label(frame_input, text="Select Image:", bg="#f0f0f0", fg="black", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entry_file = tk.Entry(frame_input, width=50, bd=2, relief="solid")
entry_file.grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_input, text="Browse", command=select_file, bg="#4caf50", fg="white", font=("Arial", 10), relief="raised").grid(row=0, column=2, padx=5, pady=5)

tk.Label(frame_input, text="Product Name:", bg="#f0f0f0", fg="black", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
entry_product_name = tk.Entry(frame_input, width=50, bd=2, relief="solid")
entry_product_name.grid(row=1, column=1, padx=5, pady=5)

frame_buttons = tk.Frame(root, bg="#f0f0f0")
frame_buttons.grid(row=1, column=0, columnspan=2, sticky="e")

tk.Button(frame_buttons, text="Process", command=process_product, bg="#2196f3", fg="white", font=("Arial", 12), relief="raised").pack(side="right", padx=10, pady=10)
tk.Button(frame_buttons, text="Quit", command=root.quit, bg="#f44336", fg="white", font=("Arial", 12), relief="raised").pack(side="right", padx=10, pady=10)

frame_result = tk.Frame(root, bg="#f0f0f0")
frame_result.grid(row=2, column=0, sticky="ew")

result_text = tk.StringVar()
result_text.set("")
result_label = tk.Label(frame_result, textvariable=result_text, bg="#f0f0f0", fg="black", font=("Arial", 12))
result_label.pack(padx=10, pady=10)

input_label = tk.Label(frame_result, bg="#f0f0f0")
input_label.pack(padx=10, pady=10)

root.mainloop()
