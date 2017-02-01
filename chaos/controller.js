/**
 * Created by saturnman on 17/01/2017.
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

    $scope.testList = [1,2,3,4,5];

    $scope.params = {
        r:4.0,
        x1start:0.2,
        x2start:0.2000000001,
        iter_count:200,
        lines:1
    };
    $scope.testList = [1,2];

    $scope.drawline = function () {

        console.log("drawline called.");
        var data = {
            r:$scope.params.r,
            x1start:$scope.params.x1start,
            x2start:$scope.params.x2start,
            iter_count:$scope.params.iter_count,
            lines:$scope.params.lines,
            handlerName:'drawLogisticPopulationModel'
        };
        console.log("data="+JSON.stringify(data));
        $scope.bridge.callHandler('RunPyFunction', data, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
        })
    };

    $scope.ChaosModel_drawFibu = function () {
        var data = {
            handlerName:"ChaosModel_drawFibu"
        };
        $scope.bridge.callHandler('RunPyFunction', data, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
        })
    };



    $scope.animate = function () {
        $scope.animation.start();
    };
    $scope.stopAnimate = function () {
        $scope.animation.stop();
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

        $scope.animation = {
            stopped:true,
            interval:40,
            timer:null,
            tick:function () {
                if(this.stopped){
                    clearInterval(this.timer);
                    this.timer = null;
                    return;
                }

                $scope.bridge.callHandler("RunPyFunction",{'handlerName':'drawRandomGridMap'},function(responseData){
                    console.log("JS received response:", responseData);
                });

                console.log("run tick fn");
            },
            start:function () {
                this.stopped = false;
                this.timer = setInterval(this.tick,this.interval);
            },
            stop:function () {
                console.log("in stop fn");

                this.stopped = true;

                clearInterval(this.timer);
                this.timer = null;

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