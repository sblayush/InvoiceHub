angular.module('mainApp')
.controller('invoicePageController', function HomePageController($scope, $http, userDataModal) {

	vm.commonMap = userDataModal.commonMap;
	var url = userDataModal.properties.url;
	$scope.origin = "amazon";
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

    function getData(){
        var data;
        if ($scope.origin == 'amazon'){
            data = {
                'order_id' : $scope.flags.order_id,
                'origin' : $scope.origin,
                'hsn' : $scope.amazon.hsn
            }
        }
        else if($scope.origin == 'flipkart'){
            data = {
                'order_id' : $scope.flags.order_id,
                'origin' : $scope.origin
            }
        }
        else{
             data = {
                'order' : $scope.order,
                'origin' : $scope.origin
            }
        }
        return data;
    }

    function createInvoiceSuccess(result){
        $scope.applicationFlags.isSpinner = false;
        swal({
            title : "Success",
            text : "Successfully generated Invoice!",
            icon : "success",
        });
    }

    function createInvoiceFailure(error){
        $scope.applicationFlags.isSpinner = false;
        swal({
            title : "Error",
            text : "Some error in generating Invoice!",
            icon : "error",
        });
    }

	$scope.createInvoice = function(){
	    var data = getData()
		console.log(data);
        $scope.applicationFlags.isSpinner = true;
		$http({
            method : "POST",
            contentType : 'application/json; charset=utf-8',
            url : url + '/createInvoice',
            data : angular.toJson(data),
        })
        .then(createInvoiceSuccess, createInvoiceFailure);
	}

});