(function(){
	var app = angular.module("InstrumentEditor", []);

	app.controller("InstrumentController", ['$http', function($http){
		this.instrument = {
			name: "Loading....",
			description: "Please Wait for the questionnaire to load.",
			questions: []
		};

		var ictrl = this;

		$http.get('/ajax/v/current/eda5.json')
			.success(function(data){
				ictrl.instrument = data;
			})

			.error(function(err){
				$log.error(err);
			});
	}]);

	app.directive('questionEdit', function(){
		return {
			templateUrl: '/templates/editor/question.html',
			restrict: 'E'
		};
	});
})();