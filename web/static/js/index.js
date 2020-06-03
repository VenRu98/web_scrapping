$(document).ready(function() {

    $('#bukalapak').DataTable({
        responsive: true,
        lengthMenu: [3, 5, 10],
        scrollY: "400px",
        scrollCollapse: true,
    });
    $('#lazada').DataTable({
        responsive: true,
        lengthMenu: [3, 5, 10],
        scrollY: "400px",
        scrollCollapse: true,
    });
    $('#tokopedia').DataTable({
        responsive: true,
        lengthMenu: [3, 5, 10],
        scrollY: "400px",
        scrollCollapse: true,
    });
});