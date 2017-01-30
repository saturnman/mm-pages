/**
 * Created by saturnman on 18/01/2017.
 */

var mathModelApp = angular.module("mathModelApp",['ngRoute','ui.bootstrap']);

var TestModelController = mathModelApp.controller("TestModelController",['$location',"$scope",function ($location,$scope) {
    function setupWebViewJavascriptBridge(callback) {
        if (window.WebViewJavascriptBridge) { return callback(WebViewJavascriptBridge); }
        if (window.WVJBCallbacks) { return window.WVJBCallbacks.push(callback); }
        window.WVJBCallbacks = [callback];
        var WVJBIframe = document.createElement('iframe');
        WVJBIframe.style.display = 'none';
        WVJBIframe.src = 'https://__bridge_loaded__';
        document.documentElement.appendChild(WVJBIframe);
        setTimeout(function() { document.documentElement.removeChild(WVJBIframe) }, 0)
    };

    $scope.params = {
        b:1.0,
        x1start:0.2,
        x2start:0.2,
        iter_count:200,
        lines:1,
        exampleSel:1,
        speed:1,
        width:120,
        height:120,
        demoSelection:0
    };

    $scope.demoList = [
        {name:"随机分布博弈",value:0},
        {name:"合作者入侵",value:1},
        {name:"背叛者入侵",value:2},
        {name:"异步更新合作者入侵",value:3}
    ];

    $scope.config = function (command) {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'SimulatedAnnealingTSP_config',
            'command':command
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            deferred.resolve();
        });
        return deferred.promise();
    };

    $scope.patch = function (posX,posY,data) {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'SimulatedAnnealingTSP_patch',
            posX:posX,
            posY:posY,
            d:data
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            deferred.resolve();
        });
        return deferred.promise();
    };

    $scope.demoSelectionChanged = function () {
        if($scope.params.demoSelection==0){
            $scope.slowProcessPainter.stop();
            $scope.slowProcessPainter.async = false;
            $scope.config("random").then(function () {
                $scope.draw();
                $scope.start();
            });
        }else if($scope.params.demoSelection==1){
            $scope.slowProcessPainter.stop();
            $scope.slowProcessPainter.async = false;
            $scope.config("alld").then(function () {
                $scope.patch(60,60,[[0,0],[0,0]]).then(function () {
                    $scope.draw();
                    $scope.slowProcessPainter.continue();
                });
            });
        }else if($scope.params.demoSelection==2){
            $scope.slowProcessPainter.stop();
            $scope.slowProcessPainter.async = false;
            $scope.config("allc").then(function () {
                $scope.patch(60,60,[[1,1],[1,1]]).then(function () {
                    $scope.draw();
                    $scope.slowProcessPainter.continue();
                });
            });
        }else{
            $scope.slowProcessPainter.stop();
            $scope.slowProcessPainter.async = true;
            $scope.config("alld").then(function () {
                $scope.patch(60,60,[[0,0,0],[0,0,0],[0,0,0]]).then(function () {
                    $scope.draw();
                    $scope.slowProcessPainter.continue();
                });
            });
        }
    };

    $scope.start = function () {
        $scope.setup().then(function () {
            $scope.slowProcessPainter.start();
        });
    };

    $scope.continue = function () {
        $scope.slowProcessPainter.continue();
    };

    $scope.stop = function () {
        $scope.slowProcessPainter.stop();
    };

    $scope.step = function () {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'SimulatedAnnealingTSP_step'
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            deferred.resolve();
        });
        return deferred.promise();
    };

    $scope.draw = function () {

        var data = {
            'handlerName':'SimulatedAnnealingTSP_draw'
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
        });
    };

    $scope.setup = function () {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'SimulatedAnnealingTSP_setup'
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
            deferred.resolve();
        });
        return deferred.promise();
    };

    $scope.changeSpeed = function () {
        $scope.animation.changeSpeed();
    };

    $scope.reload = function () {
        window.location.reload();
    };

    $scope.init = function () {
        setupWebViewJavascriptBridge(function(bridge) {

            /* Initialize your app here */

            bridge.registerHandler('JS Echo', function(data, responseCallback) {
                console.log("JS Echo called with:", data);
                responseCallback(data)
            });

            $scope.bridge = bridge;
        });

        $scope.slowProcessPainter = {
            stopped:true,
            interval:100,
            counter:0,
            async:false,
            timer:null,
            data:{
            },
            step:function () {
                if(this.stopped){
                    clearInterval(this.timer);
                    this.timer = null;
                    return;
                }
                this.counter -= 1;
                if($scope.slowProcessPainter.async==true){
                    $scope.asyncstep().then(function () {
                        $scope.draw();
                    });
                }else {
                    $scope.step().then(function () {
                        $scope.draw();
                    });
                }
                if(this.counter==0){
                    this.stop();
                }
                //console.log("run tick fn");
            },
            start:function () {
                if(this.stopped) {
                    //this.interval = ;
                    this.counter = 10000;
                    this.stopped = false;
                    this.timer = setInterval(this.step, this.interval);
                }
            },
            stop:function () {
                console.log("in stop fn");
                this.stopped = true;
                this.counter = 0;
                clearInterval(this.timer);
                this.timer = null;
            },
            continue:function () {
                if(this.timer==null) {
                    this.stopped = false;
                    this.timer = setInterval(this.step, this.interval);
                }
            }
        };
    };
    $scope.init();

}]);

mathModelApp.config(function($routeProvider) {
    $routeProvider.when("/",{
        controller:"TestModelController",
        templateUrl:"test.html"
    }).otherwise({
        redirectTo:"/"
    })
});