function get_alert(text, type_alert) {
    var alert_name = '#bottom-alert-' + type_alert
    $('#alert-text-' + type_alert).text(text);
    if (!$(alert_name).hasClass("show")) {
        $(alert_name).toggleClass('show')
    }
    $(alert_name).delay(3500).queue(function () {
        if ($(this).hasClass("show")) {
            $(this).toggleClass('show')
        }
        $(this).dequeue();
    });
}
