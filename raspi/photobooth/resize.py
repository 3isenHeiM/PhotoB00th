from PIL import Image
import time

def scale_image(input_image_path,
                output_image_path,
                width=None,
                height=None
                ):
    original_image = Image.open(input_image_path)
    w, h = original_image.size
    print('Original image : {wide}x{height} '
          'high'.format(wide=w, height=h))
 
    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, h)
    elif height:
        max_size = (w, height)
    else:
        # No width or height specified
        raise RuntimeError('Width or height required!')
 
    original_image.thumbnail(max_size, Image.ANTIALIAS)
    original_image.save(output_image_path)
 
    scaled_image = Image.open(output_image_path)
    width, height = scaled_image.size
    print('Scaled image : {wide}x{height} '
          'high'.format(wide=width, height=height))
 
 
if __name__ == '__main__':

    start = time.time()

    scale_image(input_image_path='2018-11-30_20:12:39.jpg',
                output_image_path='2018-11-30_20:12:39_scaled.jpg',
                width=1920)

    elapsed = time.time() - start
    print 'Elapsed time: %.3fs' % (elapsed)

