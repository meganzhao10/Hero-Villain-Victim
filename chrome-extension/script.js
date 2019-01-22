var __name__ = "__main__";
var run;
run = function(tabs) {
    var url;
    url = tabs[0].url;
    localhost = "http://127.0.0.1:5000/";
    // $(document).ready(function() {
    //     $.get(localhost, {"url": url}, function(data){
    //         // document.getElementById("loading").innerHTML = "";
    //         // // document.getElementById("f1").innerHTML = data[0];
    //         // // document.getElementById("f2").innerHTML = data[1];
    //         // // document.getElementById("f3").innerHTML = data[2];
    //     });
    // });
};

chrome.tabs.query({
    active: true,
    currentWindow: true
}, run);
