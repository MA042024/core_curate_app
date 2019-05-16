/**
 * Load controllers for enter data
 */
$(document).ready(function() {
    initModules();
    refreshTooltipPosition();
});

/**
 * Clear the fields of the current curated data
 */
var clearFields = function() {
    $("#clear-fields-modal").modal("show");
};

/**
 * AJAX call, clears fields
 */
var clear_fields = function() {
    var objectID = $("#curate_data_structure_id").html();
    $.ajax({
        url: clearFieldsUrl,
        type: "POST",
        data: {
            'id': objectID
        },
        dataType: "json",
        success: function(data) {
            $("#xsdForm").html(data.xsdForm);

            $('link.module').each(function(index, item) {
                item.remove();
            });

            $('script.module').each(function(index, item) {
                item.remove();
            });

            initModules();
        }
    });
    $("#clear-fields-modal").modal("hide");
};


/**
 * Cancel the changes of the current curated data
 */
var cancelChanges = function() {
    $("#cancel-changes-modal").modal("show");
};


/**
 * AJAX call, cancel changes
 */
var cancel_changes = function() {
    var objectID = $("#curate_data_structure_id").html();
    $.ajax({
        url: cancelChangesUrl,
        type: "POST",
        data: {
            'id': objectID
        },
        dataType: "json",
        success: function(data) {
            $("#xsdForm").html(data.xsdForm);

            $('link.module').each(function(index, item) {
                item.remove();
            });

            $('script.module').each(function(index, item) {
                item.remove();
            });

            initModules();
        }
    });
    $("#cancel-changes-modal").modal("hide");
};


/**
 * Cancel the form
 */
var cancelForm = function() {
    $("#cancel-form-modal").modal("show");
};


/**
 * AJAX call, cancel form
 */
var cancel_form = function() {
    $("#cancel-form-modal").modal("hide");
    var objectID = $("#curate_data_structure_id").html();
    $.ajax({
        url: cancelFormUrl,
        type: "POST",
        data: {
            'id': objectID
        },
        dataType: "json",
        success: function(data) {
            window.location = curateIndexUrl;
        },
        error: function() {

        }
    });
};


/**
 * Display the saving confirmation popup
 */
var saveForm = function() {
    $("#save-form-modal").modal("show");
};

/**
 * Save the form in the database
 */
var sendSaveRequest = function() {
    $("#save-form-modal").modal("hide");
    var objectID = $("#curate_data_structure_id").html();
    $.ajax({
        url: saveFormUrl,
        type: 'POST',
        data: {
            'id': objectID
        },
        dataType: 'json',
        success: function(data) {
            $.notify(data.message, { style: data.tags });
        },
        error: function() {

        }
    });
};


/**
 * Shows a dialog to choose dialog options
 */
var downloadOptions = function() {
    $("#download-modal").modal("show");
};


/**
 * Validate the current data to curate.
 */
var validateXML = function() {
    var objectID = $("#curate_data_structure_id").html();

    clearPreviousWarning();

    $.ajax({
        url: validateFormUrl,
        type: "POST",
        data: {
            'id': objectID
        },
        dataType: "json",
        success: function(data) {
            if ('errors' in data) {
                showXMLDataValidationError(data.errors);
            } else {
                var useErrors = checkElementUse();

                if (useErrors.length > 0) {
                    useErrorsAndView(useErrors);
                } else {
                    reviewDataDialog();
                }

                // if we have warnings, we have to display it in the validation modal
                if ('warning' in data)
                    displayWarningInValidModal(data.warning);
                //find warning tooltip to display warning in the validation modal
                if (findFormWarningTooltip())
                    displayWarningInValidModal(' this form may contain predefined XML entities. These entities will be automatically escaped if you want to continue.');
            }
        }
    });
};


/**
 * Shows XML validation warning message in the modal.
 * @param warningMessage
 */
var displayWarningInValidModal = function(warningMessage) {
    var modalContainerSelector = $(".warning-modal-container");

    // build the warning element
    var node = document.createElement("div");
    node.classList.add("alert");
    node.classList.add("alert-warning");
    node.classList.add("alert-warning-xml");
    node.innerHTML = "<strong>Warning!</strong> " + warningMessage;

    clearPreviousWarning();

    // if there are multiple modal with warning container we have to fill all there modal's container
    if (modalContainerSelector.length && modalContainerSelector.length > 0) {

        for (var index = 0; index < modalContainerSelector.length; ++index) {
            modalContainerSelector[index].prepend(node.cloneNode(true)); // need to call clone function otherwise prepend will perform a move operation
        }

    }


}

