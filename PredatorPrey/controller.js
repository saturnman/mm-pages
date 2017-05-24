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
        x:1.0,
        y:1.0,
        speed:1
    };

    $scope.config = function (command) {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'PredatorPrey_config',
            'command':command
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            deferred.resolve();
        });
        return deferred.promise();
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
            'handlerName':'PredatorPrey_step'
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            deferred.resolve();
        });
        return deferred.promise();
    };

    $scope.draw = function () {

        var data = {
            'handlerName':'PredatorPrey_draw'
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
        });
    };

    $scope.setup = function () {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'PredatorPrey_setup',
            'x':$scope.params.x,
            'y':$scope.params.y
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