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
            document.getElementById("heroDiv").querySelectorAll("#hero")[0].innerHTML = data[0][0];
            document.getElementById("villainDiv").querySelectorAll("#villain")[0].innerHTML = data[0][1];
            document.getElementById("victimDiv").querySelectorAll("#victim")[0].innerHTML = data[0][2];

            if (data[1][0] == null) {
                word1 = "None"; word2 = "None"; word3 = "None";
            } else {
                word1 = data[1][0][0];
                word2 = data[1][0][1];
                word3 = data[1][0][2];
            }
            document.getElementById("heroDiv").querySelectorAll(".word1")[0].innerHTML = word1;
            document.getElementById("heroDiv").querySelectorAll(".word2")[0].innerHTML = word2;
            document.getElementById("heroDiv").querySelectorAll(".word3")[0].innerHTML = word3;

            if (data[1][1] == null) {
                word1 = "None"; word2 = "None"; word3 = "None";
            } else {
                word1 = data[1][1][0];
                word2 = data[1][1][1];
                word3 = data[1][1][2];  
            }
            document.getElementById("villainDiv").querySelectorAll(".word1")[0].innerHTML = word1;
            document.getElementById("villainDiv").querySelectorAll(".word2")[0].innerHTML = word2;
            document.getElementById("villainDiv").querySelectorAll(".word3")[0].innerHTML = word3;

            if (data[1][2] == null){
                word1 = "None"; word2 = "None"; word3 = "None";
            } else {
                word1 = data[1][2][0];
                word2 = data[1][2][1];
                word3 = data[1][2][2];       
            }
            document.getElementById("victimDiv").querySelectorAll(".word1")[0].innerHTML = word1;
            document.getElementById("victimDiv").querySelectorAll(".word2")[0].innerHTML = word2;
            document.getElementById("victimDiv").querySelectorAll(".word3")[0].innerHTML = word3; 

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
