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

    $scope.configList = [{title:"Barnsley fern",value:0},{title:"Cyclosorus",value:1},{title:"Modified Barnsley fern",value:2},{title:"Culcita",value:3},{title:"Fishbone",value:4},{title:"A fractal tree",value:5}];



    $scope.demoSelectionChanged = function(){
        $scope.demoData = $scope.BarnsleyParams[$scope.params.exampleSel];
    };

    //a b c d e f |p
    $scope.BarnsleyParams = [
        [
            [0,0,0,0.16,0,0,0.01],
            [0.85,0.04,-0.04,0.85,0,1.6,0.85],
            [0.2,-0.26,0.23,0.22,0,1.6,0.07],
            [-0.15,0.28,0.26,0.24,0,0.44,0.07]
        ],
        [
            [0,0,0,0.25,0,-0.4,0.02],
            [0.95,0.005,-0.005,0.93,-0.002,0.5,0.84],
            [0.035,-0.2,0.16,0.04,-0.09,0.02,0.07],
            [-0.04,0.2,0.16,0.04,0.083,0.12,0.07]
        ],
        [
            [0,0,0,0.2,0,-0.12,0.01],
            [0.845,0.036,-0.035,0.82,0,1.6,0.85],
            [0.2,-0.31,0.255,0.245,0,0.29,0.07],
            [-0.15,0.24,0.25,0.2,0,0.68,0.07]
        ],
        [
            [0,0,0,0.25,0,-0.14,0.02],
            [0.85,0.02,-0.02,0.83,0,1,0.84],
            [0.09,-0.28,0.3,0.11,0,0.6,0.07],
            [-0.09,0.28,0.3,0.09,0,0.7,0.07]
        ],
        [
            [0,0,0,0.25,0,-0.4,0.02],
            [0.95,0.002,-0.002,0.93,-0.002,0.5,0.84],
            [0.036,-0.11,0.27,0.01,-0.05,0.005,0.07],
            [-0.04,0.11,0.27,0.01,0.047,0.06,0.07]
        ],
        [
            [0,0,0,0.5,0,0,0.05],
            [0.42,-0.42,0.42,0.42,0,0.2,0.4],
            [0.42,0.42,-0.42,0.42,0,0.2,0.4],
            [0.1,0,0,0.1,0,0.2,0.15]
        ]
    ];

    $scope.shapeList = [false,true,false,false,true,false]

    $scope.params = {
        r:4.0,
        x1start:0.2,
        x2start:0.2,
        iter_count:200,
        lines:1,
        exampleSel:0,
        speed:1,
        ruleDesp:""
    };

    $scope.demoData = $scope.BarnsleyParams[$scope.params.exampleSel];

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


        $scope.bridge.callHandler('RunPyFunction', {"handlerName":"LSystem_draw_Barnsley","slim":$scope.shapeList[$scope.params.exampleSel],"params":$scope.BarnsleyParams[$scope.params.exampleSel]}, function responseCallback(responseData) {
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