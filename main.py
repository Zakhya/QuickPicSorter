
import tkinter as tk
from PIL import Image, ImageTk
from PIL import Image, ImageDraw
import os
from PIL import Image, ImageTk
import tkinter.filedialog
import shutil
import tempfile

# Create a temporary directory
temp_dir = tempfile.mkdtemp()

root = tk.Tk()
root.geometry("1800x1000")


# Calculate the width of the window and the spacing between the buttons
window_width = 1800
# window_height = 1000
button_width = 100
spacing = (window_width - 4 * button_width) / 5

directory = ""

first_image_file = None
first_image_path = None
first_image = None
first_photo = None

second_image_file = None
second_image_path = None
second_image = None
second_photo = None

third_image_file = None
third_image_path = None
third_image = None
third_photo = None

deleted_images = [] 
image_files = []
actions = []

# Create an empty label for the image
image_label = tk.Label(root)
image_label.place(x=window_width/2 - 600, y=600, anchor="center")

# Create two more labels for the additional images
second_image_label = tk.Label(root)
second_image_label.place(x=window_width/2, y=600, anchor="center")

third_image_label = tk.Label(root)
third_image_label.place(x=window_width/2 + 600, y=600, anchor="center")


def delete_image(color):
    global first_image_file, first_image_path, first_image, first_photo
    global second_image_file, second_image_path, second_image, second_photo
    global third_image_file, third_image_path, third_image, third_photo
    global directory, image_files, actions

    # Move the first image to the temporary directory
    if os.path.exists(first_image_path):
        shutil.move(first_image_path, os.path.join(temp_dir, first_image_file))

        # Store the action in the actions list
        actions.append(('delete', first_image_file, image_files.index(first_image_file), directory)) 

        # Remove the deleted image from the list
        if first_image_file in image_files:
            image_files.remove(first_image_file)

        # Shift the second image to the first position
        first_image_file = second_image_file
        first_image_path = second_image_path
        first_image = second_image
        first_photo = second_photo
        image_label.config(image=first_photo)
        image_label.image = first_photo

        # Shift the third image to the second position
        second_image_file = third_image_file
        second_image_path = third_image_path
        second_image = third_image
        second_photo = third_photo
        second_image_label.config(image=second_photo)
        second_image_label.image = second_photo

        # Load the next image into the third position
        if len(image_files) > 2:
            third_image_file = image_files[2]
            third_image_path = os.path.join(directory, third_image_file)
            third_image = Image.open(third_image_path)
            third_photo = ImageTk.PhotoImage(third_image)
            third_image_label.config(image=third_photo)
            third_image_label.image = third_photo

def choose_input_directory():
    global first_image_file, first_image_path, first_image, first_photo
    global second_image_file, second_image_path, second_image, second_photo
    global third_image_file, third_image_path, third_image, third_photo
    global image_files, directory

    directory = tkinter.filedialog.askdirectory()
    if directory:
        files = os.listdir(directory)
        image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg'))]
        if image_files:
            # Load the first image
            first_image_file = image_files[0]
            first_image_path = os.path.join(directory, first_image_file)
            first_image = Image.open(first_image_path)
            first_photo = ImageTk.PhotoImage(first_image)
            image_label.config(image=first_photo)
            image_label.image = first_photo

            # Load the second image if it exists
            if len(image_files) > 1:
                second_image_file = image_files[1]
                second_image_path = os.path.join(directory, second_image_file)
                second_image = Image.open(second_image_path)
                second_photo = ImageTk.PhotoImage(second_image)
                second_image_label.config(image=second_photo)
                second_image_label.image = second_photo

            # Load the third image if it exists
            if len(image_files) > 2:
                third_image_file = image_files[2]
                third_image_path = os.path.join(directory, third_image_file)
                third_image = Image.open(third_image_path)
                third_photo = ImageTk.PhotoImage(third_image)
                third_image_label.config(image=third_photo)
                third_image_label.image = third_photo

def update_image_count():
    image_count = len(image_files)
    image_count_label.config(text=f"Number of images: {image_count}")

