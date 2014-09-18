/**
 * Created by gabriel on 17/09/14.
 */

$( document ).ready(function() {
//    $("#edit_profile_form").hide();
//    $(".edit_profile_form_element").hide();
//    console.log("Hiding");
    var editing = false;

    $("#edit_profile_button").click(
        function() {

            if (editing == false) {
                // User wants to edit
                console.log("Hiding info elements");
                $(".info_element").hide();

                console.log("Showing form elements");
                $(".edit_profile_form_element").show();

                $("#edit_profile_button").text("Cancelar");

                editing = true;
            }
            else {
                // User canceled edition    TODO: Cómo hacer que se reinicien los valores del form?
                console.log("Hiding form elements");
                $(".edit_profile_form_element").hide();

                console.log("Showing info elements");
                $(".info_element").show();

                $("#edit_profile_button").text("Editar");

                editing = false;
            }



        }
    );
});