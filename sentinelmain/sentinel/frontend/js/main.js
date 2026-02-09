/**
 * Sentinel AI - Main Application Entry Point
 * Initializes the app and handles user interactions
 */

const App = {
    // Current state
    state: {
        activeTab: 'image',
        selectedFile: null,
        isLoading: false
    },

    /**
     * Initialize the application
     */
    init() {
        // Initialize UI module
        UI.init();

        // Set up event listeners
        this.setupTabNavigation();
        this.setupFileInputs();
        this.setupDragAndDrop();
        this.setupTextInput();
        this.setupButtons();

        console.log('Sentinel AI initialized');
    },

    /**
     * Set up tab navigation
     */
    setupTabNavigation() {
        UI.elements.tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const tabId = btn.dataset.tab;
                this.state.activeTab = tabId;
                this.state.selectedFile = null;
                UI.switchTab(tabId);
            });
        });
    },

    /**
     * Set up file input handlers
     */
    setupFileInputs() {
        // Image input
        UI.elements.fileImage.addEventListener('change', (e) => {
            this.handleFileSelect('image', e.target.files[0]);
        });

        // Video input
        UI.elements.fileVideo.addEventListener('change', (e) => {
            this.handleFileSelect('video', e.target.files[0]);
        });

        // Audio input
        UI.elements.fileAudio.addEventListener('change', (e) => {
            this.handleFileSelect('audio', e.target.files[0]);
        });

        // Remove file buttons
        document.querySelectorAll('.remove-file').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const type = this.state.activeTab;
                UI.clearPreview(type);
                this.state.selectedFile = null;
            });
        });
    },

    /**
     * Set up drag and drop handlers
     */
    setupDragAndDrop() {
        const dropAreas = [
            { element: UI.elements.dropImage, type: 'image' },
            { element: UI.elements.dropVideo, type: 'video' },
            { element: UI.elements.dropAudio, type: 'audio' }
        ];

        dropAreas.forEach(({ element, type }) => {
            if (!element) return;

            // Click to open file dialog
            element.addEventListener('click', () => {
                const input = document.getElementById(`file-${type}`);
                input.click();
            });

            // Drag events
            element.addEventListener('dragover', (e) => {
                e.preventDefault();
                UI.setDragOver(element, true);
            });

            element.addEventListener('dragleave', (e) => {
                e.preventDefault();
                UI.setDragOver(element, false);
            });

            element.addEventListener('drop', (e) => {
                e.preventDefault();
                UI.setDragOver(element, false);

                const file = e.dataTransfer.files[0];
                if (file) {
                    this.handleFileSelect(type, file);
                }
            });
        });
    },

    /**
     * Set up text input handler
     */
    setupTextInput() {
        UI.elements.textInput.addEventListener('input', (e) => {
            const text = e.target.value;
            UI.updateCharCount(text.length);
            UI.setCheckButtonEnabled(text.trim().length > 0);
        });
    },

    /**
     * Set up button handlers
     */
    setupButtons() {
        // Check button
        UI.elements.checkBtn.addEventListener('click', () => {
            this.handleCheck();
        });

        // New check button
        UI.elements.newCheckBtn.addEventListener('click', () => {
            UI.reset();
            this.state.selectedFile = null;
        });

        // Retry button
        UI.elements.retryBtn.addEventListener('click', () => {
            UI.reset();
            this.state.selectedFile = null;
        });
    },

    /**
     * Handle file selection
     * @param {string} type - File type (image, video, audio)
     * @param {File} file - Selected file
     */
    async handleFileSelect(type, file) {
        if (!file) return;

        // Validate file
        let validation;
        switch (type) {
            case 'image':
                validation = Validators.validateImage(file);
                break;
            case 'video':
                validation = await Validators.validateVideo(file);
                break;
            case 'audio':
                validation = await Validators.validateAudio(file);
                break;
        }

        if (!validation.valid) {
            alert(validation.error);
            return;
        }

        // Store file and show preview
        this.state.selectedFile = file;
        UI.showFilePreview(type, file);
    },

    /**
     * Handle check button click
     */
    async handleCheck() {
        if (this.state.isLoading) return;

        const type = this.state.activeTab;

        try {
            this.state.isLoading = true;
            UI.showLoading();

            let result;

            switch (type) {
                case 'text':
                    const text = UI.elements.textInput.value;
                    const textValidation = Validators.validateText(text);
                    if (!textValidation.valid) {
                        throw new Error(textValidation.error);
                    }
                    result = await API.analyzeText(text);
                    break;

                case 'image':
                    if (!this.state.selectedFile) {
                        throw new Error('Please select an image');
                    }
                    result = await API.analyzeImage(this.state.selectedFile);
                    break;

                case 'audio':
                    if (!this.state.selectedFile) {
                        throw new Error('Please select an audio file');
                    }
                    result = await API.analyzeAudio(this.state.selectedFile);
                    break;

                case 'video':
                    if (!this.state.selectedFile) {
                        throw new Error('Please select a video');
                    }
                    result = await API.analyzeVideo(this.state.selectedFile);
                    break;
            }

            UI.displayResult(result);

        } catch (error) {
            console.error('Analysis error:', error);
            UI.displayError(error.message || 'Something went wrong. Please try again.');
        } finally {
            this.state.isLoading = false;
        }
    }
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});