/**
 * Find all the tooltip with the warning class in the DOM
 * @return jquerySelectorCollection or undefined if no result
 */
var findFormWarningTooltip = function() {
    var tooltipSelector = $(".tooltip-inner.warning-tooltip-inner");
    return tooltipSelector.length > 0 ? tooltipSelector : undefined;
}

/**
 * Clear all the previous warning (By default there is only one warning container in the modal).
 */
var clearPreviousWarning = function() {
    var alertWarningNode = $(".warning-modal-container");
    if (alertWarningNode.length && alertWarningNode.length > 0) {
        // for all the validation modal in the page
        for (var index = 0; index < alertWarningNode.length; ++index) {
            // get the warning message element
            var warningMessage = $(alertWarningNode[index]).find(".alert-warning-xml");
            if (warningMessage.length && warningMessage.length > 0) {
                // for all the warning message in the current modal
                for (var warningIndex = 0; warningIndex < warningMessage.length; ++warningIndex) {
                    // delete the message element
                    warningMessage[warningIndex].remove();
                }
            }
        }
    }
}

/**
 * Shows XML validation error message.
 * @param errors
 */
var showXMLDataValidationError = function(errors) {
    $("#xmlErrorMessage").html(errors);
    $("#xml-error-modal").modal("show");
};

/**
 * Check required, recommended elements
 * @returns {string}
 */
var checkElementUse = function() {
    var required_count = 0;
    $(".required:visible").each(function() {
        if (!$(this).closest("li").hasClass("removed")) {
            if ($(this).val().trim() == "") {
                required_count += 1;
            }
        }
    });

    var recommended_count = 0;
    $(".recommended:visible").each(function() {
        if (!$(this).closest("li").hasClass("removed")) {
            if ($(this).val().trim() == "") {
                recommended_count += 1;
            }
        }
    });

    var errors = "";
    if (required_count > 0 || recommended_count > 0) {
        errors += "<ul>";
        errors += "<li>" + required_count.toString() + " required element(s) are empty.</li>";
        errors += "<li>" + recommended_count.toString() + " recommended element(s) are empty.</li>";
        errors += "</ul>";
    }

    return errors;
};

/**
 * Displays use error before viewing data
 * @param errors
 */
var useErrorsAndView = function(errors) {
    $("#useErrorMessage").html(errors);
    $("#use-warning-modal").modal("show");

};

/**
 * Dialog to redirect to review page
 */
var reviewDataDialog = function() {
    $("#xml-valid-modal").modal("show");
};

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
            title: "Warning! this field may contain predefined XML entities. These entities will be automatically escaped.",
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

/**
 * Show / Hide
 */
var toggleWarning = function() {
    var warningModalContainer = $('.warning-modal-container');
    if (warningModalContainer.css('display') == 'none') {
        warningModalContainer.css('display', 'block');
        warningModalContainer.css('opacity', 1);
    } else {
        warningModalContainer.css('display', 'none');
        warningModalContainer.css('opacity', 0);
    }
}

$(document).on('click', '.btn.clear-fields', clearFields);
$(document).on('click', '.btn.cancel-changes', cancelChanges);
$(document).on('click', '.btn.cancel-form', cancelForm);
$(document).on('click', '.btn.save-form', saveForm);
$(document).on('click', '.btn.download', downloadOptions);
$(document).on('click', '.btn.validate', validateXML);

$(document).on('click', '#btn-cancel-changes', cancel_changes);
$(document).on('click', '#btn-clear-fields', clear_fields);
$(document).on('click', '#btn-cancel-form', cancel_form);
$(document).on('click', '#btn-save-form', sendSaveRequest);

$(document).on('click', '#valid-modal-toggle-warning', toggleWarning);

$(document).on('blur', 'input.default', checkPredefinedXmlEntities);
$(document).on('blur', 'textarea', function() { setTimeout(refreshTooltipPosition, 500) });
$(document).on('click', '.add', function() { setTimeout(refreshTooltipPosition, 500) });
$(document).on('click', '.remove', function() { setTimeout(refreshTooltipPosition, 500) });

$(document).scroll(debounce(function() { refreshTooltipPosition(); }, 300));
$(window).resize(debounce(function() { refreshTooltipPosition(); }, 300));