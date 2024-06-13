document.addEventListener("DOMContentLoaded", function() {
    // Check if the redirection was intentional
    var redirectedFromOrigin = sessionStorage.getItem('redirectedFromOrigin');
    
    if (redirectedFromOrigin === 'true') {
        // Get the XML string and name from session storage
        var xmlString = sessionStorage.getItem('xmlData');
        var name = sessionStorage.getItem('name');

        // Automatically press the "Select Test" button next to templateID=1
        document.querySelector('td[templateID="1"] + td .set-template').click();

        // Wait for the modal to appear
        setTimeout(() => {
            // Select the radio button for "Upload Record"
            document.getElementById('curate_form_upload').checked = true;

            // Get the input field for uploading files
            let fileInput = document.getElementById('id_file');

            // Create a new Blob object from the XML string
            let blob = new Blob([xmlString], { type: 'text/xml' });

            // Create a new File object from the Blob
            let file = new File([blob], `${name}.xml`, { type: 'text/xml' });

            // Set the file to the file input
            fileInput.files = [file];

            // Press the "btn-save-data" button
            document.getElementById('btn-save-data').click();
        }, 1000); // Adjust the timeout as necessary to ensure the modal is fully loaded
    }
});