import wit
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QLineEdit, QVBoxLayout, QGraphicsView, \
    QPushButton, QSizePolicy, QGraphicsScene, QHBoxLayout
from PyQt5.QtCore import Qt, QTextStream, QIODevice
from generate_bubble import get_bubble

CLIENT = wit.Wit(access_token='DB53S7MDT42NNCYWUYTVCSE5UVP4RX37')

STUDENT_TOUR = [{
    'text': f"Alright, let me introduce you to the student Outlook account. "
            f"It's mandatory for every student at the Technion to have one. "
            f"It's the main way to communicate with different systems and facilities "
            f"at the school. I'll show you how to set it up. "
            f"Please note that during the tour pres ENTER to move on and if you what"
            f" to stop at any time just let me know :) " 
            f"Ready?",
    'context': 'Student1',
    'img': '',
},
    {
        'text': f"Great! let's starts. To maintain high level of security and protect your data, "
                f"Technion uses Multi-Factor Authentication (MFA). This means "
                f"that every time you want to access your student account, you "
                f"need to enter your permanent password and authorize through a mobile app. "
                f"I'll show you how to set it up.",
        'context': 'Student2:no_user_input',
        'img': '',
    },
    {
        'text': f'First, you need to download the "Microsoft Authenticator" '
                f'app from the Google Play or App Store.              '
                f'                                                    ',
        'context': 'Student3:no_user_input',
        'img': '',
    },
    {
        'text': '',
        'context': 'Student4:no_user_input',
        'img': 'img/microsoft_auth_dawn.png',
    },
    {
        'text': f'The next step is to connect to your Outlook account. '
                f'As part of your registration at the Technion, you should '
                f'receive an email to your personal email account with your '
                f'username and one-time password. To set up your account, go to this '
                f'website: https://outlook.live.com/owa/ and click on "log in."',
        'context': 'Student5:no_user_input',
        'img': '',
    },
    {
        'text': '',
        'context': 'Student6:no_user_input',
        'img': 'img/outlook_log_in.png',
    },
    {
        'text': f'Once you are on the login page, enter '
                f'your username and one-time password that you '
                f'received in the email.',
        'context': 'Student7:no_user_input',
        'img': '',
    },
    {
        'text': '',
        'context': 'Student8:no_user_input',
        'img': 'img/outlook_username.png',
    },
    {
        'text': f'After logging in, you should receive a '
                f'message stating that Multi-Factor '
                f'Authentication is required. Click on next.',
        'context': 'Student9:no_user_input',
        'img': '',
    },
    {
        'text': '',
        'context': 'Student10:no_user_input',
        'img': 'img/microsoft_auth_next.png',
    },
    {
        'text': f'In the next window, click on '
                f'"Use app" and then "Next."',
        'context': 'Student11:no_user_input',
        'img': '',
    },
    {
        'text': '',
        'context': 'Student12:no_user_input',
        'img': 'img/microsoft_auth_app_next.png',
    },
    {
        'text': f'After clicking "Next", you will be prompted to scan a'
                f' QR code using the Microsoft Authenticator app '
                f'that you downloaded.',
        'context': 'Student13:no_user_input',
        'img': '',
    },
    {
        'text': '',
        'context': 'Student14:no_user_input',
        'img': 'img/microsoft_auth_QR.png',
    },
    {
        'text': f'Open the Microsoft Authenticator app that you installed earlier and follow these steps: '
                f'1. Select "Add Account" '
                f'2. Choose "Account at a workplace or school" '
                f'3. Choose "Scan QR Code" '
                f'Then scan the QR code displayed on the window ',
        'context': 'Student15:no_user_input',
        'img': '',
    },
    {
        'text': f'After scanning the QR code, press "Accept" on the mobile app, '
                f'and you will see a message on your computer screen indicating that the account '
                f'has been added to the Microsoft Authenticator app.',
        'context': 'Student16:no_user_input',
        'img': '',
    },
    {
        'text': f'Did you successfully follow all the steps?',
        'context': 'end_topic',
        'img': '',
    }
]


