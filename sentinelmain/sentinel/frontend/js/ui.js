/**
 * Sentinel AI - UI Module
 * DOM manipulation and display utilities
 */

const UI = {
    // DOM element references (cached on init)
    elements: {},

    /**
     * Initialize UI - cache DOM references
     */
    init() {
        this.elements = {
            // Sections
            inputSection: document.querySelector('.input-section'),
            loadingSection: document.getElementById('loading'),
            resultSection: document.getElementById('result'),
            errorSection: document.getElementById('error'),

            // Tabs
            tabBtns: document.querySelectorAll('.tab-btn'),
            tabPanels: document.querySelectorAll('.tab-panel'),

            // File inputs
            fileImage: document.getElementById('file-image'),
            fileVideo: document.getElementById('file-video'),
            fileAudio: document.getElementById('file-audio'),
            textInput: document.getElementById('text-input'),

            // Drop areas
            dropImage: document.getElementById('drop-image'),
            dropVideo: document.getElementById('drop-video'),
            dropAudio: document.getElementById('drop-audio'),

            // Previews
            previewImage: document.getElementById('preview-image'),
            previewVideo: document.getElementById('preview-video'),
            previewAudio: document.getElementById('preview-audio'),
            previewImg: document.getElementById('preview-img'),
            previewVid: document.getElementById('preview-vid'),
            previewAud: document.getElementById('preview-aud'),

            // Buttons
            checkBtn: document.getElementById('check-btn'),
            newCheckBtn: document.getElementById('new-check-btn'),
            retryBtn: document.getElementById('retry-btn'),

            // Result elements
            resultCard: document.getElementById('result-card'),
            riskBadge: document.getElementById('risk-badge'),
            riskIcon: document.getElementById('risk-icon'),
            riskLabel: document.getElementById('risk-label'),
            scoreValue: document.getElementById('score-value'),
            explanations: document.getElementById('explanations'),
            actionText: document.getElementById('action-text'),

            // Error
            errorMessage: document.getElementById('error-message'),

            // Character count
            charCount: document.getElementById('char-count')
        };
    },

    /**
     * Show loading state
     */
    showLoading() {
        this.elements.inputSection.hidden = true;
        this.elements.resultSection.hidden = true;
        this.elements.errorSection.hidden = true;
        this.elements.loadingSection.hidden = false;
    },

    /**
     * Hide loading state
     */
    hideLoading() {
        this.elements.loadingSection.hidden = true;
    },

    /**
     * Display analysis result
     * @param {Object} data - Analysis result from API
     */
    displayResult(data) {
        this.hideLoading();
        this.elements.inputSection.hidden = true;
        this.elements.errorSection.hidden = true;
        this.elements.resultSection.hidden = false;

        // Determine risk level
        const riskLevel = this.getRiskLevel(data.verdict);

        // Update card styling
        this.elements.resultCard.className = `result-card ${riskLevel}`;

        // Update badge
        this.elements.riskBadge.className = `risk-badge ${riskLevel}`;
        this.elements.riskIcon.textContent = this.getRiskIcon(riskLevel);
        this.elements.riskLabel.textContent = data.verdict;

        // Update score
        this.elements.scoreValue.textContent = data.risk_score;

        // Update explanations
        this.elements.explanations.innerHTML = data.explanations
            .map(exp => `
                <div class="explanation-item">
                    <span class="explanation-bullet"></span>
                    <p class="explanation-text">${this.escapeHtml(exp)}</p>
                </div>
            `)
            .join('');

        // Update action
        this.elements.actionText.textContent = data.action;
    },

    /**
     * Display error state
     * @param {string} message - Error message
     */
    displayError(message) {
        this.hideLoading();
        this.elements.inputSection.hidden = true;
        this.elements.resultSection.hidden = true;
        this.elements.errorSection.hidden = false;
        this.elements.errorMessage.textContent = message;
    },

    /**
     * Reset to initial state
     */
    reset() {
        this.elements.loadingSection.hidden = true;
        this.elements.resultSection.hidden = true;
        this.elements.errorSection.hidden = true;
        this.elements.inputSection.hidden = false;

        // Clear previews
        this.clearAllPreviews();

        // Reset text input
        this.elements.textInput.value = '';
        this.updateCharCount(0);

        // Disable check button
        this.setCheckButtonEnabled(false);
    },

    /**
     * Switch active tab
     * @param {string} tabId - Tab identifier (image, video, audio, text)
     */
    switchTab(tabId) {
        // Update tab buttons
        this.elements.tabBtns.forEach(btn => {
            const isActive = btn.dataset.tab === tabId;
            btn.classList.toggle('active', isActive);
            btn.setAttribute('aria-selected', isActive);
        });

        // Update tab panels
        this.elements.tabPanels.forEach(panel => {
            const panelId = panel.id.replace('panel-', '');
            const isActive = panelId === tabId;
            panel.classList.toggle('active', isActive);
            panel.hidden = !isActive;
        });

        // Clear previews and reset button
        this.clearAllPreviews();
        this.setCheckButtonEnabled(tabId === 'text' && this.elements.textInput.value.trim().length > 0);
    },

    /**
     * Show file preview
     * @param {string} type - Content type (image, video, audio)
     * @param {File} file - The file to preview
     */
    showFilePreview(type, file) {
        const url = URL.createObjectURL(file);

        switch (type) {
            case 'image':
                this.elements.previewImg.src = url;
                this.elements.dropImage.hidden = true;
                this.elements.previewImage.hidden = false;
                break;
            case 'video':
                this.elements.previewVid.src = url;
                this.elements.dropVideo.hidden = true;
                this.elements.previewVideo.hidden = false;
                break;
            case 'audio':
                this.elements.previewAud.src = url;
                this.elements.dropAudio.hidden = true;
                this.elements.previewAudio.hidden = false;
                break;
        }

        this.setCheckButtonEnabled(true);
    },

    /**
     * Clear file preview
     * @param {string} type - Content type (image, video, audio)
     */
    clearPreview(type) {
        switch (type) {
            case 'image':
                if (this.elements.previewImg.src) {
                    URL.revokeObjectURL(this.elements.previewImg.src);
                }
                this.elements.previewImg.src = '';
                this.elements.previewImage.hidden = true;
                this.elements.dropImage.hidden = false;
                this.elements.fileImage.value = '';
                break;
            case 'video':
                if (this.elements.previewVid.src) {
                    URL.revokeObjectURL(this.elements.previewVid.src);
                }
                this.elements.previewVid.src = '';
                this.elements.previewVideo.hidden = true;
                this.elements.dropVideo.hidden = false;
                this.elements.fileVideo.value = '';
                break;
            case 'audio':
                if (this.elements.previewAud.src) {
                    URL.revokeObjectURL(this.elements.previewAud.src);
                }
                this.elements.previewAud.src = '';
                this.elements.previewAudio.hidden = true;
                this.elements.dropAudio.hidden = false;
                this.elements.fileAudio.value = '';
                break;
        }

        this.setCheckButtonEnabled(false);
    },

    /**
     * Clear all previews
     */
    clearAllPreviews() {
        ['image', 'video', 'audio'].forEach(type => this.clearPreview(type));
    },

    /**
     * Set drag over state on drop area
     * @param {HTMLElement} dropArea - The drop area element
     * @param {boolean} isDragging - Whether dragging over
     */
    setDragOver(dropArea, isDragging) {
        dropArea.classList.toggle('drag-over', isDragging);
    },

    /**
     * Enable/disable check button
     * @param {boolean} enabled - Whether to enable
     */
    setCheckButtonEnabled(enabled) {
        this.elements.checkBtn.disabled = !enabled;
    },

    /**
     * Update character count display
     * @param {number} count - Character count
     */
    updateCharCount(count) {
        this.elements.charCount.textContent = count.toLocaleString();
    },

    /**
     * Get risk level from verdict
     * @param {string} verdict - Verdict string
     * @returns {string} - Risk level (safe, caution, danger)
     */
    getRiskLevel(verdict) {
        switch (verdict) {
            case 'Safe':
                return 'safe';
            case 'Possibly AI':
                return 'caution';
            case 'High Risk':
                return 'danger';
            default:
                return 'caution';
        }
    },

    /**
     * Get icon for risk level
     * @param {string} level - Risk level
     * @returns {string} - Emoji icon
     */
    getRiskIcon(level) {
        switch (level) {
            case 'safe':
                return '✓';
            case 'caution':
                return '⚠';
            case 'danger':
                return '✕';
            default:
                return '?';
        }
    },

    /**
     * Escape HTML to prevent XSS
     * @param {string} text - Text to escape
     * @returns {string} - Escaped text
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Export for use in other modules
window.UI = UI;
