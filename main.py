
import tkinter as tk
from tkinter import ttk
import random
import os
import tkinter.filedialog
import shutil
import tempfile
import json
import string
from PIL import Image, ImageTk

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
# Load the data from the JSON file
with open(file_path_default_task, 'r') as file:
    data = json.load(file)

page_name = "main"


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

undo_button = None
deleteButton = None
setMainDir = None
button1 = None
setButton1 = None
button2 = None
setButton2 = None
button3 = None
button4 = None
button5 = None
button6 = None
face_model_dropdown = None

prompt_positive_text_box = ''
prompt_negative_text_box = ''
prompt_steps_text_box = 25
prompt_sampler_text_box = 'DPM++ 2M SDE Karras'
prompt_cfg_scale_text_box = 7.5
prompt_size_height_box = 512
prompt_size_width_box = 512
prompt_id = None
prompt_n_iterations = 1
prompt_seed = -1
prompt_batch_size = 1
prompt_checkpoint = 'dreamshaper_8.safetensors [879db523c3]'
prompt_custom_params = None

PROMPT_POSITIVE_DEFAULT = ''
PROMPT_NEGATIVE_DEFAULT = ''
PROMPT_STEPS_DEFAULT = tk.IntVar()
PROMPT_STEPS_DEFAULT.set(34)
PROMPT_SAMPLER_DEFAULT = 'DPM++ 2M SDE Karras'
PROMPT_CFG_SCALE_DEFAULT = tk.DoubleVar()
PROMPT_CFG_SCALE_DEFAULT.set(4.5)
PROMPT_SIZE_HEIGHT_DEFAULT = tk.IntVar()
PROMPT_SIZE_HEIGHT_DEFAULT.set(1024)
PROMPT_SIZE_WIDTH_DEFAULT = tk.IntVar()
PROMPT_SIZE_WIDTH_DEFAULT.set(512)
PROMPT_ID_DEFAULT = None
PROMPT_N_ITERATIONS_DEFAULT = tk.IntVar()
PROMPT_N_ITERATIONS_DEFAULT.set(1)
PROMPT_SEED_DEFAULT = tk.IntVar()
PROMPT_SEED_DEFAULT.set(-1)
PROMPT_BATCH_SIZE_DEFAULT = tk.IntVar()
PROMPT_BATCH_SIZE_DEFAULT.set(1)
PROMPT_CHECKPOINT_DEFAULT = 'dreamshaper_8.safetensors [879db523c3]'
PROMPT_CUSTOM_PARAMS_DEFAULT ='eJzNU0tv1DAQTtTN7nYfLV0Q78cee6GCnrhVdBGViJQDEsfK8iZmxyKxLcfZrZCQOMbIR3OAX8eVXwGThwCpfwAnGWsm45lvvhl/Hnz9she069Ifx4F1gb84+/mtWd/f/MJlWxkHzfPJH7sRL0kqmPG1GzFB1znLvHXDQmZVzrwbCClwi1BnOapJqw53jG/A+Dh0ES/ohvnETTUr+UdGGk/vDldaqiUV2fJta/ZunMsd2WpaYPi50jJlZSk1wVO+heSmBlABmWeEXjete9PBpuIZFSkjpaEaIQRu9sfERNZgmit+xXKimH7PUoP5ZqkURsu8Bzc+p3njn3lwtFuTAkRbwElcqQriLr9kETqQyXAgs/lwa8OyrplpGMGYzLMlJQhbwtaLZtw5GOFi42yEeExFYcf0+6qF3qYckL1RA7W1OTQper9BC6iaxM45dx3ahIl1Rrmn7wtsI+wV4NAwtR3xAY9a2A/TiESQLT64zD3MJBSxocdtuNbjuKA1jgsZsWbv3DBdy2cKcvFO7VcD+BBzU8hEfwGEJ4gt/yv4KSWBc+8/DULbgod1Rhu8nz0xcnUogr7yYr5Pu11AXTOBJ1jzEO49DWKHH67cXZj+6q1NYNVu9evfQWp6kvJkysdWMlS274trkBqSwKiuOG5qgbPcBgEF6i7a+srcUgNkn6Nz5lJ78BBUFmzA=='

prompt_positive_text_box_label = None
prompt_negative_text_box_label = None
prompt_steps_text_box_label = None
prompt_sampler_text_box_label = None
prompt_cfg_scale_text_box_label = None
prompt_size_height_box_label = None
prompt_size_width_box_label = None
prompt_id_label = None
prompt_n_iterations_label = None
prompt_seed_label = None
prompt_batch_size_label = None
prompt_checkpoint_label = None
prompt_custom_params_label = None
sampler_dropdown = None


