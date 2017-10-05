var app = angular.module('myApp', ['ui.bootstrap']);

app.filter('startFrom', function() {
    return function(input, start) {
        if(input) {
            start = +start; //parse to int
            return input.slice(start);
        }
        return [];
    }
});

app.filter('unique', function() {
   return function(collection, keyname) {
      var output = [], 
          keys = [];

      angular.forEach(collection, function(item) {
          var key = item[keyname];
          if(keys.indexOf(key) === -1) {
              keys.push(key);
              output.push(item);
          }
      });
      return output;
   };
});

app.filter('isArray', function() {
  return function (input) {
    return angular.isArray(input);
  };
});

app.filter('isObject', function() {
  return function (input) {
    return angular.isObject(input);
  };
});

app.filter('isHTTP', function() { 
  return function (input) {
    var lowerStr = input.toLowerCase();
    return lowerStr.indexOf('http://') === 0 || lowerStr.indexOf('https://') === 0;
  };
});

app.controller('dataCrtl', function ($http, $timeout, filterFilter) {
    var vm = this;

    vm.hardware = true; // hardware features
    vm.software = true; // software features
    vm.security = true; // security features
    vm.feature = ""; //feature
    vm.server = "ALL"; //default server
    vm.predicate = "Server"; //default order
    vm.entryLimit = 5; //max no of items to display in a page
    vm.colHide = []; //columns to hide
    vm.getData = function() {
	var mybody = angular.element(document).find('body'); 
	mybody.addClass('waiting');
        $http.get(vm.feature).success(function(data){
	    vm.serversList = data;
	    if (vm.server != "ALL") {
            	vm.list = filterFilter(data, {'Server': vm.server}, true);
		vm.predicate = "Server";
		if (vm.list.length == 0) {
		    vm.server = "ALL";
            	    vm.list = data;
		}
	    } else {
            	vm.list = data;
	    }
            vm.currentPage = 1; //current page
            vm.filteredItems = vm.list.length; //Initially for no filter  
            vm.totalItems = vm.list.length;
	    mybody.removeClass('waiting');
        }).error(function() {
	    vm.serversList = "";
	    vm.server = "ALL";
	    vm.predicate = "Server";
	    vm.list = "";
            vm.filteredItems = vm.list.length; //Initially for no filter  
            vm.totalItems = vm.list.length;
	    mybody.removeClass('waiting');
	});
    };
    vm.setPage = function(pageNo) {
        vm.currentPage = pageNo;
    };
    vm.filter = function() {
        $timeout(function() { 
            vm.filteredItems = vm.filtered.length;
        }, 10);
    };
    vm.sort_by = function(predicate) {
        vm.predicate = predicate;
        vm.reverse = !vm.reverse;
    };
    vm.sortSub_by = function(predicate) {
        vm.predicateSub = predicate;
        vm.reverseSub = !vm.reverseSub;
    };
    vm.sortSub2_by = function(predicate) {
        vm.predicateSub2 = predicate;
        vm.reverseSub2 = !vm.reverseSub2;
    };
    vm.hide = function(column) {
	vm.colHide.push(column);
    };
    vm.isHidden = function(column) {
	if (vm.colHide.indexOf(column) < 0) {
	    return false;
	} else {
	    return true;
	}
    };
    vm.showAll = function(featureCol) {
	for (i = vm.colHide.length-1; i >= 0; i--) {
	    var item = vm.colHide[i].toString();
	    if (item.startsWith(featureCol)) {
		vm.colHide.splice(i,1);
	    }
	}
    };
});
