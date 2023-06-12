const axios = require('axios');

var modelManager = "http://127.0.0.1:8000"
var cloudManager = "http://127.0.0.1:4003"
var classsifier = "http://127.0.0.1:4002"

/*
<!-- <a href="#" class="list-group-item list-group-item-action">
                <div class="file-name"><%= file.name %></div>
                <div class="file-label"><%= file.label %></div>
                <div class="file-id"><%= file._id %></div>
              </a> -->
*/

var ModelApi = axios.create({
    baseURL: modelManager,
    timeout: 100000,
});

var ClassifierApi = axios.create({
    baseURL: classsifier,
    timeout: 500000,
});

var CloudApi = axios.create({
    baseURL: cloudManager,
    timeout: 100000,
});

module.exports = {
    ModelApi ,
    CloudApi,
    ClassifierApi
}