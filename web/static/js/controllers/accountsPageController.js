angular.module('mainApp')
.controller('accountsPageController', function HomePageController($scope, $http, userDataModal) {

	vm = $scope;
	var url = userDataModal.properties.url;

    $scope.orders_rows = [];
    $scope.showOrdersTable = false;

    $scope.t_qty = 0;
    $scope.t_amnt = 0;
    $scope.t_cgst = 0;
    $scope.t_sgst = 0;
    $scope.t_igst = 0;
    $scope.total_am = 0;

	$scope.years = ['2018', '2019', '2020'];
    $scope.selectedYear = $scope.years[0];
    $scope.selectYear = function (year) {
        $scope.selectedYear = year;
    }

	$scope.months = {"January":1, "February" :2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9,  "October":10,  "November":11,  "December":12}
    $scope.selectedMonth = "January";
    $scope.selectMonth = function (month) {
        $scope.selectedMonth = month;
    }

    $scope.roundOff = function(num){
        return num.toFixed(2);
    }
	
	function getData(){
	    var data = {
            "month": $scope.months[$scope.selectedMonth],
            "year": $scope.selectedYear
        }
	    return data;
	}

    function getOrdersForMonthSuccess(result){
        console.log(result);
        $scope.applicationFlags.isSpinner = false;
        orders = result.data;
        $scope.orders_rows = [];
        $scope.t_qty = 0;
        $scope.t_amnt = 0;
        $scope.t_cgst = 0;
        $scope.t_sgst = 0;
        $scope.t_igst = 0;
        $scope.total_am = 0;

        for(order_index in orders){
            order = orders[order_index];
            items = order['items'];
            for(item_index in items){
                var order_row = JSON.parse(JSON.stringify(orders[order_index]));
                delete(order_row['items']);
                for(item_key in items[item_index]){
                    order_row[item_key] = items[item_index][item_key];
                }
                order_row['amount'] = parseFloat(order_row['rate']) * (parseFloat(order_row['qty']) - parseFloat(order_row['discount']))
                order_row['total_amount'] = parseFloat(order_row['amount']) + (parseFloat(order_row['cgst_amt'])+parseFloat(order_row['igst_amt'])+parseFloat(order_row['sgst_amt']))
//                order_row['amount'] = parseFloat(order_row['total_amount']) - (parseFloat(order_row['cgst_amt'])+parseFloat(order_row['igst_amt'])+parseFloat(order_row['sgst_amt']))

                $scope.t_qty += parseInt(order_row['qty']);
                $scope.t_amnt += order_row['amount'];
                $scope.t_cgst += order_row['cgst_amt'];
                $scope.t_sgst += order_row['sgst_amt'];
                $scope.t_igst += order_row['igst_amt'];
                $scope.total_am += order_row['total_amount'];

                delete(order_row['_id']);
                $scope.orders_rows.push(order_row);
            }
        }
        console.log($scope.orders_rows);
        $scope.showOrdersTable = true;
    }

    function getOrdersForMonthFailure(error){
        console.log(error);
        $scope.applicationFlags.isSpinner = false;
        swal({
            title : "Error",
            text : "Some error in generating Invoice!",
            icon : "error",
        });
    }
	
	$scope.getOrdersForMonth = function(){
	    var data = getData()
		console.log(data);
        $scope.applicationFlags.isSpinner = true;
		$http({
            method : "POST",
            contentType : 'application/json; charset=utf-8',
            url : url + '/getOrdersForMonth',
            data : angular.toJson(data),
        })
        .then(getOrdersForMonthSuccess, getOrdersForMonthFailure);
	}

	$scope.selectElementContents = function () {
	    el = angular.element('#account_table')
        var body = document.body, range, sel;
        if (document.createRange && window.getSelection) {
            range = document.createRange();
            sel = window.getSelection();
            sel.removeAllRanges();
            try {
                range.selectNodeContents(el);
                sel.addRange(range);
            } catch (e) {
                range.selectNode(el);
                sel.addRange(range);
            }
        } else if (body.createTextRange) {
            range = body.createTextRange();
            range.moveToElementText(el);
            range.select();
        }
    }

});