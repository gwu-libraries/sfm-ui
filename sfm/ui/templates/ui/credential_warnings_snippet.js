<script>
    var credential_warnings = {
    {% for credential_id, warning in credential_use_map.items %}
        "{{ credential_id}}": ["{{ warning.0 }}","{{ warning.1 }}"],
    {% endfor %}
    "": ["",""]
    };
    function set_credential_warning() {
        var warning_div = $("#credential_warning");
        var warning = credential_warnings[$("#id_credential").val()];
        warning_div.text(warning[1]);
        warning_div.removeClass();
        if (warning[0] != "") {
            warning_div.addClass("alert alert-" + warning[0]);
        }
    }
    $(function() {
        $("#id_credential").change(set_credential_warning);
        set_credential_warning();
    });
</script>
