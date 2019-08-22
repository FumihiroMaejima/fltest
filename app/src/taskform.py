from flask import Flask

class TaskForm():
    title = None
    content = None

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def title_require(self):
        validation_msg = ''
        target_title = self.title

        if(target_title == ''):
            validation_msg = 'タスク名を入力してください。'

        return validation_msg

    def title_length(self):
        validation_msg = ''
        title_length = len(self.title)

        if(title_length > 20):
            validation_msg = '20文字以内で入力してください。　'

        return validation_msg

    def content_length(self):
        validation_msg = ''
        content_length = len(self.content)

        if(content_length > 600):
            validation_msg = '600文字以内で入力してください。　'

        return validation_msg
