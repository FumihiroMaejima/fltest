from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, ValidationError


class BlogForm(FlaskForm):
    blog_title = StringField("タイトル")
    description = TextAreaField("本文")
    tags = StringField("タグ (カンマ区切りで入力してください。)")

    def validate_blog_title(self, blog_title):
        """バリデーション内容:
        - 未入力は禁止
        - 文字数が10文字以上は禁止
        - 「/」を含むことは禁止
        """
        if blog_title.data == "":
            raise ValidationError("タイトルを入力してください")

        if len(blog_title.data) > 10:
            raise ValidationError("タイトルは10文字以下にしてください。")

        if "/" in blog_title.data:
            raise ValidationError("タイトルに「/」は含められません。")

    def validate_description(self, description):
        """バリデーション内容:
        - 未入力は禁止
        - 文字数が10文字未満は禁止
        """

        if description.data == "":
            raise ValidationError("本文を入力してください。")

        if len(description.data) < 10:
            raise ValidationError("本文は10文字以上にしてください。")

    def validate_tags(self, tags):
        """バリデーション内容:
        - 4つ以上は禁止
        """

        tag_list = tags.data.strip().split(",")
        if len(tag_list) > 3:
            raise ValidationError("タグは3つ以下にしてください。")
