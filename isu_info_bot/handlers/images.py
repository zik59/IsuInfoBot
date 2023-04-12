from PIL import Image


async def merge_images(images: list) -> str:
    images = [Image.open(x) for x in images]
    images = [i.resize((164, 250)) for i in images]
    width = images[0].size[0]*5
    height = images[0].size[1]*2
    new_image = Image.new('RGB', (width, height))
    x_offset = 0
    y_offset = 0
    for i, image in enumerate(images):
        if i == 5:
            x_offset = 0
            y_offset = image.size[1]
        new_image.paste(image, (x_offset, y_offset))
        x_offset += images[i].size[0]
    filename = '/home/zik/Desktop/Python/isuInfo/isu_info_bot/images/test.jpg'
    new_image.save(filename)
    return filename
