angular.module("mainApp").controller("spinnerController", function(userDataModal, $scope) {
	$scope.applicationFlags = userDataModal.applicationFlags;
});