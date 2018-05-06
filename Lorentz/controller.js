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

    $scope.configList = [{title:"Koch",value:0},{title:"Dragon",value:1},{title:"Triangle",value:2},{title:"Plant",value:3},{title:"Hilbert",value:4},{title:"Sierpinski",value:5}];

    $scope.params = {
        rho:28.0,
        sigma:10.,
        beta:2.66
    };

    $scope.setParams = function(){
        var deferred = $.Deferred();
        var data = {
            'handlerName':'Lorentz_System_setParams',
            'rho':$scope.params.rho,
            'sigma':$scope.params.sigma,
            'beta':$scope.params.beta
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
            deferred.resolve();
        });
        return deferred.promise();
    }

    $scope.start = function () {
        $scope.slowProcessPainter.start();
    };

    $scope.stop = function () {
        $scope.slowProcessPainter.stop();
    };

    $scope.continue = function () {
        $scope.slowProcessPainter.continue();
    };

    $scope.step = function () {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'Lorentz_System_step'
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            deferred.resolve();
        });
        return deferred.promise();
    };

    $scope.draw = function () {
        var data = {
            'handlerName':'Lorentz_System_draw'
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
        });
    };

    $scope.setup = function () {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'Lorentz_System_setup'
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
            deferred.resolve();
        });
        return deferred.promise();
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
            interval:150,
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
            start:function () {
                if(this.stopped) {
                    //this.interval = ;
                    this.counter = 10000;
                    this.stopped = false;
                    $scope.setParams();
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