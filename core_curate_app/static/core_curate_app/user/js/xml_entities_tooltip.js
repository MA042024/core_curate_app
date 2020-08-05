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
    var tooltipSelector = $(".tooltip-inner.warning-tooltip-inner");
    return tooltipSelector.length > 0 ? tooltipSelector : undefined;
}


/**
 * In the displayed form, check all the field and display warning tooltips if predefined XML entities are found
 */
var checkPredefinedXmlEntities = function(selector) {
    var template = '<div class="tooltip" role="tooltip"><div class="tooltip-arrow warning-tooltip-arrow"></div><div class="tooltip-inner warning-tooltip-inner"></div></div>'
    selector = selector.val ? selector : $(this)
    var value = selector.val();
    value = value.replace(/((&amp;)|(&gt;)|(&lt;)|(&apos;)|(&quot;))/g, '');
    if (value.indexOf('<') > -1 || value.indexOf('>') > -1 || value.indexOf('&') > -1 || value.indexOf('"') > -1 || value.indexOf("'") > -1) {
        selector.tooltip({
            title: "Warning! This field may contain predefined XML entities. These entities will be automatically escaped.",
            template: template,
            animation: true,
            trigger: "manual",
            placement: function(tip, element) {
                var jqueryTip = $(tip);
                jqueryTip.css('opacity', 0);
                setTimeout(function() {
                    var circleItemNumber = checkCircleItem(element);

                    if (circleItemNumber > 0) {
                        var tipLeftPosition = parseFloat(jqueryTip.css("left").replace("px", ""));
                        tipLeftPosition += 25 * circleItemNumber;
                        $(tip).css({
                            left: tipLeftPosition + "px"
                        });
                    };

                    jqueryTip.css('opacity', 1);
                }, 100);

                return "right";
            }
        });

        selector.tooltip('show');
    } else {
        selector.tooltip("hide");
    }
}

/**
 * For the first render of the form check the predefined Xml entities in all the fields
 */
var refreshTooltipPosition = function() {
    var inputs = $('input.default');
    for (var i = 0; i < inputs.length; ++i) {
        if (isElementInViewport(inputs[i])) checkPredefinedXmlEntities($(inputs[i]));
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
$(document).on('blur', 'textarea', function() { setTimeout(refreshTooltipPosition, 500) });
$(document).on('click', '.add', function() { setTimeout(refreshTooltipPosition, 500) });
$(document).on('click', '.remove', function() { setTimeout(refreshTooltipPosition, 500) });

$(document).scroll(debounce(function() { refreshTooltipPosition(); }, 300));
$(window).resize(debounce(function() { refreshTooltipPosition(); }, 300));
