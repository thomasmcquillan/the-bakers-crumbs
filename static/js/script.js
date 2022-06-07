// hover function for custom search icon
$(document).ready(function() {
	$("#icon-wrap").hover(function() {
        $("#tbc-search").toggle();
		$("#tbc-search-hover").toggle();
	}, function() {
        $("#tbc-search").toggle();
		$("#tbc-search-hover").toggle();
	});
});

$(document).ready(function() {
    $("#nav-trigger").click(function() {
        $("#navlinks-sm").toggle();
    });
});