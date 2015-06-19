angular.module('hbApp.controllers').controller('ServerOverloadCtrl', ['$scope', '$http', '$log', 'ngDialog', function($scope, $http, $log, ngDialog){


    //$scope.triggers = [
    //    {
    //        fromLoad: 20,
    //        toLoad: 60,
    //        actions: [
    //            {type: "response", value: "503", percentage: "60"},
    //            {type: "response", value: "429", percentage: "10"}
    //        ]
    //    }
    //];

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
            //template: 'externalTemplate.html',
            template: '<div class="dialog-contents"> \
                        <input ng-model="action.type" placeholder="Type" /><br /> \
                        <input ng-model="action.value" placeholder="Value" /><br /> \
                        <input ng-model="action.percentage" placeholder="Percentage" /><br /> \
                        <button ng-click="confirm(action)">Confirm</button> \
                        <button ng-click="closeThisDialog(1)">Cancel</button> \
                        </div>',
            plain: true,
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
            });
    };

}]);