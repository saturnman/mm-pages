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
        r:4.0,
        x1start:0.2,
        x2start:0.2,
        iter_count:200,
        lines:1,
        exampleSel:1,
        speed:1,
        width:500,
        height:500,
        temperature:50
    };

    $scope.start = function () {
        $scope.slowProcessPainter.start(500,500,$scope.params.temperature);
    };

    $scope.stop = function () {
        $scope.slowProcessPainter.stop();
    };

    $scope.reload = function () {
        window.location.reload();
    };

    $scope.step = function () {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'Ising_step'
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            deferred.resolve();
        });
        return deferred.promise();
    };

    $scope.draw = function () {
        var data = {
            'handlerName':'Ising_draw'
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
        });
    };

    $scope.setTemperature = function () {
        var data = {
            'handlerName':'Ising_setTemperature',
            temperature:$scope.params.temperature
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
            deferred.resolve();
        });
    };


    $scope.setup = function (width,height,temperature) {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'Ising_setup',
            width:width,
            height:height,
            temperature:temperature
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


    $scope.continue = function () {
        $scope.slowProcessPainter.continue();
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
            interval:200,
            counter:0,
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
                $scope.step().then(function () {
                    $scope.draw();
                });
                if(this.counter==0){
                    this.stop();
                }
                //console.log("run tick fn");
            },
            start:function (width,height,temperature) {
                if(this.stopped) {
                    //this.interval = ;
                    this.counter = 10000;
                    this.stopped = false;
                    $scope.setup(width,height,temperature);
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