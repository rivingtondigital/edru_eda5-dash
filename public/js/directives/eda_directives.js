
app = angular.module('eda.directives', ['eda.instrument_service',
                                        'eda.auth_service',
                                        'ui.codemirror',
                                        'textAngular']);


app.directive('edaLogin', ['AuthService', function(authservice){
	return {
		restrict: 'E',
		templateUrl: 'login.html',
		scope: {},
		link: function(scope, ele, attr){
			scope.submit_login = function(is_valid){
				if (is_valid == true){
					authservice.authenticate(scope.auth);
				}
			};

			scope.$on('authfailure', function(){
				scope.authfailure = true;
			});


		}
	}
}]);

app.directive('edaInstrument', ['$modal', 'InstrumentService', function($modal, iService){
	return{
		restrict: 'E',
		templateUrl: 'instrument.html',
		config: function(scope){
			iService.setCard('prelims', null);
		}
	}

}]);

app.directive('edaSidebar', ['$modal', 'InstrumentService', function($modal, iService){
	return{
		restrict: 'E',
		templateUrl: 'sidebar.html',
		link: function(scope, element, attrs){
			scope.instrument = iService.current;

			scope.changeCard = function(card){
				if (card == 'prelims'){
					iService.setCard('prelims', null);
				}
				else{
					iService.setCard('question', card);
				}
			};

			scope.add_question = function(){
				iService.addQuestion();
				var qs = $('.divIndex');
				var last = qs[qs.length - 1];
				var qbox = $('#question_box');
				qbox.animate({"scrollTop": $('#question_box')[0].scrollHeight}, "slow");
			};


			scope.$on('change_instrument', function(){
				scope.instrument = iService.current;
			});

			scope.$on('save_version_questionnaire', function(evt){
				var a = 1;
				a = evt;
			});

		}

	};

}]);

app.directive('edaNav', ['$modal', 'InstrumentService', function($modal, iaservice){
	return{
		restrict: 'E',
		templateUrl: 'top_nav.html',

        link: function(scope, element, attrs, controller){

            scope.instruments = iaservice.all_questionnaires;


            scope.pop_interview = function(){
                var preview_url = iaservice.preview_server
                                    +"?q="+iaservice.current.urlname
                                    +"&major="+iaservice.current.version.major
                                    +"&minor="+iaservice.current.version.minor


                window.open(preview_url, 'preview',
                    config="toolbar=no,"+
                    "directories=no,"+
                    "status=no,"+
                    "menubar=no,"+
                    "scrollbars=no,"+
                    "resizable=yes,"+
                    "width=600,"+
                    "height=700,"+
                    "top=50,"+
                    "left=100");
            };

            document.addEventListener("keydown", function(e) {
                  if (e.keyCode == 83 && (navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey))      {
                    e.preventDefault();
                    scope.save_current();
                  }
                }, false);

            scope.save_current = function(){
                (scope, element, attrs, controller);
                scope.$emit('save_current_questionnaire');
            };

            iaservice.fetch_all_questionnaires();
            scope.$on('update_questionnaires', function(){
                scope.instruments = iaservice.all_questionnaires;
            });

            scope.select_version = function(instrument, version){
                iaservice.setCurrent(instrument, version.version);
            }

            scope.save_copy = function(size){
                var versionDetails = $modal.open({
                    templateUrl: 'myModalContent.html',
                    controller: function($scope, $modalInstance){
                        $scope.version = {
                            shortname: '',
                            description: ''
                        }
                        $scope.ok = function(isValid){
                            if (isValid){
                                $scope.$emit('save_version_questionnaire', $scope.version);
                                $modalInstance.close();
                            }
                        };
                        $scope.cancel = function(){
                            $modalInstance.close();
                        };
                    },
                    size: size,
                    resolve: {
                        version: function(){
                            return scope.version;
                        }
                    }
                });
                versionDetails.result.then(function(selectedItems){
                    var a  = 1;

                });
            };

            scope.delete_version = function(size){
                var confirm = $modal.open({
                    size: 'sm',
                    templateUrl: 'VersionDelete.html',
                    controller: function($scope, $modalInstance){
                        $scope.ok = function(){
                            $scope.$emit('delete_current_version', $scope.version);
                            $modalInstance.close();
                        }
                        $scope.cancel = function(){
                            $modalInstance.close();
                        }
                    }
                });
            };
        }
    };
}]);

app.directive('edaCard', ['$http', '$templateCache',  '$compile', function($http, $templates, $compile){
	return {
		restrict: 'E',
		replace: true,
		template: '<div class="test"></div>',
		controller:function($scope){
			$scope.textAreaSetup = function($element){
				$element.attr('ui-codemirror', '');
			};
		},
		link: function(scope, element, attrs, controller){
			var getTemplate = function(cardtype){
				template_urls = {
					prelims: 'prelims.html',
					question: 'question.html'
				}
				promise = $http.get(template_urls[cardtype], {cache: $templates});
				return promise;
			}

			var setCard = function(){
				getTemplate(scope.cardtype)
					.success(function(data){
						var template = angular.element(data);
						var comper = $compile(template);
						var ele = comper(scope);
						$('div[cardtype]').children().remove();
						element.append(ele);
					})
					.error(function(data, status, headers, config){
						debugger;
					});
			}
			setCard();


			scope.$on('change_card', function(){
				setCard();
			});

			scope.delete_question = function(){
				scope.$emit('delete_question', scope.card);
			}

		}
	}
}]);

app.directive('edaAnswers', function(){
	return {
		restrict: 'E',
		scope:{
			answers: '='
		},
		controller: function($scope){

			$scope.add_trigger = function(){
				this.answer.triggers.push({
					identifier: null,
					value: null
				});
			};

			$scope.add_answer = function(){
				var qid = this.$parent.$parent.card.question_id;
				var count = this.answers.length
				this.$parent.answers.push({
					triggers:[],
					description:'',
					answer_id: '',
					question_id: qid
				});
				for(var i=0; i<=count; i++){
					this.$parent.answers[i].answer_id = qid+'.'+i
				}
			};

			$scope.delete_answer = function(){
				var index = this.$index;
				this.answers.splice(index,1);
			};

		},
		templateUrl: 'answers.html'
	};

});


app.directive('edaTrigger', function(){
	return{
		restrict: 'EA',
		scope:{
			trigger: '='
		},
		controller: function($scope){
			$scope.remove_trigger = function(){
				var index = this.$parent.$index;
				this.$parent.answer.triggers.splice(index,1);
			};
		},
		templateUrl: 'trigger.html'
	};
});

app.directive('edaRules', function(){
	return{
		restrict: 'E',
		scope:{
			rules: '='
		},
		controller: function($scope){
			$scope.add_rule = function(){
				var qid = this.$parent.$parent.card.question_id;
				this.rules.push({
					expression: '',
					target: '',
					diagnosis: false,
					diagnosisname: '',
					endifdiagnosis: false,
					question_id: qid
				});
			};
			$scope.delete_rule = function(){
				var index = this.$index;
				this.rules.splice(index, 1);
			}
		},
		templateUrl: 'rules.html'
	};
});

