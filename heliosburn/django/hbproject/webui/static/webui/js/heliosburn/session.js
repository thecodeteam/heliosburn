
angular.module('hbApp').config(function($stateProvider, $urlRouterProvider) {

        $stateProvider

            // route to show our basic form (/form)
            .state('form', {
                url: '/form',
                templateUrl: '/static/webui/partials/session/form.html',
                controller: 'SessionCtrl'
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

angular.module('hbApp.controllers').controller('SessionCtrl', ['$scope', function($scope){

    // we will store all of our form data in this object
    $scope.formData = {};

    // function to process the form
    $scope.processForm = function() {
        alert('awesome!');
    };

}]);