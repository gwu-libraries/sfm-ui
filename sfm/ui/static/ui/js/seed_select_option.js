$(document).ready(function() {
        // seed multiselect available only with "Selected seeds"
        $("input#id_id_seed_choice_0_3").on("click", function () {
          $(".longseed").show();
        });
	$("input#id_id_seed_choice_0_2").on("click", function() {
          $(".longseed").hide();
	});
	$("input#id_id_seed_choice_0_1").on("click", function() {
          $(".longseed").hide();
        });
        // show seed multiselect and error message if export page reloaded 
	// because error in use of selection control 
	if ( $("input#id_id_seed_choice_0_3:checked").length ) {
	 $(".longseed").show();
        }
 });
