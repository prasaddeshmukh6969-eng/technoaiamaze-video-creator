/**
 * Analytics Tracking Library
 * Simple, zero-dependency tracking for user behavior
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Generate a simple visitor ID (stored in sessionStorage)
const getVisitorId = (): string => {
    if (typeof window === 'undefined') return '';

    let visitorId = sessionStorage.getItem('visitor_id');
    if (!visitorId) {
        visitorId = `visitor_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        sessionStorage.setItem('visitor_id', visitorId);
    }
    return visitorId;
};

/**
 * Track a page view
 */
export const trackPageView = async (page: string) => {
    if (typeof window === 'undefined') return;

    try {
        await fetch(`${API_URL}/api/v1/analytics/page-view`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                page,
                visitor_id: getVisitorId()
            })
        });
    } catch (error) {
        // Silently fail - don't break user experience
        console.debug('Analytics error:', error);
    }
};

/**
 * Track template card click
 */
export const trackTemplateClick = async (templateId: string) => {
    if (typeof window === 'undefined') return;

    try {
        await fetch(`${API_URL}/api/v1/analytics/template-click`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                template_id: templateId,
                visitor_id: getVisitorId()
            })
        });
    } catch (error) {
        console.debug('Analytics error:', error);
    }
};

/**
 * Submit email signup
 */
export const signupEmail = async (email: string, source: string = 'landing_page'): Promise<{ success: boolean; message: string }> => {
    try {
        const response = await fetch(`${API_URL}/api/v1/analytics/email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, source })
        });

        const data = await response.json();

        if (response.ok) {
            return { success: true, message: data.message || 'Thank you for signing up!' };
        } else {
            return { success: false, message: data.detail || 'Failed to sign up' };
        }
    } catch (error) {
        console.error('Email signup error:', error);
        return { success: false, message: 'Network error. Please try again.' };
    }
};

/**
 * Vote for a feature
 */
export const voteFeature = async (featureId: string): Promise<{ success: boolean; message: string }> => {
    if (typeof window === 'undefined') return { success: false, message: '' };

    try {
        const response = await fetch(`${API_URL}/api/v1/analytics/vote`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                feature_id: featureId,
                visitor_id: getVisitorId()
            })
        });

        const data = await response.json();

        if (response.ok) {
            return { success: true, message: data.message || 'Vote recorded!' };
        } else {
            return { success: false, message: data.detail || 'Failed to vote' };
        }
    } catch (error) {
        console.error('Vote error:', error);
        return { success: false, message: 'Network error. Please try again.' };
    }
};

/**
 * Initialize analytics on page load
 */
export const initAnalytics = () => {
    if (typeof window === 'undefined') return;

    // Track initial page view
    const currentPath = window.location.pathname;
    trackPageView(currentPath);
};
