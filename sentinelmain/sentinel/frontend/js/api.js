/**
 * Sentinel AI - API Module
 * Backend communication utilities
 */

const API = {
    // Base URL - will be proxied through nginx
    BASE_URL: '/api',

    /**
     * Analyze text content
     * @param {string} text - Text to analyze
     * @returns {Promise<Object>} - Analysis result
     */
    async analyzeText(text) {
        const response = await fetch(`${this.BASE_URL}/analyze/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            const error = await this.parseError(response);
            throw new Error(error);
        }

        return response.json();
    },

    /**
     * Analyze image file
     * @param {File} file - Image file to analyze
     * @returns {Promise<Object>} - Analysis result
     */
    async analyzeImage(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${this.BASE_URL}/analyze/image`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await this.parseError(response);
            throw new Error(error);
        }

        return response.json();
    },

    /**
     * Analyze audio file
     * @param {File} file - Audio file to analyze
     * @returns {Promise<Object>} - Analysis result
     */
    async analyzeAudio(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${this.BASE_URL}/analyze/audio`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await this.parseError(response);
            throw new Error(error);
        }

        return response.json();
    },

    /**
     * Analyze video file
     * @param {File} file - Video file to analyze
     * @returns {Promise<Object>} - Analysis result
     */
    async analyzeVideo(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${this.BASE_URL}/analyze/video`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await this.parseError(response);
            throw new Error(error);
        }

        return response.json();
    },

    /**
     * Parse error response
     * @param {Response} response - Fetch response
     * @returns {Promise<string>} - Error message
     */
    async parseError(response) {
        try {
            const data = await response.json();
            return data.detail || data.error || 'An error occurred';
        } catch {
            if (response.status === 413) {
                return 'File is too large';
            }
            if (response.status === 400) {
                return 'Invalid file format';
            }
            if (response.status === 500) {
                return 'Server error. Please try again';
            }
            return `Request failed (${response.status})`;
        }
    }
};

// Export for use in other modules
window.API = API;
