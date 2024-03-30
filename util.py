import os
from loguru import logger
import subprocess
from PIL import Image
from typing import Union
from pathlib import Path
from fastapi import UploadFile

def save_image(image: UploadFile, filename: str):
    """
    Saves the uploaded image to a PNG file.
    """
    with open(filename, "wb") as f:
        f.write(image.file.read())


def mkdir_working(overwrite:bool = False):
    """makes a working dir to store intermediate files

    Args:
        overwrite (bool, optional): overwrite previous working directory. Defaults to False.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    try:
        os.mkdir(path=os.path.join(current_directory,"./working"))
        
    except FileExistsError:
        if overwrite is True:
            for root, dirs, files in os.walk(os.path.join(current_directory,"./working"), topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    os.rmdir(dir_path)
        else:   
            logger.error("Working directory already exists and contains files,\n to overwrite pass overwrite as true")


def run_system_command(command: str) -> bool:
    """
    Runs a system command and checks if it was successful.

    Args:
        command (str): The system command to execute.

    Returns:
        bool: True if the command was successful, False otherwise.
    """
    try:
        # Execute the command
        subprocess.run(command, shell=True, check=True)
        return True  # Command executed successfully
    except subprocess.CalledProcessError:
        return False  # Command failed
    
def read_image(path:str) -> Union[Image.Image,None]:
    """reads image at given path

    Args:
        path (str): image file path

    Returns:
        PIL.Image | None : image file if it can be read.
    """
    try:
        image = Image.open(path)
        image = image.convert("RGB")
    
        logger.success("image was read successfully.")
        return image
    except FileNotFoundError:
        logger.error(f"image file at path:\t{path} could not be found.")
        return None
    except:
        logger.error("Could not get image.") 



def convert_to_png(input_image_path:str, output_image_path:str):
    """convers images of all formats to .png

    Args:
        input_image_path (str): path to read the image 
        output_image_path (_type_): path to save the image
    """
    try:
        image = Image.open(input_image_path)
        image.save(output_image_path, format="PNG")
        logger.success(f"Image converted to PNG and saved as {output_image_path}")
    except Exception as e:
        logger.error(f"Error converting image: {e}")
        
def resize_image(input_path, output_path, size):
    """
    Resizes an image to the specified target size.

    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the resized image.
        target_size (int): The desired size for the largest dimension (width or height).

    Returns:
        None
    """
    try:
        # Open the input image
        image = Image.open(input_path)

        # Calculate the aspect ratio
        width, height = image.size
        aspect_ratio = width / height

        # Determine the new dimensions
        if width > height:
            new_width = size
            new_height = int(size / aspect_ratio)
        else:
            new_height = size
            new_width = int(size * aspect_ratio)

        # Resize the image
        resized_image = image.resize((new_width, new_height))

        # Save the resized image
        resized_image.save(output_path)
        logger.success(f"Resized image to {resized_image.size} saved to {output_path}")
    except Exception as e:
        logger.error(f"Error resizing image: {e}")

def get_filename(path:str)->str:
    """gets file name

    Args:
        path (str): file path

    Returns:
        str: file name
    """
    
    return Path(path).stem



def resize_images(folder_path, dim):
    """
    Resizes all PNG images in the specified folder to have the largest dimension equal to 'dim'.

    Args:
        folder_path (str): Path to the folder containing PNG images.
        dim (int): Desired size for the largest dimension (width or height).

    Returns:
        None
    """
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            try:
                img = Image.open(image_path)
                width, height = img.size

                # Calculate the new dimensions while maintaining the aspect ratio
                if width > height:
                    new_width = dim
                    new_height = int(height * (dim / width))
                else:
                    new_height = dim
                    new_width = int(width * (dim / height))

                # Resize the image
                resized_img = img.resize((new_width, new_height))

                # Save the resized image (overwrite the original)
                resized_img.save(image_path)
                print(f"Resized {filename} to {new_width}x{new_height}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
