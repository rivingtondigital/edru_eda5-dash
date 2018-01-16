app = angular.module('eda.config', []);

app.service('EdaConfig', ['$rootScope','$http', function($rootScope, $http){
    this.preview_server = "http://interview.eda5.org/index.html";
}])
