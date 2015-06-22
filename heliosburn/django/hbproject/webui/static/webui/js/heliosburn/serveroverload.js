angular.module('hbApp.controllers').controller('ServerOverloadCtrl', ['$scope', '$http', '$log', 'ngDialog', function($scope, $http, $log, ngDialog){

    $scope.saveText = "Save";
    $scope.saving = false;

    $scope.triggers = response_triggers;

    $scope.newTrigger = function() {
        $scope.triggers.push({fromLoad:0, toLoad:100, actions: []});
    };

    $scope.removeTrigger = function(trigger) {
        var idx = $scope.triggers.indexOf(trigger);
        $log.debug("Removing trigger index " + idx);

        if(idx !== -1) {
            $scope.triggers.splice(idx,1);
        }
    };

    $scope.removeAction = function(trigger, action) {
        var trigger_idx = $scope.triggers.indexOf(trigger);

        if(trigger_idx !== -1) {
            var action_idx = $scope.triggers[trigger_idx].actions.indexOf(action);
            $log.debug("Removing action " + action_idx + " in trigger " + trigger_idx);

            if (action_idx !== -1) {
                $scope.triggers[trigger_idx].actions.splice(action_idx, 1);
            }
        }
    };

    $scope.newAction = function(trigger) {
        var dialog = ngDialog.openConfirm({
            template: 'newActionDialog',
            controller: ['$scope', function ($scope) {
                $log.info('Dialog open');
            }]
        }).then(
            function (value) {
                $log.info('Dialog confirmed: ' + value);
                $log.info(value);

                trigger.actions.push(value);
            },
            function (value) {
                $log.info('Dialog dismissed');
            }
        );
    };

    $scope.saveTriggers = function() {
        $log.debug("Saving triggers");
        $scope.saving = true;
        $scope.saveText = "Saving";

        var data = {
            pk: "557fffcdeb9089088541bc1c",
            name: "response_triggers",
            value: $scope.triggers
        }

        $http.post('/webui/serveroverload/update/', data)
            .success(function() {
                $log.debug("Trigger updated successfully");
            })
            .error(function() {
                $log.error("Error updating trigger");
            })
            .finally(function () {
                $scope.saving = false;
                $scope.saveText = "Save";
            });
    };

}]);