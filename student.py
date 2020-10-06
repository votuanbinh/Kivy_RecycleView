from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import ObjectProperty

KV = '''

<MyViewClass>:
    orientation: 'horizontal'
    CheckBox:
        on_state: root.set_state(self.state,app)
    Label:
        text: root.text

BoxLayout:
    orientation: 'vertical'    
    padding: 10
    spacing: 10

    BoxLayout:
        size_hint_y: None
        height: "40dp"

        Label:
            text: "First name"
        TextInput:
            id: first_name
        Label:
            text: "Last name"
        TextInput:
            id: last_name
    BoxLayout:
        Button:
            size_hint_y: 0.1
            text: "Submit"
            on_release: rv.submit()
        Button:
            size_hint_y: 0.1
            text: "Delete"
            on_release: rv.delete()
        Button:
            size_hint_y: 0.1
            text: "Replace"
            on_release: rv.replace()
    
    MyRecycleView:
        first_name: first_name
        last_name: last_name
        id: rv
        viewclass: 'MyViewClass'
        RecycleBoxLayout:
            orientation: 'vertical'
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
                   
'''

class MyViewClass(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty("")
    index = None

    def set_state(self,state,app):
        app.root.ids.rv.data[self.index]['selected'] = state

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(MyViewClass, self).refresh_view_attrs(rv, index, data)

class MyRecycleView(RecycleView):
    data = [{"text": "Ruby", "selected": 'normal'}]
    first_name = ObjectProperty()
    last_name = ObjectProperty()
   
    def submit(self):
        if self.first_name.text != "" or self.last_name.text != "":
            self.data.append({'text': self.first_name.text + ' ' + self.last_name.text, "selected": 'normal'})
        self.refresh_from_data()

    def delete(self):
        for item in self.data: 
            if item['selected'] == 'down':
                self.data.remove(item)
        self.refresh_from_data()
        
    def replace(self):
        if self.first_name.text != "" or self.last_name.text != "":
            for item in self.data: 
                if item['selected'] == 'down':
                    item['text'] = self.first_name.text + ' ' + self.last_name.text
        self.refresh_from_data()   
   

class Test(App):
    def build(self):
        root = Builder.load_string(KV)
        return root

Test().run()