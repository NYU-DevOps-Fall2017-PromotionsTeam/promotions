$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#promo_id").val(res.id);
        $("#promo_name").val(res.name);
        $("#promo_type").val(res.promo_type);
        $("#promo_value").val(res.value);
        $("#promo_start_date").val(res.start_date);
        $("#promo_end_date").val(res.end_date);
        $("#promo_detail").val(res.detail);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#promo_name").val("");
        $("#promo_type").val("");
        $("#promo_value").val("");
        $("#promo_start_date").val("");
        $("#promo_end_date").val("");
        $("#promo_detail").val("");
        $("#promo_available_date").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Promotion
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#promo_name").val();
        var type = $("#promo_type").val();
        var value = Number($("#promo_value").val());
        var start_date = $("#promo_start_date").val();
        var end_date = $("#promo_end_date").val();
        var detail = $("#promo_detail").val();

        var data = {};

        if (name)
            data.name = name;
        if (type)
            data.promo_type = type;
        if (value)
            data.value = value;
        if (start_date)
            data.start_date = start_date
        if (end_date)
            data.end_date = end_date
        if (detail)
            data.detail = detail

        var ajax = $.ajax({
            type: "POST",
            url: "/promotions",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Promotion
    // ****************************************

    $("#update-btn").click(function () {

        var id = $("#promo_id").val();
        var name = $("#promo_name").val();
        var type = $("#promo_type").val();
        var value = Number($("#promo_value").val());
        var start_date = $("#promo_start_date").val();
        var end_date = $("#promo_end_date").val();
        var detail = $("#promo_detail").val();

        data = {};

        if (name)
            data.name = name;
        if (type)
            data.promo_type = type;
        if (value)
            data.value = value;
        if (start_date)
            data.start_date = start_date
        if (end_date)
            data.end_date = end_date
        if (detail)
            data.detail = detail

        var ajax = $.ajax({
            type: "PUT",
            url: "/promotions/" + id,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Promotion
    // ****************************************

    $("#retrieve-btn").click(function () {

        var promo_id = $("#promo_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/promotions/" + promo_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Promotion
    // ****************************************

    $("#delete-btn").click(function () {

        var promo_id = $("#promo_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/promotions/" + promo_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Promotion with ID [" + promo_id + "] has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        console.log("haha")
        $("#promo_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Promotion
    // ****************************************

    $("#search-btn").click(function () {

        var type = $("#promo_type").val();
        var available_date = $("#promo_available_date").val();

        var queryString = ""

        if (type) {
            queryString += 'promo_type=' + type
        }
        if (available_date) {
            if (queryString.length > 0) {
                queryString += '&available_on=' + available_date
            } else {
                queryString += 'available_on=' + available_date
            }
        }

        if (queryString){
            var ajax = $.ajax({
                type: "GET",
                url: "/promotions?" + queryString,
                contentType: "application/json",
                data: ''
            })
        }
        else {
            var ajax = $.ajax({
                type: "GET",
                url: "/promotions",
                contentType: "application/json",
                data: ''
            })
        }

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'

            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:10%">Name</th>'
            header += '<th style="width:10%">Type</th>'
            header += '<th style="width:10%">Value</th>'
            header += '<th style="width:30%">Start Date</th>'
            header += '<th style="width:30%">End Date</th>'
            header += '<th style="width:30%">Detail</th>'

            $("#search_results").append(header);
            for (var i = 0; i < res.length; i++) {
                promo = res[i];
                var row = "<tr><td>" + promo.id + "</td><td>" + promo.name + "</td><td>" + promo.promo_type + "</td><td>" + promo.value + "</td>";
                row += "<td>" + promo.start_date + "</td><td>" + promo.end_date + "</td><td>" + promo.detail + "</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

})
