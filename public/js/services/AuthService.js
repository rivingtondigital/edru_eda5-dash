function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



app = angular.module('eda.auth_service', []);
app.service('AuthService', ['$rootScope','$http',
										function($rootScope, $http){
	var me = this;
	var auth_server = 'http://localhost:8000/auth/token/new.json'
//	var auth_server = 'http://interview.eda5.org/api/auth/'
	me.auth = {
		username: null,
		password: null
	};

	$rootScope.authenticated = false;

	me.authenticate = function(auth){
		$http.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken');
		me.auth = auth;

		promise = $http({
		    method: 'POST',
		    url: auth_server,
		    data: $.param(auth),
		    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		});

//		promise = $http.post(auth_server, auth);

		promise.success(function(data){
			if (data.success){
				token = btoa(me.auth.username+':'+data.token);
				$http.defaults.headers.common.Authorization = "Basic "+token
				$rootScope.authenticated = true;
				$rootScope.$broadcast('authenticated');
			}
			else{
				$rootScope.$broadcast('authfailure');
			}
		});

		promise.error(function(data, status, headers){
			$rootScope.$broadcast('netfailure');
		});

	};

}]);
