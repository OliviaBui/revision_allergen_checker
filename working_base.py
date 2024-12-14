import tkinter as tk
from tkinter import Text
from PIL import Image, ImageTk
from fuzzywuzzy import fuzz
import re

# Global variables
ingList = []
custom_allergens = []  # List to store custom allergens
next_button = None  # This will hold the reference to the 'Next' button

#########################################
# 🏛Allergen dictionaries & found_allergens 🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛🏛️🏛️🏛️🏛️️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛DONE:🎁
#########################################
allergen_categories = {
    "Fragrances": {"Amyl cinnamal", "Amylcinnamyl alcohol", "Anisyl alcohol", "Benzyl alcohol", "Benzyl benzoate",
                   "Benzyl cinnamate", "Benzyl salicylate", "Cinnamyl alcohol", "Cinnamaldehyde", "Citral",
                   "Citronellol", "Coumarin", "Eugenol", "Farnesol", "Geraniol", "Hexyl cinnamaladehyde",
                   "Hydroxycitronellal", "Hydroxyisohexyl 3-cyclohexene carboxaldehyde", "HICC", "Lyral",
                   "Isoeugenol", "Lilial", "d-Limonene", "Linalool", "Methyl 2-octynoate", "g-Methylionone",
                   "Oak moss extract", "Tree moss extract"},
    "Colourants": {"p-phenylenediamine", "PPD", "Coal-tar", "Tar", "Coal"},
    "Rubbers": {"Latex"},
    "Preservatives": {"Methylisothiazolinone", "MIT", "Methylchloroisothiazolinone", "CMIT", "Bronopol",
                      "2-bromo-2-nitropropane-1,3-diol", "5-bromo-5-nitro-1,3-dioxane", "Diazolidinyl urea", "DMDM",
                      "hydantoin", "1,3-dimethylol-5,5-dimethylhydantoin", "Imidazolidinyl urea",
                      "Sodium hydroxymethylglycinate", "Quaternium-15", "Dowicil200",
                      "N-(3-chloroallyl)hexaminium chloride"},
    "Metals": {"Nickel", "Gold"},
}

# The allergens selected by the user for comparison (default: all categories unselected)
selectedallergens = {category: False for category in allergen_categories}

######### "store_and_print_ingredients" creates "ingList"
# Function to store ingredients and print the list
def store_and_print_ingredients():
    # Get the text from the textbox
    ingredients_text = textbox.get("1.0", "end-1c").strip()

    # Ensure no placeholder text is included
    if ingredients_text != "Paste ingredients here...🌼" and ingredients_text != "":
        # Split the ingredients into a list by commas
        ingredients_list = [ingredient.strip() for ingredient in ingredients_text.split(",")]

        # Initialize a list to store processed ingredients
        processed_ingredients = []

        for ingredient in ingredients_list:
            # If the ingredient contains a slash ("/"), split it into separate strings
            if "/" in ingredient:
                split_ingredients = ingredient.split("/")
                processed_ingredients.extend([i.strip() for i in split_ingredients])  # No quotes around ingredients
            else:
                processed_ingredients.append(ingredient.strip())  # No quotes around ingredient

        # Append the processed ingredients to the global list
        ingList.extend(processed_ingredients)

        # Remove duplicates by converting the list to a set and back to a list
        ingList[:] = list(set(ingList))

        # Print the ingredients and the list
        print("Stored Ingredients:", ", ".join(processed_ingredients))
        print("Ingredients List (No Duplicates):", ingList)
    else:
        print("No ingredients to store.")

    # Simulate going to the next page
    print("Going to Allergen Check Page...")

# Function to clear the frame (clear all widgets)
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

#############################
# 🌉Background images with each frame 🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉🌉
#############################

