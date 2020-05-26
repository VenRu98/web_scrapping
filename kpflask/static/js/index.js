$(document).ready(function() {
    $('#bukalapak').DataTable({
        scrollX: false,
        scrollCollapse: true,
        responsive: true,
        autoWidth: false,
        lengthMenu: [5, 10],
    });
    $('#lazada').DataTable({
        scrollX: true,
        scrollCollapse: true,
        responsive: true,
        autoWidth: false,
        lengthMenu: [5, 10],
    });
    $('#tokopedia').DataTable({
        scrollX: true,
        scrollCollapse: true,
        responsive: true,
        autoWidth: false,
        lengthMenu: [5, 10],
    });
    $(".linkbaris").on('mouseup', function(e) {
        if (e.which == 2 || e.which == 1) {
            window.open($(this).data("href"), "_blank");
        }
    });
});