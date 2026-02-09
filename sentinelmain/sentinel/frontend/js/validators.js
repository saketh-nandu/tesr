/**
 * Sentinel AI - Validators Module
 * File type and content validation utilities
 */

const Validators = {
    // File size limits in bytes
    MAX_FILE_SIZE: 50 * 1024 * 1024, // 50MB

    // Duration limits in seconds
    MAX_AUDIO_DURATION: 30,
    MAX_VIDEO_DURATION: 8,

    // Text limits
    MAX_TEXT_LENGTH: 10000,
    MIN_TEXT_LENGTH: 1,

    // Allowed MIME types
    ALLOWED_TYPES: {
        image: ['image/jpeg', 'image/png'],
        video: ['video/mp4', 'video/quicktime', 'video/webm'],
        audio: ['audio/mpeg', 'audio/wav', 'audio/x-wav', 'audio/mp4', 'audio/ogg']
    },

    /**
     * Validate image file
     * @param {File} file - The file to validate
     * @returns {Object} - { valid: boolean, error: string|null }
     */
    validateImage(file) {
        if (!file) {
            return { valid: false, error: 'No file selected' };
        }

        if (!this.ALLOWED_TYPES.image.includes(file.type)) {
            return { valid: false, error: 'Please upload a JPG or PNG image' };
        }

        if (file.size > this.MAX_FILE_SIZE) {
            return { valid: false, error: 'File is too large. Maximum size is 50MB' };
        }

        return { valid: true, error: null };
    },

    /**
     * Validate video file
     * @param {File} file - The file to validate
     * @returns {Promise<Object>} - { valid: boolean, error: string|null, duration: number }
     */
    async validateVideo(file) {
        if (!file) {
            return { valid: false, error: 'No file selected' };
        }

        if (!this.ALLOWED_TYPES.video.includes(file.type)) {
            return { valid: false, error: 'Please upload an MP4, MOV, or WebM video' };
        }

        if (file.size > this.MAX_FILE_SIZE) {
            return { valid: false, error: 'File is too large. Maximum size is 50MB' };
        }

        // Check duration
        try {
            const duration = await this.getVideoDuration(file);
            if (duration > this.MAX_VIDEO_DURATION) {
                return {
                    valid: false,
                    error: `Video is too long. Maximum duration is ${this.MAX_VIDEO_DURATION} seconds`,
                    duration
                };
            }
            return { valid: true, error: null, duration };
        } catch (e) {
            // If we can't check duration, allow the upload (backend will validate)
            return { valid: true, error: null, duration: null };
        }
    },

    /**
     * Validate audio file
     * @param {File} file - The file to validate
     * @returns {Promise<Object>} - { valid: boolean, error: string|null, duration: number }
     */
    async validateAudio(file) {
        if (!file) {
            return { valid: false, error: 'No file selected' };
        }

        if (!this.ALLOWED_TYPES.audio.includes(file.type)) {
            return { valid: false, error: 'Please upload an MP3, WAV, or M4A audio file' };
        }

        if (file.size > this.MAX_FILE_SIZE) {
            return { valid: false, error: 'File is too large. Maximum size is 50MB' };
        }

        // Check duration
        try {
            const duration = await this.getAudioDuration(file);
            if (duration > this.MAX_AUDIO_DURATION) {
                return {
                    valid: false,
                    error: `Audio is too long. Maximum duration is ${this.MAX_AUDIO_DURATION} seconds`,
                    duration
                };
            }
            return { valid: true, error: null, duration };
        } catch (e) {
            // If we can't check duration, allow the upload (backend will validate)
            return { valid: true, error: null, duration: null };
        }
    },

    /**
     * Validate text content
     * @param {string} text - The text to validate
     * @returns {Object} - { valid: boolean, error: string|null }
     */
    validateText(text) {
        if (!text || text.trim().length < this.MIN_TEXT_LENGTH) {
            return { valid: false, error: 'Please enter some text to analyze' };
        }

        if (text.length > this.MAX_TEXT_LENGTH) {
            return {
                valid: false,
                error: `Text is too long. Maximum length is ${this.MAX_TEXT_LENGTH.toLocaleString()} characters`
            };
        }

        return { valid: true, error: null };
    },

    /**
     * Get video duration
     * @param {File} file - Video file
     * @returns {Promise<number>} - Duration in seconds
     */
    getVideoDuration(file) {
        return new Promise((resolve, reject) => {
            const video = document.createElement('video');
            video.preload = 'metadata';

            video.onloadedmetadata = () => {
                URL.revokeObjectURL(video.src);
                resolve(video.duration);
            };

            video.onerror = () => {
                URL.revokeObjectURL(video.src);
                reject(new Error('Could not load video'));
            };

            video.src = URL.createObjectURL(file);
        });
    },

    /**
     * Get audio duration
     * @param {File} file - Audio file
     * @returns {Promise<number>} - Duration in seconds
     */
    getAudioDuration(file) {
        return new Promise((resolve, reject) => {
            const audio = document.createElement('audio');
            audio.preload = 'metadata';

            audio.onloadedmetadata = () => {
                URL.revokeObjectURL(audio.src);
                resolve(audio.duration);
            };

            audio.onerror = () => {
                URL.revokeObjectURL(audio.src);
                reject(new Error('Could not load audio'));
            };

            audio.src = URL.createObjectURL(file);
        });
    }
};

// Export for use in other modules
window.Validators = Validators;
