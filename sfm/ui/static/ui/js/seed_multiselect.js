$(document).ready(function() {
        // seed multiselect
        $('#id_seeds').selectpicker({
           size: 10,	
           liveSearch: true,
           width: "200px",
           selectedTextFormat: "count",
           dropupAuto: false
        });
 });