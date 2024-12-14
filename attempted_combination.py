#########################################
# 🌼General setup 🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼🌼
#########################################
import tkinter as tk
from tkinter import Text
from PIL import Image, ImageTk
from fuzzywuzzy import fuzz
import re

# Global variables
global ingList
ingList = []
custom_allergens = []  # List to store custom allergens
next_button = None  # This will hold the reference to the 'Next' button


# Create the main Tkinter window
root = tk.Tk()
root.title("𓍢ִ໋🌷͙֒Pretty Clean Ingredientsִ໋🌷͙ᩚ")
root.geometry("1920x1080")
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill="both", expand=True)


#########################################
# 🏛Allergen dictionaries & found_allergens 🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛🏛️🏛️🏛️🏛️🏛️️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛️🏛🏛️🏛️🏛
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
    canvas = tk.Canvas(frame, width=frame.winfo_width(), height=frame.winfo_height(), highlightthickness=0, bg="#c8f61b")
    canvas.pack(fill="both", expand=True)

    # Load the image
    bg_img = Image.open(image_path)

    # Get screen dimensions
    screen_width = frame.winfo_width()
    screen_height = frame.winfo_height()

    # Resize the image proportionally to fit within the screen size (1920x1080)
    img_width, img_height = bg_img.size
    aspect_ratio = img_width / img_height
    if screen_width / screen_height > aspect_ratio:
        # Resize based on screen height
        new_height = screen_height
        new_width = int(new_height * aspect_ratio)
    else:
        # Resize based on screen width
        new_width = screen_width
        new_height = int(new_width / aspect_ratio)

    bg_img = bg_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_img)

    # Add the background image to the canvas with NSEW centering
    canvas.create_image(screen_width // 2, screen_height // 2, image=bg_image)
    canvas.image = bg_image  # Keep a reference to prevent garbage collection

    # Allow widgets to be added on top of the canvas
    frame.canvas = canvas

    # Run the widget setup function, if provided
    if widget_setup_function:
        widget_setup_function(frame)

    return canvas

#############################
# 🏠Page: Home 🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠🏠
#############################
def setup_home_widgets(frame):
    """Sets up widgets for the home page."""
    tk.Button(frame.canvas, text="Next", command=switch_to_clean).place(x=900, y=600)
    tk.Label(frame.canvas, text="Home Page", font=("Helvetica", 24), bg="white").place(x=850, y=500)
    ## add required widgets

def switch_to_home():
    """Switch to the home page."""
    clear_frame(main_frame)
    setup_page_with_background(main_frame, "home.png", setup_home_widgets)

# Add title label
tk.Label(main_frame, text="Step 1: Enter your ingredients", font=("Helvetica", 18), bg="white").pack(pady=20)

# Create the Text widget (textbox) inside the defined area and place it directly under the title
global textbox  # Use global to access `textbox` in other functions
textbox = tk.Text(main_frame, wrap="word", height=11, width=60)
textbox.pack(pady=20)  # Place textbox right under the title with padding

# Set the background and border to make it look like a rectangle
textbox.config(bg="#FFFFFF", bd=4, relief="solid", font=("Helvetica", 15, "bold"), fg="#2f2f2f")

# Clear the text box each time we go back to the Home page (reset the content)
textbox.delete("1.0", "end")

# Insert the placeholder text in the Text widget (textbox) (this acts as the instruction for user)
textbox.insert("1.0", "Paste ingredients here...🌼")

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
next_button = tk.Button(main_frame, text="NEXT", command=lambda: [store_and_print_ingredients(), display_allergenCheck(root, main_frame)])
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
tk.Button(main_frame, text="🙆‍♀️️DISCLAIMER", command=lambda: switch_to_disclaimer(root, main_frame)).pack(pady=10)

# EXIT Button
tk.Button(main_frame, text="🚪Exit program", command=root.quit).pack(pady=10)

#############################
# 🐣️Page: Disclaimer 🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣🐣
#############################
def setup_disclaimer_widgets(frame):
    """Sets up widgets for the disclaimer page."""
    tk.Button(frame, text="🏠", command=lambda: switch_to_home(root, frame)).pack(pady=10)
    tk.Button(frame, text="GO BACK HOME", command=lambda: switch_to_home(root, frame)).pack(pady=10)

def switch_to_disclaimer():
    """Switch to the disclaimer page."""
    clear_frame(main_frame)
    setup_page_with_background(main_frame, "disclaimer.png", setup_disclaimer_widgets)


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

#############################
# 📝Page: Allergen check 📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝📝
#############################
def setup_allergencheck_widgets(frame):
    """Sets up widgets for the allergencheck page."""
    tk.Button(frame, text="🏠", command=lambda: switch_to_home(root, frame)).pack(pady=10)
    tk.Button(frame, text="Go back a step", command=lambda: switch_to_home(root, frame)).pack(pady=10)
    ##add more required widgets

def switch_to_allergencheck():
    """Switch to the allergen check page."""
    clear_frame(main_frame)
    setup_page_with_background(main_frame, "allergencheck.png", setup_allergencheck_widgets)

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

#############################
# 🔍Backend: Allergen checking function 🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍🔍
#############################
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

#############################
# 🪢Backend: Cleaning up strings 🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢🪢
#############################
def clean_string(input_string):
    """Clean up the ingredient and allergen strings by removing non-alphabetic characters and extra spaces"""
    # Remove non-alphabetic characters (except spaces) and lower the case
    cleaned = re.sub(r'[^a-zA-Z\s]', '', input_string)
    # Remove extra spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

#############################
# ✨Page: Results ✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨
#############################
def setup_results_widgets(frame):
    """Sets up widgets for the allergencheck page."""
    ##add required widgets
    ##need to work out function to display correct png background ("if" statement)

def switch_to_results():
    """Switch to the allergen check page."""
    clear_frame(main_frame)
    setup_page_with_background(main_frame, "allergencheck.png", setup_allergencheck_widgets)

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

    # Button to go back
    tk.Button(frame, text="Do another", command=lambda: switch_to_home(root, frame)).pack(pady=10)

    # Button to go back
    tk.Button(frame, text="Do another", command=lambda: switch_to_home(root, frame)).pack(pady=10)

    # Update scroll region when content changes
    content_frame.update_idletasks()

#############################
# 🏁Running the loop 🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁
#############################
root.mainloop()




