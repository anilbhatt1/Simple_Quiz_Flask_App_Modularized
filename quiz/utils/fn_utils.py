from quiz import app
from PIL import Image
import time, os

# Function to save the image as part of questions
def save_image_qn(image_file_list, current_name_list, action):
    image_filename_list = list()
    for idx, image_file in enumerate(image_file_list):
        if image_file is None:
            if action == 'add':
                image_filename_list.append('default.jpg')
            else:
                image_filename_list.append(current_name_list[idx])
        else:
            img = Image.open(image_file)
            img_filename_list = image_file.filename.split('.')
            timestr = time.strftime("%Y%m%d-%H%M%S")
            img_save_name = str(img_filename_list[0]) + '_' + str(timestr) + '.' + img_filename_list[-1]
            image_save_path = os.path.join(app.root_path, 'static/images', img_save_name)
            img = img.resize((200, 200))
            img.save(image_save_path)
            image_filename_list.append(img_save_name)
    return image_filename_list