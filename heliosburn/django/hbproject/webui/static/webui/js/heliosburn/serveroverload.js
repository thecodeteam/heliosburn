angular.module('hbApp.controllers').controller('ServerOverloadCtrl', ['$scope', '$http', '$log', 'ngDialog', function($scope, $http, $log, ngDialog){

    $scope.triggers = [
        {fromLoad: 50, toLoad: 70, actions: []},
        {fromLoad: 60, toLoad: 80, actions: []},
        {fromLoad: 50, toLoad: 90, actions: []},
        {fromLoad: 30, toLoad: 100, actions: []},
        {fromLoad: 10, toLoad: 100, actions: []}
    ];


    $scope.newTrigger = function() {
        ngDialog.open({
            //template: 'externalTemplate.html',
            template: '<p>my template</p>',
            plain: true,
            controller: ['$scope', function ($scope) {
                alert("sep");
            }]
        });
    };
}]);