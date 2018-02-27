
app = angular.module('eda.directives', ['eda.instrument_service',
                                        'eda.auth_service',
                                        'ui.codemirror',
                                        'textAngular']);


app.directive('edaLogin', ['AuthService', function(authservice){
	return {
		restrict: 'E',
		templateUrl: 'login.html',
		scope: {
		    auth: '@'
		},
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
//                scope.$broadcast('auth_set_timeout');

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

			scope.orderByFunc = function(question){
                return parseFloat(question.question_id);
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

      get_url = function(debug){
        var params = {
          q: iaservice.current.urlname,
          major: iaservice.current.version.major,
          minor: iaservice.current.version.minor,
          lang: iaservice.current.language.id,
          debug: true
        }

        var obs = window.btoa(JSON.stringify(params));
        return iaservice.preview_server + '?t=' + obs;
      }

      scope.pop_interview = function(){
      var preview_url = get_url(false);

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

			scope.$on('change_instrument', function(){
				scope.prod_url = get_url(false);
			});

      document.addEventListener("keydown", function(e) {
        if (e.keyCode == 83 && (navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)){
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

      scope.create_new = function(){
        var versionDetails = $modal.open({
          templateUrl: 'new_questionnaire.html',
          controller: function($scope, $modalInstance){
            $scope.newq = {
                displayname: '',
                q_number: '',
                url_name: '',
                description: ''
            }
            $scope.ok = function(isValid){
                if (isValid){
                    $scope.$emit('create_new_questionnaire', $scope.newq);
                    $modalInstance.close();
                }
            };
            $scope.cancel = function(){
                $modalInstance.close();
            };
            $scope.box_name = 'New Questionnaire';
          },
          size: 'md',
          resolve: {
              version: function(){
                  return scope.version;
              }
          }
        });

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
            $scope.box_name = 'Save Version';

          },
          size: 'md',
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
			$scope.language_options = [
			    {id: 'en', name: 'English'},
			    {id: 'no', name: 'Norwegian'}
			]
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
                        $('div[cardtype]').children().remove();
						var template = angular.element(data);
						var comper = $compile(template);
						var ele = comper(scope);
						element.append(ele);
					})
					.error(function(data, status, headers, config){
					    console.info(data);
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

