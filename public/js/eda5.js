(function(){
	var app = angular.module("eda.instrument_editor", ['ui.bootstrap',
																										 'textAngular',
																										 'ui.codemirror',
																										 'eda.instrument_service',
																										 'eda.autosize',
																										 'eda.auth_service',
																										 'eda.directives']);


// 	app.controller('AllInstrumentsController', ['$scope', '$http', 'InstrumentService', function($scope, $http, InstrumentService){
// 		this.all_instruments = InstrumentService.all_questionnaires;
// 		InstrumentService.fetch_all_questionnaires();

// 		var all = this;

// 		$scope.select_version = function(instrument, selected_version){
// 			InstrumentService.setCurrent(instrument, selected_version.version);
// 		};


// 		/*
// 		$http.jsonp('http://localhost:8000/ajax/v/list.json?callback=JSON_CALLBACK')
// 			.success(function(data){
// 				all.all_instruments = data;
// 			})
// 			.error(function(err){
// 				console.info('error');
// 				console.info(err);
// 			});
// 		*/
// 	}]);


//	app.controller("InstrumentController", ['$scope', '$http','$log', 'InstrumentService', function($scope, $http, $log, iService){
// 		$scope.instrument = iService.current;

// 		$scope.$on('change_instrument', function(){
// 			$scope.instrument = iService.current;
// 		});

// 		$scope.$on('save_version_questionnaire', function(evt){
// 			var a = 1;
// 			a = evt;
// 		});

// 		$scope.changeCard = function(card){
// 			if (card == 'prelims'){
// 				iService.setCard('prelims', null);
// 			}
// 			else{
// 				iService.setCard('question', card);
// 			}
// 		};

// 		$scope.add_question = function(){
// 			iService.addQuestion();
// 			var qs = $('.divIndex');
// 			var last = qs[qs.length - 1];
// 			var qbox = $('#question_box');
// 			//var scroll = last.offsetTop + last.offsetHeight;
// 			//var scroll = $('#question_box')[0].scrollHeight;
// 			//$('#question_box').scrollTop(1E10);
// 			qbox.animate({"scrollTop": $('#question_box')[0].scrollHeight}, "slow");
// 		};

//	}]);

	app.controller('CardController', ['$scope', 'InstrumentService', function($scope, iService){
	
		$scope.instrument = iService.current;
		$scope.cardtype = iService.cardtype;
		$scope.card = iService.card;
		$scope.editorOptions = {
			height: '200px'
		}

		$scope.$on('change_card', function(){
			$scope.instrument = iService.current;
			$scope.cardtype = iService.cardtype;
			$scope.card = iService.card;
		});



	}]);

	app.directive('edaError', ['$modal', function($modal){
		return{
			restrict:'E',
			template:'<div></div>',
			controller: function($scope){

				var open_modal = function(error){
					var confirm = $modal.open({
							size: 'lg',
							templateUrl: 'error.html',
							controller: function($scope, $modalInstance){
								$scope.error = error;

								$scope.ok = function(){
									$modalInstance.close();
								};
							}
						});

				};

				$scope.$on('error_duplicate_questions', function(evt, dups){
					var error = {
						title: 'Error',
						message: 	'Could not save this edit. ',
						details: 'The following question ids were used more then once: ' + dups.join(', ')
					};
					open_modal(error);
				});
			},
		};
	}]);
	
	app.filter('json_expand', function(){
		return function(input){
			return JSON.stringify(input, null, 4);
		};
	});


})();