prompt_positive_radio_button = tk.StringVar()
prompt_positive_radio_front = tk.Radiobutton(root, text="front", variable=prompt_positive_radio_button, value="front")
prompt_positive_radio_none = tk.Radiobutton(root, text="none", variable=prompt_positive_radio_button, value="none")
prompt_positive_radio_back = tk.Radiobutton(root, text="end", variable=prompt_positive_radio_button, value="end")


prompt_negative_radio_button = tk.StringVar()
prompt_negative_radio_front = tk.Radiobutton(root, text="front", variable=prompt_negative_radio_button, value="front")
prompt_negative_radio_none = tk.Radiobutton(root, text="none", variable=prompt_negative_radio_button, value="none")
prompt_negative_radio_back = tk.Radiobutton(root, text="end", variable=prompt_negative_radio_button, value="end")

prompt_checkpoint_var = tk.IntVar()
prompt_checkpoint_checkbox = tk.Checkbutton(root, variable=prompt_checkpoint_var)
prompt_positive_var = tk.IntVar()
prompt_positive_checkbox = tk.Checkbutton(root, variable=prompt_positive_var)
prompt_negative_var = tk.IntVar()
prompt_negative_checkbox = tk.Checkbutton(root, variable=prompt_negative_var)
prompt_steps_var = tk.IntVar()
prompt_steps_checkbox = tk.Checkbutton(root, variable=prompt_steps_var)
prompt_sampler_var = tk.IntVar()
prompt_sampler_checkbox = tk.Checkbutton(root, variable=prompt_sampler_var)
prompt_cfg_scale_var = tk.IntVar()
prompt_cfg_scale_checkbox = tk.Checkbutton(root, variable=prompt_cfg_scale_var)
prompt_size_height_var = tk.IntVar()
prompt_size_height_checkbox = tk.Checkbutton(root, variable=prompt_size_height_var)
prompt_size_width_var = tk.IntVar()
prompt_size_width_checkbox = tk.Checkbutton(root, variable=prompt_size_width_var)
prompt_iterations_var = tk.IntVar()
prompt_iterations_checkbox = tk.Checkbutton(root, variable=prompt_iterations_var)
prompt_batch_size_var = tk.IntVar()
prompt_batch_size_checkbox = tk.Checkbutton(root, variable=prompt_batch_size_var)
prompt_seed_var = tk.IntVar()
prompt_seed_checkbox = tk.Checkbutton(root, variable=prompt_seed_var)
prompt_custom_params_var = tk.IntVar()
prompt_custom_params_checkbox = tk.Checkbutton(root, variable=prompt_custom_params_var)

prompt_new_variations = {}
labels_and_Checkbuttons = {}
variations_checkbox_vars = []
prompt_add_variation_text_box = tk.Text(root, width=50, height=1)

variation_data = None
if os.path.isfile('variations.json'):
    with open('variations.json', 'r') as file:
        variation_data = json.load(file)
cfg_spinbox = None

samplers_object = (
    'DPM++ 2M Karras',
    'DPM++ SDE Karras',
    'DPM++ 2M SDE Exponential',
    'DPM++ 2M SDE Karras',
    'Euler a',
    'Euler',
    'LMS',
    'Heun',
    'DPM2',
    'DPM2 A',
    'DPM++ 2S a',
    'DPM++ 2M',
    'DPM SDE',
    'DPM 2M SDE',
    'DPM++ 2M SDE Heun',
    'DPM++ 2M SDE Heun Karras',
    'DPM++ 2M SDE Heun Exponential',
    'DPM++ 3M SDE',
    'DPM++ 3M SDE Karras',
    'DPM++ 3M SDE Exponential',
    'DPM fast',
    'DPM adaptive',
    'LMS Karras',
    'DPM2 Karras',
    'DPM2 a Karras',
    'DPM++ 2S a Karras',
    'restart',
    'DDIM',
    'PLMS',
    'UniPC'
)

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

def delete_image():
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
    update_image_count()

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

image_count_label = None
input_directory_label_text = None
input_directory_label = None
output_directory_label_text1 = None
output_directory_label1 = None
output_directory_label_text2 = None
output_directory_label2 = None
output_directory_label_text3 = None



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


    if upscale_bool == True:
        for function_index in range(5):
            if os.path.isfile(prompt_list_file_path):
                with open(prompt_list_file_path, 'r') as file:
                    prompt_list = json.load(file)
                    pageExists = True
            process_parameters(pageExists, prompt_list, data, function_index, False)

    # Save the current state before performing the action
    actions.append(('sort', first_image_file, image_files.index(first_image_file),output_directory))
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
    
