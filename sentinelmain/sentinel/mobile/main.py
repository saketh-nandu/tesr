"""
Sentinel AI Mobile Application
Python-based mobile app using KivyMD
"""

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from plyer import filechooser
import requests
import os
import base64


class HomeScreen(MDScreen):
    """Main home screen with tabs for different content types"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        self.selected_file = None
        self.content_type = 'text'
        self.build_ui()
    
    def build_ui(self):
        """Build the main UI"""
        layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20)
        )
        
        # Header
        header = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            spacing=dp(10)
        )
        
        title = MDLabel(
            text="Sentinel AI",
            font_style="H4",
            halign="center",
            theme_text_color="Primary"
        )
        
        subtitle = MDLabel(
            text="Check if it's real or a scam",
            font_style="Body1",
            halign="center",
            theme_text_color="Secondary"
        )
        
        header.add_widget(title)
        header.add_widget(subtitle)
        
        # Tabs for content types
        self.tabs = MDTabs(
            on_tab_switch=self.on_tab_switch,
            background_color=self.theme_cls.primary_color
        )
        
        # Add tabs
        self.text_tab = Tab(title="Text", icon="text")
        self.image_tab = Tab(title="Image", icon="image")
        self.audio_tab = Tab(title="Audio", icon="microphone")
        self.video_tab = Tab(title="Video", icon="video")
        
        self.tabs.add_widget(self.text_tab)
        self.tabs.add_widget(self.image_tab)
        self.tabs.add_widget(self.audio_tab)
        self.tabs.add_widget(self.video_tab)
        
        # Content area
        self.content_area = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(10)
        )
        
        # Text input (default)
        self.text_input = MDTextField(
            hint_text="Paste the message or text you want to check...",
            multiline=True,
            mode="outlined",
            max_height=dp(200),
            helper_text="Max 10,000 characters",
            helper_text_mode="on_focus"
        )
        
        # File selection card (hidden by default)
        self.file_card = MDCard(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(200),
            elevation=2
        )
        
        file_icon = MDIconButton(
            icon="upload",
            pos_hint={'center_x': 0.5},
            icon_size=dp(48)
        )
        
        self.file_label = MDLabel(
            text="Tap to select file",
            halign="center",
            theme_text_color="Secondary"
        )
        
        select_btn = MDRaisedButton(
            text="Choose File",
            pos_hint={'center_x': 0.5},
            on_release=self.select_file
        )
        
        self.file_card.add_widget(file_icon)
        self.file_card.add_widget(self.file_label)
        self.file_card.add_widget(select_btn)
        
        # Preview area
        self.preview_area = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(250)
        )
        
        # Add text input by default
        self.content_area.add_widget(self.text_input)
        
        # Check button
        self.check_btn = MDRaisedButton(
            text="Check",
            pos_hint={'center_x': 0.5},
            size_hint_x=0.8,
            on_release=self.analyze_content
        )
        
        # Add all to layout
        layout.add_widget(header)
        layout.add_widget(self.tabs)
        layout.add_widget(self.content_area)
        layout.add_widget(self.check_btn)
        
        self.add_widget(layout)
    
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """Handle tab switching"""
        self.content_area.clear_widgets()
        self.selected_file = None
        
        if tab_text == "Text":
            self.content_type = 'text'
            self.content_area.add_widget(self.text_input)
        else:
            if tab_text == "Image":
                self.content_type = 'image'
            elif tab_text == "Audio":
                self.content_type = 'audio'
            elif tab_text == "Video":
                self.content_type = 'video'
            
            self.content_area.add_widget(self.file_card)
            self.content_area.add_widget(self.preview_area)
    
    def select_file(self, instance):
        """Open file picker"""
        if self.content_type == 'image':
            filters = [("Images", "*.jpg", "*.jpeg", "*.png")]
        elif self.content_type == 'audio':
            filters = [("Audio", "*.mp3", "*.wav", "*.m4a")]
        elif self.content_type == 'video':
            filters = [("Video", "*.mp4", "*.mov", "*.webm")]
        else:
            filters = []
        
        try:
            selection = filechooser.open_file(
                title="Select file",
                filters=filters
            )
            
            if selection:
                self.selected_file = selection[0]
                self.file_label.text = f"Selected: {os.path.basename(self.selected_file)}"
                self.show_preview()
        except Exception as e:
            self.show_error(f"Error selecting file: {str(e)}")
    
    def show_preview(self):
        """Show preview of selected file"""
        self.preview_area.clear_widgets()
        
        if self.content_type == 'image' and self.selected_file:
            img = Image(
                source=self.selected_file,
                size_hint=(1, 1)
            )
            self.preview_area.add_widget(img)
        elif self.content_type == 'video' and self.selected_file:
            vid = Video(
                source=self.selected_file,
                state='play',
                options={'eos': 'loop'}
            )
            self.preview_area.add_widget(vid)
    
    def analyze_content(self, instance):
        """Analyze the content"""
        # Show loading dialog
        self.loading_dialog = MDDialog(
            title="Analyzing...",
            type="custom",
            content_cls=MDCircularProgressIndicator(
                size_hint=(None, None),
                size=(dp(48), dp(48)),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
        )
        self.loading_dialog.open()
        
        # Perform analysis in background
        Clock.schedule_once(self.perform_analysis, 0.5)
    
    def perform_analysis(self, dt):
        """Perform the actual analysis"""
        try:
            api_url = "http://localhost:8000"  # Change to your backend URL
            
            if self.content_type == 'text':
                text = self.text_input.text
                if not text.strip():
                    raise ValueError("Please enter some text")
                
                response = requests.post(
                    f"{api_url}/analyze/text",
                    json={"text": text},
                    timeout=30
                )
            else:
                if not self.selected_file:
                    raise ValueError("Please select a file")
                
                with open(self.selected_file, 'rb') as f:
                    files = {'file': f}
                    response = requests.post(
                        f"{api_url}/analyze/{self.content_type}",
                        files=files,
                        timeout=60
                    )
            
            if response.status_code == 200:
                result = response.json()
                self.loading_dialog.dismiss()
                self.show_result(result)
            else:
                raise Exception(f"Server error: {response.status_code}")
        
        except Exception as e:
            self.loading_dialog.dismiss()
            self.show_error(str(e))
    
    def show_result(self, result):
        """Show analysis result"""
        self.manager.get_screen('result').display_result(result)
        self.manager.current = 'result'
    
    def show_error(self, message):
        """Show error dialog"""
        dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()


class Tab(MDFloatLayout, MDTabsBase):
    """Tab widget"""
    pass


class ResultScreen(MDScreen):
    """Screen to display analysis results"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'result'
        self.build_ui()
    
    def build_ui(self):
        """Build result UI"""
        self.layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20)
        )
        
        # Result card
        self.result_card = MDCard(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15),
            elevation=3
        )
        
        # Risk badge
        self.risk_badge = MDLabel(
            text="",
            font_style="H5",
            halign="center",
            theme_text_color="Custom"
        )
        
        # Risk score
        self.risk_score = MDLabel(
            text="",
            font_style="H3",
            halign="center",
            theme_text_color="Primary"
        )
        
        # Explanations
        self.explanations = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        self.explanations.bind(minimum_height=self.explanations.setter('height'))
        
        # Action text
        self.action_card = MDCard(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(100)
        )
        
        self.action_text = MDLabel(
            text="",
            theme_text_color="Secondary",
            halign="left"
        )
        
        self.action_card.add_widget(self.action_text)
        
        # Back button
        back_btn = MDRaisedButton(
            text="Check Another",
            pos_hint={'center_x': 0.5},
            on_release=self.go_back
        )
        
        # Add to card
        self.result_card.add_widget(self.risk_badge)
        self.result_card.add_widget(self.risk_score)
        self.result_card.add_widget(self.explanations)
        self.result_card.add_widget(self.action_card)
        
        # Add to layout
        self.layout.add_widget(self.result_card)
        self.layout.add_widget(back_btn)
        
        self.add_widget(self.layout)
    
    def display_result(self, result):
        """Display the analysis result"""
        # Update risk badge
        verdict = result.get('verdict', 'Unknown')
        self.risk_badge.text = verdict
        
        # Set color based on verdict
        if verdict == 'Safe':
            self.risk_badge.text_color = (0.13, 0.77, 0.37, 1)  # Green
        elif verdict == 'Possibly AI':
            self.risk_badge.text_color = (0.96, 0.62, 0.04, 1)  # Orange
        else:
            self.risk_badge.text_color = (0.94, 0.27, 0.27, 1)  # Red
        
        # Update risk score
        risk_score = result.get('risk_score', 0)
        self.risk_score.text = f"Risk Score: {risk_score}"
        
        # Update explanations
        self.explanations.clear_widgets()
        explanations = result.get('explanations', [])
        for exp in explanations:
            exp_label = MDLabel(
                text=f"• {exp}",
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(40)
            )
            self.explanations.add_widget(exp_label)
        
        # Update action
        action = result.get('action', '')
        self.action_text.text = action
    
    def go_back(self, instance):
        """Go back to home screen"""
        self.manager.current = 'home'


class SentinelApp(MDApp):
    """Main application class"""
    
    def build(self):
        """Build the app"""
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Screen manager
        sm = MDScreenManager()
        sm.add_widget(HomeScreen())
        sm.add_widget(ResultScreen())
        
        return sm


if __name__ == '__main__':
    SentinelApp().run()
