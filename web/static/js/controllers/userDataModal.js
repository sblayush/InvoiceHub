angular.module('mainApp')
.factory('userDataModal', function($http) {
	var properties = {
		url : "http://127.0.0.1:8083"
	}
	
	var applicationFlags = {
		isSpinner : false
	}

	return {
		applicationFlags : applicationFlags,
		properties : properties
	}
});