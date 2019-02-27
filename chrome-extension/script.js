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


            if (data[1][0] != null) {
                document.getElementById("heroDiv").querySelectorAll(".word1")[0].innerHTML = data[1][0][0];
                document.getElementById("heroDiv").querySelectorAll(".word2")[0].innerHTML = data[1][0][1];
                document.getElementById("heroDiv").querySelectorAll(".word3")[0].innerHTML = data[1][0][2];
            }

            if (data[1][1] != null) {
                document.getElementById("villainDiv").querySelectorAll(".word1")[0].innerHTML = data[1][1][0];
                document.getElementById("villainDiv").querySelectorAll(".word2")[0].innerHTML = data[1][1][1];
                document.getElementById("villainDiv").querySelectorAll(".word3")[0].innerHTML = data[1][1][2];
            }

            if (data[1][2] != null){
                document.getElementById("victimDiv").querySelectorAll(".word1")[0].innerHTML = data[1][2][0];
                document.getElementById("victimDiv").querySelectorAll(".word2")[0].innerHTML = data[1][2][1];
                document.getElementById("victimDiv").querySelectorAll(".word3")[0].innerHTML = data[1][2][2]; 
            }

            // Show everything except loading message
            $('div').hide();
            $('div:not(#loading)').show();
            

            if (data[1][0] == null) {
                $('#heroWords').hide();
            }
            if (data[1][1] == null) {
                $('#villainWords').hide();
            }
            if (data[1][2] == null) {
                $('#victimWords').hide();
            }

        });
    });
};

chrome.tabs.query({
    active: true,
    currentWindow: true
}, run);
