<script>


    function set_date_warning() {



        var warning_div2 = $("#date_warning");
        warning_div2.htmldate_warning("Use start and end times in order to avoid using up monthly limit imposed by the API.See Twitter's <a href='https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api#v2-access-level' target='_blank'>API access levels and versions here</a>.");
        warning_div2.removeClass();
        warning_div2.css('position', 'absolute');
        warning_div2.css('top', 175); 
        warning_div2.css('left', 10); 

        

        warning_div2.addClass("alert alert-warning");


        
    }
    $(function() {

    
        set_date_warning();
    });
</script>
