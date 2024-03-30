"""A program to test the Transfer module

Returns:
    _type_: _description_
"""
import requests
import argparse
import shutil
from loguru import logger
def create_arg_parser():
    """
    Creates an argument parser for the specified command-line arguments.
    
    --api_url API_URL     API URL for processing.
  
    --content_image CONTENT_IMAGE
                        Path to the content image file.
                        
    --style_image STYLE_IMAGE
                        Path to the style image file.
                        
    --alpha ALPHA         Alpha value for blending content and style.
    
    --size SIZE           Size of the output image.
    """
    parser = argparse.ArgumentParser(
        description="Process API URL, content image, style image, alpha, and size.")

    # API URL argument
    parser.add_argument("--api_url", type=str, required=True,
                        help="API URL for processing.")

    # Content image path argument
    parser.add_argument("--content_image", type=str,
                        required=True, help="Path to the content image file.")

    # Style image path argument
    parser.add_argument("--style_image", type=str,
                        required=True, help="Path to the style image file.")

    # Alpha (float) argument
    parser.add_argument("--alpha", type=float, default=0.5,
                        help="Alpha value for blending content and style.")

    # Size (integer) argument
    parser.add_argument("--size", type=int, default=256,
                        help="Size of the output image.")

    return parser


def test(content, style, size, alpha,api_url):
    """This functions makes a python request to the API,
    to test wether it has been setup properly.
    First you must run main.py in the parrent directory.
    
    To see what arguments you need to supply to this progrma run /tester/main.py -h
    
    the output is saved as a zip file in the current dir.

    Args:
        content (str): content image path
        style (_type_): style image path
        size (_type_): size dimension for the style transfer model
        alpha (_type_): alpha hyperparameter, must be between 0 and 1, defaults to 1
        api_url (_type_): the api url provieded by the main program output + the specific url
         
    """
 
    try:
        shutil.copy(content, 'content.png')
        logger.success("File copied successfully.")
    
    # If source and destination are same
    except shutil.SameFileError:
        pass
    
    # If there is any permission issue
    except PermissionError:
        logger.error("Permission denied.")
    
    # For other errors
    except:
        logger.error("Error occurred while copying file.")
        
    try:
        shutil.copy(style, 'style.png')
        logger.success("File copied successfully.")
    
    # If source and destination are same
    except shutil.SameFileError:
        pass
    
    # If there is any permission issue
    except PermissionError:
        logger.error("Permission denied.")
    
    # For other errors
    except:
        logger.error("Error occurred while copying file.")
        
        
    try:
        # Read image files
        with open(content, 'rb') as img1_file, open(style, 'rb') as img2_file:
            files = [('files',img1_file),('files',img2_file)]

            # Prepare data payload
            data = {'size': size, 'alpha': alpha}

            # Make the POST request
            response = requests.post(api_url, files=files, data=data)

            # Check response status
            if response.status_code == 200:
                logger.success("Request successful! Response content saved at response.zip")
                zip_filename = 'response.zip'
                with open(zip_filename, 'wb') as zip_file:
                    for chunk in response.iter_content(chunk_size=255):
                        if chunk:
                            zip_file.write(chunk)
            else:
                logger.error(
                    f"Request failed with status code {response.status_code}.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    # Access the parsed arguments
    api_url = args.api_url
    content_image_path = args.content_image
    style_image_path = args.style_image
    alpha = args.alpha
    size = args.size
    test(content_image_path,style_image_path,size,alpha,api_url)