 $(document).ready(function() {
        if ($.fn.dataTable.isDataTable('.seed-dt')) {
            dt = $('.seed-dt').DataTable();
        }
        else {
            dt =  $('.seed-dt').dataTable({
            "sPaginationType": oPaginationType,
            "language": oLanguages,
            "order": [[ 1, "desc" ],[ 2, "desc" ]],
                "serverSide": true,
                "ajax": {
                    "url": SEED_LIST_JSON_URL
                }
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
 });