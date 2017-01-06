//Load controllers for enter data
$(document).ready(function() {
    initModules();

    $('.btn.clear-fields').on('click', clearFields);
    $('.btn.cancel-changes').on('click', cancelChanges);
    $('.btn.cancel-form').on('click', cancelForm);
    $('.btn.save-form').on('click', saveForm);
    $('.btn.download').on('click', downloadOptions);
    $('.btn.download_xsd').on('click', downloadXSD);
    $('.btn.download_xml').on('click', downloadCurrentXML);
    $('.btn.validate').on('click', validateXML);
});

//Clear the fields of the current curated data
var clearFields = function()
{
    var objectID = $("#curate_data_structure_id").html();
    $(function() {
        $( "#dialog-cleared-message" ).dialog({
            modal: true,
            buttons: {
                Cancel: function() {
                    $( this ).dialog( "close" );
                },
                Clear: function() {
                    clear_fields(objectID);
                    $( this ).dialog( "close" );
                }
        }
        });
    });
};


//AJAX call, clears fields
var clear_fields = function(objectID){
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
};


//Cancel the changes of the current curated data
var cancelChanges = function()
{
    var objectID = $("#curate_data_structure_id").html();
    $(function() {
        $( "#dialog-cancel-message" ).dialog({
            modal: true,
            buttons: {
                Cancel: function() {
                    $( this ).dialog( "close" );
                },
                Confirm: function() {
                    cancel_changes(objectID);
                    $( this ).dialog( "close" );
                }
        }
        });
    });
};


//AJAX call, cancel changes
var cancel_changes = function(objectID){
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
};


//Cancel the form
var cancelForm = function()
{
    var objectID = $("#curate_data_structure_id").html();
    $(function() {
        $( "#dialog-cancel-form-message" ).dialog({
            modal: true,
            buttons: {
                Cancel: function() {
                    $( this ).dialog( "close" );
                },
                Confirm: function() {
                    cancel_form(objectID);
                    $( this ).dialog( "close" );
                }
        }
        });
    });
};


//AJAX call, cancel form
var cancel_form = function(objectID){
    $.ajax({
        url : cancelFormUrl,
        type : "POST",
        data:{
            'id': objectID
        },
        dataType: "json",
        success: function(data){
            //FIXME: update hardcoded url when available
            window.location = "/curate"
        }
    });
};


// Display the saving confirmation popup
var saveForm = function()
{
    var objectID = $("#curate_data_structure_id").html();
    $(function() {
        $( "#dialog-save-form-message" ).dialog({
            modal: true,
            buttons: {
                Save: function() {
                    sendSaveRequest(objectID);
                    $( this ).dialog( "close" );
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
};

// Save the form in the database
var sendSaveRequest = function(objectID) {
    $.ajax({
        url: saveFormUrl,
        type: 'POST',
        data:{
            'id': objectID
        },
        dataType: 'json',
        success: function() {
            $( "#dialog-saved-message" ).dialog({
                modal: true,
                buttons: {
                    Ok: function() {
                        //FIXME: update hardcoded url when available
                        window.location = '/curate';
                        $( this ).dialog( "close" );
                    }
                }
            });
        },
        error: function() {

        }
    });
};


//Shows a dialog to choose dialog options
var downloadOptions = function()
{
 $(function() {
    $( "#dialog-download-options" ).dialog({
      modal: true,
      buttons: {
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });
  });
};



//Download the XSD template
var downloadXSD = function()
{
    window.location = downloadXSDUrl;
};


//Download the current XML document
var downloadCurrentXML = function()
{
    window.location = downloadXMLUrl;
};


//Validate the current data to curate.
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
                    useErrosAndView(useErrors);
                } else {
                    reviewDataDialog();
                }
            }
        }
    });
};


//Shows XML validation error message.
var showXMLDataValidationError = function(errors)
{
    // set error message
    $("#xmlErrorMessage").html(errors);

    // show error dialog
    $(function() {
        $("#dialog-xml-error-message").dialog({
            modal: true,
            buttons: {
                Ok: function(){
                    $(this).dialog("close");
                }
            }
        });
    });
};

//Check required, recommended elements
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

//Displays use error before viewing data
var useErrosAndView = function(errors){
    $("#useErrorMessage").html(errors);
    $(function() {
        $( "#dialog-use-message" ).dialog({
            modal: true,
            height: 250,
            width: 485,
            buttons: {
            	Cancel: function() {
            		$( this ).dialog( "close" );
                },
                "Proceed to Review": function() {
                    redirectReviewPage();
                }
            },
            close: function(){
                $("#useErrorMessage").html("");
            }
        });
    });
};

//Dialog to redirect to review page
var reviewDataDialog = function()
{
    // show error dialog
    $(function() {
        $("#dialog-xml-valid-message").dialog({
            modal: true,
            buttons: {
                Cancel: function(){
                    $(this).dialog("close");
                },
                "Proceed to Review": function () {
                    redirectReviewPage();
                }
            }
        });
    });
};

// Redirects to review page
var redirectReviewPage = function () {
    window.location = viewDataUrl;
};
