
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from PIL import Image, ImageDraw
import os
from PIL import Image, ImageTk
import tkinter.filedialog
import shutil
import tempfile
import json
import requests
import json
import io
import base64
import string
import random

# Create a temporary directory
temp_dir = tempfile.mkdtemp()

root = tk.Tk()
root.geometry("1800x1000")
root.configure(background='black')

# Calculate the width of the window and the spacing between the buttons
window_width = 1800
# window_height = 1000
button_width = 100
spacing = (window_width - 4 * button_width) / 5

directory = ""


# Path to the JSON file
file_path_default_task = 'defaultTask.json'

data = None


prompt_list_file_path = 'promptList.json'
face_model_params = None

pageExists = False
seed = None
image_metadata = None
first_image_file = None
first_image_path = None
first_image = None
first_photo = None
first_image_info = None

second_image_file = None
second_image_path = None
second_image = None
second_photo = None

third_image_file = None
third_image_path = None
third_image = None
third_photo = None

# display_img1 = None
# display_img2 = None
# display_img3 = None

deleted_images = [] 
image_files = []
actions = []
history = {}
prompt_list = None

upscale_bool = False


image_label = tk.Label(root)
image_label.place(x=window_width/2 - 600, y=0, anchor="n")

second_image_label = tk.Label(root)
second_image_label.place(x=window_width/2, y=0, anchor="n")

third_image_label = tk.Label(root)
third_image_label.place(x=window_width/2 + 600, y=0, anchor="n")



def delete_image(color):
    global first_image_file, first_image_path, first_image, first_photo
    global second_image_file, second_image_path, second_image, second_photo
    global third_image_file, third_image_path, third_image, third_photo
    global directory, image_files, actions

    # Move the first image to the temporary directory
    if os.path.exists(first_image_path):
        first_image.close()
        
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
            third_photo = ImageTk.PhotoImage(resize_image_for_display(third_image_path))
            third_image_label.config(image=third_photo)
            third_image_label.image = third_photo

def resize_image_for_display(input_image_path):
    img = Image.open(input_image_path)
    width, height = img.size
    if width > 512:
        new_height = int(height * 512 / width)
        img = img.resize((512, new_height), Image.LANCZOS)
    return img

def choose_input_directory(from_history = False):
    global first_image_file, first_image_path, first_image, first_photo, first_image_info
    global second_image_file, second_image_path, second_image, second_photo
    global third_image_file, third_image_path, third_image, third_photo
    global image_files, directory
    global display_img1, display_img2, display_img3
    if from_history == False:
        directory = tkinter.filedialog.askdirectory()
    if directory:  # Check if directory is not None
        directory_name = os.path.basename(directory)  # Get the name of the directory
        input_directory_label_text.set(directory_name)
        files = os.listdir(directory)
        image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg'))]
    if image_files:
        # Load the first image
        first_image_file = image_files[0]
        first_image_path = os.path.join(directory, first_image_file)
        first_image = Image.open(first_image_path)
        first_photo = ImageTk.PhotoImage(resize_image_for_display(first_image_path))
        image_label.config(image=first_photo)
        image_label.image = first_photo
        first_image_info = first_image.info

        # Load the second image if it exists
        if len(image_files) > 1:
            second_image_file = image_files[1]
            second_image_path = os.path.join(directory, second_image_file)
            second_image = Image.open(second_image_path)
            second_photo = ImageTk.PhotoImage(resize_image_for_display(second_image_path))
            second_image_label.config(image=second_photo)
            second_image_label.image = second_photo

        # Load the third image if it exists
        if len(image_files) > 2:
            third_image_file = image_files[2]
            third_image_path = os.path.join(directory, third_image_file)
            third_image = Image.open(third_image_path)
            third_photo = ImageTk.PhotoImage(resize_image_for_display(third_image_path))
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
        first_photo = ImageTk.PhotoImage(resize_image_for_display(first_image_path))
        image_label.config(image=first_photo)
        image_label.image = first_photo

        # Load the second image if it exists
        if len(image_files) > 1:
            second_image_file = image_files[1]
            second_image_path = os.path.join(directory, second_image_file)
            second_image = Image.open(second_image_path)
            second_photo = ImageTk.PhotoImage(resize_image_for_display(second_image_path))
            second_image_label.config(image=second_photo)
            second_image_label.image = second_photo

        # Load the third image if it exists
        if len(image_files) > 2:
            third_image_file = image_files[2]
            third_image_path = os.path.join(directory, third_image_file)
            third_image = Image.open(third_image_path)
            third_photo = ImageTk.PhotoImage(resize_image_for_display(third_image_path))
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
    global first_image_file, first_image_path, first_image, first_photo, first_image_info
    global second_image_file, second_image_path, second_image, second_photo
    global third_image_file, third_image_path, third_image, third_photo
    global directory, image_files, actions, data, prompt_list, image_metadata, seed, pageExists

    pageExists = False

    with Image.open(first_image_path) as img:
        # Get the width and height of the image
        image_metadata = img.info
        parameters = image_metadata.get('parameters')

    # If 'parameters' key is not present in the dictionary, parameters will be None
    if parameters is not None:
        # Split the parameters string into individual parameters
        parameters_list = parameters.split(', ')

        # Loop through the parameters to find the seed
        for param in parameters_list:
            if 'Seed' in param:
                seed = int(param.split(': ')[1])  # Extract the seed value and convert it to an integer
                print(f'seed: {seed}')
                break

    else:
        print("No parameters found in image metadata")

    # Load the data from the JSON file
    with open(file_path_default_task, 'r') as file:
        data = json.load(file)

    if upscale_bool == True:
        for function_index in range(5):
            if os.path.isfile(prompt_list_file_path):
                with open(prompt_list_file_path, 'r') as file:
                    prompt_list = json.load(file)
                    pageExists = True
            process_parameters(pageExists, prompt_list, data, function_index)
       
    
    # Save the current state before performing the action
    actions.append(('sort', first_image_file, image_files.index(first_image_file), output_directory))
    if directory and first_image_file and first_image_path and os.path.exists(first_image_path):
        first_image.close()
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
                third_photo = ImageTk.PhotoImage(resize_image_for_display(third_image_path))
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
    update_image_count()
    