def process_parameters(pageExists, prompt_list, prompt_data, function_index, from_prompt_window):
    prompt, negative_prompt, steps, sampler, cfg_scale, size, model_hash, model, lora_hashes, width, height, denoising_strength, task_id = None, None, None, None, None, None, None, None, None, None, None, None, None
    global variation_data
    if os.path.isfile('variations.json'):
        with open('variations.json', 'r') as file:
            variation_data = json.load(file)
            print(f"line 502 variation_data: {variation_data}")

    if from_prompt_window == False:
        with open(prompt_list_file_path, 'w') as file:
            for item in prompt_data:  
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
                        if 'enable_hr' in key and upscale_bool == False:
                            data[0]['params']['args']['enable_hr'] = False

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
    else:
        with open(prompt_list_file_path, 'w') as file:
            data[0]['params']['args']['enable_hr'] = False

            # data[0]['params']['args']['prompt'] = prompt_positive_text_box.get('1.0', 'end-1c')
            # data[0]['params']['args']['negative_prompt'] = prompt_negative_text_box.get('1.0', 'end-1c')

            negative_text = prompt_negative_text_box.get('1.0', 'end-1c')
            positive_text = prompt_positive_text_box.get('1.0', 'end-1c')

            if function_index is not None and 'positive_front' in variation_data[function_index]:
                # Combine positive_front with the text from prompt_positive_text_box
                combined_positive_text = variation_data[function_index]['positive_front'] + " " + positive_text
                data[0]['params']['args']['prompt'] = combined_positive_text
            elif function_index is not None and 'positive_back' in variation_data[function_index]:
                # Combine positive_back with the text from prompt_positive_text_box
                combined_positive_text = positive_text + " " + variation_data[function_index]['positive_back']
                data[0]['params']['args']['prompt'] = combined_positive_text
            else:
                data[0]['params']['args']['prompt'] = positive_text

            if function_index is not None and 'negative_front' in variation_data[function_index]:
                # Combine negative_front with the text from prompt_negative_text_box
                combined_negative_text = variation_data[function_index]['negative_front'] + " " + negative_text
                data[0]['params']['args']['negative_prompt'] = combined_negative_text
            elif function_index is not None and 'negative_back' in variation_data[function_index]:
                # Combine negative_back with the text from prompt_negative_text_box
                combined_negative_text = negative_text + " " + variation_data[function_index]['negative_back']
                data[0]['params']['args']['negative_prompt'] = combined_negative_text
            else:
                data[0]['params']['args']['negative_prompt'] = negative_text

            print(f"line 594 variation_data: {variation_data}")
            print(f"line 595 function_index: {function_index}")
            if function_index is not None and 'steps' in variation_data[function_index]:
                steps_value = variation_data[function_index]['steps']
            else:
                steps_value = int(prompt_steps_text_box.get())
            data[0]['params']['args']['steps'] = int(steps_value)

            if function_index is not None and 'sampler' in variation_data[function_index]:
                sampler_value = variation_data[function_index]['sampler']
            else:
                sampler_value = sampler_dropdown.get()  
            data[0]['params']['args']['sampler_name'] = sampler_value

            if function_index is not None and 'cfg_scale' in variation_data[function_index]:
                cfg_scale_value = variation_data[function_index]['cfg_scale']
            else:
                cfg_scale_value = float(cfg_spinbox.get())
            data[0]['params']['args']['cfg_scale'] = float(cfg_scale_value)

            if function_index is not None and 'height' in variation_data[function_index]:
                height_value = variation_data[function_index]['height']
            else:   
                height_value = int(prompt_size_height_box.get())
            data[0]['params']['args']['height'] = int(height_value)

            if function_index is not None and 'width' in variation_data[function_index]:
                width_value = variation_data[function_index]['width']
            else:
                width_value = int(prompt_size_width_box.get())
            data[0]['params']['args']['width'] = int(width_value)
            
            if function_index is not None and 'n_iter' in variation_data[function_index]:
                n_iter_value = variation_data[function_index]['n_iter']
            else:
                n_iter_value = int(prompt_n_iterations.get())
            data[0]['params']['args']['n_iter'] = int(n_iter_value)

            if function_index is not None and 'seed' in variation_data[function_index]:
                seed_value = variation_data[function_index]['seed']
            else:
                seed_value = int(prompt_seed.get())
            data[0]['params']['args']['seed'] = int(seed_value)

            if function_index is not None and 'batch_size' in variation_data[function_index]:
                batch_size_value = variation_data[function_index]['batch_size']
            else:
                batch_size_value = int(prompt_batch_size.get())
            data[0]['params']['args']['batch_size'] = int(batch_size_value)

            if function_index is not None and 'checkpoint' in variation_data[function_index]:
                checkpoint_value = variation_data[function_index]['checkpoint']
            else:
                checkpoint_value = prompt_checkpoint.get()
            data[0]['params']['checkpoint'] = checkpoint_value

            if function_index is not None and 'custom_params' in variation_data[function_index]:
                custom_params_value = variation_data[function_index]['custom_params']   
            else:
                custom_params_value = prompt_custom_params.get("1.0", "end-1c")
            data[0]['script_params'] = custom_params_value

            # data[0]['params']['args']['sampler_name'] = sampler_dropdown.get()
            # data[0]['params']['args']['cfg_scale'] = float(cfg_spinbox.get())
            # data[0]['params']['args']['height'] = int(prompt_size_height_box.get())
            # data[0]['params']['args']['width'] = int(prompt_size_width_box.get())
            # data[0]['params']['args']['n_iter'] = int(prompt_n_iterations.get())
            # data[0]['params']['args']['seed'] = int(prompt_seed.get())
            # data[0]['params']['args']['batch_size'] = int(prompt_batch_size.get())
            # data[0]['params']['checkpoint'] = prompt_checkpoint.get()
            # data[0]['script_params'] = prompt_custom_params.get("1.0", "end-1c")

            
            characters = string.ascii_lowercase + string.digits  # Define the character set
            task_id = ''.join(random.choice(characters) for _ in range(15))
            data[0]['id'] = f'task({task_id})'
            data[0]['params']['args']['id_task'] = f'task({task_id})'


            if pageExists == True:
                prompt_list.extend(data)
                json.dump(prompt_list, file)
            else:
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
    button6.place(x=4.5*spacing + 3.5*button_width, y=window_height - (button_height + button_spacing), width=button_width, anchor="s")

     # Place the labels
    input_directory_label.place(x=spacing - 50, y=window_height - (3 * button_height + button_spacing + 20))
    output_directory_label1.place(x=2*spacing + button_width - 50, y=window_height - (2 * button_height + button_spacing + 20))
    output_directory_label2.place(x=3*spacing + 2*button_width - 50, y=window_height - (2 * button_height + button_spacing + 20))

