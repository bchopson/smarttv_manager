/**
 * Created by bjami on 3/28/2016.
 */
var editorApp = angular.module('editorApp', ['ngResource', 'ngRoute']);

editorApp.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

var Tvs = editorApp.factory('Tvs', ['$resource', function($resource) {
  return $resource('/api/tvs/', null);
}]);

var Slides = editorApp.factory('Slides', ['$resource', function($resource) {
  return $resource('/api/tvs/:ids/slides/', { ids: '@ids' });
}]);

var EditorCtrl = editorApp.controller('EditorCtrl', ['$scope', '$resource', '$route', 'Slides', 'Tvs',
function($scope, $resource, $route, Slides, Tvs) {
  $scope.tvs = [];
  $scope.slides = [];
  $scope.currentTv = null;

  Tvs.query().$promise.then(function(data) {
    $scope.tvs = data;
    $scope.currentTv = $scope.tvs[0];
  });
}]);
