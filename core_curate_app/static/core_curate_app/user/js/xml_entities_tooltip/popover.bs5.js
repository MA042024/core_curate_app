/**
 * Hide the popover attached to the given selector.
 * @param selector
 */
let hideTooltip = function(selector) {
    let selectorPopover = bootstrap.Popover.getInstance(selector);

    // If the popover exist, hide it.
    if (selectorPopover !== null) selectorPopover.hide();
}

/**
 * Show the tooltip for a given selector and options.
 * @param selector
 * @param options
 */
let showTooltip = function(selector, options) {
    options.template = `
        <div class="popover warning-popover" role="popover">
            <div class="popover-arrow warning-popover-arrow"></div>
            <div class="popover-header warning-popover-text"></div>
        </div>
    `;

    let selectorPopover = bootstrap.Popover.getInstance(selector);
    if (selectorPopover === null)  // Create the popover if it does not exist.
        selectorPopover = new bootstrap.Popover(selector, options);

    selectorPopover.show();
}
