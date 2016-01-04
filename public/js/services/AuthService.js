app = angular.module('eda.auth_service', []);

app.service('AuthService', ['$rootScope','$http', function($rootScope, $http){
	var me = this;
//	var auth_server = 'http://localhost:8000/auth/'
	var auth_server = '/api/auth/'
	me.auth = {
		username: null,
		password: null
	};

    $rootScope.authenticated = localStorage.getItem('AuthToken') != null;

	me.authenticate = function(auth){
		me.auth = auth;
		var request_data = JSON.stringify(me.auth);
		promise = $http.post(auth_server+'auth_token/', request_data);

		promise.success(function(data){
            localStorage.setItem('AuthToken', data);
            location = location;
            $rootScope.authenticated = true;
            if ($rootScope.retry){
                $http($rootScope.retry);
            }
		});

		promise.error(function(data, status, headers){
			$rootScope.authenticated = false;
			$rootScope.$broadcast('authfailure');
		});

	};

}]);