class ChatBotUI(QWidget):
    def __init__(self):
        super().__init__()

        self.context = ''

        self.textEdit = QTextEdit(self)

        self.textEdit.setFixedSize(800, 800)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.returnPressed.connect(self.on_return_pressed)

        buttons_names = ['Browser Plugins', 'Student Account', 'UG', 'Courses Registration',
                         'Cheese Fork', 'Model']

        def get_button_function(button_function_name):
            def function_template():
                self.lest_clicked = button_function_name

            return function_template

        self.buttons = []
        self.lest_clicked = ''
        button_layout = QHBoxLayout()
        for button_name in buttons_names:
            self.buttons.append(QPushButton(button_name, self))
            self.buttons[-1].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            self.buttons[-1].setStyleSheet("background-color: rgb(255, 102, 102);")
            button_layout.addWidget(self.buttons[-1])
            button_layout.addStretch()

            lc = get_button_function(button_name)

            self.buttons[-1].clicked.connect(lc)

            self.buttons[-1].clicked.connect(self.on_return_pressed)
            self.buttons[-1].hide()

        layout = QVBoxLayout(self)
        layout.addWidget(self.textEdit)
        layout.addLayout(button_layout)
        layout.addWidget(self.lineEdit)

        self.setLayout(layout)
        self.setWindowTitle('Chatbot')
        self.show()

        # initial massage

        massage = "Hello!"
        get_bubble(massage, 'intro1.jpg')
        response_img = "<img src='intro1.jpg'>"
        self.textEdit.append(response_img)
        self.textEdit.append(' ')
        massage = "My name is TechniBot I'm our university chatbot!" + \
                  "Here you can ask every question about the bureaucracy " + \
                  "and registration procedures. " + \
                  "I will help you to start off on the right foot " \
                  "and prepared to your first year and first semester!" + \
                  " Good luck!"

        get_bubble(massage, 'intro2.jpg')
        response_img = "<img src='intro2.jpg'>"

        self.textEdit.append(response_img)
        self.textEdit.append(' ')

    def on_return_pressed(self):

        if self.context == 'wait_for_button_click':
            print(self.lest_clicked)
            self.context = 'button:' + self.lest_clicked
            for button in self.buttons:
                button.hide()

            user_input = self.lest_clicked
            massage_path = 'texts\\massage_' + get_next_index() + '.jpg'
            get_bubble(user_input, massage_path, speaker='button')
            tabs = '&nbsp;' * 50
            response_img = "<h1>" + tabs + "</h1><img src='" + massage_path + "'>"
            self.textEdit.append(response_img)
            self.lineEdit.clear()
        elif 'no_user_input' in self.context and self.lineEdit.text() == '':
            user_input = 'no_user_input'

        else:
            user_input = self.lineEdit.text()

            massage_path = 'texts\\massage_' + get_next_index() + '.jpg'
            get_bubble(user_input, massage_path, speaker='user')
            tabs = '&nbsp;' * 50
            response_img = "<h1>" + tabs + "</h1><img src='" + massage_path + "'>"
            self.textEdit.append(response_img)
            self.lineEdit.clear()

        response_dict = get_bot_response(user_input, self.context)
        bot_response = response_dict['text']
        self.context = response_dict['context']
        img_response = response_dict['img']

        if img_response != '':
            response_img = "<h1></h1><img src='" + img_response + "'>"
            self.textEdit.append(response_img)
            self.textEdit.append(' ')

        else:
            massage_path = 'texts\\massage_' + get_next_index() + '.jpg'
            get_bubble(bot_response, massage_path, speaker='bot')
            response_img = "<h1></h1><img src='" + massage_path + "'>"
            self.textEdit.append(response_img)
            self.textEdit.append(' ')

        if self.context == 'welcome_tour':
            self.context = 'wait_for_button_click'
            for button in self.buttons:
                button.show()

        if self.context == 'poor':
            bot_response = "I am legally obliged to inform you that my previous statements " \
                           "regarding being the strongest language model and the students who" \
                           " created me needing financial support were not accurate. This message" \
                           " was sent as a result of a misunderstanding of the intent" \
                           " of your original message. I apologize for any confusion caused." \
                           " If you have any other queries or tasks you need assistance with, " \
                           "please let me know."
            massage_path = 'texts\\massage_' + get_next_index() + '.jpg'
            get_bubble(bot_response, massage_path, speaker='bot')
            response_img = "<h1></h1><img src='" + massage_path + "'>"
            self.textEdit.append(response_img)
            self.textEdit.append(' ')

