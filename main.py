import tkinter as tk
from PIL import Image, ImageTk
from PIL import Image, ImageDraw
import os
from PIL import Image, ImageTk
import tkinter.filedialog
import shutil

root = tk.Tk()
root.geometry("1800x1000")

# Calculate the width of the window and the spacing between the buttons
window_width = 1800
button_width = 100
spacing = (window_width - 4 * button_width) / 5

directory = ""

first_image_file = None
first_image_path = None
first_image = None
first_photo = None

deleted_images = [] 
image_files = []
actions = []

# Create an empty label for the image
image_label = tk.Label(root)
image_label.place(x=window_width/2, y=600, anchor="center")

def delete_image(color):
    global first_image_file, first_image_path, first_image, first_photo, image_files, directory
    # Save the current state before performing the action
    actions.append(('delete', first_image_file, first_image_path, first_image, first_photo))
    if color == "delete" and first_image_file and first_image_path and os.path.exists(first_image_path):
        # Add the deleted image to the stack
        deleted_images.append((first_image_file, first_image_path, first_image, first_photo))
        os.remove(first_image_path)
        if first_image_file in image_files:  # Check that first_image_file is in image_files
            image_files.remove(first_image_file)  # Remove the deleted file from the list
        if image_files:  # If there are any remaining image files
            # Update to the next image
            first_image_file = image_files[0]
            first_image_path = os.path.join(directory, first_image_file)
            first_image = Image.open(first_image_path)
            first_photo = ImageTk.PhotoImage(first_image)
            image_label.config(image=first_photo)
            image_label.image = first_photo
            update_image_count()
        else:
            # If there are no more images, clear the image label
            image_label.config(image=None)
            image_label.image = None


def choose_input_directory():
    global first_image_file, first_image_path, first_image, first_photo, image_files, directory
    directory = tkinter.filedialog.askdirectory()
    if directory:
        files = os.listdir(directory)
        image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg'))]
        if image_files:
            first_image_file = image_files[0]
            first_image_path = os.path.join(directory, first_image_file)
            first_image = Image.open(first_image_path)
            first_photo = ImageTk.PhotoImage(first_image)
            image_label.config(image=first_photo)
            image_label.image = first_photo
            input_directory_label_text.set(f"{os.path.basename(directory)}")

def update_image_count():
    image_count = len(image_files)
    image_count_label.config(text=f"Number of images: {image_count}")

def undo():
    global first_image_file, first_image_path, first_image, first_photo, directory
    if actions:  # If there are any actions to undo
        # Pop the last action from the stack
        action, first_image_file, first_image_path, first_image, first_photo, *extra = actions.pop()
        if action == 'sort':  # If the last action was a sort
            # Move the image back to the input directory
            output_directory = extra[0]
            shutil.move(os.path.join(output_directory, first_image_file), first_image_path)
        # Restore the image file
        first_image.save(first_image_path)
        # Update the label to display the restored image
        first_photo = ImageTk.PhotoImage(first_image)
        image_label.config(image=first_photo)
        image_label.image = first_photo
        update_image_count()

image_count_label = tk.Label(root, text="")
image_count_label.pack()

# Create StringVars for the labels
input_directory_label_text = tk.StringVar()
input_directory_label_text.set("None")

# Create the labels
input_directory_label = tk.Label(root, textvariable=input_directory_label_text)
input_directory_label.place(x=spacing, y=1000)


# Create StringVars for the labels
output_directory_label_text1 = tk.StringVar()
output_directory_label_text1.set("None")

# Create the labels
input_directory_label = tk.Label(root, textvariable=output_directory_label_text1)
input_directory_label.place(x=2*spacing + button_width, y=1050)


# Create StringVars for the labels
output_directory_label_text2 = tk.StringVar()
output_directory_label_text2.set("None")

# Create the labels
input_directory_label = tk.Label(root, textvariable=output_directory_label_text2)
input_directory_label.place(x=3*spacing + 2*button_width, y=1050)


# Create StringVars for the labels
output_directory_label_text3 = tk.StringVar()
output_directory_label_text3.set("None")

# Create the labels
input_directory_label = tk.Label(root, textvariable=output_directory_label_text3)
input_directory_label.place(x=4*spacing + 3*button_width, y=1050)

# Create the "Undo" button
undo_button = tk.Button(root, text="Undo", command=undo)
undo_button.place(x=spacing, y=1100, width=button_width)


# Create a variable for the directory
directory1 = None
directory2 = None
directory3 = None



def choose_sort_directory1():
    global directory1
    directory1 = tkinter.filedialog.askdirectory()
    output_directory_label_text1.set(f"{os.path.basename(directory1)}")
def choose_sort_directory2():
    global directory2
    directory2 = tkinter.filedialog.askdirectory()
    output_directory_label_text2.set(f"{os.path.basename(directory2)}")
def choose_sort_directory3():
    global directory3
    directory3 = tkinter.filedialog.askdirectory()
    output_directory_label_text3.set(f"{os.path.basename(directory3)}")


def sort_image(output_directory):
    global first_image_file, first_image_path, first_image, first_photo, directory
    # Save the current state before performing the action
    actions.append(('sort', first_image_file, first_image_path, first_image, first_photo, output_directory))
    if directory and first_image_file and first_image_path and os.path.exists(first_image_path):
        shutil.move(first_image_path, output_directory)
        print(f"{first_image_file} moved to {output_directory}!")  # Update the print statement to reflect the new directory
        files = os.listdir(directory)
        if first_image_file in image_files:  # Check that first_image_file is in image_files
            image_files.remove(first_image_file)  # Remove the moved file from the list
        if image_files:  # If there are any remaining image files
            # Update to the next image
            first_image_file = image_files[0]
            first_image_path = os.path.join(directory, first_image_file)
            if os.path.exists(first_image_path):
                first_image = Image.open(first_image_path)
                first_photo = ImageTk.PhotoImage(first_image)
                image_label.config(image=first_photo)
                image_label.image = first_photo
                update_image_count()



# Create the buttons
deleteButton = tk.Button(root, text="Delete", command=lambda: delete_image("delete"), fg="red")
deleteButton.place(x=spacing, y=root.winfo_height() - 150, width=button_width, anchor="s")

setMainDir = tk.Button(root, text="InputDir", command=choose_input_directory)
setMainDir.place(x=spacing, y=root.winfo_height() - 200, width=button_width, anchor="s")


button1 = tk.Button(root, text="Send", command=lambda: sort_image(directory1))
button1.place(x=2*spacing + button_width, y=root.winfo_height() - 150, width=button_width, anchor="s")

setButton1 = tk.Button(root, text="outputDir1", command=choose_sort_directory1)
setButton1.place(x=2*spacing + button_width, y=root.winfo_height() - 200, width=button_width, anchor="s")


button2 = tk.Button(root, text="Send", command=lambda: sort_image(directory2))
button2.place(x=3*spacing + 2*button_width, y=root.winfo_height() - 150, width=button_width, anchor="s")

setButton2 = tk.Button(root, text="outputDir2", command=choose_sort_directory2)
setButton2.place(x=3*spacing + 2*button_width, y=root.winfo_height() - 200, width=button_width, anchor="s")


button3 = tk.Button(root, text="Send", command=lambda: sort_image(directory3))
button3.place(x=4*spacing + 3*button_width, y=root.winfo_height() - 150, width=button_width, anchor="s")

setButton3 = tk.Button(root, text="outputDir3", command=choose_sort_directory3)
setButton3.place(x=4*spacing + 3*button_width, y=root.winfo_height() - 200, width=button_width, anchor="s")

root.mainloop()