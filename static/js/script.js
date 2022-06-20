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

//    setTimeout function to dismiss flash messages courtesy
//    of Naoise Gaffney on Code Institute Slack Channel.
setTimeout(()=> {
    flash_message = document.getElementsByClassName("flash-message");

    for (let i = 0; i < flash_message.length; i++) {
        flash_message[i].style.display="none";
    }
}, 1100);