def setup_page_with_background(frame, image_path, widget_setup_function=None):
    """
    Sets up a dynamically resized background PNG behind widgets for a given frame.

    Parameters:
    - frame: The frame or root window where the background and widgets will be displayed.
    - image_path: Path to the PNG image to use as the background.
    - widget_setup_function: Optional. A function to set up widgets on the page.
    """
    # Clear the frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a canvas for the background
    canvas = Canvas(frame, width=frame.winfo_width(), height=frame.winfo_height(), highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Load and resize the image to match the current screen size
    screen_width = frame.winfo_screenwidth()
    screen_height = frame.winfo_screenheight()

    # Open the image using PIL and resize it to fit the screen size
    bg_img = Image.open(image_path).resize((screen_width, screen_height), Image.ANTIALIAS)
    bg_image = ImageTk.PhotoImage(bg_img)

    # Add the background image to the canvas
    canvas.create_image(0, 0, anchor="nw", image=bg_image)
    canvas.image = bg_image  # Keep a reference to prevent garbage collection

    # Allow widgets to be added on top of the canvas
    frame.canvas = canvas

    # Run the widget setup function, if provided
    if widget_setup_function:
        widget_setup_function(frame)

    return canvas

#############################
# 🏠Page: Home 🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠DONE:🎁
#############################
def display_home(root, frame):
    """Display the Home page"""
    clear_frame(frame)

    # Set the background image
    def display_home(root, frame):
        """Display the Home page."""
        canvas = initialize_page(root, frame, "home.png", "Step 1: Enter your ingredients")

    # Add title label
    tk.Label(frame, text="Step 1: Enter your ingredients", font=("Helvetica", 18), bg="white").pack(pady=20)

    # Create the Text widget (textbox) inside the defined area and place it directly under the title
    global textbox  # Use global to access `textbox` in other functions
    textbox = tk.Text(frame, wrap="word", height=11, width=60)
    textbox.pack(pady=20)  # Place textbox right under the title with padding

    # Set the background and border to make it look like a rectangle
    textbox.config(bg="#FFFFFF", bd=4, relief="solid", font=("Helvetica", 15, "bold"), fg="#2f2f2f")

    # Clear the text box each time we go back to the Home page (reset the content)
    textbox.delete("1.0", "end-1c")  # Clear any existing text

    # Reset ingList to empty if you want to start fresh every time
    global ingList
    ingList = []

    # Create the textbox with the placeholder text (if the textbox is empty)
    textbox.insert("1.0", "Paste ingredients here...🌼")
    textbox.tag_add("placeholder", "1.0", "end-1c")
    textbox.tag_configure("placeholder", foreground="#bbbbbb", font=("Helvetica", 17, "bold"))

    # Function to set and remove the placeholder text
    def on_focus_in(event):
        if textbox.get("1.0", "end-1c") == "Paste ingredients here...🌼":
            textbox.delete("1.0", "end")

    def on_focus_out(event):
        if textbox.get("1.0", "end-1c") == "":
            textbox.insert("1.0", "Paste ingredients here...🌼", "placeholder")

    # Bind the focus-in and focus-out events
    textbox.bind("<FocusIn>", on_focus_in)
    textbox.bind("<FocusOut>", on_focus_out)

    # Add the NEXT button and link it to the function
    next_button = tk.Button(frame, text="NEXT", command=lambda: [store_and_print_ingredients(), display_allergenCheck(root, frame)])
    next_button.pack(pady=10)

    # Disable the NEXT button initially
    next_button.config(state=tk.DISABLED)

    # Function to enable/disable the NEXT button based on the textbox content
    def check_ingredient_entry(event=None):
        ingredients_text = textbox.get("1.0", "end-1c").strip()
        if ingredients_text != "" and ingredients_text != "Paste ingredients here...🌼":
            next_button.config(state=tk.NORMAL)
        else:
            next_button.config(state=tk.DISABLED)

    # Bind the event to check when the content changes
    textbox.bind("<KeyRelease>", check_ingredient_entry)

    # DISCLAIMER Button
    tk.Button(frame, text="🙆‍♀️️DISCLAIMER", command=lambda: display_disclaimer(root, frame)).pack(pady=10)

    # EXIT Button
    tk.Button(frame, text="🚪Exit program", command=root.quit).pack(pady=10)


#############################
# 🐣️Page: Disclaimer 🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣DONE:🎁
#############################
def display_disclaimer(root, frame):
    """Display Disclaimer"""
    clear_frame(frame)

    # Title of the Disclaimer page
    tk.Label(frame, text="Disclaimer", font=("Helvetica", 18), bg="white").pack(pady=20)

    # Disclaimer Text
    disclaimer_text = (
        "This is a first prototype and is not a substitute for professional medical advice. "
        "The information provided is based on the FDA’s list of cosmetic allergens, which may include "
        "specific American spelling. This list is limited to the FDA’s five categories of cosmetic allergens "
        "and includes the following allergens:\n\n"
        "Fragrances: Amyl cinnamal, Amylcinnamyl alcohol, Anisyl alcohol, Benzyl alcohol, Benzyl benzoate, "
        "Benzyl cinnamate, Benzyl salicylate, Cinnamyl alcohol, Cinnamaldehyde, Citral, Citronellol, Coumarin, "
        "Eugenol, Farnesol, Geraniol, Hexyl cinnamaladehyde, Hydroxycitronellal, Hydroxyisohexyl 3-cyclohexene "
        "carboxaldehyde, HICC, Lyral, Isoeugenol, Lilial, d-Limonene, Linalool, Methyl 2-octynoate, g-Methylionone, "
        "Oak moss extract, Tree moss extract\n\n"
        "Colourants: p-phenylenediamine (PPD), Coal-tar, Tar, Coal\n\n"
        "Rubbers: Latex\n\n"
        "Preservatives: Methylisothiazolinone (MIT), Methylchloroisothiazolinone (CMIT), Bronopol, "
        "2-bromo-2-nitropropane-1,3-diol, 5-bromo-5-nitro-1,3-dioxane, Diazolidinyl urea, DMDM hydantoin, "
        "1,3-dimethylol-5,5-dimethylhydantoin, Imidazolidinyl urea, Sodium hydroxymethylglycinate, Quaternium-15, "
        "Dowicil200, N-(3-chloroallyl)hexaminium chloride\n\n"
        "Metals: Nickel, Gold\n\n"
        "Please consult with a healthcare professional if you have concerns or are experiencing allergic reactions "
        "to any ingredients."
    )

    # Label for Disclaimer Text
    tk.Label(frame, text=disclaimer_text, font=("Helvetica", 10), bg="white", justify="left", wraplength=600).pack(
        pady=10)

    # Buttons to go back to home
    tk.Button(frame, text="🏠", command=lambda: display_home(root, frame)).pack(pady=10)
    tk.Button(frame, text="GO BACK HOME", command=lambda: display_home(root, frame)).pack(pady=10)

def switch_to_home(root, frame):
    """Switch to the home page."""
    switch_to_page(main_frame, "home.png", setup_home_widgets)

#############################
# 📝Page: Allergen check 📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝DONE:🎁
#############################
def display_allergenCheck(root, frame):
    """Display Allergen Check"""
    clear_frame(frame)

    # Title label
    tk.Label(frame, text="Step 2: Select your allergens", font=("Helvetica", 18), bg="white").pack(pady=20)

    # Add Go back a step button that preserves the ingredients
    tk.Button(frame, text="🏠", command=lambda: display_home(root, frame)).pack(pady=10)
    tk.Button(frame, text="Go back a step", command=lambda: display_home(root, frame)).pack(pady=10)

    # Create a frame to hold the checkboxes for allergen categories
    allergen_frame = tk.Frame(frame, bg="white")
    allergen_frame.pack(pady=10)

    # Function to update selected allergens based on checkbox selections
    def update_selected(category, var):
        selectedallergens[category] = var.get()

    # Function to update all allergen checkboxes when "All the Above" is selected/deselected
    def toggle_allergen_checkboxes(select_all):
        for category in allergen_categories:
            selectedallergens[category] = select_all
            vars[category].set(select_all)  # Update the state of each checkbox

    # Create a dictionary to hold the BooleanVars for each allergen
    vars = {}

    # "All the Above" checkbox to select/deselect all allergens
    all_the_above_var = tk.BooleanVar()
    all_the_above_checkbox = tk.Checkbutton(allergen_frame, text="All the Above", font=("Helvetica", 15), bg="white", variable=all_the_above_var,
                                            command=lambda: toggle_allergen_checkboxes(all_the_above_var.get()))
    all_the_above_checkbox.pack(anchor="w")

    # Loop through allergen categories to create checkboxes dynamically
    for category in allergen_categories:
        var = tk.BooleanVar(value=selectedallergens.get(category, False))  # Get current state
        checkbox = tk.Checkbutton(allergen_frame, text=category, font=("Helvetica", 15), bg="white", variable=var,
                                  command=lambda category=category, var=var: update_selected(category, var))
        checkbox.pack(anchor="w")
        vars[category] = var  # Store the variable for future reference

    # Add checkbox for Custom allergens
    tk.Label(frame, text="Add Custom Allergens", font=("Helvetica", 16), bg="white").pack(pady=10)
    custom_allergen_text = tk.Entry(frame, font=("Helvetica", 15), bg="white", width=30, bd=2, relief="solid",
                                    highlightbackground="black", highlightthickness=2)  # Add black outline
    custom_allergen_text.pack(pady=10)

    def add_custom_allergen():
        custom_allergen = custom_allergen_text.get().strip()
        if custom_allergen:
            # Add multiple allergens separated by commas
            allergens = [a.strip() for a in custom_allergen.split(",")]
            for allergen in allergens:
                if allergen not in custom_allergens:
                    custom_allergens.append(allergen)
                    print(f"Custom allergen added: {allergen}")
            # Update the displayed list of allergens
            update_allergen_list()

        custom_allergen_text.delete(0, "end")

    add_button = tk.Button(frame, text="Add Custom Allergen", command=add_custom_allergen)
    add_button.pack(pady=10)

    # Create a frame for the list of custom allergens with buttons to delete or edit
    custom_list_frame = tk.Frame(frame, bg="white")
    custom_list_frame.pack(pady=10)

    # Listbox to display custom allergens
    allergen_listbox = tk.Listbox(custom_list_frame, height=6, width=40, font=("Helvetica", 15))
    allergen_listbox.pack(side="left", fill="y")

    # Scrollbar for the listbox
    scrollbar = tk.Scrollbar(custom_list_frame, orient="vertical", command=allergen_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    allergen_listbox.config(yscrollcommand=scrollbar.set)

    # Function to update the allergen list in the listbox
    def update_allergen_list():
        allergen_listbox.delete(0, "end")  # Clear the listbox
        for allergen in custom_allergens:
            allergen_listbox.insert("end", allergen)

    # Function to delete selected allergen
    def delete_selected_allergen():
        try:
            selected = allergen_listbox.curselection()
            if selected:
                allergen_to_delete = allergen_listbox.get(selected)
                custom_allergens.remove(allergen_to_delete)
                print(f"Custom allergen deleted: {allergen_to_delete}")
                update_allergen_list()
        except Exception as e:
            print("Error deleting allergen:", e)

    # Function to edit selected allergen
    def edit_selected_allergen():
        try:
            selected = allergen_listbox.curselection()
            if selected:
                allergen_to_edit = allergen_listbox.get(selected)
                new_allergen = custom_allergen_text.get().strip()
                if new_allergen and new_allergen != allergen_to_edit:
                    custom_allergens[custom_allergens.index(allergen_to_edit)] = new_allergen
                    print(f"Custom allergen edited: {allergen_to_edit} -> {new_allergen}")
                    update_allergen_list()
                custom_allergen_text.delete(0, "end")
        except Exception as e:
            print("Error editing allergen:", e)

    # Buttons to delete or edit allergen
    edit_button = tk.Button(frame, text="Edit Allergen", command=edit_selected_allergen)
    edit_button.pack(pady=5)
    delete_button = tk.Button(frame, text="Delete Allergen", command=delete_selected_allergen)
    delete_button.pack(pady=5)

    # Add an Analyse button that will display the results
    tk.Button(frame, text="Analyse", command=lambda: display_results(root, frame)).pack(pady=10)

    # Update the allergen list initially
    update_allergen_list()

def perform_allergen_check():
    """Perform allergen check and show results"""
    print("Performing allergen check...")

    # List to store allergens found during the check
    found_allergens = []

    # Printing the selected categories and custom allergens for tracking
    print("Selected categories:")
    for category, selected in selectedallergens.items():
        if selected:
            print(f"- {category}")

    print("\nCustom allergens:")
    for custom_allergen in custom_allergens:
        print(f"- {custom_allergen}")

    # Checking for allergens from the predefined categories
    for ingredient in ingList:
        for category, allergens in allergen_categories.items():
            for allergen in allergens:
                match_percentage = fuzz.partial_ratio(ingredient.lower(), allergen.lower())

                if match_percentage >= 90:
                    found_allergens.append(f"Certain match: {allergen} (97%+)")
                    print(f"Ingredient '{ingredient}' contains allergen '{allergen}' with a certain match ({match_percentage}%)")
                elif 80 <= match_percentage < 90:
                    found_allergens.append(f"Unsure match: {allergen} ({match_percentage}%)")
                    print(f"Ingredient '{ingredient}' contains allergen '{allergen}' with an unsure match ({match_percentage}%)")

    # Checking for custom allergens
    for custom_allergen in custom_allergens:
        for ingredient in ingList:
            match_percentage = fuzz.partial_ratio(ingredient.lower(), custom_allergen.lower())

            if match_percentage >= 90:
                found_allergens.append(f"Certain match: {custom_allergen} (97%+)")
                print(f"Ingredient '{ingredient}' contains custom allergen '{custom_allergen}' with a certain match ({match_percentage}%)")
            elif 80 <= match_percentage < 90:
                found_allergens.append(f"Unsure match: {custom_allergen} ({match_percentage}%)")
                print(f"Ingredient '{ingredient}' contains custom allergen '{custom_allergen}' with an unsure match ({match_percentage}%)")

    # Displaying results in the console
    if found_allergens:
        print("\nAllergens detected:", ", ".join(found_allergens))
    else:
        print("No allergens detected.")

import tkinter as tk

def display_allergenCheck(root, frame):
    """Display Allergen Check"""
    clear_frame(frame)

    # Title label
    tk.Label(frame, text="Step 2: Select your allergens", font=("Helvetica", 18), bg="white").pack(pady=20)

    # Add Go back a step button that preserves the ingredients
    tk.Button(frame, text="🏠", command=lambda: display_home(root, frame)).pack(pady=10)
    tk.Button(frame, text="Go back a step", command=lambda: display_home(root, frame)).pack(pady=10)

    # Create a frame to hold the checkboxes for allergen categories
    allergen_frame = tk.Frame(frame, bg="white")
    allergen_frame.pack(pady=10)

    # Function to update selected allergens based on checkbox selections
    def update_selected(category, var):
        selectedallergens[category] = var.get()

    # Loop through allergen categories to create checkboxes dynamically
    for category in allergen_categories:
        var = tk.BooleanVar(value=selectedallergens.get(category, False))  # Get current state
        checkbox = tk.Checkbutton(allergen_frame, text=category, font=("Helvetica", 15), bg="white", variable=var,
                                  command=lambda category=category, var=var: update_selected(category, var))
        checkbox.pack(anchor="w")

    # Add checkbox for Custom allergens
    tk.Label(frame, text="Add Custom Allergens", font=("Helvetica", 16), bg="white").pack(pady=10)
    custom_allergen_text = tk.Entry(frame, font=("Helvetica", 15), bg="white", width=30, relief="solid", bd=2)  # Outline added
    custom_allergen_text.pack(pady=10)

    # Variable to track the allergen being edited
    selected_allergen_to_edit = None

    # Function to toggle between adding a new allergen and saving an edit
    def save_or_edit_allergen():
        nonlocal selected_allergen_to_edit
        custom_allergen = custom_allergen_text.get().strip()
        if not custom_allergen:
            return  # Do nothing if the input field is empty

        if selected_allergen_to_edit:  # Editing an existing allergen
            index = custom_allergens.index(selected_allergen_to_edit)
            custom_allergens[index] = custom_allergen
            print(f"Custom allergen edited: {selected_allergen_to_edit} -> {custom_allergen}")
            selected_allergen_to_edit = None  # Clear edit state
        else:  # Adding a new allergen
            allergens = [a.strip() for a in custom_allergen.split(",")]
            for allergen in allergens:
                if allergen not in custom_allergens:
                    custom_allergens.append(allergen)
                    print(f"Custom allergen added: {allergen}")

        update_allergen_list()
        custom_allergen_text.delete(0, "end")

    # Save/Edit button
    save_edit_button = tk.Button(frame, text="➕ Save/Edit", command=save_or_edit_allergen)
    save_edit_button.pack(pady=10)

    # Create a frame for the list of custom allergens with buttons to delete or edit
    custom_list_frame = tk.Frame(frame, bg="white")
    custom_list_frame.pack(pady=10)

    # Listbox to display custom allergens
    allergen_listbox = tk.Listbox(custom_list_frame, height=6, width=40, font=("Helvetica", 15))
    allergen_listbox.pack(side="left", fill="y")

    # Scrollbar for the listbox
    scrollbar = tk.Scrollbar(custom_list_frame, orient="vertical", command=allergen_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    allergen_listbox.config(yscrollcommand=scrollbar.set)

    # Function to update the allergen list in the listbox
    def update_allergen_list():
        allergen_listbox.delete(0, "end")  # Clear the listbox
        for allergen in custom_allergens:
            allergen_listbox.insert("end", allergen)

    # Function to delete selected allergen
    def delete_selected_allergen():
        try:
            selected = allergen_listbox.curselection()
            if selected:
                allergen_to_delete = allergen_listbox.get(selected)
                custom_allergens.remove(allergen_to_delete)
                print(f"Custom allergen deleted: {allergen_to_delete}")
                update_allergen_list()
        except Exception as e:
            print("Error deleting allergen:", e)

    # Delete Custom Allergen button
    delete_button = tk.Button(frame, text="❌ Delete Selected Custom Allergen", command=delete_selected_allergen)
    delete_button.pack(pady=10)

    # Reset custom allergens to empty list
    def reset_custom_allergens():
        custom_allergens.clear()
        update_allergen_list()
        custom_allergen_text.delete(0, "end")
        print("All custom allergens have been reset.")

    # Reset button
    reset_button = tk.Button(frame, text="🔄 Reset All Custom Allergens", command=reset_custom_allergens)
    reset_button.pack(pady=10)

    # Add an Analyse button that will display the results
    tk.Button(frame, text="Analyse", command=lambda: display_results(root, frame)).pack(pady=10)

    # Add double-click event to edit allergen
    def on_double_click(event):
        nonlocal selected_allergen_to_edit
        selected = allergen_listbox.curselection()
        if selected:
            allergen_to_edit = allergen_listbox.get(selected)
            custom_allergen_text.delete(0, "end")
            custom_allergen_text.insert(0, allergen_to_edit)
            selected_allergen_to_edit = allergen_to_edit
            print(f"Editing allergen: {allergen_to_edit}")

    allergen_listbox.bind("<Double-1>", on_double_click)

    # Update the allergen list initially
    update_allergen_list()

def perform_allergen_check():
    """Perform allergen check and show results"""
    print("Performing allergen check...")

    # List to store allergens found during the check
    found_allergens = []

    # Printing the selected categories and custom allergens for tracking
    print("Selected categories:")
    for category, selected in selectedallergens.items():
        if selected:
            print(f"- {category}")

    print("\nCustom allergens:")
    for custom_allergen in custom_allergens:
        print(f"- {custom_allergen}")

    # Checking for allergens from the predefined categories
    for ingredient in ingList:
        for category, allergens in allergen_categories.items():
            for allergen in allergens:
                match_percentage = fuzz.partial_ratio(ingredient.lower(), allergen.lower())

                if match_percentage >= 90:
                    found_allergens.append(f"Certain match: {allergen} (97%+)")
                    print(f"Ingredient '{ingredient}' contains allergen '{allergen}' with a certain match ({match_percentage}%)")
                elif 80 <= match_percentage < 90:
                    found_allergens.append(f"Unsure match: {allergen} ({match_percentage}%)")
                    print(f"Ingredient '{ingredient}' contains allergen '{allergen}' with an unsure match ({match_percentage}%)")

    # Checking for custom allergens
    for custom_allergen in custom_allergens:
        for ingredient in ingList:
            match_percentage = fuzz.partial_ratio(ingredient.lower(), custom_allergen.lower())

            # Debugging line to track custom allergen matching
            print(f"Checking: '{ingredient}' vs '{custom_allergen}' -> {match_percentage}%")  # Debug line

            if match_percentage >= 90:
                found_allergens.append(f"Certain match: {custom_allergen} (97%+)")
                print(f"Ingredient '{ingredient}' contains custom allergen '{custom_allergen}' with a certain match ({match_percentage}%)")
            elif 80 <= match_percentage < 90:
                found_allergens.append(f"Unsure match: {custom_allergen} ({match_percentage}%)")
                print(f"Ingredient '{ingredient}' contains custom allergen '{custom_allergen}' with an unsure match ({match_percentage}%)")

    # Displaying results in the console
    if found_allergens:
        print("\nAllergens detected:", ", ".join(found_allergens))
    else:
        print("No allergens detected.")


def clean_string(input_string):
    """Clean up the ingredient and allergen strings by removing non-alphabetic characters and extra spaces"""
    # Remove non-alphabetic characters (except spaces) and lower the case
    cleaned = re.sub(r'[^a-zA-Z\s]', '', input_string)
    # Remove extra spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def display_results(root, frame):
    """Display the allergen results with fuzzy matching, slash handling, category grouping, sorted by match score."""
    clear_frame(frame)

    # Create a frame to center the text box and scrollable content in the root window
    results_frame = tk.Frame(frame, bg="white", relief="solid", bd=2)
    results_frame.pack(pady=20, padx=10, expand=True, fill="both", anchor="center")  # Center the frame

    # Page title (outside the scrollable area)
    result_label = tk.Label(results_frame, text="Allergen Results", font=("Helvetica", 18), bg="white", anchor="center")
    result_label.pack(pady=20, anchor="center")

    # Add a legend explaining the emojis (outside the scrollable area)
    legend_frame = tk.Frame(results_frame, bg="white")
    legend_frame.pack(pady=10, anchor="center")

    legend_label = tk.Label(
        legend_frame,
        text="Legend: 🤷‍♀️ = 80-90% spelling match (possibly matched), ❗️ = 90%+ spelling match (match found)",
        font=("Helvetica", 12), bg="white", wraplength=500, anchor="center"
    )
    legend_label.pack(pady=10)

    # Create a Canvas to hold the scrollable area for allergen results
    canvas = tk.Canvas(results_frame)
    scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the allergen results content
    content_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Pack the scrollbar and canvas inside the results_frame
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Dictionary to store allergens grouped by category and their match scores
    grouped_allergens = {category: [] for category in allergen_categories}
    allergens_found = False  # Flag to track if any allergens are found

    # Function to clean up the ingredient and allergen strings (removes non-alphabetic characters and extra spaces)
    def clean_string(input_string):
        cleaned = re.sub(r'[^a-zA-Z\s]', '', input_string)  # Remove non-alphabetic characters
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()  # Remove extra spaces
        return cleaned

    # Find matching allergens using fuzzy matching
    for category, allergens in allergen_categories.items():
        if selectedallergens.get(category, False):
            seen_allergens = set()  # Keep track of allergens that have already been matched

            for ingredient in ingList:
                ingredient_cleaned = clean_string(ingredient.lower())  # Clean the ingredient string

                for allergen in allergens:
                    allergen_cleaned = clean_string(allergen.lower())  # Clean the allergen string

                    # Use fuzzywuzzy to compare the cleaned strings
                    match_score = fuzz.partial_ratio(ingredient_cleaned, allergen_cleaned)

                    # Only store allergens with match score of 80% or higher
                    if match_score >= 80:
                        if allergen not in seen_allergens:  # Prevent duplicates
                            seen_allergens.add(allergen)
                            allergens_found = True  # Mark that allergens were found

                            # Determine emoji based on match score
                            emoji = "❗️" if match_score >= 90 else "🤷‍♀️"

                            # Append the allergen to the grouped_allergens
                            grouped_allergens[category].append((allergen, match_score, emoji))

    # Display custom allergens
    if custom_allergens:
        custom_allergen_label = tk.Label(content_frame, text="Custom Allergens", font=("Helvetica", 16, "bold"), bg="white", anchor="center")
        custom_allergen_label.pack(pady=10, anchor="center")

        for custom_allergen in custom_allergens:
            seen_custom_allergen = set()  # Track if we've already added this custom allergen

            for ingredient in ingList:
                ingredient_cleaned = clean_string(ingredient.lower())
                custom_allergen_cleaned = clean_string(custom_allergen.lower())

                match_score = fuzz.partial_ratio(ingredient_cleaned, custom_allergen_cleaned)

                if match_score >= 80 and custom_allergen not in seen_custom_allergen:
                    seen_custom_allergen.add(custom_allergen)
                    allergens_found = True  # Mark that allergens were found

                    emoji = "❗️" if match_score >= 90 else "🤷‍♀️"

                    result_text = tk.Label(content_frame, text=f"- {custom_allergen} {emoji} ({match_score}%)", font=("Helvetica", 12), bg="white", wraplength=380, anchor="center")
                    result_text.pack(pady=3, anchor="center")

    # Display allergen results inside the scrollable content area
    if any(grouped_allergens.values()):
        for category, allergens in grouped_allergens.items():
            if allergens:  # Only display categories that have found allergens
                sorted_allergens = sorted(allergens, key=lambda x: x[1], reverse=True)

                # Category as a subheading
                category_label = tk.Label(content_frame, text=category, font=("Helvetica", 16, "bold"), bg="white", anchor="center")
                category_label.pack(pady=5, anchor="center")

                # Display each allergen in that category on a new line with smaller text
                for allergen, score, emoji in sorted_allergens:
                    result_text = tk.Label(content_frame, text=f"- {allergen} {emoji} ({score}%)", font=("Helvetica", 12), bg="white", wraplength=380, anchor="center")
                    result_text.pack(pady=3, anchor="center")

    # Only display "No allergens found!" if no allergens were detected anywhere
    if not allergens_found:
        no_results_label = tk.Label(content_frame, text="No allergens found!", font=("Helvetica", 14), bg="white", wraplength=380, anchor="center")
        no_results_label.pack(pady=20, anchor="center")

    # Button to go back
    tk.Button(frame, text="Do another", command=lambda: display_home(root, frame)).pack(pady=10)

    # Update scroll region when content changes
    content_frame.update_idletasks()



# Create the main Tkinter window
root = tk.Tk()
root.title("𓍢ִ໋🌷͙֒Pretty Clean Ingredientsִ໋🌷͙ᩚ")
root.geometry("1920x1080")
frame = tk.Frame(root, bg="white")
frame.pack(fill="both", expand=True)

display_home(root, frame)

root.mainloop()


