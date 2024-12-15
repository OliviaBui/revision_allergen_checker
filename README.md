### Revision: Allergen Checker
**Olivia's Python Allergen Checker** – To be reviewed.  
Main focus: running `.png` background files & correcting widget placement.  

---

### Quick-View Questions
1. 🍏Why is print happening but not frame switch? -> in button functions e.g.
          # DISCLAIMER Button
    tk.Button(frame, text="🙆‍♀️️DISCLAIMER", command=lambda: switch_to_disclaimer(Frame)).pack(pady=10)
    print("Navigating to Disclaimer page...") => output is only console print, no root screen change. NOTE: all "display_" has been changed to "switch_to" in "attempt_combination_2.py" file.

2. 🍏Should I revert to a fixed size (with NW alignment) for better widget stability? Would this make alignment easier long-term, even if it’s less dynamic?  
3. 🍏When positioning widgets at specific pixel (x, y) coordinates, will dynamic fullscreen scaling cause misalignment issues?
4. 🍏Is merging the functionalities of `working_base.py` and `working_fullscreen.py` feasible, or should I focus on keeping these separate for simplicity?
     a) how do I set a .png background image (that changes with the matching new frame) in the 'working_base.py' file?
5. 🍏What challenges may I encounter in widget aesthetics and placement on top of the .png background?
      a) should I give up on pretty checkboxes and go for tkinter checkboxes?😵‍💫
      b) should I give up on pretty purple button and go for tkinter button?😮‍💨
6. 🍏Question: Is tailoring 'Do Another' buttons to not wipe ingredients lists worth the effort, or should I just let the application reset and delete any previously entered text whenever going to home (even if it's to 'go back a step')? => this might mean I delete either the '🏠' or 'go back to home' button on the disclaimer & allergen check pages bc they are doubling up visually and functionally if that is the case.
       a)how can I best handle returning to a previous screen without clearing the “enter your ingredients” list - but only for certain buttons? Some button should return to home and CLEAR textbox, but some should NOT CLEAR. Will this be hard to code for? How should I approach this? (probs ask chat gpt....) 
7. 🍏Are there better approaches for testing responsiveness on non-standard screen resolutions (e.g., my MacBook’s display)?
8. 🍏Anything I might be overlooking in this build?
9. 🍏Any essential tips or thoughts for these steps/documents (relfection, video, README, GitHub)?

---

# Note: This is not a proper README. I’m using this document to explain:*  
1. Files outline & required libraries
2. What I’ve already done successfully (for context).  
3. Current issues and what I need help with (ranked by priority).  
4. My plans and next steps from here.  

---

### Part 1: Files Outline & Required Libraries**
Files: 
1. working_base.py: The core functional application (to be submitted as a fallback if needed).
2. working_fullscreen.py: Code for dynamic full-screen background image fitting, demonstrating the ability to create dynamic backgrounds with widgets layered on top.
3. combination_CHATGPT_template.py: A successfully working template integrating function + aesthetic ('working_base.py' + 'working_fullscreen.py'), but widgets + their function must be changed/added + allergen dictionaries need to be added.
5. attempted_combination_2.py: Attempts to custom the above ChatGPT template. Having trouble with background alignment & widget placement + fucntion (not taking to next page, maybe can't to other function like storage too etc.)
           a) attempted_combination.py: A inferior attempt to combine base + fullscreen py's.
7. page.png series (e.g., home.png, disclaimer.png): Blank versions of the background images.
8. full_images folder: Contains the complete versions of the background images, envisioning widget aesthetics and placements.

To run and test the project, you’ll need the following libraries installed:  
- tkinter
- PIL (pillow)  
- fuzzywuzzy
- requests (re)
- python-Levenshtein

---

### Part 2: What I’ve Successfully Done (For Context) 
**File: `working_base.py`**  
This is a fully functioning allergen checker and could easily be the final submission. 
Successful already:  
- Testing input flexibility: Conducted experiments with typos, grammatical errors, spacing, and substring/full-string matching (full-string proved better).  
- Custom ingredient management:  
  - Add ingredients.  
  - Edit ingredients via double-click.  
  - Save changes, delete, or reset custom ingredients.  
  - Scrollable listbox with input bar.  

