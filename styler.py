try:
    from .WCT2.transfer import WCT2
    from .WCT2.model import WaveEncoder, WaveDecoder
    from .WCT2.utils.core import feature_wct
    from .WCT2.utils.io import Timer, open_image, load_segment, compute_label_info
    from .WCT2.transfer import run_bulk
except:
    from WCT2.transfer import WCT2
    from WCT2.model import WaveEncoder, WaveDecoder
    from WCT2.utils.core import feature_wct
    from WCT2.utils.io import Timer, open_image, load_segment, compute_label_info
    from WCT2.transfer import run_bulk


# import importlib.util
import os
from util import resize_images
import shutil
from loguru import logger
from torch.cuda import empty_cache
class ArgsDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
class StyleTransfer:
    """This is the API between the WCT2 and the rest of the pipline
    """
    def __init__(self):
        try:
            self.model = WCT2()
            logger.success("WTC2 loaded successfully.")
        except Exception as e:
            logger.error(f"There was an error\t{e}")
          
    def transfer(self,content:str,content_segment:str,style:str,style_segment:str,size:int = 400,alpha:float = 1):  
        """This function runs inference for the WCT2 model and makes the dir tree for the WCT2

        Args:
            content (str): content file path
            content_segment (str): content segmentation mask file path
            style (str): style file path
            style_segment (str): style segmentation mask file path
            size (int, optional): resolution. Defaults to 400.
            alpha (float, optional): alpha hyper paremeter. Defaults to 1.
        """
        os.mkdir('./working/content')
        os.mkdir('./working/content_segment')
        os.mkdir('./working/style')
        os.mkdir('./working/style_segment')
        os.mkdir('./working/output')
        
        shutil.copy(content,'./working/content/image.png')
        shutil.copy(content_segment,'./working/content_segment/image.png')
        shutil.copy(style,'./working/style/image.png')
        shutil.copy(style_segment,'./working/style_segment/image.png')
        
        args = ArgsDict({
            'content':'./working/content/',
            'content_segment':'./working/content_segment/',
            'style':'./working/style/',
            'style_segment':'./working/style_segment/',
            'output':'./working/output/',
            'image_size':size,
            'alpha':alpha,
            'option_unpool':'cat5',
            'transfer_at_encoder':False,
            'transfer_at_decoder':False,
            'transfer_at_skip':False,
            'transfer_all':True,
            'cpu':False,
            'verbose':True
            
            
        })
        resize_images('./working/',size)
        empty_cache()
        run_bulk(args)
        resize_images('./working/output',size*4)
        
       
        