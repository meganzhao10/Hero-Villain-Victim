var __name__ = "__main__";
var run;
run = function(tabs) {
    localhost = "http://127.0.0.1:5000/";
    var url;
    url = tabs[0].url;

    // Hide everything except loading message (and title)
    $('div:not(#loading)').hide();
    $('div#title').show();

    $(document).ready(function() {
        $.get(localhost, {"url": url}, function(data){
            // document.getElementById("loading").innerHTML = "";
            // // document.getElementById("f1").innerHTML = data[0];
            // // document.getElementById("f2").innerHTML = data[1];
            // // document.getElementById("f3").innerHTML = data[2];
            document.getElementById("heroDiv").querySelectorAll("#hero")[0].innerHTML = data[0];
            document.getElementById("villainDiv").querySelectorAll("#villain")[0].innerHTML = data[1];
            document.getElementById("victimDiv").querySelectorAll("#victim")[0].innerHTML = data[2];

            // Show everything except loading message
            $('div').hide();
            $('div:not(#loading)').show();
        });
    });
};

chrome.tabs.query({
    active: true,
    currentWindow: true
}, run);