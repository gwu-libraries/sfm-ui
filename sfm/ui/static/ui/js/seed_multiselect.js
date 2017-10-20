$(document).ready(function() {
        // seed multiselect
        $('#id_seeds').multiselect({
           includeSelectAllOption: false,
           enableFiltering: true,
           enableCaseInsensitiveFiltering: true,
           maxHeight: 350,
           buttonWidth: 200

        });
 });