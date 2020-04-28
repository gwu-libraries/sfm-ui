/* Set the defaults for DataTables initialisation */
$.extend( true, $.fn.dataTable.defaults, {
    "sPaginationType": "bs_normal",
    "oLanguage": {
        "sSearch": "Search"
    }
} );

/* Default class modification */
$.extend( $.fn.dataTableExt.oStdClasses, {
	"sWrapper": "dataTables_wrapper form-inline"
} );

/* API method to get paging information */
$.fn.dataTableExt.oApi.fnPagingInfo = function ( oSettings )
{
	return {
		"iStart":         oSettings._iDisplayStart,
		"iEnd":           oSettings.fnDisplayEnd(),
		"iLength":        oSettings._iDisplayLength,
		"iTotal":         oSettings.fnRecordsTotal(),
		"iFilteredTotal": oSettings.fnRecordsDisplay(),
		"iPage":          oSettings._iDisplayLength === -1 ?
			0 : Math.ceil( oSettings._iDisplayStart / oSettings._iDisplayLength ),
		"iTotalPages":    oSettings._iDisplayLength === -1 ?
			0 : Math.ceil( oSettings.fnRecordsDisplay() / oSettings._iDisplayLength )
	};
};

/* Bootstrap style pagination control */
$.extend( $.fn.dataTableExt.oPagination, {
	"bs_normal": {
		"fnInit": function( oSettings, nPaging, fnDraw ) {
			var oLang = oSettings.oLanguage.oPaginate;
			var fnClickHandler = function ( e ) {
				e.preventDefault();
				if ( oSettings.oApi._fnPageChange(oSettings, e.data.action) ) {
					fnDraw( oSettings );
				}
			};

			$(nPaging).append(
				'<nav class="hidden"><ul class="pagination justify-content-center align-items-center">'+
				    '<li class="page-item"><a class="page-link rounded-pill mr-1" href="#">&laquo;</a></li>' +
				    '<li class="page-item"><a class="page-link rounded-pill mr-1" href="#">'+oLang.sPrevious+'</a></li>'+
				    '<li class="page-item active">&nbsp;1 of 5&nbsp;</li>' +
					'<li class="page-item"><a class="page-link rounded-pill ml-1" href="#">'+oLang.sNext+'</a></li>'+
					'<li class="page-item"><a class="page-link rounded-pill ml-1" href="#"> &raquo;</a></li>' +
				'</ul></nav>'
			);
			var els = $('a', nPaging);
			$(els[0]).bind( 'click.DT', { action: "first" }, fnClickHandler );
			$(els[1]).bind( 'click.DT', { action: "previous" }, fnClickHandler );
			$(els[2]).bind( 'click.DT', { action: "next" }, fnClickHandler );
			$(els[3]).bind( 'click.DT', { action: "last" }, fnClickHandler );
		},
		"fnUpdate": function ( oSettings, fnDraw ) {
			var oPaging = oSettings.oInstance.fnPagingInfo();
			var an = oSettings.aanFeatures.p;

			for ( i=0, ien=an.length ; i<ien ; i++ ) {
				if ( oPaging.iPage === 0 ) {
				    $('li:eq(0)', an[i]).css('display', 'none');
					$('li:eq(1)', an[i]).css('display', 'none');
				} else {
					$('li:eq(0)', an[i]).css('display', 'inline-block');
					$('li:eq(1)', an[i]).css('display', 'inline-block');
				}

				if ( oPaging.iPage === oPaging.iTotalPages-1 || oPaging.iTotalPages === 0 ) {
					$('li:eq(3)', an[i]).css('display', 'none');
					$('li:eq(4)', an[i]).css('display', 'none');
				} else {
					$('li:eq(3)', an[i]).css('display', 'inline-block');
					$('li:eq(4)', an[i]).css('display', 'inline-block');
				}
				$('li.active', an[i]).text(' ' + (oPaging.iPage + 1) + ' of ' + oPaging.iTotalPages + ' ');

				if (oPaging.iTotalPages != 0) {
				    $('nav', an[i]).removeClass('hidden');
				}
			}
		}
	}
} );



