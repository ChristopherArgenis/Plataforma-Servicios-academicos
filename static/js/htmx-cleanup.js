/**
 * HTMX Initialization Handler
 * 
 * SIMPLIFIED APPROACH:
 * - Let HTMX handle swap (innerHTML replaces content)
 * - Only handle initialization after swap
 * - NO manual cleanup (causes issues)
 */

(function() {
    'use strict';

    console.log('[HTMX Init] Module loaded');

    // ==========================================
    // INITIALIZATION: After swap completes
    // ==========================================
    document.body.addEventListener('htmx:afterSwap', function(evt) {
        const target = evt.detail.target;
        
        if (target && target.id === 'main-content') {
            console.log('[HTMX Init] Content swapped into #main-content');
            
            // Trigger custom event for modules to initialize
            const initEvent = new CustomEvent('content:ready', {
                detail: { container: target }
            });
            document.dispatchEvent(initEvent);
        }
    });

})();
