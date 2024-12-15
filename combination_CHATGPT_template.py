from tkinter import Tk, Canvas, Frame, Button, Label
from PIL import Image, ImageTk

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


# Widget setup functions for each page
def setup_home_widgets(frame):
    Label(frame.canvas, text="Welcome to the Home Page!", font=("Helvetica", 18), bg="white").place(x=850, y=400)
    Button(frame.canvas, text="Go to Allergen Check", command=lambda: switch_to_allergencheck()).place(x=850, y=500)
    Button(frame.canvas, text="Exit", command=root.quit).place(x=850, y=550)


def setup_allergencheck_widgets(frame):
    Label(frame.canvas, text="Allergen Check Page", font=("Helvetica", 18), bg="white").place(x=850, y=400)
    Button(frame.canvas, text="Go to Clean", command=lambda: switch_to_clean()).place(x=850, y=500)
    Button(frame.canvas, text="Go to Home", command=lambda: switch_to_home()).place(x=850, y=550)


def setup_clean_widgets(frame):
    Label(frame.canvas, text="Clean Page", font=("Helvetica", 18), bg="white").place(x=850, y=400)
    Button(frame.canvas, text="Go to Not Clean", command=lambda: switch_to_notclean()).place(x=850, y=500)
    Button(frame.canvas, text="Go to Home", command=lambda: switch_to_home()).place(x=850, y=550)


def setup_notclean_widgets(frame):
    Label(frame.canvas, text="Not Clean Page", font=("Helvetica", 18), bg="white").place(x=850, y=400)
    Button(frame.canvas, text="Go to Disclaimer", command=lambda: switch_to_disclaimer()).place(x=850, y=500)
    Button(frame.canvas, text="Go to Home", command=lambda: switch_to_home()).place(x=850, y=550)


def setup_disclaimer_widgets(frame):
    Label(frame.canvas, text="Disclaimer Page", font=("Helvetica", 18), bg="white").place(x=850, y=400)
    Button(frame.canvas, text="Finish", command=root.quit).place(x=850, y=500)
    Button(frame.canvas, text="Go to Home", command=lambda: switch_to_home()).place(x=850, y=550)


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
    setup_page_with_background(main_frame, "disclaimer.png", setup_disclaimer_widgets)


# Main application setup
if __name__ == "__main__":
    root = Tk()
    root.attributes('-fullscreen', True)  # Fullscreen mode

    main_frame = Frame(root)
    main_frame.pack(fill="both", expand=True)

    # Start with the home page
    root.after(1, switch_to_home)

    root.mainloop()