def load_next_image():
    global first_image_file, first_image_path, first_image, first_photo
    global second_image_file, second_image_path, second_image, second_photo
    global third_image_file, third_image_path, third_image, third_photo
    global directory

    # Get the list of image files from the directory
    files = os.listdir(directory)
    image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg'))]

    if image_files:
        # Load the first image
        first_image_file = image_files[0]
        first_image_path = os.path.join(directory, first_image_file)
        first_image = Image.open(first_image_path)
        first_photo = ImageTk.PhotoImage(first_image)
        image_label.config(image=first_photo)
        image_label.image = first_photo

        # Load the second image if it exists
        if len(image_files) > 1:
            second_image_file = image_files[1]
            second_image_path = os.path.join(directory, second_image_file)
            second_image = Image.open(second_image_path)
            second_photo = ImageTk.PhotoImage(second_image)
            second_image_label.config(image=second_photo)
            second_image_label.image = second_photo

        # Load the third image if it exists
        if len(image_files) > 2:
            third_image_file = image_files[2]
            third_image_path = os.path.join(directory, third_image_file)
            third_image = Image.open(third_image_path)
            third_photo = ImageTk.PhotoImage(third_image)
            third_image_label.config(image=third_photo)
            third_image_label.image = third_photo

def undo():
    global first_image_file, first_image_path, first_image, first_photo
    global second_image_file, second_image_path, second_image, second_photo
    global third_image_file, third_image_path, third_image, third_photo
    global directory, image_files, actions

    if actions:
        action = actions.pop()
        action_type, image_file, original_index, sorted_dir = action

        if action_type == 'delete':
            # If the action was a delete, move the image back to the original directory and add it back to the image_files list at its original index
            shutil.move(os.path.join(temp_dir, image_file), os.path.join(directory, image_file))
            image_files.insert(original_index, image_file)

        elif action_type == 'sort':
            # If the action was a sort, move the image back to the original directory and add it back to the image_files list at its original index
            shutil.move(os.path.join(sorted_dir, image_file), os.path.join(directory, image_file))
            image_files.insert(original_index, image_file)

        # Load the next image
        load_next_image()

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
output_directory_label1 = tk.Label(root, textvariable=output_directory_label_text1)
output_directory_label1.place(x=2*spacing + button_width, y=1050)


# Create StringVars for the labels
output_directory_label_text2 = tk.StringVar()
output_directory_label_text2.set("None")

# Create the labels
output_directory_label2 = tk.Label(root, textvariable=output_directory_label_text2)
output_directory_label2.place(x=3*spacing + 2*button_width, y=1050)


# Create StringVars for the labels
output_directory_label_text3 = tk.StringVar()
output_directory_label_text3.set("None")

# Create the labels
output_directory_label3 = tk.Label(root, textvariable=output_directory_label_text3)
output_directory_label3.place(x=4*spacing + 3*button_width, y=1050)



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
    global first_image_file, first_image_path, first_image, first_photo
    global second_image_file, second_image_path, second_image, second_photo
    global third_image_file, third_image_path, third_image, third_photo
    global directory, image_files, actions

    # Save the current state before performing the action
    actions.append(('sort', first_image_file, image_files.index(first_image_file), output_directory))
    if directory and first_image_file and first_image_path and os.path.exists(first_image_path):
        shutil.move(first_image_path, output_directory)
        print(f"{first_image_file} moved to {output_directory}!")  # Update the print statement to reflect the new directory
        if first_image_file in image_files:  # Check that first_image_file is in image_files
            image_files.remove(first_image_file)  # Remove the moved file from the list
        if image_files:  # If there are any remaining image files
            # Shift the second image to the first position
            first_image_file = second_image_file
            first_image_path = second_image_path
            first_image = second_image
            first_photo = second_photo
            image_label.config(image=first_photo)
            image_label.image = first_photo

            # Shift the third image to the second position
            second_image_file = third_image_file
            second_image_path = third_image_path
            second_image = third_image
            second_photo = third_photo
            second_image_label.config(image=second_photo)
            second_image_label.image = second_photo

            # Load a new image into the third position
            if len(image_files) > 2:
                third_image_file = image_files[2]
                third_image_path = os.path.join(directory, third_image_file)
                third_image = Image.open(third_image_path)
                third_photo = ImageTk.PhotoImage(third_image)
                third_image_label.config(image=third_photo)
                third_image_label.image = third_photo

            update_image_count()
        else:
            # If there are no more images, clear the image labels
            image_label.config(image=None)
            image_label.image = None
            second_image_label.config(image=None)
            second_image_label.image = None
            third_image_label.config(image=None)
            third_image_label.image = None