def set_custom_params(event):
    global face_model_dropdown, face_model_params
    with open("face_model_params.json", "r") as file:
        full_face_model_params = json.load(file)
        face_model_text = face_model_dropdown.get()
        output_directory_label_text3.set(face_model_text)

        if face_model_text in full_face_model_params:
            face_model_params = full_face_model_params[face_model_text]
        if prompt_custom_params is not None:
            prompt_custom_params.delete("1.0", "end")
            prompt_custom_params.insert("1.0", face_model_params)

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
        if 'input_dir' in history and history['input_dir'] is not None:
            directory = history['input_dir']
            input_directory_label_text.set(f"{os.path.basename(directory)}")
        if 'output_dir' in history and history['output_dir'] is not None:
            directory1 = history['output_dir']
            output_directory_label_text1.set(f"{os.path.basename(directory1)}")
        if 'output_dir2' in history and history['output_dir2'] is not None:
            directory2 = history['output_dir2']
            output_directory_label_text2.set(f"{os.path.basename(directory2)}")
        if 'face_model' in history and history['face_model'] is not None:
            face_model_params = history['face_model_params']
            face_model_dropdown.set(f"{history['face_model']}")
        if 'upscale_bool' in history and history['upscale_bool'] is not None:
            upscale_bool = history['upscale_bool']
            if upscale_bool == True:
                button3.config(bg="green", fg="white")
                button3.config(activebackground='red', activeforeground='grey')
            else:    
                button3.config(bg="red", fg="grey")
                button3.config(activebackground='green', activeforeground='white')
        choose_input_directory(True)


