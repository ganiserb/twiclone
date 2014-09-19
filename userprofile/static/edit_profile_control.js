/**
 * Created by gabriel on 17/09/14.
 */

$( document ).ready(function() {
    var editing = false;

    $("#edit_profile_button").click(
        function() {

            if (editing == false) {
                // User wants to edit
                console.log("Hiding info elements");
                $(".info_element").hide();

                console.log("Showing form elements");
                $(".edit_profile_form_element").show();

                $("#edit_profile_button span").attr('class', "glyphicon glyphicon-remove"); // TODO: El editor me dice que ese $() es ineficiente

                editing = true;
            }
            else {
                // User canceled edition    TODO: Cómo hacer que se reinicien los valores del form?
                console.log("Hiding form elements");
                $(".edit_profile_form_element").hide();

                console.log("Showing info elements");
                $(".info_element").show();

                $("#edit_profile_button span").attr('class', "glyphicon glyphicon-edit");

                editing = false;
            }

        }
    );


    $("#edit_tags_form_submit").click(
        function() {
            var tags_form = $("#edit_tags_form");
            $.post( "edit_tags_ajax", tags_form.serialize()).done(
                function (data) {
                    console.log(data);
                }
            );
        }
    );



});