def update_button_positions(event=None):
    # Get the new window height
    global window_height
    window_height = root.winfo_height()

  # Place the buttons
    undo_button.place(x=spacing, y=window_height -(button_height + button_spacing), width=button_width, anchor="s")
    deleteButton.place(x=spacing, y=window_height - button_height, width=button_width, anchor="s")
    setMainDir.place(x=spacing, y=window_height - (2 * button_height + button_spacing), width=button_width, anchor="s")
    button1.place(x=2*spacing + button_width, y=window_height - button_height, width=button_width, anchor="s")
    setButton1.place(x=2*spacing + button_width, y=window_height -(button_height + button_spacing), width=button_width, anchor="s")
    button2.place(x=3*spacing + 2*button_width, y=window_height - button_height, width=button_width, anchor="s")
    setButton2.place(x=3*spacing + 2*button_width, y=window_height -(button_height + button_spacing), width=button_width, anchor="s")
    button3.place(x=4*spacing + 3*button_width, y=window_height - button_height , width=button_width, anchor="s")
    setButton3.place(x=4*spacing + 3*button_width, y=window_height -(button_height + button_spacing), width=button_width, anchor="s")

     # Place the labels
    input_directory_label.place(x=spacing - 50, y=window_height - (3 * button_height + button_spacing + 20))
    output_directory_label1.place(x=2*spacing + button_width - 50, y=window_height - (2 * button_height + button_spacing + 20))
    output_directory_label2.place(x=3*spacing + 2*button_width - 50, y=window_height - (2 * button_height + button_spacing + 20))
    output_directory_label3.place(x=4*spacing + 3*button_width - 50, y=window_height - (2 * button_height + button_spacing + 20))

# Delay the placement of the buttons until after the window is displayed
root.after(100, update_button_positions)

# Assuming you have 8 buttons
button_height = 50
button_spacing = 50

window_height = root.winfo_height()

# Create the "Undo" button
undo_button = tk.Button(root, text="Undo", command=undo)
undo_button.place(x=spacing, y=window_height -(button_height + button_spacing), width=button_width, anchor="s")

# deleteButton
deleteButton = tk.Button(root, text="Delete", command=lambda: delete_image("delete"), fg="red")
deleteButton.place(x=spacing, y=window_height - button_height, width=button_width, anchor="s")

# setMainDir
setMainDir = tk.Button(root, text="InputDir", command=choose_input_directory)
setMainDir.place(x=spacing, y=window_height - (2 * button_height + button_spacing), width=button_width, anchor="s")

# button1
button1 = tk.Button(root, text="Send", command=lambda: sort_image(directory1))
button1.place(x=2*spacing + button_width, y=window_height - button_height, width=button_width, anchor="s")

# setButton1
setButton1 = tk.Button(root, text="outputDir1", command=choose_sort_directory1)
setButton1.place(x=2*spacing + button_width, y=window_height -(button_height + button_spacing), width=button_width, anchor="s")

# button2
button2 = tk.Button(root, text="Send", command=lambda: sort_image(directory2))
button2.place(x=3*spacing + 2*button_width, y=window_height - button_height, width=button_width, anchor="s")

# setButton2
setButton2 = tk.Button(root, text="outputDir2", command=choose_sort_directory2)
setButton2.place(x=3*spacing + 2*button_width, y=window_height -(button_height + button_spacing), width=button_width, anchor="s")

# button3
button3 = tk.Button(root, text="Send", command=lambda: sort_image(directory3))
button3.place(x=4*spacing + 3*button_width, y=window_height - button_height , width=button_width, anchor="s")

# setButton3
setButton3 = tk.Button(root, text="outputDir3", command=choose_sort_directory3)
setButton3.place(x=4*spacing + 3*button_width, y=window_height -(button_height + button_spacing), width=button_width, anchor="s")


root.bind('<Configure>', update_button_positions)

root.mainloop()