from django import forms

from .models import Topic,Entry
    
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title','text',]
        labels = {'title':'标题','text': '内容'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
        '''小部件 （widget）是一个HTML表单
        元素，如单行文本框、多行文本区域或下拉列表。通过设置属性widgets
        ，可覆盖Django选择的默认小部件。通过让Django使用forms.Textarea
        ，我们定制了字段'text' 的输入小部件，将文本区域的宽度设置为80
        列，而不是默认的40列。这给用户提供了足够的空间来编写有意义的条
        目。'''