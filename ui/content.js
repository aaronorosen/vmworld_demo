var lastId = 0; // 0; FOR TESTING ONLY
var dataTableBody = false;
var updateFreq = 500; // in milliseconds
var slideDownDuration = 3000; // in milliseconds

function sleep_getTime() {
    return (new Date()).getTime();
}

function sleep(ms) {
    var startTime = sleep_getTime();
    while (sleep_getTime() - startTime < ms) {}
}

function updateTable() {
    $.ajax({
        url: "content_ajax.php",
        data: "lastContentId=" + lastId,
        dataType: "json",
        success: function(data) {
            var i,row;

            for (i = 0; i < data.rows.length; ++i) {
                row = data.rows[i];
                lastId = row.id;
                console.log("lastId is " + lastId);
                dataTableBody.prepend(
                    "<tr>" +
                       "<td>" + row.phone_number + "</td>" +
                        "<td>" + row.hostname  + "</td>" +
                    "</tr>"
                );

                dataTableBody.first().slideDown();
            }


            sleep(updateFreq);
            updateTable();
//            setTimeout(updateTable, 0);
//            setTimeout(updateTable, updateFreq);
        },
        failure: function(data) {
            console.log("Table updating has stopped: " + data.error);
        }
    });
}

$(window).load(function() {
    dataTableBody = $('#dataTable tbody');

    updateTable();
});
