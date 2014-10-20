/**
 * Created by gabriel on 20/10/14.
 */

$( document ).ready(function() {
    console.log("url:", follow_control_url);
    console.log("username:", follow_control_username);
    console.log("action:", follow_control_action);

    var follow_control_button = $("#follow_control_button");

    follow_control_button.click(
        function() {

            var csrftoken = $.cookie('csrftoken');
            function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            // Macke the actual POST
            $.post(
                follow_control_url,
                {username: follow_control_username, action: follow_control_action}
            );
        }
    );
});
