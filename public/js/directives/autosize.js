
app = angular.module("eda.autosize", []);

app.directive('autoSize', ['$compile', function($compile){
	return{
		require: 'ngModel',
		link:{
			post: function(scope, element, attrs, controller){
				var a = 1;
				attrs.$observe('ngModel', function(value){
					(scope, element, attrs, controller, $compile);
					var text = scope.$eval(value) || "";
					var width = $(element).width();
					var height = text.length/(width/10) + 2;
					element.attr('rows', height);
				});
			}
		}
	};

}]);
