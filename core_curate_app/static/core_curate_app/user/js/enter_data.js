var editor = null;
var schema = null;
var form =  null
var contentFormat =  null;

/**
 * Load controllers for enter data
 */
$(document).ready(function() {
    contentFormat = $("#template_format").html();
    if(contentFormat == "XSD") initModules();
    else if(contentFormat == "JSON") initJSONFormEditor($("#form_string").html());
    else $.notify("Template format not supported.", "danger");

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
    var icon = $("[id^='btn-clear-fields'] > i").attr("class");

    // Show loading spinner
    showSpinner($("[id^='btn-clear-fields'] > i"))
    if (contentFormat == "XSD"){
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
                $.notify("Fields cleared with success.", "success");
            },
            error: function() {
                $.notify("An error occurred while clearing fields.", "danger");
            }
        }).always(function(data) {
            // get old button icon
            hideSpinner($("[id^='btn-clear-fields'] > i"), icon)
            $("#clear-fields-modal").modal("hide");
        });
    }
    else if (contentFormat == "JSON") {
        initJSONFormEditor();
        hideSpinner($("[id^='btn-clear-fields'] > i"), icon)
        $("#clear-fields-modal").modal("hide");
        $.notify("Fields cleared with success.", "success");
    }
    else $.notify("Template format not supported.", "danger");

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
    var icon = $("[id^='btn-cancel-changes'] > i").attr("class");
    // Show loading spinner
    showSpinner($("[id^='btn-cancel-changes'] > i"))
    $.ajax({
        url: cancelChangesUrl,
        type: "POST",
        data: {
            'id': objectID
        },
        dataType: "json",
        success: function(data) {
            if (contentFormat == "XSD") {
                $("#xsdForm").html(data.xsdForm);

                $('link.module').each(function(index, item) {
                    item.remove();
                });

                $('script.module').each(function(index, item) {
                    item.remove();
                });
                initModules();
            }
            else {
                if(data.content == "")
                    editor.setValue({});
                else
                    editor.setValue(JSON.parse(data.content));
            }
            $.notify("Changes canceled  with success.", "success");
        },
        error: function() {
            $.notify("An error occurred while canceling changes.", "danger");
        }
    }).always(function() {
        // get old button icon
        hideSpinner($("[id^='btn-cancel-changes'] > i"), icon)
        $("#cancel-changes-modal").modal("hide");
    });

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
    // Show loading spinner
    showSpinner($("[id^='btn-cancel-form'] > i"))
    $("#cancel-form-modal").modal("hide");

    var objectID = $("#curate_data_structure_id").html();
    $.ajax({
        url: cancelFormUrl,
        type: "POST",
        data: {
            'id': objectID
        },
        dataType: "json",
        success: function() {
            window.location = curateIndexUrl;
        },
        error: function(dataXHR){
            $.notify(dataXHR.responseJSON.error, "danger");
        }
    });
};


/**
 * Display the saving confirmation popup
 */
var saveFormDialog = function() {
    $("#save-form-modal").modal("show");
};

/**
 * Save the form in the database
 */
var sendSaveRequest = function() {
    saveForm($("[id^='btn-save-form'] > i"), $("#save-form-modal"))
};

/**
 * AJAX call, validate the current data to curate.
 */
var validate = function() {
    let objectID = $("#curate_data_structure_id").html();
    let $validateButton = $(".validate > i");
    let validateButtonIcon = $validateButton.attr("class");

    showSpinner($validateButton);
    clearPreviousWarning();

    let validateData = {
        "id": objectID
    }
    if (contentFormat === "JSON")
        validateData.form_string = JSON.stringify(editor.getValue())

    $.ajax({
        url: validateFormUrl,
        type: "POST",
        data: validateData,
        dataType: "json",
        success: function (data) {
            if ("errors" in data) {
                showDataValidationError(data.errors);
            } else {
                let useErrors = checkElementUse();
                if (contentFormat === "XSD" && useErrors.length > 0)
                    useErrorsAndView(useErrors);
                else reviewDataDialog();

                // If we have warnings, we have to display it in the validation modal
                if ("warning" in data)
                    displayWarningInValidModal(data.warning);

                // Find warning tooltip to display warning in the validation modal
                if (typeof findFormWarningTooltip === "function" && findFormWarningTooltip())
                    displayWarningInValidModal(
                        "This form may contain predefined XML entities. These entities will be automatically escaped if you want to continue."
                    );
            }
        }
    }).always(function(data) {
        hideSpinner($validateButton, validateButtonIcon);
    });
};

/**
 * Format a list of error message to output HTML ul/li list.
 *
 * @param errorList
 * @returns {string}
 */
function buildMessageFromList(errorList) {
    let node = document.createElement("ul");
    node.innerHTML = errorList.map((item) => {return `<li>${item}</li>`}).join("");

    // Display the list of item nicely.
    node.style.padding = "revert";
    node.style.margin = "0";
    node.style.listStyle = "initial";

    return node.outerHTML;
}

/**
 * Build an error message depending on the data passed.
 *
 * @param errorObject
 * @returns {string}
 */
function buildErrorMessage(errorObject) {
    if (typeof errorObject === "string") {
        return errorObject;
    } else if (Array.isArray(errorObject)) {
        return buildMessageFromList(errorObject);
    } else {
        return "Cannot display error: format not supported!";
    }
}

/**
 * Shows validation error message.
 * @param errors
 */
