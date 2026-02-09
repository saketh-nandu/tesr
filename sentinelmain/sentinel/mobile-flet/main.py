"""
Sentinel AI Mobile Application
Built with Flet (Flutter-based Python framework)
Easier to build and deploy than Kivy
"""

import flet as ft
import requests
import base64
import os
from io import BytesIO


class SentinelApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sentinel AI"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.scroll = ft.ScrollMode.AUTO
        
        # API Configuration
        # Your Render backend URL
        self.api_url = "https://sentinel-ai-3yc8.onrender.com"
        
        # State
        self.selected_file = None
        self.current_tab = "text"
        
        # Build UI
        self.build_ui()
    
    def build_ui(self):
        """Build the main UI"""
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.SHIELD, size=40, color=ft.colors.BLUE),
                    ft.Text("Sentinel AI", size=32, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text(
                    "Check if it's real or a scam",
                    size=16,
                    color=ft.colors.GREY_700,
                    text_align=ft.TextAlign.CENTER
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.only(bottom=20)
        )
        
        # Tabs
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            on_change=self.on_tab_change,
            tabs=[
                ft.Tab(
                    text="Text",
                    icon=ft.icons.TEXT_FIELDS,
                ),
                ft.Tab(
                    text="Image",
                    icon=ft.icons.IMAGE,
                ),
                ft.Tab(
                    text="Audio",
                    icon=ft.icons.MIC,
                ),
                ft.Tab(
                    text="Video",
                    icon=ft.icons.VIDEO_LIBRARY,
                ),
            ],
        )
        
        # Content area
        self.content_area = ft.Container(
            content=self.build_text_input(),
            padding=20,
        )
        
        # Check button
        self.check_button = ft.ElevatedButton(
            "Check",
            icon=ft.icons.SHIELD_OUTLINED,
            on_click=self.analyze_content,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE,
                padding=15,
            ),
            width=200,
        )
        
        # Loading indicator
        self.loading = ft.ProgressRing(visible=False)
        
        # Result area
        self.result_area = ft.Container(visible=False)
        
        # Add all to page
        self.page.add(
            header,
            self.tabs,
            self.content_area,
            ft.Row(
                [self.check_button, self.loading],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            self.result_area,
        )
    
    def build_text_input(self):
        """Build text input UI"""
        self.text_field = ft.TextField(
            label="Enter text to analyze",
            multiline=True,
            min_lines=5,
            max_lines=10,
            max_length=10000,
            counter_text="",
            on_change=self.update_char_count,
        )
        
        self.char_count = ft.Text("0 / 10,000 characters", size=12, color=ft.colors.GREY_600)
        
        return ft.Column([
            self.text_field,
            self.char_count,
        ])
    
    def build_file_picker(self):
        """Build file picker UI"""
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.page.overlay.append(self.file_picker)
        
        self.file_info = ft.Text("No file selected", size=14, color=ft.colors.GREY_600)
        
        self.preview_image = ft.Image(
            visible=False,
            width=300,
            height=300,
            fit=ft.ImageFit.CONTAIN,
        )
        
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.UPLOAD_FILE, size=60, color=ft.colors.BLUE_200),
                    ft.Text("Tap to select file", size=16),
                    ft.ElevatedButton(
                        "Choose File",
                        icon=ft.icons.FOLDER_OPEN,
                        on_click=self.open_file_picker,
                    ),
                    self.file_info,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                border=ft.border.all(2, ft.colors.BLUE_200),
                border_radius=10,
                padding=30,
                alignment=ft.alignment.center,
            ),
            self.preview_image,
        ])
    
    def on_tab_change(self, e):
        """Handle tab change"""
        tab_index = e.control.selected_index
        tabs = ["text", "image", "audio", "video"]
        self.current_tab = tabs[tab_index]
        self.selected_file = None
        
        if self.current_tab == "text":
            self.content_area.content = self.build_text_input()
        else:
            self.content_area.content = self.build_file_picker()
        
        self.result_area.visible = False
        self.page.update()
    
    def open_file_picker(self, e):
        """Open file picker dialog"""
        if self.current_tab == "image":
            self.file_picker.pick_files(
                allowed_extensions=["jpg", "jpeg", "png"],
                dialog_title="Select Image"
            )
        elif self.current_tab == "audio":
            self.file_picker.pick_files(
                allowed_extensions=["mp3", "wav", "m4a"],
                dialog_title="Select Audio"
            )
        elif self.current_tab == "video":
            self.file_picker.pick_files(
                allowed_extensions=["mp4", "mov", "webm"],
                dialog_title="Select Video"
            )
    
    def on_file_picked(self, e: ft.FilePickerResultEvent):
        """Handle file selection"""
        if e.files:
            self.selected_file = e.files[0].path
            filename = os.path.basename(self.selected_file)
            self.file_info.value = f"Selected: {filename}"
            
            # Show preview for images
            if self.current_tab == "image":
                self.preview_image.src = self.selected_file
                self.preview_image.visible = True
            
            self.page.update()
    
    def update_char_count(self, e):
        """Update character count"""
        count = len(self.text_field.value or "")
        self.char_count.value = f"{count:,} / 10,000 characters"
        self.page.update()
    
    def analyze_content(self, e):
        """Analyze the content"""
        # Show loading
        self.loading.visible = True
        self.check_button.disabled = True
        self.result_area.visible = False
        self.page.update()
        
        try:
            if self.current_tab == "text":
                text = self.text_field.value
                if not text or not text.strip():
                    raise ValueError("Please enter some text")
                
                response = requests.post(
                    f"{self.api_url}/analyze/text",
                    json={"text": text},
                    timeout=30
                )
            else:
                if not self.selected_file:
                    raise ValueError("Please select a file")
                
                # Get file name and open file
                filename = os.path.basename(self.selected_file)
                
                with open(self.selected_file, 'rb') as f:
                    files = {'file': (filename, f, self.get_content_type())}
                    response = requests.post(
                        f"{self.api_url}/analyze/{self.current_tab}",
                        files=files,
                        timeout=120
                    )
            
            if response.status_code == 200:
                result = response.json()
                self.display_result(result)
            else:
                error_msg = f"Server error: {response.status_code}"
                try:
                    error_detail = response.json()
                    if 'detail' in error_detail:
                        error_msg = f"{error_msg} - {error_detail['detail']}"
                except:
                    pass
                raise Exception(error_msg)
        
        except requests.exceptions.Timeout:
            self.show_error("Request timed out. The file might be too large or server is slow.")
        except requests.exceptions.ConnectionError:
            self.show_error("Cannot connect to server. Check your internet connection.")
        except Exception as error:
            self.show_error(str(error))
        
        finally:
            self.loading.visible = False
            self.check_button.disabled = False
            self.page.update()
    
    def get_content_type(self):
        """Get content type based on current tab"""
        if self.current_tab == "image":
            if self.selected_file.lower().endswith('.png'):
                return 'image/png'
            return 'image/jpeg'
        elif self.current_tab == "audio":
            if self.selected_file.lower().endswith('.wav'):
                return 'audio/wav'
            elif self.selected_file.lower().endswith('.m4a'):
                return 'audio/mp4'
            return 'audio/mpeg'
        elif self.current_tab == "video":
            if self.selected_file.lower().endswith('.mov'):
                return 'video/quicktime'
            elif self.selected_file.lower().endswith('.webm'):
                return 'video/webm'
            return 'video/mp4'
        return 'application/octet-stream'
    
    def display_result(self, result):
        """Display analysis result"""
        verdict = result.get('verdict', 'Unknown')
        risk_score = result.get('risk_score', 0)
        explanations = result.get('explanations', [])
        action = result.get('action', '')
        
        # Determine color based on verdict
        if verdict == 'Safe':
            color = ft.colors.GREEN
            icon = ft.icons.CHECK_CIRCLE
        elif verdict == 'Possibly AI':
            color = ft.colors.ORANGE
            icon = ft.icons.WARNING
        else:
            color = ft.colors.RED
            icon = ft.icons.DANGEROUS
        
        # Build result UI
        result_content = ft.Column([
            # Risk badge
            ft.Container(
                content=ft.Row([
                    ft.Icon(icon, color=color, size=30),
                    ft.Text(verdict, size=24, weight=ft.FontWeight.BOLD, color=color),
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=20,
            ),
            
            # Risk score
            ft.Container(
                content=ft.Column([
                    ft.Text(str(risk_score), size=48, weight=ft.FontWeight.BOLD),
                    ft.Text("Risk Score", size=14, color=ft.colors.GREY_600),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=10,
            ),
            
            ft.Divider(),
            
            # Explanations
            ft.Text("Why?", size=18, weight=ft.FontWeight.BOLD),
            ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.CIRCLE, size=8, color=ft.colors.BLUE),
                    ft.Text(exp, size=14, expand=True),
                ])
                for exp in explanations
            ]),
            
            ft.Divider(),
            
            # Action
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.INFO_OUTLINE, color=ft.colors.BLUE),
                        ft.Text("What to do:", weight=ft.FontWeight.BOLD),
                    ]),
                    ft.Text(action, size=14),
                ]),
                bgcolor=ft.colors.BLUE_50,
                border_radius=10,
                padding=15,
            ),
            
            # New check button
            ft.ElevatedButton(
                "Check Another",
                icon=ft.icons.REFRESH,
                on_click=self.reset_app,
                style=ft.ButtonStyle(
                    color=ft.colors.BLUE,
                ),
            ),
        ])
        
        self.result_area.content = ft.Card(
            content=ft.Container(
                content=result_content,
                padding=20,
            ),
            elevation=5,
        )
        self.result_area.visible = True
        self.page.update()
    
    def show_error(self, message):
        """Show error message"""
        # Add helpful context for common errors
        if "500" in message:
            message += "\n\n💡 Tip: Your backend might need to be redeployed with the latest code. The free tier may also be sleeping (first request takes 30-60 seconds)."
        elif "Connection" in message or "connect" in message.lower():
            message += "\n\n💡 Tip: Check if your backend URL is correct and accessible."
        
        self.result_area.content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.ERROR_OUTLINE, size=60, color=ft.colors.RED),
                    ft.Text("Error", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(message, size=14, text_align=ft.TextAlign.CENTER),
                    ft.ElevatedButton(
                        "Try Again",
                        on_click=self.reset_app,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
            ),
            elevation=5,
        )
        self.result_area.visible = True
        self.page.update()
    
    def reset_app(self, e):
        """Reset app to initial state"""
        self.result_area.visible = False
        self.selected_file = None
        if self.current_tab == "text":
            self.text_field.value = ""
            self.char_count.value = "0 / 10,000 characters"
        else:
            self.file_info.value = "No file selected"
            self.preview_image.visible = False
        self.page.update()


def main(page: ft.Page):
    SentinelApp(page)


if __name__ == "__main__":
    ft.app(target=main)
