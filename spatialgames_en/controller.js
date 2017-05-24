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
        {name:"Randomized Initialization",value:0},
        {name:"C Invasion",value:1},
        {name:"D Invasion",value:2},
        {name:"Asyncronous C Invasion",value:3}
    ];

    $scope.config = function (command) {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'SpatialGame_config',
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
            'handlerName':'SpatialGame_patch',
            posX:posX,
            posY:posY,
            d:data
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            deferred.resolve();
        });
        return deferred.promise();
    };

    $scope.reload = function () {
        window.location.reload();
    };

    $scope.continue = function () {
        $scope.slowProcessPainter.continue();
    };

    $scope.demoSelectionChanged = function () {
        if($scope.params.demoSelection==0){
            $scope.slowProcessPainter.stop();
            $scope.slowProcessPainter.async = false;
            $scope.config("random").then(function () {
                $scope.draw();
                $scope.slowProcessPainter.continue();
            });
        }else if($scope.params.demoSelection==1){
            $scope.slowProcessPainter.stop();
            $scope.slowProcessPainter.async = false;
            $scope.config("alld").then(function () {
                $scope.patch(59,59,[[0,0,0],[0,0,0],[0,0,0]]).then(function () {
                    $scope.draw();
                    $scope.slowProcessPainter.continue();
                });
            });
        }else if($scope.params.demoSelection==2){
            $scope.slowProcessPainter.stop();
            $scope.slowProcessPainter.async = false;
            $scope.config("allc").then(function () {
                $scope.patch(60,60,[[1,1,1],[1,1,1],[1,1,1]]).then(function () {
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


    $scope.setb = function () {
        var data = {
            'handlerName':'SpatialGame_setb',
            'b':$scope.params.b
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {

        });
    };

    $scope.start = function () {
        $scope.setup(120,120).then(function () {
            //$scope.slowProcessPainter.start(120,120);
            $scope.demoSelectionChanged();
        });
        //$scope.slowProcessPainter.start(120,120);
    };

    $scope.stop = function () {
        $scope.slowProcessPainter.stop();
    };

    $scope.asyncstep = function () {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'SpatialGame_asyncstep'
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            deferred.resolve();
        });
        return deferred.promise();
    };

    $scope.step = function () {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'SpatialGame_step'
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            deferred.resolve();
        });
        return deferred.promise();
    };

    $scope.draw = function () {
        var data = {
            'handlerName':'SpatialGame_draw'
        };
        $scope.bridge.callHandler('RunPyFunction',data, function responseCallback(responseData) {
            console.log("JS received response:", responseData);
        });
    };

    $scope.setup = function (width,height) {
        var deferred = $.Deferred();
        var data = {
            'handlerName':'SpatialGame_setup',
            width:width,
            height:height
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
            start:function (width,height) {
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
                    this.counter = 10000;
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