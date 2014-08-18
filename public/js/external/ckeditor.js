angular.module('ngCkeditor', [])
	.directive('ckeditor', function() {
  var calledEarly, loaded;
  loaded = false;
  calledEarly = false;

  return {
    require: '?ngModel',
    compile: function(element, attributes, transclude) {
      var loadIt, local;

      local = this;
      loadIt = function() {
        return calledEarly = true;
      };

      element.ready(function() {
        return loadIt();
      });

      return {
        post: function($scope, element, attributes, controller) {
          if (calledEarly) {
            return local.link($scope, element, attributes, controller);
          }
          loadIt = (function($scope, element, attributes, controller) {
            return function() {
              local.link($scope, element, attributes, controller);
            };
          })($scope, element, attributes, controller);
        }
      };
    },

    link: function($scope, elm, attr, ngModel) {
      var ck;
      if (!ngModel) {
        return;
      }

      if (calledEarly && !loaded) {
        return loaded = true;
      }
      loaded = false;

      ck = CKEDITOR.replace(elm[0]);
      ck.on('pasteState', function() {
        $scope.$apply(function() {
          ngModel.$setViewValue(ck.getData());
        });
      });

      ngModel.$render = function(value) {
        ck.setData(ngModel.$viewValue);
      };
    }
  };
});