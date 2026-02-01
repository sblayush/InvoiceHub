angular.module('mainApp')
.controller('aboutPageController', function HomePageController($scope, $http, userDataModal) {

	vm = $scope;
	vm.commonMap = userDataModal.commonMap;
	var url = userDataModal.properties.url;
	
	function getLastUpdatedDate(){
		var data = {
		'command' : "getLastUpdatedDate",
		'argumentsList' : []
		}
		$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
		$http({
			url: url,
			method: "POST",
			data: JSON.stringify(data)
		})
		.then(function(response) {
			vm.commonMap.lastUpdatedDate = response.data['success'];
			console.log(response.data['success']);
			hidePreloader();
		});
	}

});