(function(){
    var accountingApp = angular.module("mainApp", ["ngRoute"]);

    accountingApp.config(function($routeProvider) {
        $routeProvider.when("/", {
            templateUrl : "/static/partials/aboutPage.html",
            controller : "aboutPageController"
        }).when("/about", {
            templateUrl : "/static/partials/aboutPage.html",
            controller : "aboutPageController"
        }).when("/invoice", {
            templateUrl : "/static/partials/invoicePage.html",
            controller : "invoicePageController"
        }).when("/accounts", {
            templateUrl : "/static/partials/accountsPage.html",
            controller : "accountsPageController"
        }).when("/sales", {
            templateUrl : "/static/partials/salesPage.html",
            controller : "salesPageController"
        }).when("/editInvoice", {
            templateUrl : "/static/partials/editInvoicePage.html",
            controller : "editInvoicePageController"
        }).otherwise({
            redirectTo : '/'
        });
    });
}());
