"""
This challenge requires performing a visual XOR between 
the RGB bytes of the two images - not an XOR of all the 
data bytes of the files.
"""
from PIL import Image
from pathlib import Path

# XOR-encrypted images file path
lemur_img_filepath = Path(__file__).parent / "assets/lemur.png"
flag_img_filepath = Path(__file__).parent / "assets/flag.png"


def convert_to_RGB(img_path):
    # Open the image and convert it to 'RGB' mode.
    with Image.open(img_path) as img:
        img = img.convert('RGB')
        width, height = img.size
        rgb_values = [img.getpixel((x, y)) for y in range(height) for x in range(width)]
        
        return width, height, rgb_values
        
def revert_from_RGB(width, height, pixel_list, filepath):
    # Convert from 'RGB' mode and store it as PNG image
    img = Image.new("RGB", (width, height))
    img.putdata(pixel_list)
    img.save(filepath)
    
    return img
    

width, height, lemur_rgb = convert_to_RGB(lemur_img_filepath)
assert lemur_rgb[0] == (197, 193, 204)
assert isinstance(lemur_rgb, list)
assert isinstance(lemur_rgb[0], tuple) 

_, _, flag_rgb = convert_to_RGB(flag_img_filepath)
assert flag_rgb[0] == (247, 243, 247)

decrypted_img_filepath = Path(__file__).parent / "assets/decrypted-img.png"

xor_rgb = [
        (  
            rgb_bytes[0] ^ flag_rgb[index][0], 
            rgb_bytes[1] ^ flag_rgb[index][1],
            rgb_bytes[2] ^ flag_rgb[index][2]
        ) 
        for index, rgb_bytes in enumerate(lemur_rgb)
    ]
            
new_img = revert_from_RGB(width, height, xor_rgb, decrypted_img_filepath)
new_img.show()
