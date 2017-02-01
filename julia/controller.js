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

    $scope.rangeSelList = [0,1,2];
    $scope.rangeSelChange = function () {
        selList = $scope.drawRangeList[$scope.params.rangeSel];
        $scope.params.x_min = selList[0];
        $scope.params.x_max = selList[1];
        $scope.params.y_min = selList[2];
        $scope.params.y_max = selList[3];
    };

    $scope.params = {
        x_min:-2.2,
        x_max:1,
        y_min:-1.2,
        y_max:1.2,
        rangeSel:0,
        presetSel:0,
        c:[0,0]
    };


    //draw range
    $scope.drawRangeList = [
        [-1.5,1,5,-1.5,1.5],
        [-2.0,2.0,-1.5,1.5],
        [-0.748766715922161, -0.748766705771757, 0.123640844894862, 0.123640851045266]
    ];

    $scope.presetList = [
        {title:"Mandelbrot Set",value:0,c:[0,0]},
        {title:"Julia Set c=1−φ",value:1,c:[1-1.618,0]},
        {title:"Julia Set c=(φ−2)+(φ−1)i",value:2,c:[1.618-2,1.618-1]},
        {title:"Julia Set c=0.285+0i",value:3,c:[0.285,0]},
        {title:"Julia Set c=0.285+0.01i",value:4,c:[0.285,0.01]},
        {title:"Julia Set c=0.45+0.1428i",value:5,c:[0.45,0.1428]},
        {title:"Julia Set c=-0.70176-0.3842i",value:6,c:[0.70176,-0.3842]},
        {title:"Julia Set c=-0.835-0.2321i",value:7,c:[-0.835,-0.2321]},
        {title:"Julia Set c=-0.8+0.156i",value:8,c:[-0.8,0.156]},
        {title:"Julia Set c=-0.7269+0.1889i",value:9,c:[-0.7269,0.1889]},
        {title:"Julia Set c=-0.8i",value:10,c:[0,-0.8]}
    ];
    $scope.start = function () {
        $scope.slowProcessPainter.start(200,500);
    };

    $scope.stop = function () {
        $scope.slowProcessPainter.stop();
    };


    $scope.drawSet = function () {
        $scope.setup().then(function () {
            $scope.slowProcessPainter.start(50,500);
        });

        var data = {
            handlerName:'Julia_setup'
        };

        $scope.bridge.callHandler('RunPyFunction', data, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
        });
    };

    $scope.improve = function () {
        var deferred = $.Deferred();
        var data = {
            handlerName:'Julia_improve'
        };
        $scope.bridge.callHandler('RunPyFunction', data,function () {
            deferred.resolve();
        });
        return deferred.promise();
    };

    $scope.draw = function () {
        var data = {
            handlerName:'Julia_draw'
        };
        $scope.bridge.callHandler('RunPyFunction', data,function () {
            deferred.resolve();
        });
    };


    $scope.setup = function () {
        //alert($scope.params.presetSel);
        var deferred = $.Deferred();
        $scope.params.c = $scope.presetList[$scope.params.presetSel].c;
        var data = {
            handlerName:'Julia_setup'
        };
        data = $.extend(data,$scope.params);
        $scope.bridge.callHandler('RunPyFunction', data, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
            deferred.resolve();
        });
        return deferred.promise();
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
            interval:400,
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
                $scope.improve().then(function () {
                    $scope.draw();
                });
                if(this.counter==0){
                    this.stop();
                }
                //console.log("run tick fn");
            },
            start:function (totalSteps,interval) {
                if(this.stopped) {
                    this.interval = interval;
                    this.counter = totalSteps;
                    this.stopped = false;
                    $scope.setup();

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