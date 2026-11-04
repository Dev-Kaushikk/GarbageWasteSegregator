/**
 * Garbage Waste Segregator Frontend - Configuration
 *
 * Configure API endpoints and project-wide constants here.
 */
const PROJECT_ROOT = '/garbage-waste-segregator';

// API Base URL for backend
export const API_BASE_URL = `http://localhost:5000`;

// Allowed image extensions for uploads
export const ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.webp'];

// Default upload limits
export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

// Timeout for API requests
export const API_TIMEOUT = 30000;

// Export project paths
export { PROJECT_ROOT };
