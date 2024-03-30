

import os
from loguru import logger
import subprocess
import sys
import util

import os, csv, torch, numpy, scipy.io, PIL.Image, torchvision.transforms
# Our libs
from mit_semseg.models import ModelBuilder, SegmentationModule
from mit_semseg.utils import colorEncode



class Segment():
    """Handles the segmentation part of the pipline
    """
    def __init__(self) -> None:
        # Network Builders
        self.net_encoder = ModelBuilder.build_encoder(
            arch='resnet50dilated',
            fc_dim=2048,
            weights='ckpt/ade20k-resnet50dilated-ppm_deepsup/encoder_epoch_20.pth')
        self.net_decoder = ModelBuilder.build_decoder(
            arch='ppm_deepsup',
            fc_dim=2048,
            num_class=150,
            weights='ckpt/ade20k-resnet50dilated-ppm_deepsup/decoder_epoch_20.pth',
            use_softmax=True)

        logger.success("Segmentation model is loaded.")
        
        self.crit = torch.nn.NLLLoss(ignore_index=-1)
        self.segmentation_module = SegmentationModule(self.net_encoder, self.net_decoder, self.crit)
        self.segmentation_module.eval()
        self.segmentation_module.cuda()

    

    
    def inference(self,input_image:str) -> PIL.Image:
        """runs inference for the segmenation model

        Args:
            input_image (str): the path to input image

        Raises:
            FileNotFoundError: raise and error is the given path is wrong

        Returns:
            PIL.Image: returns the segmented image
        """
        if os.path.exists(input_image):
                        # Load and normalize one image as a singleton tensor batch
            pil_to_tensor = torchvision.transforms.Compose([
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], # These are RGB mean+std values
                    std=[0.229, 0.224, 0.225])  # across a large photo dataset.
            ])
            pil_image = PIL.Image.open(input_image).convert('RGB')
            img_original = numpy.array(pil_image)
            img_data = pil_to_tensor(pil_image)
            singleton_batch = {'img_data': img_data[None].cuda()}
            output_size = img_data.shape[1:]
      
                        
            # Run the segmentation at the highest resolution.
            with torch.no_grad():
                scores = self.segmentation_module(singleton_batch, segSize=output_size)
                
            # Get the predicted scores for each pixel
            _, pred = torch.max(scores, dim=1)
            pred = pred.cpu()[0].numpy()


            colors = scipy.io.loadmat('color150.mat')['colors']
            names = {}
            with open('object150_info.csv') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    names[int(row[0])] = row[5].split(";")[0]
            # colorize prediction
            pred_color = colorEncode(pred, colors).astype(numpy.uint8)
            # PIL.Image.fromarray(pred_color,'RGB').save(util.get_filename(input_image)+'-segmentation-mask.png')
            return PIL.Image.fromarray(pred_color,'RGB')      
           
        else:
            raise FileNotFoundError
            
       