/**
 * Created by gabriel on 17/09/14.
 */

$( document ).ready(function() {
    var editing = false;


    //$('#edit_tags_form_submit').tooltip( "show" );

    var $edit_profile_button = $("#edit_profile_button");
    $edit_profile_button.click(
        function() {

            if (editing == false) {
                // User wants to edit
                console.log("Hiding info elements");
                $(".info_element").hide();

                console.log("Showing form elements");
                $(".edit_profile_form_element").show();

                $edit_profile_button.attr('class', "glyphicon glyphicon-remove");

                editing = true;
            }
            else {
                // User canceled edition    TODO: Cómo hacer que se reinicien los valores del form?
                console.log("Hiding form elements");
                $(".edit_profile_form_element").hide();

                console.log("Showing info elements");
                $(".info_element").show();

                $edit_profile_button.attr('class', "glyphicon glyphicon-edit");

                editing = false;
            }

        }
    );


    $("#edit_tags_form_submit").click(
        function() {
            $('#edit_tags_form_submit').popover('toggle');

            var tags_form = $("#edit_tags_form");
            $.post( "edit_tags_ajax", tags_form.serialize()).done(
                function (data) {
                    console.log(data);
                    var edit_tags_form_submit = $('#edit_tags_form_submit');
                    edit_tags_form_submit.tooltip( {placement: "right",
                                          title: data,
                                          trigger: "manual"
                                         } );
                    edit_tags_form_submit.tooltip( "show" );

                    // Show response and destroy de tooltip (Because it's created on every click)
                    setTimeout(function () {
                        edit_tags_form_submit.tooltip( 'destroy' );
                        }, 2000);
                }
            );
        }
    );



});