def load_prompt_window():
    global prompt_list, page_name, prompt_positive_text_box, prompt_negative_text_box, prompt_steps_text_box, prompt_sampler_text_box, prompt_size_height_box, prompt_size_width_box, prompt_id, prompt_n_iterations, prompt_seed, prompt_batch_size, prompt_checkpoint, prompt_steps_text_box_label, prompt_size_height_box_label, prompt_size_width_box_label, prompt_n_iterations_label, prompt_seed_label, prompt_batch_size_label, prompt_checkpoint_label, sampler_dropdown, cfg_spinbox, prompt_custom_params

    prompt_params = None
    upscale_bool = False

    # Hide the current buttons
    page_name = "queueBuilder"                               
    image_count_label.destroy()
    input_directory_label.destroy()
    output_directory_label1.destroy()
    output_directory_label2.destroy()
    undo_button.destroy()
    deleteButton.destroy()
    setMainDir.destroy()
    button1.destroy()
    setButton1.destroy()
    button2.destroy()
    setButton2.destroy()
    button3.destroy()
    button4.destroy()
    button5.destroy()
    button6.destroy()
    # face_model_dropdown.destroy()

    #checkpoint
    prompt_checkpoint_label = tk.Label(root, text="Checkpoint", bg="black", fg="white")
    prompt_checkpoint_label.grid(row=0, column=0, sticky='nw', padx=15, pady=(5,5))
    prompt_checkpoint = ttk.Combobox(root)
    prompt_checkpoint['values']= ('dreamshaper_8.safetensors [879db523c3]', 'dreamshaper_8.safetensors [879db523c3]')
    prompt_checkpoint.set('dreamshaper_8.safetensors [879db523c3]') # set the default option
    prompt_checkpoint.grid(row=1, column=0, sticky='nw', padx=(15,0), pady=(2,20))

    prompt_checkpoint_checkbox = tk.Checkbutton(root, variable=prompt_checkpoint_var)
    prompt_checkpoint_checkbox.grid(row=1, column=0, sticky='nw', padx=(165,15), pady=(3,5))
    
    #prompt
    prompt_positive_text_box = tk.Text(root, width=50, height=5)
    prompt_positive_text_box.insert("1.0", "Positive Prompt")
    prompt_positive_text_box.grid(row=2, column=0, sticky='nw', padx=15, pady=(2, 20), columnspan=3, rowspan=2)

    prompt_positive_radio_front.grid(row=2, column=0, sticky='nw', padx=(425,0), pady=(0,5))
    prompt_positive_radio_none.grid(row=2, column=0, sticky='nw', padx=(425,0), pady=(30,5))
    prompt_positive_radio_back.grid(row=2, column=0, sticky='nw', padx=(425,0), pady=(60,5))
    prompt_positive_radio_button.set("none")

    prompt_negative_text_box = tk.Text(root, width=50, height=5)
    prompt_negative_text_box.insert("1.0", "Negative Prompt")
    prompt_negative_text_box.grid(row=4, column=0, sticky='nw', padx=15, pady=(2,20), columnspan=3, rowspan=2)

    prompt_negative_radio_front.grid(row=4, column=0, sticky='nw', padx=(425,0), pady=(0,5))
    prompt_negative_radio_none.grid(row=4, column=0, sticky='nw', padx=(425,0), pady=(30,5))
    prompt_negative_radio_back.grid(row=4, column=0, sticky='nw', padx=(425,0), pady=(60,5))
    prompt_negative_radio_button.set("none")

    # create dropdown menu
    prompt_sampler_text_box = tk.Label(root, text="Sampler", bg="black", fg="white")
    prompt_sampler_text_box.grid(row=6, column=0, sticky='nw', padx=15, pady=(2,2))
    
    sampler_dropdown = ttk.Combobox(root)
    sampler_dropdown['values']= samplers_object
    sampler_dropdown.set(PROMPT_SAMPLER_DEFAULT) # set the default option
    sampler_dropdown.grid(row=7, column=0, sticky='nw', padx=15, pady=(2,20))

    prompt_sampler_checkbox = tk.Checkbutton(root, variable=prompt_sampler_var)
    prompt_sampler_checkbox.grid(row=7, column=0, sticky='nw', padx=(165,15), pady=(3,5))


    #steps
    prompt_steps_text_box_label = tk.Label(root, text="Steps", bg="black", fg="white")
    prompt_steps_text_box_label.grid(row=6, column=1, sticky='nw', padx=15, pady=(5,5))
    prompt_steps_text_box = tk.Spinbox(root, from_=1, to=150, textvariable=PROMPT_STEPS_DEFAULT)
    prompt_steps_text_box.grid(row=7, column=1, sticky='nw', padx=15, pady=(2,20))

    prompt_steps_checkbox = tk.Checkbutton(root, variable=prompt_steps_var)
    prompt_steps_checkbox.grid(row=7, column=1, sticky='nw', padx=(165,15), pady=(3,5))

    #height and width
    prompt_size_height_box_label = tk.Label(root, text="Height", bg="black", fg="white")
    prompt_size_height_box_label.grid(row=8, column=0, sticky='nw', padx=15, pady=(5,5))
    
    prompt_size_height_box = tk.Spinbox(root, from_=64, to=2048, textvariable=PROMPT_SIZE_HEIGHT_DEFAULT)
    prompt_size_height_box.grid(row=9, column=0, sticky='nw', padx=15, pady=(2,20))

    prompt_size_height_checkbox = tk.Checkbutton(root, variable=prompt_size_height_var)
    prompt_size_height_checkbox.grid(row=9, column=0, sticky='nw', padx=(165,15), pady=(3,5))

    prompt_size_width_box_label = tk.Label(root, text="Width", bg="black", fg="white")
    prompt_size_width_box_label.grid(row=8, column=1, sticky='nw', padx=15, pady=(5,5))

    prompt_size_width_box = tk.Spinbox(root, from_=64, to=2048, textvariable=PROMPT_SIZE_WIDTH_DEFAULT)
    prompt_size_width_box.grid(row=9, column=1, sticky='nw', padx=15, pady=(2,20))

    prompt_size_width_checkbox = tk.Checkbutton(root, variable=prompt_size_width_var)
    prompt_size_width_checkbox.grid(row=9, column=1, sticky='nw', padx=(165,15), pady=(3,5))

    #batch count and iterations

    prompt_n_iterations_label = tk.Label(root, text="Iterations", bg="black", fg="white")
    prompt_n_iterations_label.grid(row=10, column=0, sticky='nw', padx=15, pady=(5,5))
    prompt_n_iterations = tk.Spinbox(root, from_=1, to=100, textvariable=PROMPT_N_ITERATIONS_DEFAULT)
    prompt_n_iterations.grid(row=11, column=0, sticky='nw', padx=15, pady=(2,20))

    prompt_iterations_checkbox = tk.Checkbutton(root, variable=prompt_iterations_var)
    prompt_iterations_checkbox.grid(row=11, column=0, sticky='nw', padx=(165,15), pady=(3,5))

    prompt_batch_size_label = tk.Label(root, text="Batch Size", bg="black", fg="white")
    prompt_batch_size_label.grid(row=10, column=1, sticky='nw', padx=15, pady=(5,5))
    prompt_batch_size = tk.Spinbox(root, from_=1, to=8, textvariable=PROMPT_BATCH_SIZE_DEFAULT)
    prompt_batch_size.grid(row=11, column=1, sticky='nw', padx=15, pady=(2,20))

    prompt_batch_size_checkbox = tk.Checkbutton(root, variable=prompt_batch_size_var)
    prompt_batch_size_checkbox.grid(row=11, column=1, sticky='nw', padx=(165,15), pady=(3,5))
    
    cfg_spinbox_label = tk.Label(root, text="CFG Scale", bg="black", fg="white")
    cfg_spinbox_label.grid(row=12, column=0, sticky='nw', padx=15, pady=(5,5))
    cfg_spinbox = tk.Spinbox(root, from_=1, to=30, textvariable=PROMPT_CFG_SCALE_DEFAULT, increment=0.1)
    cfg_spinbox.grid(row=13, column=0, sticky='nw', padx=15, pady=(2,20))

    prompt_cfg_scale_checkbox = tk.Checkbutton(root, variable=prompt_cfg_scale_var)
    prompt_cfg_scale_checkbox.grid(row=13, column=0, sticky='nw', padx=(165,15), pady=(3,5))

    #seed
    prompt_seed_label = tk.Label(root, text="Seed", bg="black", fg="white")
    prompt_seed_label.grid(row=12, column=1, sticky='nw', padx=15, pady=(5,5))
    prompt_seed = tk.Spinbox(root, from_=-1, to=9999999999, textvariable=PROMPT_SEED_DEFAULT)
    prompt_seed.grid(row=13, column=1, sticky='nw', padx=15, pady=(2,20))

    prompt_seed_checkbox = tk.Checkbutton(root, variable=prompt_seed_var)
    prompt_seed_checkbox.grid(row=13, column=1, sticky='nw', padx=(165,15), pady=(3,5))

    #propmt params
    prompt_params_label = tk.Label(root, text="Custom Params", bg="Black", fg="white")
    prompt_params_label.grid(row=14, column=0, sticky='nw', padx=15, pady=(5,5))

    prompt_custom_params_checkbox = tk.Checkbutton(root, variable=prompt_custom_params_var)
    prompt_custom_params_checkbox.grid(row=14, column=0, sticky='nw', padx=(675,15), pady=(3,5))

    prompt_custom_params = tk.Text(root, width=85, height=11)
    prompt_custom_params.grid(row=15, column=0, sticky='nw', padx=15, pady=(2,20), columnspan=4, rowspan=3)
    prompt_custom_params.insert("1.0", "eJzNU0tv1DAQTtTN7nYfLV0Q78cee6GCnrhVdBGViJQDEsfK8iZmxyKxLcfZrZCQOMbIR3OAX8eVXwGThwCpfwAnGWsm45lvvhl/Hnz9she069Ifx4F1gb84+/mtWd/f/MJlWxkHzfPJH7sRL0kqmPG1GzFB1znLvHXDQmZVzrwbCClwi1BnOapJqw53jG/A+Dh0ES/ohvnETTUr+UdGGk/vDldaqiUV2fJta/ZunMsd2WpaYPi50jJlZSk1wVO+heSmBlABmWeEXjete9PBpuIZFSkjpaEaIQRu9sfERNZgmit+xXKimH7PUoP5ZqkURsu8Bzc+p3njn3l3lwtFuTAkRbwElcqQriLr9kETqQyXAgs/lwa8OyrplpGMGYzLMlJQhbwtaLZtw5GOFi42yEeExFYcf0+6qF3qYckL1RA7W1OTQper9BC6iaxM45dx3ahIl1Rrmn7wtsI+wV4NAwtR3xAY9a2A/TiESQLT64zD3MJBSxocdtuNbjuKA1jgsZsWbv3DBdy2cKcvFO7VcD+BBzU8hEfwGEJ4gt/yv4KSWBc+8/DULbgod1Rhu8nz0xcnUogr7yYr5Pu11AXTOBJ1jzEO49DWKHH67cXZj+6q1NYNVu9evfQWp6kvJkysdWMlS274trkBqSwKiuOG5qgbPcBgEF6i7a+srcUgNkn6Nz5lJ78BBUFmzA==")

    face_model_dropdown.current(0)
    face_model_dropdown.grid(row=14, column=0, sticky='nw', padx=(105, 15), pady=(4,20), rowspan=2)

    prompt_add_variation_button = tk.Button(root, text="Add Variation", command=lambda: add_variation())
    prompt_variation_dropdown = ttk.Combobox(root)
    prompt_add_variation_button.grid(row=19, column=0, sticky='nw', padx=(15,15), pady=(3,5))
    # prompt_variation_dropdown.grid(row=19, column=0, sticky='nw', padx=(100, 15), pady=(4,20), rowspan=2)


    #Add to Queue button
    prompt_add_to_queue_button = tk.Button(root, text="Add to Queue", command=lambda:run_process_parameters(pageExists, prompt_list, data))
    prompt_add_to_queue_button.grid(row=19, column=0, sticky='nw', padx=(613,0), pady=(5,5))

    prompt_add_variation_text_box.grid(row=19, column=0, sticky='nw', padx=(100, 15), pady=(4,20))

    print_variations()