def process_parameters(pageExists, prompt_list, data, function_index):
    
    print(f'function_index: {function_index}')
    prompt, negative_prompt, steps, sampler, cfg_scale, size, model_hash, model, lora_hashes, width, height, denoising_strength, task_id = None, None, None, None, None, None, None, None, None, None, None, None, None
    with open(prompt_list_file_path, 'w') as file:

        for item in data:  
            print(f"item: {item}")
            if 'parameters' in item:
                parameters = item['parameters'].split(', ')

                # Initialize an empty dictionary to store parameter variables
                parameter_vars = {}
                # Loop through the parameters
                for param in parameters:
                    key_value = param.split(': ')
                    
                    # Handling cases where parameter is a single value or a key-value pair
                    if len(key_value) == 2:
                        key, value = key_value
                        parameter_vars[key.strip()] = value.strip()
                    else:
                        parameter_vars['param_' + str(index)] = param.strip()

        split_params = first_image_info['parameters'].split('\n')
        for index, part in enumerate(split_params):
            if index == 0:
                prompt = part
            if index == 1:
                negative_prompt = part.lstrip("Negative prompt: ")
            if index == 2:
                key_value_pairs = part.split(', ')
                for pair in key_value_pairs:
                    key, value = pair.split(': ', 1)
                    if 'Prompt' in key:
                        prompt = value
                    if 'Steps' in key:
                        steps = int(value)
                    if 'Sampler' in key:
                        sampler = value
                    if 'CFG scale' in key:
                        cfg_scale = float(value)
                    if 'Seed' in key:
                        seed = int(value)
                    if 'Size' in key:
                        size = value
                        sizeArr = size.split('x')
                        print(f"sizeArr: {sizeArr}")
                        width = int(sizeArr[0])
                        height = int(sizeArr[1])
                    if 'Model hash' in key:
                        model_hash = value
                    if 'Model' in key:
                        model = value
                    if 'Lora Hashes' in key:
                        lora_hashes = value
                
                if function_index == 0:
                    denoising_strength = 0.28
                elif function_index == 1:
                    denoising_strength = 0.38
                elif function_index == 2:
                    denoising_strength = 0.55
                elif function_index == 3:
                    denoising_strength = 0.70
                elif function_index == 4:
                    denoising_strength = 0.85
                data[0]['params']['args']['seed'] = seed
                data[0]['params']['args']['prompt'] = prompt
                data[0]['params']['args']['negative_prompt'] = negative_prompt
                data[0]['params']['args']['steps'] = steps
                data[0]['params']['args']['sampler_name'] = sampler
                data[0]['params']['args']['cfg_scale'] = cfg_scale
                data[0]['params']['args']['height'] = height
                data[0]['params']['args']['width'] = width
                data[0]['params']['args']['denoising_strength'] = denoising_strength
                if not face_model_params:
                    raise Exception("No face model params")
                data[0]['script_params'] = face_model_params

                characters = string.ascii_lowercase + string.digits  # Define the character set

                task_id = ''.join(random.choice(characters) for _ in range(15))
                data[0]['id'] = f'task({task_id})'
                data[0]['params']['args']['id_task'] = f'task({task_id})'
                if pageExists == True:
                    print(f'prompt_list: {prompt_list}')
                    prompt_list.extend(data)
                    json.dump(prompt_list, file)
                else:
                    print(f'data:{data}')
                    json.dump(data, file)

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
    face_model_dropdown.place(x=4*spacing + 3*button_width, y=window_height -(button_height + button_spacing), width=button_width, anchor="s")
    button4.place(x=4*spacing + 3*button_width, y=window_height - (button_height + button_spacing * 2.5), width=button_width, anchor="s")
    button5.place(x=4*spacing + 3*button_width, y=window_height - (button_height + button_spacing * 3.5), width=button_width, anchor="s")

     # Place the labels
    input_directory_label.place(x=spacing - 50, y=window_height - (3 * button_height + button_spacing + 20))
    output_directory_label1.place(x=2*spacing + button_width - 50, y=window_height - (2 * button_height + button_spacing + 20))
    output_directory_label2.place(x=3*spacing + 2*button_width - 50, y=window_height - (2 * button_height + button_spacing + 20))

