var __name__ = "__main__";
var run;
run = function(tabs) {
    var url;
    url = tabs[0].url;
    localhost = "http://127.0.0.1:5000/newssite/";
    $(document).ready(function() {
        $.get(localhost, {"url": url}, function(data){
            alert(data);
        })
    });
};

chrome.tabs.query({
    active: true,
    currentWindow: true
}, run);