def write_new_variations():
    prompt_new_variations['name'] = prompt_add_variation_text_box.get("1.0", "end-1c")
    if prompt_checkpoint_var.get() == 1:
        prompt_new_variations['checkpoint'] = prompt_checkpoint.get()
    if prompt_positive_radio_button.get() == 'front':
        prompt_new_variations['positive_front'] = prompt_positive_text_box.get("1.0", "end-1c")
    elif prompt_positive_radio_button.get() == 'end':
        prompt_new_variations['positive_back'] = prompt_positive_text_box.get("1.0", "end-1c")
    if prompt_negative_radio_button.get() == 'front':
        prompt_new_variations['negative_front'] = prompt_negative_text_box.get("1.0", "end-1c")
    elif prompt_negative_radio_button.get() == 'end':
        prompt_new_variations['negative_back'] = prompt_negative_text_box.get("1.0", "end-1c")
    if prompt_sampler_var.get() == 1:
        prompt_new_variations['sampler'] = sampler_dropdown.get()
    if prompt_steps_var.get() == 1:
        prompt_new_variations['steps'] = prompt_steps_text_box.get()
    if prompt_size_height_var.get() == 1:
        prompt_new_variations['height'] = prompt_size_height_box.get()
    if prompt_size_width_var.get() == 1:
        prompt_new_variations['width'] = prompt_size_width_box.get()
    if prompt_iterations_var.get() == 1:
        prompt_new_variations['n_iter'] = prompt_n_iterations.get()
    if prompt_batch_size_var.get() == 1:
        prompt_new_variations['batch_size'] = prompt_batch_size.get()
    if prompt_cfg_scale_var.get() == 1:
        prompt_new_variations['cfg_scale'] = cfg_spinbox.get()
    if prompt_seed_var.get() == 1:
        prompt_new_variations['seed'] = prompt_seed.get()
    if prompt_custom_params_var.get() == 1:
        prompt_new_variations['custom_params'] = prompt_custom_params.get("1.0", "end-1c")

