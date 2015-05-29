var hbApp = angular.module('hbApp', ['hbApp.controllers', 'ngAnimate', 'ui.router'])

    .config(function($httpProvider) {

        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

    });

angular.module('hbApp.controllers', []);