from PIL import Image, ImageDraw, ImageFont
import math


def get_bubble(text, save_path, max_row_len=50, speaker='bot'):

    row_len = len(text)*8
    row_num = 1

    if len(text) > max_row_len:
        row_num = math.ceil(len(text)/max_row_len)
        row_len = max_row_len*8

    massage_color = 'lightgreen'

    if speaker == 'bot':
        massage_color = 'lightgray'
    elif speaker == 'button':
        massage_color = 'rgb(255, 102, 102)'

    # Create a blank image with a white background
    image = Image.new('RGB', (10 + row_len, 10 + 25 * row_num), massage_color)

    # Create a draw object to draw on the image
    draw = ImageDraw.Draw(image)

    curr_len = 0
    curr_sent = ''

    for word in text.split(' '):
        curr_len += len(word) + 1
        if curr_len > max_row_len:
            curr_len = len(word) + 1
            curr_sent += '\n' + word + ' '
        else:
            curr_sent += word + ' '

    font = ImageFont.truetype("arial.ttf", 16)
    draw.text((10, 10), curr_sent, fill='black', font=font)

    # Save the image
    image.save(save_path)


# massage = "My name is TechniBot I'm our university chatbot!" + \
#           "Here you can ask every question about the bureaucracy " + \
#           "and registration procedures. " + \
#           "I will help you to start off on the right foot " \
#           "and prepared to your first year and first semester!" + \
#           " Good luck!"
# get_bubble(massage, 'fesd', bot_speaking=False)