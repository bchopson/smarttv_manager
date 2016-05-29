/**
 * Created by bjami on 3/28/2016.
 */
var editorApp = angular.module('editorApp', ['ngResource', 'dndLists']);

editorApp.config(['$httpProvider', '$resourceProvider', function($httpProvider, $resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

var Tvs = editorApp.factory('Tvs', ['$resource', function($resource) {
  return $resource('/api/tvs/', null);
}]);

var Slides = editorApp.factory('Slides', ['$resource', function($resource) {
  return $resource('/api/tvs/:ids/slides/', { ids: '@ids' }, {
    save: { isArray: true, method: 'POST' }
  });
}]);

var SlidesDetail = editorApp.factory('SlidesDetail', ['$resource', function($resource) {
  return $resource('/api/tvs/:ids/slides/:idx', { ids: '@ids', idx: '@idx' });
}]);

var EditorCtrl = editorApp.controller('EditorCtrl', ['Slides', 'SlidesDetail', 'Tvs',
function(Slides, SlidesDetail, Tvs) {
  var self = this;
  self.tvs = [];
  self.slides = [];
  self.currentTv = null;

  Tvs.query().$promise.then(function(data) {
    self.tvs = data;
    self.currentTv = self.tvs[0];
  });

  self.moveSlide = function(index, oldIndex) {
    self.currentTv.slides.splice(index, 1);
    self.clearSlides();
    for (var i = 0; i < self.currentTv.slides.length; i++) {
      self.currentTv.slides[i].index = i;
    }
    var params = { ids: self.currentTv.id };
    Slides.save(params, self.currentTv.slides);
  };

  self.clearSlides = function () {
    for (var i = 0; i < self.currentTv.slides.length; i++) {
      var params = { ids: self.currentTv.id, idx: self.currentTv.slides[i].index };
      SlidesDetail.delete(params);
    }
  };
}]);
