from tkinter import Tk, Canvas, Frame, Button, Label
from PIL import Image, ImageTk

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
    canvas = Canvas(frame, width=frame.winfo_width(), height=frame.winfo_height(), highlightthickness=0, bg="#c8f61b")
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


def setup_home_widgets(frame):
    """Sets up widgets for the home page."""
    Button(frame.canvas, text="Next", command=switch_to_clean).place(x=900, y=600)
    Label(frame.canvas, text="Home Page", font=("Helvetica", 24), bg="white").place(x=850, y=500)


def setup_clean_widgets(frame):
    """Sets up widgets for the clean page."""
    Button(frame.canvas, text="Next", command=switch_to_allergencheck).place(x=900, y=600)
    Label(frame.canvas, text="Clean Page", font=("Helvetica", 24), bg="white").place(x=850, y=500)


def setup_allergencheck_widgets(frame):
    """Sets up widgets for the allergencheck page."""
    Button(frame.canvas, text="Next", command=switch_to_notclean).place(x=900, y=600)
    Label(frame.canvas, text="Allergen Check", font=("Helvetica", 24), bg="white").place(x=850, y=500)


def setup_notclean_widgets(frame):
    """Sets up widgets for the not clean page."""
    Button(frame.canvas, text="Next", command=switch_to_disclaimer).place(x=900, y=600)
    Label(frame.canvas, text="Not Clean Page", font=("Helvetica", 24), bg="white").place(x=850, y=500)


def setup_disclaimer_widgets(frame):
    """Sets up widgets for the disclaimer page."""
    Button(frame.canvas, text="Finish", command=root.quit).place(x=900, y=600)
    Label(frame.canvas, text="Disclaimer Page", font=("Helvetica", 24), bg="white").place(x=850, y=500)


def switch_to_page(frame, image_path, widget_setup_function):
    """Switches to a new page with a given background and widgets."""
    setup_page_with_background(frame, image_path, widget_setup_function)


def switch_to_home():
    """Switch to the home page."""
    setup_page_with_background(main_frame, "home.png", setup_home_widgets)


def switch_to_clean():
    """Switch to the clean page."""
    setup_page_with_background(main_frame, "clean.png", setup_clean_widgets)


def switch_to_allergencheck():
    """Switch to the allergen check page."""
    setup_page_with_background(main_frame, "allergencheck.png", setup_allergencheck_widgets)


def switch_to_notclean():
    """Switch to the not clean page."""
    setup_page_with_background(main_frame, "notclean.png", setup_notclean_widgets)


def switch_to_disclaimer():
    """Switch to the disclaimer page."""
    setup_page_with_background(main_frame, "disclaimer.png", setup_disclaimer_widgets)


# Main application setup
if __name__ == "__main__":
    root = Tk()
    root.attributes('-fullscreen', True)  # Set the window to full screen automatically

    # Create a main frame to manage content
    main_frame = Frame(root)
    main_frame.pack(fill="both", expand=True)

    # Set the initial home page when the app starts
    root.after(1, switch_to_home)  # Call switch_to_home with a slight delay to ensure the window is ready

    root.mainloop()
