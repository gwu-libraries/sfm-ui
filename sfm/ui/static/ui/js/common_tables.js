 $(document).ready(function() {
        if ($.fn.dataTable.isDataTable('.datatable')) {
            dt = $('.datatable');
        }
        else {
            var dt = $('.datatable');
            dt.dataTable({
                "sPaginationType": oPaginationType,
                "language": oLanguages
            });
        }
        dt.each(function(){
            var datatable = $(this);
            // SEARCH - Add the placeholder for Search and Turn this into in-line form control
            var search_input = datatable.closest('.dataTables_wrapper').find('div[id$=_filter] input');
            search_input.attr('placeholder', 'Search');
            search_input.addClass('form-control input-sm');
            // LENGTH - Inline-Form control
            var length_sel = datatable.closest('.dataTables_wrapper').find('div[id$=_length] select');
            length_sel.addClass('form-control input-sm');
        });
        // seed multiselect
        $('#id_seeds').multiselect({
           includeSelectAllOption: true,
           enableFiltering:true,
           maxHeight: 350,
           buttonWidth: 200

        });
 });