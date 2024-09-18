import tkinter as tk
from tkinter import messagebox
import wikipedia
import webbrowser
import speech_recognition as sr
from PIL import Image, ImageTk

wikipedia.set_lang("en")
wikipedia.set_rate_limiting(True)


def get_wikipedia_summary_and_link(place):
    try:
        summary = wikipedia.summary(place, sentences=3)
        page = wikipedia.page(place)
        url = page.url
        return summary, url
    except wikipedia.exceptions.PageError:
        return "Sorry, no information found for the place.", None
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Ambiguous query; multiple results found: {e.options}", None

# Function to search for the place using text or voice input
def search_place():
    place_name = entry.get()
    if not place_name:
        messagebox.showerror("Input Error", "Please enter a place name.")
        return
    summary, url = get_wikipedia_summary_and_link(place_name)
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, summary)
    text_area.config(state=tk.DISABLED)
    if url:
        link_button.config(state=tk.NORMAL)
        link_button.url = url
    else:
        link_button.config(state=tk.DISABLED)
    maps_button.config(state=tk.NORMAL)
    maps_button.url = f"https://www.google.com/maps/search/?api=1&query={place_name.replace(' ', '+')}"

# Function to open the Wikipedia link
def open_link():
    webbrowser.open(link_button.url)

# Function to open the Google Maps link
def open_maps_link():
    webbrowser.open(maps_button.url)


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a place name...")
        try:
            audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            entry.delete(0, tk.END)  # Clear the entry field
            entry.insert(0, text)    # Insert recognized text into the entry field
            search_place()           # Perform the search
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand the audio.")
        except sr.RequestError:
            messagebox.showerror("Error", "Could not request results; check your network connection.")
        except sr.WaitTimeoutError:
            messagebox.showerror("Timeout", "Listening timed out.")


# About dialog
def show_about():
    messagebox.showinfo("About", "Wikipedia Place Search\nVersion 1.0\nDeveloped using Python and Tkinter By DINESH")

# Help dialog
def show_help():
    help_text = ("1. Enter the name of a place in the text field.\n"
                 "2. Click 'Search' to get a summary and Wikipedia link.\n"
                 "3. Alternatively, click 'Search by Voice' to use voice recognition.\n"
                 "4. Use the 'Open Wikipedia Link' to visit the full Wikipedia page.\n"
                 "5. Click 'Search Location on Google Maps' to find the place on Google Maps. contact @ dineshanandhan512@gmail.com")
    messagebox.showinfo("Help", help_text)

# GUI setup
window = tk.Tk()
window.title("Wikipedia Place Search with Google Maps")
window.geometry("700x500")

# Load the background image (Make sure the image path is correct)
bg_image = Image.open("AI image.jpg")  # Replace with your image path
bg_image = bg_image.resize((1200, 1200), Image.LANCZOS)  # Resize the image to fit the window
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label for the background image
bg_label = tk.Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place the background label

# Create a menu bar
menu_bar = tk.Menu(window)

# Add 'About' menu
about_menu = tk.Menu(menu_bar, tearoff=0)
about_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="About", menu=about_menu)

# Add 'Help' menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Help", command=show_help)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Attach the menu bar to the window
window.config(menu=menu_bar)

# Widgets (Place widgets on top of the background image)
label = tk.Label(window, text="Enter the name of a place:", font=("Arial", 14), bg='#2b2b2b', fg='#ffffff')
label.pack(pady=20)

entry = tk.Entry(window, width=40, font=("Arial", 14), bg='#ffffff', fg='#000000', bd=2)
entry.pack(pady=10)

search_button = tk.Button(window, text="Search", font=("Arial", 12), bg='#007acc', fg='#ffffff', activebackground='#005f99', activeforeground='#ffffff', bd=0, padx=10, pady=5, command=search_place)
search_button.pack(pady=10)

voice_button = tk.Button(window, text="Search by Voice", font=("Arial", 12), bg='#ffcc00', fg='#ffffff', activebackground='#ffaa00', activeforeground='#ffffff', bd=0, padx=10, pady=5, command=recognize_speech)
voice_button.pack(pady=10)

text_area = tk.Text(window, height=10, width=70, wrap=tk.WORD, font=("Arial", 12), bg='#e6e6e6', fg='#000000', bd=0, padx=10, pady=10, state=tk.DISABLED)
text_area.pack(pady=10)

link_button = tk.Button(window, text="Open Wikipedia Link", font=("Arial", 12), bg='#ff6f61', fg='#ffffff', activebackground='#ff4436', activeforeground='#ffffff', bd=0, padx=10, pady=5, state=tk.DISABLED, command=open_link)
link_button.pack(pady=10)

maps_button = tk.Button(window, text="Search Location on Google Maps", font=("Arial", 12), bg='#32cd32', fg='#ffffff', activebackground='#28a428', activeforeground='#ffffff', bd=0, padx=10, pady=5, state=tk.DISABLED, command=open_maps_link)
maps_button.pack(pady=10)

window.mainloop()
