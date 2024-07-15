import os
import base64
from cherry_parser import grep_images, parse_file

parse_file('report.ctd')

def save_image(full_path, content):
    
    directory = os.path.dirname(full_path)
    
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    
    with open(full_path, 'wb') as file:
        file.write(content)


for i,images in enumerate(grep_images()):


    for n,image in enumerate(images):
        decoded_image = base64.b64decode(image) 
        save_image(f"img/{i}/image-{n}.png",decoded_image)



