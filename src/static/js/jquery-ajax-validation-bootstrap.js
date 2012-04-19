function bootstrap_callback(data, form) {
    $(form).find(".alert-error").remove();
    var field_divs = $(form).find(".control-group").filter(".error");
    field_divs.removeClass("error");
    field_divs.find("[id^=error_1_]").remove();
    $.each(data.errors, function(key, val) {
        if (key == "__all__") {
            $(form).prepend('<div class="alert alert-block alert-error"><ul></ul></div>');
            $.each(val, function(key, error) {
                $(".alert-error ul").append("<li>" + error + "</li>");
            });
        } else {
            var field_div = $(form).find(".control-group").filter("#div_" + key);
            field_div.addClass("error");
            field_div.children(".controls").append('<span id="error_1_' + key + '" class="help-inline"><strong>' + val + "</strong></span>");
        }
    });
}