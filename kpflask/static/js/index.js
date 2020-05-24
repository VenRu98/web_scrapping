$(document).ready(function() {
    $('#bukalapak').DataTable({
        scrollX: true,
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
});