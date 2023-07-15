/**
 * Hide the popover attached to the given selector.
 * @param selector
 */
let hideTooltip = function(selector) {
    selector.popover("hide");
}

/**
 * Show the tooltip for a given selector and options.
 * @param selector
 * @param options
 */
let showTooltip = function(selector, options) {
    options.template = `
        <div class="popover warning-popover" role="tooltip">
            <div class="arrow warning-popover-arrow"></div>
            <div class="popover-header warning-popover-text"></div>
        </div>
    `;

    selector.popover(options);
    selector.popover("show");
}
