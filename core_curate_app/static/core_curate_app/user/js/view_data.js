//Load controllers for view data
$(document).ready(function() {
    $('.btn.download-xml').on('click', downloadXML);
    $('.btn.save-to-repo').on('click', saveToRepository);
});

//Download the current XML document
var downloadXML = function()
{
    window.location = downloadXMLUrl;
};

//Save Form to repository
var saveToRepository = function()
{
    $(function() {
        $( "#dialog-save-confirm-message" ).dialog({
          modal: true,
          buttons: {
                Cancel: function() {
                    $( this ).dialog( "close" );
                },
                Save: function() {
                    saveToRepositoryProcess();
                    $( this ).dialog( "close" );
                }
            }
        });
      });
};

// AJAX, to start form save
var saveToRepositoryProcess = function()
{
   var objectID = $("#curate_data_structure_id").html();
   $.ajax({
        url : saveDataUrl,
        type: 'POST',
        data: {
          'id': objectID
        },
        dataType: 'json',
        success : function(data) {
            XMLDataSavedSuccess();
        },
        error:function(data){
            console.log(data);
            XMLDataSavedError(data.responseJSON.errors);
        }
    });
};

//Saved XML data to DB success message.
var XMLDataSavedSuccess = function()
{
    $(function() {
        $( "#dialog-saved-success-message" ).dialog({
            modal: true,
            close: function(){
                window.location = "/curate"
            },
            buttons: {
                Ok: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
};

//Saved XML data to DB error message.
var XMLDataSavedError = function(errors)
{
    $("#saveErrorMessage").html(errors);
    $(function() {
        $( "#dialog-saved-error-message" ).dialog({
            modal: true,
            buttons: {
                Ok: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
};