def add_variation():
    global variation_data
    write_new_variations()

    # Check if 'name' is the only key in prompt_new_variations
    if list(prompt_new_variations.keys()) == ['name']:
        return

    if os.path.isfile('variations.json'):
        with open('variations.json', 'r+') as file:
            if list(prompt_new_variations.keys()) != ['name']:
                print(f"line 963 prompt_new_variations: {prompt_new_variations}")
                variation_data.append(prompt_new_variations.copy())
            json.dump(variation_data, file)
    else:
        with open('variations.json', 'w') as file:
            json.dump([prompt_new_variations], file)
        with open('variations.json', 'r') as file:
            variation_data = json.load(file)
    x = 0
    while x < len(labels_and_Checkbuttons):
        labels_and_Checkbuttons[x]['checkbox'].destroy()
        labels_and_Checkbuttons[x]['label'].destroy()
        labels_and_Checkbuttons[x]['button'].destroy()
        x += 1
    print(f"line 977 variation_data: {variation_data}")
    print_variations()

def print_variations():
    global labels_and_Checkbuttons, variations_checkbox_vars
    if variation_data is None or len(variation_data) == 0:
        return
    y = 0
    while y < len(variation_data):
        # Create a new IntVar for the checkbox
        checkbox_var = tk.IntVar()
        variations_checkbox_vars.append(checkbox_var)

        labels_and_Checkbuttons[y] = {'label': tk.Label(root, text=str(variation_data[y]['name'])[:80], bg="black", fg="white"), 'checkbox': tk.Checkbutton(root, variable=checkbox_var), 'button': tk.Button(root, text="Delete", command=lambda y=y: delete_variation(y))}
        y += 1
    z = 0
    while z < len(labels_and_Checkbuttons):
        labels_and_Checkbuttons[z]['checkbox'].grid(row=z, column=2, sticky='nw', padx=(5,15), pady=(3,5))
        labels_and_Checkbuttons[z]['label'].grid(row=z, column=2, sticky='nw', padx=(50,15), pady=(3,5))
        labels_and_Checkbuttons[z]['button'].grid(row=z, column=2, sticky='nw', padx=(550,15), pady=(3,5))
        z += 1
    prompt_new_variations.clear()
    
    
