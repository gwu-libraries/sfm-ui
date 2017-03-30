$(document).ready(function(){
    var active = $("#ActiveTable tr");
    var deleted = $("#DeletedTable tr");
    var btnMoreActive = $("#seeMoreActiveRecords");
    var btnLessActive = $("#seeLessActiveRecords");
    var btnMoreDeleted = $("#seeMoreDeletedRecords");
    var btnLessDeleted = $("#seeLessDeletedRecords");
    var activeLength = active.length;
    var deletedLength = deleted.length;
    var currentActiveIndex = 0;
    var currentDeletedIndex = 0;

    active.hide();
    deleted.hide();
    active.slice(0, 11).show();
    deleted.slice(0, 11).show();
    btnLessActive.hide();
    btnLessDeleted.hide();
    checkButton();
 
    btnMoreActive.click(function (e) { 
        e.preventDefault();
        $("#ActiveTable tr").show();
        $("#DeletedTable tr").show();
        btnMoreActive.hide();
        btnLessActive.show();
    });

    btnLessActive.click(function (e) { 
        e.preventDefault();
        active.hide();
        deleted.hide();
        $("#ActiveTable tr").slice(currentActiveIndex, 11).show();
        $("#DeletedTable tr").slice(currentDeletedIndex, 11).show();
        btnLessActive.hide();
        btnMoreActive.show();
    });

    btnMoreDeleted.click(function (e) { 
        e.preventDefault();
        $("#ActiveTable tr").show();
        $("#DeletedTable tr").show();
        btnMoreDeleted.hide();
        btnLessDeleted.show();
    });

    btnLessDeleted.click(function (e) { 
        e.preventDefault();
        active.hide();
        deleted.hide();
        $("#ActiveTable tr").slice(currentActiveIndex, 11).show();
        $("#DeletedTable tr").slice(currentDeletedIndex, 11).show();
        btnLessDeleted.hide();
        btnMoreDeleted.show();
    });
 
   function checkButton() {
        if (activeLength<=11) {
            btnMoreActive.hide();            
        } else {
            btnMoreActive.show();   
        }
        if (deletedLength<=11) {
            btnMoreDeleted.hide();            
        } else {
            btnMoreDeleted.show();   
        }
   }

   (function($){
            $('#filter').keyup(function () {
            var rex = new RegExp($(this).val(), 'i');
            $('.searchable tr').hide();
            $('.searchable tr').filter(function () {
                return rex.test($(this).text());
            }).show();
        })
    }(jQuery));

    (function($){
            $('#filterHarvest').keyup(function () {
            var rex = new RegExp($(this).val(), 'i');
            $('.HarvestSearch tr').hide();
            $('.HarvestSearch tr').filter(function () {
                return rex.test($(this).text());
            }).show();
        })
    }(jQuery));

});

    function filterText()
        {
                var rex = new RegExp($('#filterText').val());
                if(rex =="/all/"){clearFilter()}else{
                        $('.HarvestContent').hide();
                        $('.HarvestContent').filter(function() {
                        return rex.test($(this).text());
                        }).show();
                }
        }
        
    function clearFilter()
        {
                $('.filterText').val('');
                $('.HarvestContent').show();
        }


