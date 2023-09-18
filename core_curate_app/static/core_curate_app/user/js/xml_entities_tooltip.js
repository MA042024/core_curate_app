/**
 * XML entities tooltip script
 */
$(document).ready(function() {
    refreshTooltipPosition();
});

/**
 * Find all the tooltip with the warning class in the DOM
 * @return jquerySelectorCollection or undefined if no result
 */
var findFormWarningTooltip = function() {
    var tooltipSelector = $(".popover-header.warning-popover-text");
    return tooltipSelector.length > 0 ? tooltipSelector : undefined;
}

/**
 * In the displayed form, check all the field and display warning tooltips if predefined XML entities are found
 */
var checkPredefinedXmlEntities = function(selector) {
    selector = selector.val ? selector : $(this);
    let value = selector.val().replace(
        /((&amp;)|(&gt;)|(&lt;)|(&apos;)|(&quot;))/g,
        ""
    );

    if (!value.match("[<>&\"\']+")) {  // No xml entities found.
        hideTooltip(selector);
        return;
    }

    let tooltipTitle = `Warning! This field may contain predefined XML 
        entities. These entities will be automatically escaped.`
    let tooltipOptions = {
        title: tooltipTitle,
        template: null,
        animation: true,
        trigger: "manual",
        placement: function (tip, element) {
            // Move the tooltip if there are + or - buttons.
            let jqueryTip = $(tip);
            jqueryTip.css('opacity', 0);
            setTimeout(function () {
                // Delay the computation to let the buttons be drawn first.
                let circleItemNumber = checkCircleItem(element);

                if (circleItemNumber > 0) {
                    let tipLeftPosition = parseFloat(
                        jqueryTip.css("left").replace("px", "")
                    );
                    tipLeftPosition += 25 * circleItemNumber;
                    $(tip).css({
                        left: tipLeftPosition + "px"
                    });
                }

                jqueryTip.css('opacity', 1);
            }, 100);

            return "right";
        }
    }
    showTooltip(selector, tooltipOptions);
}

/**
 * For the first render of the form check the predefined Xml entities in all the fields
 */
var refreshTooltipPosition = function() {
    const inputArray = $('input.default').toArray();
    for(const index in inputArray) {
        const $input = $(inputArray[index]);

        if (isElementInViewport($input)) checkPredefinedXmlEntities($input);
        else hideTooltip($input);
    }
}

/**
 * Take a DOM element and search within it to find if there are circle icon inside
 * @return Number of circle item found in the DOM element
 */
var checkCircleItem = function(element) {
    var parentItem = $(element).parent();
    var parentString = parentItem.html();
    var buttonNumber = (parentString.match(/((fa-question-circle)|(fa-plus-circle)|(fa-minus-circle))/g) || []).length;
    var hiddenButtonNumber = (parentString.match(/<span class="icon .*(hidden)/g) || []).length;

    // we count all the buttons, all the hidden buttons and return the sub to get all the visible buttons
    return buttonNumber - hiddenButtonNumber;
}

$(document).on('blur', 'input.default', checkPredefinedXmlEntities);
$(document).on('blur', 'textarea', function() { setTimeout(refreshTooltipPosition, 250) });
$(document).on('click', '.add', function() { setTimeout(refreshTooltipPosition, 250) });
$(document).on('click', '.remove', function(event) {
    setTimeout(() => {
        refreshTooltipPosition();

        // Delete all tooltips from child inputs.
        const inputArray = $(event.target).parent().find("input").toArray();
        for(const index in inputArray) {
            hideTooltip($(inputArray[index]));
        }
    }, 250);
});
$(document).scroll(debounce(function() { refreshTooltipPosition(); }, 50));
$(window).resize(debounce(function() { refreshTooltipPosition(); }, 50));
