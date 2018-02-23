/**
 * Load controllers for enter data
 */
$(document).ready(function() {
    initModules();
});

/**
 * Clear the fields of the current curated data
 */
var clearFields = function()
{
    $("#clear-fields-modal").modal("show");
};

/**
 * AJAX call, clears fields
 */
var clear_fields = function(){
    var objectID = $("#curate_data_structure_id").html();
    $.ajax({
        url : clearFieldsUrl,
        type : "POST",
        data:{
            'id': objectID
        },
        dataType: "json",
        success: function(data){
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
var cancelChanges = function()
{
    $("#cancel-changes-modal").modal("show");
};


/**
 * AJAX call, cancel changes
 */
var cancel_changes = function(){
    var objectID = $("#curate_data_structure_id").html();
    $.ajax({
        url : cancelChangesUrl,
        type : "POST",
        data:{
            'id': objectID
        },
        dataType: "json",
        success: function(data){
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
var cancelForm = function()
{
    $("#cancel-form-modal").modal("show");
};


/**
 * AJAX call, cancel form
 */
var cancel_form = function(){
    $("#cancel-form-modal").modal("hide");
    var objectID = $("#curate_data_structure_id").html();
    $.ajax({
        url : cancelFormUrl,
        type : "POST",
        data:{
            'id': objectID
        },
        dataType: "json",
        success: function(data){
            window.location = curateIndexUrl;
        },
        error: function () {

        }
    });
};


/**
 * Display the saving confirmation popup
 */
var saveForm = function()
{
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
        data:{
            'id': objectID
        },
        dataType: 'json',
        success: function(data) {
            $.notify(data.message, {style: data.tags });
        },
        error: function() {

        }
    });
};


/**
 * Shows a dialog to choose dialog options
 */
var downloadOptions = function()
{
    $("#download-modal").modal("show");
};


/**
 * Validate the current data to curate.
 */
var validateXML = function()
{
    var objectID = $("#curate_data_structure_id").html();

    $.ajax({
        url : validateFormUrl,
        type : "POST",
        data: {
          'id': objectID
        },
        dataType: "json",
        success: function(data){
            if ('errors' in data){
                showXMLDataValidationError(data.errors);
            } else {
                var useErrors = checkElementUse();

                if (useErrors.length > 0) {
                    useErrorsAndView(useErrors);
                } else {
                    reviewDataDialog();
                }
            }
        }
    });
};

/**
 * Shows XML validation error message.
 * @param errors
 */
var showXMLDataValidationError = function(errors)
{
    $("#xmlErrorMessage").html(errors);
    $("#xml-error-modal").modal("show");
};

/**
 * Check required, recommended elements
 * @returns {string}
 */
var checkElementUse = function(){
    var required_count = 0;
    $(".required:visible").each(function(){
        if (!$(this).closest("li").hasClass("removed")){
          if($(this).val().trim() == ""){
            required_count += 1;
          }
        }
    });

    var recommended_count = 0;
    $(".recommended:visible").each(function(){
        if (!$(this).closest("li").hasClass("removed")){
          if($(this).val().trim() == ""){
              recommended_count += 1;
          }
        }
    });

    var errors = "";
    if (required_count > 0 || recommended_count > 0){
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
var useErrorsAndView = function(errors){
    $("#useErrorMessage").html(errors);
    $("#use-warning-modal").modal("show");

};

/**
 * Dialog to redirect to review page
 */
var reviewDataDialog = function()
{
    $("#xml-valid-modal").modal("show");
};


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