def set_face_model(event):
    global face_model_dropdown, face_model_params
    with open("face_model_params.json", "r") as file:
        full_face_model_params = json.load(file)
        face_model_text = face_model_dropdown.get()
        output_directory_label_text3.set(face_model_text)

        if face_model_text in full_face_model_params:
            face_model_params = full_face_model_params[face_model_text]

def save_history():
    global history
    history['input_dir'] = directory
    print(f"history['input_dir']: {history['input_dir']}")
    history['output_dir'] = directory1

    history['output_dir2'] = directory2
    history['face_model_params'] = face_model_params
    history['face_model'] = face_model_dropdown.get()
    history['upscale_bool'] = upscale_bool
    print(f"history: {history}")
    with open('history.json', 'w') as file:        
        json.dump(history, file)

def load_history():
    global history, directory, directory1, directory2, face_model_params, upscale_bool
    with open('history.json', 'r') as file:
        history = json.load(file)
        print(f"history: {history}")
        if 'input_dir' in history and history['input_dir'] != None:
            directory = history['input_dir']
            input_directory_label_text.set(f"{os.path.basename(directory)}")
        if 'output_dir' in history and history['output_dir'] != None:
            directory1 = history['output_dir']
            output_directory_label_text1.set(f"{os.path.basename(directory1)}")
        if 'output_dir2' in history and history['output_dir2'] != None:
            directory2 = history['output_dir2']
            output_directory_label_text2.set(f"{os.path.basename(directory2)}")
        if 'face_model' in history and history['face_model'] != None:
            face_model_params = history['face_model_params']
            face_model_dropdown.set(f"{history['face_model']}")
        if 'upscale_bool' in history and history['upscale_bool'] != None:
            upscale_bool = history['upscale_bool']
            if upscale_bool == True:
                button3.config(bg="green", fg="white")
                button3.config(activebackground='red', activeforeground='grey')
            else:    
                button3.config(bg="red", fg="grey")
                button3.config(activebackground='green', activeforeground='white')
        choose_input_directory(True)

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

def toggle_button3(event=None):
    global upscale_bool
    # Check the current color of the button
    if upscale_bool == True:
        upscale_bool = False
        button3.config(bg="red", fg="grey")
        button3.config(activebackground='green', activeforeground='white')
    else:
        upscale_bool = True
        button3.config(bg="green", fg="white")
        button3.config(activebackground='red', activeforeground='grey')
# button3
button3 = tk.Button(root, text="Upscale", command=toggle_button3, activebackground="green", activeforeground="white")
button3.place(x=4*spacing + 3*button_width, y=window_height - button_height , width=button_width, anchor="s")
button3.config(bg="red", fg="grey")
 
button4 = tk.Button(root, text="Save", command=save_history, activebackground="green", activeforeground="white")
button4.place(x=4*spacing + 3*button_width, y=window_height - button_height, width=button_width, anchor="s")

button5 = tk.Button(root, text="Load", command=load_history, activebackground="green", activeforeground="white")
button5.place(x=4*spacing + 3*button_width, y=window_height - button_height, width=button_width, anchor="s")

# face_model_dropdown
# Read the keys from the JSON file
face_model_keys = []
with open('face_model_params.json') as f:
    face_model_data = json.load(f)
face_model_keys = list(face_model_data.keys())
# Create a StringVar to hold the selected value
selected_key = tk.StringVar()

# Create the dropdown
face_model_dropdown = ttk.Combobox(root, textvariable=selected_key)

# Populate the dropdown with the keys
face_model_dropdown['values'] = face_model_keys

# Set the first key as the initially selected value
if face_model_keys:
    face_model_dropdown.current(0)

face_model_dropdown.bind("<<ComboboxSelected>>", set_face_model)
set_face_model(event=None)
# Place the dropdown in the window
face_model_dropdown.place(x=4*spacing + 3*button_width, y=window_height -(button_height + button_spacing), width=800, height=50, anchor="s")


root.bind('<Configure>', update_button_positions)

root.mainloop()