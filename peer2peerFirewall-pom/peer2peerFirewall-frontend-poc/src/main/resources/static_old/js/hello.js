var helloApp = angular.module('hello', []);

helloApp.controller('home', function($http) {
	var self = this;
	$http.get('/resource/').then(function(response) {
		self.greeting = response.data;
	})
});