/**
 * Hestia Design System - Tailwind Configuration
 * Following Apple Human Interface Guidelines (https://developer.apple.com/design/)
 */
tailwind.config = {
    theme: {
        extend: {
            colors: {
                // Apple-inspired semantic colors
                ios: {
                    blue: '#007AFF',
                    green: '#34C759',
                    orange: '#FF9500',
                    red: '#FF3B30',
                    gray: {
                        50: '#F9FAFB',
                        100: '#F2F2F7',
                        200: '#E5E5EA',
                        300: '#D1D1D6',
                        400: '#AEAEB2',
                        500: '#8E8E93',
                        600: '#636366',
                        700: '#48484A',
                        800: '#3A3A3C',
                        900: '#1C1C1E',
                    }
                }
            },
            fontFamily: {
                sans: ['-apple-system', 'BlinkMacSystemFont', 'SF Pro Text', 'SF Pro Display', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
            },
            borderRadius: {
                'ios': '12px',
                'ios-lg': '16px',
                'ios-xl': '20px',
            },
            boxShadow: {
                'ios-sm': '0 1px 3px rgba(0, 0, 0, 0.08)',
                'ios': '0 2px 8px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06)',
                'ios-lg': '0 4px 16px rgba(0, 0, 0, 0.12), 0 1px 3px rgba(0, 0, 0, 0.08)',
                'ios-xl': '0 8px 32px rgba(0, 0, 0, 0.16), 0 2px 8px rgba(0, 0, 0, 0.08)',
            },
            minHeight: {
                'touch': '44px',
            },
            minWidth: {
                'touch': '44px',
            }
        }
    }
};
