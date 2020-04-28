 $(document).ready(function() {
        var ajax_url = SEED_LIST_JSON_URL;
        if ($.fn.dataTable.isDataTable('.seed-dt')) {
            dt = $('.seed-dt').DataTable();
        }
        else {
            dt =  $('.seed-dt').dataTable({
            "lengthChange": false,
            "pageLength": 25,
            "sPaginationType": oPaginationType,
            "autoWidth": false,
            "language": oLanguages,
            // currently, not supporting order by click column since the seed table columns are different
            //it's hard to make one rule for all table
            "ordering": false,
            //define the ajax url for the datatable
            "serverSide": true,
            "ajax": {
                    "url": ajax_url
                }
            });
        }
        // add search input for the seed datatable based on the datatable api and feature
        dt.each(function(){
            var datatable = $(this);
            // SEARCH - Turn this into in-line form control
            var search_input = datatable.closest('.dataTables_wrapper').find('div[id$=_filter] input');
            search_input.addClass('form-control');
            // LENGTH - Inline-Form control
            var length_sel = datatable.closest('.dataTables_wrapper').find('div[id$=_length] select');
            length_sel.addClass('form-control');
         });

         //reload api url for active tab
         $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            var status = $(e.target).attr('id');
            ajax_url = SEED_LIST_JSON_URL.replace ('active', status);
            // reload url request for 'active' or 'deleted' tab
            dt.ajax.url(ajax_url).load();
        });


 });