var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};

function getCities(callback) {
    getJSON("/api/v1/cities",callback);
}

function getCityChains(cityid,callback) {
    getJSON("/api/v1/chains_in_city/" + cityid, callback);
}

function getCityChainPos(cityid,chainid,callback) {
    getJSON("/api/v1/pos_in_chains_city/" + cityid + "/" + chainid, callback);
}