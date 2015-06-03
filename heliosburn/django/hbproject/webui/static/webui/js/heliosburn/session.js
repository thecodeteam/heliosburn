
angular.module('hbApp').config(function($stateProvider, $urlRouterProvider) {

        $stateProvider

            // route to show our basic form (/form)
            .state('form', {
                url: '/form',
                templateUrl: '/static/webui/partials/session/form.html'
            })

            .state('form.step1', {
                url: '/step1',
                templateUrl: '/static/webui/partials/session/step1.html'
            })

            .state('form.step2', {
                url: '/step2',
                templateUrl: '/static/webui/partials/session/step2.html'
            })

            .state('form.step3', {
                url: '/step3',
                templateUrl: '/static/webui/partials/session/step3.html'
            })

            .state('form.step4', {
                url: '/step4',
                templateUrl: '/static/webui/partials/session/step4.html'
            })

            .state('form.step5', {
                url: '/step5',
                templateUrl: '/static/webui/partials/session/step5.html'
            });

        // catch all route
        // send users to the form page
        $urlRouterProvider.otherwise('/form/step1');

    });

angular.module('hbApp.controllers').controller('SessionCtrl', ['$scope', '$http', '$log', '$window', function($scope, $http, $log, $window){

    // we will store all of our form data in this object
    $scope.formData = {};
    $scope.testplans = [];

    $http.get('/webui/testplans/', $scope.formData)
        .success(function(data) {
            $log.info(data);
            $scope.testplans = data.testplans;
            $scope.testplans.splice(0, 0, {name: "<No Test Plan selected>"});
            $scope.formData.testplan = $scope.testplans[0];

        });

    $scope.processForm = function() {

        $http.post('/webui/sessions/create/', $scope.formData)
            .success(function(url) {
                $window.location.href = url;
            });
    };

}]);