var showDataValidationError = function(errors) {
    let $errorMessage = $("#errorMessage");
    $errorMessage.empty();  // Clear validation errors.

    // Build the error element.
    let node = document.createElement("div");
    node.classList.add("alert");
    node.classList.add("alert-danger");
    node.innerHTML = `<strong>Error!</strong> ${buildErrorMessage(errors)}`;

    // Attach the element to the modal and display the modal.
    $errorMessage.prepend(node.cloneNode(true));
    $("#validation-error-modal").modal("show");
}

/**
 * Shows XML validation warning message in the modal.
 * @param warningMessage
 */
var displayWarningInValidModal = function(warningMessage) {
    let modalContainerSelector = $(".warning-modal-container");

    // build the warning element
    let node = document.createElement("div");
    node.classList.add("alert");
    node.classList.add("alert-warning");
    node.classList.add("alert-warning-xml");
    node.innerHTML = "<strong>Warning!</strong> " + warningMessage;

    clearPreviousWarning();

    // if there are multiple modal with warning container we have to fill all there
    // modal's container.
    if (modalContainerSelector.length && modalContainerSelector.length > 0) {
        for (let index = 0; index < modalContainerSelector.length; ++index) {
            // need to call clone function otherwise prepend will perform a move
            // operation.
            modalContainerSelector[index].prepend(node.cloneNode(true));
        }

    }
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
    $("#validation-modal").modal("show");
};

/**
 * AJAX call, Proceed To Review
 */
var proceedToReview = function() {
    var redirectUrl = proceedToReviewUrl.replace("curate_data_structure_id", $("#curate_data_structure_id").html());
    saveForm($(".proceed-review > i"),$("#validation-modal"), redirectUrl);
};

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

/**
 * Get template schema for the JSON forms
 */
getTemplateSchema = function(){
    var templateID = $("#template_id").html();
    $.ajax({
        url : getTemplateUrl.replace("template_id", templateID),
        type : "GET",
        async: false,
        success: function(data){
            schema = data.content
        },
        error:function(data){
            $.notify(data.responseText, "danger");
        },
    });
}

/**
 * initialize JSON form editor
 */
initJSONFormEditor = function(content = null){
    displaySpinner($(".spinner"));
    if (editor) editor.destroy();
    else {
        // Get JSON container
        form = document.getElementById("jsonForm");
        // Get JSON schema
        getTemplateSchema();
    }
    // Create the editor
    JSONEditor.defaults.editors.object.options.disable_properties = true;
    editor = new JSONEditor(form,{
        schema: JSON.parse(schema),
        iconlib: "fontawesome5",
        theme:  'bootstrap5'
    });

    editor.on('ready',() => {
        removeSpinner($(".spinner"));
        if (content) editor.setValue(JSON.parse(content));

    });


}

/**
 * AJAX call, Save form
 */
saveForm = function(btnSelector,modalValidation,redirectUrl=null){

    var icon = btnSelector.attr("class");
    // Show loading spinner
    showSpinner(btnSelector);
    var param = { 'id': $("#curate_data_structure_id").html()}
    if (contentFormat == "JSON") param.form_string = JSON.stringify(editor.getValue())

    $.ajax({
        url: saveFormUrl,
        type: 'POST',
        data: param,
        dataType: 'json',
        success: function(data) {
            if(redirectUrl)
                window.location = redirectUrl;
            else $.notify(data.message, "success");
        },
        error: function(dataXHR) {
            $.notify(dataXHR.responseJSON.error, "danger");
        }
    }).always(function(data) {
        // get old button icon
        hideSpinner(btnSelector, icon)
        modalValidation.modal("hide");
    });
}

/**
 * Display the switching to text editor confirmation popup.
 */
var switchToTextEditorModal = function() {
    $("#switch-to-text-editor").modal("show");
}


/**
 * Switch the current to text editor.
 */
var switchEditor = function() {
    if(contentFormat == "XSD"){
        var redirectUrl =  openXMLFormUrl + "?id="+ $("#curate_data_structure_id").html();
        saveForm($(".save-and-switch-to-text-editor  > i"), $(".save-and-switch-to-text-editor"), redirectUrl)
    }

    else
        if (contentFormat == "JSON"){
            var redirectUrl =  window.location =  openJSONFormUrl + "?id="+$("#curate_data_structure_id").html();
            saveForm($(".save-and-switch-to-text-editor  > i"), $(".save-and-switch-to-text-editor"), redirectUrl)
        }

        else
            $.notify("Template format not supported.", "danger");
}

/**
 * AJAX call, download document
 * @param document
 */
download = function(document){
    let toFormat = $('#format').is(':checked');

    // Download form/template
    if (document == "form")
        window.location = downloadDocumentUrl+"?pretty_print="+toFormat;
    else
        window.location = downloadTemplateUrl+"?pretty_print="+toFormat;
};


$(document).on('click', '.btn.clear-fields', clearFields);
$(document).on('click', '.btn.cancel-changes', cancelChanges);
$(document).on('click', '.btn.cancel-form', cancelForm);
$(document).on('click', '.btn.save-form', saveFormDialog);
$(document).on('click', '.btn.validate', validate);
$(document).on('click', '.btn.proceed-review', proceedToReview);
$(document).on('click', '.btn.switch-to-text-editor', switchToTextEditorModal);
$(document).on('click', '.download-document-btn', e=>download("form"));
$(document).on('click', '.download-template-btn', e=>download("template"));

$(document).on('click', '.save-and-switch-to-text-editor',switchEditor);
$(document).on('click', '#btn-cancel-changes', cancel_changes);
$(document).on('click', '#btn-clear-fields', clear_fields);
$(document).on('click', '#btn-cancel-form', cancel_form);
$(document).on('click', '#btn-save-form', sendSaveRequest);
$(document).on('click', '#valid-modal-toggle-warning', toggleWarning);
