angular.module('mainApp')
.controller('editInvoicePageController', function editInvoicePageController($scope, $http, userDataModal) {

	vm.commonMap = userDataModal.commonMap;
	var url = userDataModal.properties.url;
	$scope.flags = {
	    order_id : ""
	}
	$scope.amazon = {
	    'hsn': '5608'
	}
    $scope.applicationFlags = userDataModal.applicationFlags;
	$scope.select_origin = function(origin){
	    $scope.origin = origin;
	}	
	
	$scope.items = [];
	$scope.order = {
	    order_id: "",
        invoice_no: "",
        invoice_date: "",
        buyer_name: "",
        billing_addr_line1: "",
        billing_addr_line2: "",
        state: "",
        gstin: "",
        state_code: "",
        items: $scope.items,
        origin: "other"
	}

    $scope.addItem = function (){
        $scope.items.push({
            s_no: $scope.items.length+1,
            desc_line1: "Anti Bird Net",
            desc_line2: "",
            hsn_code: "5608",
            qty: 0,
            rate: 0,
            selling_price: 0,
            discount: 0,
            cgst_rate: 0,
            sgst_rate: 0,
            igst_rate: 0
        });
    }

    $scope.deleteItem = function (){
        $scope.items.pop();
    }

    function getInvoiceSuccess(result){
        order_details = result.data;
        $scope.order.order_id = order_details.order_id;
        $scope.order.invoice_no = order_details.invoice_no;
        $scope.order.invoice_date = order_details.invoice_date;
        $scope.order.buyer_name = "";
        $scope.order.billing_addr_line1 = order_details.billing_addr_line1;
        $scope.order.billing_addr_line2 = order_details.billing_addr_line2;
        $scope.order.state = order_details.state;
        $scope.order.gstin = order_details.gstin;
        $scope.order.state_code = order_details.state_code;
        $scope.order.origin = order_details.origin;

        $scope.items = order_details.items;

        $scope.applicationFlags.isSpinner = false;
        swal({
            title : "Success",
            text : "Successfully got Invoice!",
            icon : "success",
        });
    }

    function getInvoiceFailure(error){
        $scope.applicationFlags.isSpinner = false;
        swal({
            title : "Error",
            text : "Some error in getting Invoice!",
            icon : "error",
        });
    }

	$scope.getInvoice = function(){
	    var data = {
	        order_id: $scope.flags.order_id
	    }
		console.log(data);
        $scope.applicationFlags.isSpinner = true;
		$http({
            method : "POST",
            contentType : 'application/json; charset=utf-8',
            url : url + '/editInvoice',
            data : angular.toJson(data),
        })
        .then(getInvoiceSuccess, getInvoiceFailure);
	}

});