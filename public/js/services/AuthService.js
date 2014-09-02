app = angular.module('eda.auth_service', []);

app.service('AuthService', ['$rootScope','$http',
										function($rootScope, $http){
	var me = this;
	var auth_server = 'http://localhost:8000/auth/'
	me.auth = {
		username: null,
		password: null
	};

	$rootScope.authenticated = false;

	me.authenticate = function(auth){
		me.auth = auth;
		var request_data = base64.encode(me.auth);
		promise = $http.post(auth_server+'auth_token/', request_data);

		promise.success(function(data){
			$http.defaults.headers.common.Authorization = "Token: "+data
			$rootScope.authenticated = true;
		});

		promise.error(function(data, status, headers){
			$rootScope.$broadcast('authfailure');
		});

	};

}]);