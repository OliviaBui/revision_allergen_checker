import tkinter as tk
from tkinter import Tk, Canvas, Frame, Button, Label
from PIL import Image, ImageTk
from fuzzywuzzy import fuzz
import re

# Global variables
ingList = [] # List to store the user's product list AFTER it is cleaned up (in case they have duplicates, too many slashes, too much whitespace, detect comma use , and disable non-entries)
custom_allergens = []  # List to store custom individual allergens user wants to screen for
next_button = None  # This will hold the reference to the 'Next' button (to clear textbox everytime upon return)
selectedallergens = {} # List to store allergen categories (dictionaries) the user ticks/actually cares about screening for

#########################################
# 🏛Allergen dictionaries & found_allergens 🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛🏛️🏛️🏛️🏛️️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛
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
selectedallergens = {category: False for category in allergen_categories} #another important global variable


#########################################
# 🐻 Processing ingredients list: handling non-entries, commas, whitespace, slashes(/), duplicates & list storage 🐻🐻🐻
#########################################
# "store_and_print_ingredients" function creates "ingList" variable
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

#########################################
# 🖊️ Standardising the page setup: clear and add widgets, background, fill screen, bg image + resize 🖊️🖊️🖊️🖊️🖊️🖊️🖊️🖊️
#########################################
def setup_page_with_background(frame, image_path, widget_setup_function=None):
    """Sets up a dynamically resized background PNG behind widgets for a given frame."""
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a canvas for the background
    canvas = Canvas(frame, width=frame.winfo_width(), height=frame.winfo_height(), highlightthickness=0, bg="#c8f61b")
    canvas.pack(fill="both", expand=True)

    # Load and resize the image
    bg_img = Image.open(image_path)
    screen_width = frame.winfo_width() or 1920
    screen_height = frame.winfo_height() or 1080
    img_width, img_height = bg_img.size
    aspect_ratio = img_width / img_height
    if screen_width / screen_height > aspect_ratio:
        new_height = screen_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = screen_width
        new_height = int(new_width / aspect_ratio)
    bg_img = bg_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_img)

    canvas.create_image(screen_width // 2, screen_height // 2, image=bg_image)
    canvas.image = bg_image  # Prevent garbage collection
    frame.canvas = canvas

    # Add widgets on top of the canvas
    if widget_setup_function:
        widget_setup_function(frame)

    return canvas

#########################################
# 🐻 Setting up widgets for 5 pages : home, allergen check, clean, not clean, disclaimer 🐻🐻🐻🐻🐻🐻🐻🐻🐻🐻🐻🐻🐻
#########################################
# Home page
def setup_home_widgets(frame):
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
    next_button = tk.Button(frame, text="NEXT",
                            command=lambda: [store_and_print_ingredients(), switch_to_allergencheck(root, frame)])
    next_button.pack()  # or use .grid()/.place() based on your layout

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
    tk.Button(frame, text="🙆‍♀️️DISCLAIMER", command=lambda: switch_to_disclaimer(Frame)).pack(pady=10)
    print("Navigating to Disclaimer page...")

    # EXIT Button
    tk.Button(frame, text="🚪Exit program", command=root.quit).pack(pady=10)

# Allergen check page
def setup_allergencheck_widgets(frame):
    # Add Go back a step button that preserves the ingredients
    tk.Button(frame, text="🏠", command=lambda: switch_to_home(root, frame)).pack(pady=10)
    tk.Button(frame, text="Go back a step", command=lambda: switch_to_home(root, frame)).pack(pady=10)

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
    custom_allergen_text = tk.Entry(frame, font=("Helvetica", 15), bg="white", width=30, relief="solid",
                                    bd=2)  # Outline added
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
    tk.Button(frame, text="Analyse", command=lambda: perform_allergen_check(root, frame)).pack(pady=10)

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

# Slight detour: Establishing "perform_allergen_check" function: Compares ingredients vs allergens & displays matches or no matches.
def perform_allergen_check():
    """Perform allergen check and show results."""
    print("Performing allergen check...")

    # List to store detected allergens
    found_allergens = []

    # Printing selected categories and custom allergens for tracking
    print("Selected allergen categories:")
    for category, selected in selectedallergens.items():
        if selected:
            print(f"- {category}")

    print("\nCustom allergens to check:")
    for custom_allergen in custom_allergens:
        print(f"- {custom_allergen}")

    # Check for allergens in predefined categories
    for ingredient in ingList:
        for category, allergens in allergen_categories.items():
            if selectedallergens.get(category, False):  # Only check selected categories
                for allergen in allergens:
                    match_percentage = fuzz.partial_ratio(ingredient.lower(), allergen.lower())

                    if match_percentage >= 90:
                        found_allergens.append(f"Certain match: {allergen} (97%+)")
                        print(
                            f"Ingredient '{ingredient}' contains allergen '{allergen}' with a certain match ({match_percentage}%)"
                        )
                    elif 80 <= match_percentage < 90:
                        found_allergens.append(f"Unsure match: {allergen} ({match_percentage}%)")
                        print(
                            f"Ingredient '{ingredient}' contains allergen '{allergen}' with an unsure match ({match_percentage}%)"
                        )

    # Check for allergens in custom allergens
    for custom_allergen in custom_allergens:
        for ingredient in ingList:
            match_percentage = fuzz.partial_ratio(ingredient.lower(), custom_allergen.lower())

            # Debugging line to track custom allergen matching
            print(f"Checking: '{ingredient}' vs '{custom_allergen}' -> {match_percentage}%")  # Debug line

            if match_percentage >= 90:
                found_allergens.append(f"Certain match: {custom_allergen} (97%+)")
                print(
                    f"Ingredient '{ingredient}' contains custom allergen '{custom_allergen}' with a certain match ({match_percentage}%)"
                )
            elif 80 <= match_percentage < 90:
                found_allergens.append(f"Unsure match: {custom_allergen} ({match_percentage}%)")
                print(
                    f"Ingredient '{ingredient}' contains custom allergen '{custom_allergen}' with an unsure match ({match_percentage}%)"
                )

    # Displaying results and navigating to the appropriate page
    if found_allergens:
        print("\nAllergens detected:", ", ".join(found_allergens))
        switch_to_notclean(found_allergens)
    else:
        print("No allergens detected.")
        switch_to_clean()


# Slight detour: Establishing "clean_string" function to clean inputted list, removing non-alphabetic characters and extra spaces (e.g. "Amyl cinnamal, 98%" = "Amyl cinnamal").
def clean_string(input_string):
    """Clean up the ingredient and allergen strings by removing non-alphabetic characters and extra spaces"""
    # Remove non-alphabetic characters (except spaces) and lower the case
    cleaned = re.sub(r'[^a-zA-Z\s]', '', input_string)
    # Remove extra spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

# Clean page
def setup_clean_widgets(frame):
    Button(frame.canvas, text="🏠", command=lambda: switch_to_home()).place(x=850, y=500)
    Button(frame.canvas, text="Do another", command=lambda: switch_to_home()).place(x=850, y=550)

# Not clean page
def setup_notclean_widgets(frame):
    Button(frame.canvas, text="🏠", command=lambda: switch_to_home()).place(x=850, y=500)
    Button(frame.canvas, text="Do another", command=lambda: switch_to_home()).place(x=850, y=550)

# Disclaimer page
def setup_disclaimer_widgets(frame):
    # Buttons to go back to home
    tk.Button(frame, text="🏠", command=lambda: switch_to_home(root, frame)).pack(pady=10)
    tk.Button(frame, text="GO BACK HOME", command=lambda: switch_to_home(root, frame)).pack(pady=10)

#########################################
# 🔮 Combining '.png' + widget switch for each page: home, allergen check, clean, not clean, disclaimer 🔮🔮🔮🔮🔮🔮🔮
#########################################
def switch_to_home(root, frame):
    """Switch to the home page."""
    switch_to_page(main_frame, "home.png", setup_home_widgets)


# Navigation functions
def switch_to_home():
    setup_page_with_background(main_frame, "home.png", setup_home_widgets)


def switch_to_allergencheck():
    setup_page_with_background(main_frame, "allergencheck.png", setup_allergencheck_widgets)


def switch_to_clean():
    setup_page_with_background(main_frame, "clean.png", setup_clean_widgets)


def switch_to_notclean():
    setup_page_with_background(main_frame, "notclean.png", setup_notclean_widgets)


def switch_to_disclaimer():
    frame.destroy()
    setup_page_with_background(main_frame, "disclaimer.png", setup_disclaimer_widgets)


#########################################
# 🌺 Main application setup: root, fullscreen, title, frame, starting on home page, looping 🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺🌺
#########################################
if __name__ == "__main__":
    root = Tk()
    root.attributes('-fullscreen', True)  # Fullscreen mode
    root.title("𓍢ִ໋🌷͙֒Pretty Clean Ingredientsִ໋🌷͙ᩚ")

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill="both", expand=True)

    main_frame = Frame(root)
    main_frame.pack(fill="both", expand=True)

    # Start with the home page
    root.after(1, switch_to_home)

    root.mainloop()
