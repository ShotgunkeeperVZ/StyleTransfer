from typing import List
import util
from loguru import logger
from segmentor import Segment
from styler import StyleTransfer
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import uvicorn
import PIL
if __name__ == '__main__':

    logger.info("Setting up the API")
    

    app = FastAPI()

    
    
    
    @app.post("/upload_images/")
    def upload_images(files: List[UploadFile],size:int=400,alpha:float=1.0):
        """
        Receives two images as arguments and saves them to PNG files.
        """
        segment = Segment()
        transfer_model = StyleTransfer()
        print(files)
     
       
        for file in files:
            try:
                contents = file.file.read()
                with open(file.filename, 'wb') as f:
                    f.write(contents)
                    
            except Exception:
                return {"message": "There was an error uploading the file"}
            finally:
                f.close()
            # images[file.filename] = PIL.Image.open(await file.read())
        # content = images['content.png']
        # style= images['style.png']
        # util.save_image(content, "content.png")
        # util.save_image(style, "style.png")
        util.mkdir_working(overwrite=True)
            
            
        try:
            content_filename = util.get_filename('content.png')+'-content'
            content_base_image = f'./working/{content_filename}-base.png'
            util.resize_image('content.png','content.png',size=size)
            util.convert_to_png(input_image_path='content.png',output_image_path=content_base_image)
            content_mask = segment.inference(content_base_image)
            content_mask.save(f'./working/{content_filename}-base-segmentation-mask.png')
        except FileNotFoundError:
            logger.error(f"{os.path.basename('content.png')} could not be opened.\nCheck the provided path")
            
        try:
            style_filename = util.get_filename('style.png')+'-style'
            style_base_image = f'./working/{style_filename}-base.png'
            util.resize_image('style.png','style.png',size=size)
            util.convert_to_png(input_image_path='style.png',output_image_path=style_base_image)
            style_mask= segment.inference(style_base_image)
            style_mask.save(f'./working/{style_filename}-base-segmentation-mask.png')
            
        except FileNotFoundError:
            logger.error(f"{os.path.basename('style.png')} could not be opened.\nCheck the provided path")
        del segment
        
        

        transfer_model.transfer(content_base_image,
                                    f'./working/{content_filename}-base-segmentation-mask.png',
                                    style_base_image,
                                    f'./working/{style_filename}-base-segmentation-mask.png',size=512,alpha=alpha
                                    )
        shutil.make_archive('output', 'zip', './working/output')
        shutil.move('output.zip','./working/output.zip')
        return FileResponse('./working/output.zip')
      
    uvicorn.run(app)