However, it's ugly. 
I wanted to challenge myself by improving its aesthetics. 
Improvements wanted:  
- 🍏Question: How do I set a .png background image (that changes with the matching new frame) in this file?
- 🍏Question: What challenges may I encounter in widget aesthetics and placement on top of the .png background?
      a) should I give up on pretty checkboxes and go for tKinter checkboxes?😵‍💫
      b) should I give up on pretty purple button and go for tkinter button?😮‍💨
      

**File: `working_fullscreen.py`**   
This file demonstrates launching the .png images in fullscreen mode.
Note: There are two sets of images:
- Blank series: Stored directly in the directory.
- Full series: Located in the full_images folder.
The full series represents the desired appearance of the final design, with widgets placed on top of the background. However, I understand achieving this exact look may not be fully feasible, especially given issues like unattractive checkboxes and unrounded buttons. Using the blank images simplifies the process, as precise alignment with the underlying template is not required.

Successful already: 
- Dynamic responsiveness: Automatically fits screen width, centered (NSEW alignment), without overflow.  
- Background adjustments: A green background accommodates gaps above and below the `.png`.
- Key Discovery: My MacBook’s resolution isn’t standard 16:9 (1920x1080), which initially confused me. However, adapting the app to dynamically fit any screen feels more professional since the marker/tutor could open it on any display.

- 🍏Question: If widgets are positioned at specific pixel (x, y) coordinates, will dynamic scaling cause misalignment issues?

---

### Part 3: Current Issues & What I Need Help With (Ranked by Priority)  
**1. Combining Files (`attempted_combination_2.py`)**  
Goal: 
- Merge `working_base.py` and `working_fullscreen.py`.  
- Retain the functionality of `working_base.py` and `working_fullscreen.py`

- 🍏Question: Should I revert to a fixed size with NW alignment for better widget stability? Would this make alignment easier to manage long-term, even if it looks less dynamic?
- 🍏Why is print happening but not frame switch? -> in button functions e.g.
          # DISCLAIMER Button
    tk.Button(frame, text="🙆‍♀️️DISCLAIMER", command=lambda: switch_to_disclaimer(Frame)).pack(pady=10)
    print("Navigating to Disclaimer page...") => output is only console print, no root screen change. NOTE: all "display_" has been changed to "switch_to" in "attempt_combination_2.py" file.
- 🍏Why are screen suddenly unaligned & separated from widgets compared to the ChatGPT template?

**2. Widget Customization (Stretch Goal)**  
- Customize specific buttons:  
  - Example: Home buttons vs. “Go back one step” buttons.  
  - Users who return to a previous page shouldn’t lose their entered ingredient list when going back to home unless it makes sense ('do another' buttons).

- 🍏Question: Is tailoring 'do another' buttons worth the effort, or should I just let the application reset whenever going to home (even if it's to 'go back a step')? => this might mean I delete either the '🏠' or 'go back to home' button on the disclaimer & allergen check pages bc they are doubling up visually. 

**3. Minor Aesthetic Touches (Stretch Goal)**  
- Fun ideas like a custom cursor or sound effects for mouse clicks.  

---

### **Part 4: Plans & Next Steps**  
- **If unresolved by 5 PM today**: I’ll submit `working_base.py` as the final version.  
- **Submission Requirements**:  
  - A 1,000-word reflection.  
  - A 3-minute video demonstration.  
  - Writing the actual README file and uploading to GitHub.
 
- 🍏Question: Anything I might be overlooking in this build?
- 🍏Question: Any essential tips or thoughts for these steps/documents (relfection, video, README, GitHub)?

---

**THANK YOU SO MUCH FOR YOUR HELP!** Looking forward to wrapping this up turrdayyy🌟.  

---  
