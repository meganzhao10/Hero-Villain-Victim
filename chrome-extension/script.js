var __name__ = "__main__";
var run;
run = function(tabs) {
    localhost = "http://127.0.0.1:5000/";
    var url;
    url = tabs[0].url;

    // Hide everything except loading message (and title)
    document.getElementById("close").onclick = function(){window.close();};
    $('div:not(#loading)').hide();
    $('div#titleDiv').show();

    $(document).ready(function() {
        $.get(localhost, {"url": url}, function(data){
            // Set hero, villain, victim elements
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
