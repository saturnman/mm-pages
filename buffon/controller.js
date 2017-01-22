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
        r:4.0,
        x1start:0.2,
        x2start:0.2,
        iter_count:200,
        lines:1,
        exampleSel:1,
        speed:1,
        ruleDesp:""
    };

    $scope.ruleDespList = [
        {
            "rule":'"F":"F+F--F+F", "S":"F"',
            "direct":180,
            "angle":60,
            "iter":6,
            "title":"Koch"
        },
        {
            "rule":'"X":"X+YF+", "Y":"-FX-Y", "S":"FX"',
            "direct":0,
            "angle":90,
            "iter":13,
            "title":"Dragon"
        },
        {
            "rule":'"f":"F-f-F", "F":"f+F+f", "S":"f"',
            "direct":0,
            "angle":60,
            "iter":7,
            "title":"Triangle"
        },
        {
            "rule":'"X":"F-[[X]+X]+F[+FX]-X", "F":"FF", "S":"X"',
            "direct":-45,
            "angle":25,
            "iter":6,
            "title":"Plant"
        },
        {
            "rule":'"S":"X", "X":"-YF+XFX+FY-", "Y":"+XF-YFY-FX+"',
            "direct":0,
            "angle":90,
            "iter":6,
            "title":"Hilbert"
        },
        {
            "rule":'"S":"L--F--L--F", "L":"+R-F-R+", "R":"-L+F+L-"',
            "direct":0,
            "angle":45,
            "iter":10,
            "title":"Sierpinski"
        }
    ];

    $scope.testList = [1,2];

    $scope.drawSystem = function () {


        $scope.bridge.callHandler('RunPyFunction', {"handlerName":"LSystem_draw_Barnsley","rule":$scope.params.exampleSel}, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
        });
    };

    $scope.changeSpeed = function () {
        $scope.animation.changeSpeed();
    };

    $scope.animate = function () {

        $scope.animation.start();
    };
    $scope.stopAnimate = function () {
        $scope.animation.stop();
    };

    $scope.continueAnimate = function () {
        $scope.animation.continue();
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
            interval:400,
            timer:null,
            data:{
            },
            tick:function () {
                if(this.stopped){
                    clearInterval(this.timer);
                    this.timer = null;
                    return;
                }

                $scope.bridge.callHandler("RunPyFunction",{'handlerName':'Pendulum_step'},function(responseData){
                    $scope.bridge.callHandler("RunPyFunction",{'handlerName':'Pendulum_draw'},function(res) {
                        console.log("JS received response:", res);
                    });
                });
                //console.log("run tick fn");
            },
            start:function () {
                if(this.stopped) {
                    this.stopped = false;
                    this.data.handlerName = "Pendulum_draw";
                    $scope.bridge.callHandler("RunPyFunction", this.data, function (responseData) {
                        console.log("JS received response:", responseData);
                    });
                    this.timer = setInterval(this.tick, this.interval);
                }
            },
            stop:function () {
                console.log("in stop fn");
                this.stopped = true;
                clearInterval(this.timer);
                this.timer = null;
            },
            continue:function () {
                if(this.timer==null) {
                    this.stopped = false;
                    this.timer = setInterval(this.tick, this.interval);
                }
            },
            changeSpeed:function (speed) {
                var newSpeed = 400/speed;
                this.interval = parseInt(newSpeed.toFixed(0));
                this.stop();
                this.continue();
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