def delete_variation(index):
    global labels_and_Checkbuttons, variation_data
    variation_data.pop(index)
    with open('variations.json', 'w') as file:
        json.dump(variation_data, file)
    x = 0
    while x < len(labels_and_Checkbuttons):
        labels_and_Checkbuttons[x]['checkbox'].destroy()
        labels_and_Checkbuttons[x]['label'].destroy()
        labels_and_Checkbuttons[x]['button'].destroy()
        x += 1
    labels_and_Checkbuttons.clear()
    print_variations()

def run_process_parameters(pageExists, prompt_list, data):
    prompt_list = []
    if os.path.isfile(prompt_list_file_path):
        with open(prompt_list_file_path, 'r') as file:
            prompt_list = json.load(file)
            pageExists = True
    process_parameters(pageExists, prompt_list, data, None, True) 
    x = 0 
    while x < len(variation_data):
        print(f"line 1025 x: {x}")
        if variations_checkbox_vars[x].get() == 1:
            if os.path.isfile(prompt_list_file_path):
                with open(prompt_list_file_path, 'r') as file:
                    prompt_list = json.load(file)
                    pageExists = True
            process_parameters(pageExists, prompt_list, data, x, True)
        x += 1

def change_dropdown(*args):
    print(sampler_dropdown.get())

# link function to change dropdown

# Assuming you have 8 buttons
button_height = 50
button_spacing = 50

window_height = root.winfo_height()


def create_main_content():
    global undo_button, deleteButton, setMainDir, button1, setButton1, button2, setButton2, button3, button4, button5, button6, face_model_dropdown, page_name, image_count_label, input_directory_label_text, input_directory_label, output_directory_label_text1, output_directory_label1, output_directory_label_text2, output_directory_label2, output_directory_label_text3, face_model_dropdown

    page_name = "main"

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


    # Create the "Undo" button
    undo_button = tk.Button(root, text="Undo", command=undo)
    undo_button.place(x=spacing, y=window_height -(button_height + button_spacing), width=button_width, anchor="s")

    # deleteButton
    deleteButton = tk.Button(root, text="Delete", command=lambda: delete_image(), fg="red")
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
        if upscale_bool is True:
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
    
    button4 = tk.Button(root, text="Save", command=save_history)
    button4.place(x=4*spacing + 3*button_width, y=window_height - button_height, width=button_width, anchor="s")

    button5 = tk.Button(root, text="Load", command=load_history)
    button5.place(x=4*spacing + 3*button_width, y=window_height - button_height, width=button_width, anchor="s")

    button6 = tk.Button(root, text="Add Prompt", command=load_prompt_window)
    button6.place(x=4*spacing + 3*button_width, y=window_height - button_height, width=button_width, height=button_height * 2, anchor="s")

    # face_model_dropdown
    # Read the keys from the JSON file
    face_model_keys = []
    with open('face_model_params.json') as f:
        face_model_data = json.load(f)
    face_model_keys = list(face_model_data.keys())
    # Create a StringVar to hold the selected value
    selected_key = tk.StringVar()

    # Create the dropdown
    face_model_dropdown = ttk.Combobox(root, textvariable=selected_key, width=90)

    # Populate the dropdown with the keys
    face_model_dropdown['values'] = face_model_keys

    # Set the first key as the initially selected value
    if face_model_keys:
        face_model_dropdown.current(0)

    face_model_dropdown.bind("<<ComboboxSelected>>", set_custom_params)
    set_custom_params(event=None)
    # Place the dropdown in the window
    face_model_dropdown.place(x=4*spacing + 3*button_width, y=window_height -(button_height + button_spacing), width=800, height=50, anchor="s")

    # Delay the placement of the buttons until after the window is displayed
    root.after(100, update_button_positions)

if page_name == "main":
    create_main_content()

print(f"page_name: {page_name}")
root.mainloop()