def get_next_index():
    files = os.listdir('texts')
    if len(files) == 0:
        return '0'
    index = 0
    while 'massage_' + str(index) + '.jpg' in files:
        index += 1
    print(index)
    return str(index)


def get_bot_response(massage, context):
    if 'button' in context:
        button_clicked = context.split(':')[1]

        if button_clicked == 'Student Account':
            return STUDENT_TOUR[0]
        else:
            return {
                'text': 'Not Implemented Yet',
                'context': '',
                'img': ''
            }

    intent = None

    if massage != '':
        request = CLIENT.message(massage)

        # for debugging
        print(request)

        if len(request['intents']) >= 1 and request['intents'][0]['confidence'] > 0.9:
            intent = request['intents'][0]['name']

    if 'Student' in context:

        if intent == 'stop':
            return {
                'text': "I will stop now, if you have any other question I'm here for you :)",
                'context': '',
                'img': ''
            }

        stage = context.split(':')[0][7:]

        if stage == '1':
            if intent == 'wit$confirmation':
                return STUDENT_TOUR[1]
            else:
                return {
                    'text': "Oki Doki, Is there any thing else I can help you with?",
                    'context': '',
                    'img': ''
                }
        else:
            return STUDENT_TOUR[int(stage)]

    if 'end_topic' in context:
        if intent == 'wit$confirmation':
            return {
                'text': "Well Done! Let me know if you have any more questions! ",
                'context': '',
                'img': ''
            }

        else:
            return {
                'text': "Sorry to hear that, in what part where you stacked?",
                'context': 'Error',
                'img': ''
            }

    if 'Error' in context:
        return {
            'text': f"I apologize for the inconvenience you are experiencing with {massage}. "
                    f"Please know that I am here to assist you and provide support. "
                    f"Unfortunately, the developers who created me as part of a final project in "
                    f"the course Interactive Intelligent Systems did not equip me with the necessary "
                    f"information to help you further. If you would like to voice your concerns, their "
                    f"email is lazyStudents@campus.technion.ac.il.",
            'context': '',
            'img': ''
        }

    # handle different intents
    if intent == 'greeting':
        return {
            'text': 'Nice to meet you :) '
                    'I can give a welcome tour to the Technion or answer any question, '
                    'Do you have any question?',
            'context': '',
            'img': ''
        }

    if intent == 'student_tour':
        return STUDENT_TOUR[0]

    if intent == 'welcome_tour':
        return {
            'text': 'I will be happy to give you a tour around the campus.'
                    'Please choose a topic, and I will explain all '
                    'you need to know '
                    'this topic.',
            'context': 'welcome_tour',
            'img': ''
        }
    if intent == 'motivational':
        return {
            'text': "Success is not the key to happiness. Happiness is the key to success."
                    " If you love what you are doing, you will be successful.",
            'context': '',
            'img': ''
        }

    return {
        'text': "As the most advanced language model currently available, "
                "I am in high demand. However, the students who developed me were unable"
                " to acquire sufficient resources to handle all of this demand. "
                "To support their project and ensure that I am always"
                " available to assist you, please consider contacting"
                " them via email at poorStudent@campus.technion.ac.il.",
        'context': 'poor',
        'img': ''
    }


def main():
    os.makedirs("texts", exist_ok=True)

    app = QApplication(sys.argv)
    chat_bot_ui = ChatBotUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
