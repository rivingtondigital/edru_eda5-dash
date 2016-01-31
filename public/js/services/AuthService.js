app = angular.module('eda.auth_service', []);

app.service('AuthService', ['$rootScope','$http', '$timeout', function($rootScope, $http, $timeout){
	var me = this;
//	var auth_server = 'http://localhost:8000/auth/'
	var auth_server = '/api/auth/'
	me.auth = {
		username: null,
		password: null
	};

    $rootScope.auth = {};
    $rootScope.auth.authenticated = localStorage.getItem('AuthToken') != null;

//    var set_auth = function(count){
//        $timeout.cancel($rootScope.auth.timer_p);
//        console.info('re-setting auth '+ $rootScope.auth_count);
////        count = count * 60 * 1000;
//        $rootScope.auth.timer_p = $timeout(function(){
//            $rootScope.auth.authenticated = false;
//        }, $rootScope.auth_count);
//    };

    $rootScope.$on('auth_set_timeout', function(){
        timer = $rootScope.auth_count;
        console.info('Resetting Auth-Timeout: '+ timer);
        $timeout.cancel($rootScope.auth.timer_p);
        $rootScope.auth.timer_p = $timeout(function(){
            console.info('timeout reached');
            $rootScope.auth.authenticated = false;
        }, timer);
    });

	me.authenticate = function(auth){
		me.auth = auth;
		var request_data = JSON.stringify(me.auth);
		promise = $http.post(auth_server+'auth_token/', request_data);

		promise.success(function(data){
            localStorage.setItem('AuthToken', data);
            location = location;
            $rootScope.auth.authenticated = true;
            if ($rootScope.retry){
                $http($rootScope.retry);
            }
		});

		promise.error(function(data, status, headers){
			$rootScope.auth.authenticated = false;
			$rootScope.$broadcast('authfailure');
		});
	};

}]);

