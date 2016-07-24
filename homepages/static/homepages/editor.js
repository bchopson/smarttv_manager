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
  self.currentTv = null;
  self.newSlide = {};

  function getTvs() {
    Tvs.query().$promise.then(function(data) {
      self.tvs = data;
      self.currentTv = self.tvs[0];
    });
  }

  getTvs();

  self.moveSlide = function (index, oldIndex) {
    var detailsParams;
    var slidesParams = { ids: self.currentTv.id };
    self.currentTv.slides.splice(index, 1);
    Slides.delete(slidesParams, function () {
      for (var i = 0; i < self.currentTv.slides.length; i++) {
        detailsParams = { ids: self.currentTv.id, idx: self.currentTv.slides[i].index };
        self.currentTv.slides[i].index = i;
      }
      Slides.save(slidesParams, self.currentTv.slides);
    }, function () {
      alert('Sorry, something went wrong.');
    });
  };

  self.deleteSlide = function (listIndex, index) {
    var params = { ids: self.currentTv.id, idx: index };
    SlidesDetail.delete(params, function () {
      self.currentTv.slides.splice(listIndex, 1);
      self.tvs[self.currentTv.id - 1].slides = self.currentTv.slides;
    }, function () {
      alert('Sorry, something went wrong.');
    });
  };

  self.addSlide = function () {
    var lastSlide = self.currentTv.slides[self.currentTv.slides.length - 1];
    self.newSlide.index = lastSlide.index + 1;
    var params = { ids: self.currentTv.id };
    Slides.save(params, [self.newSlide], function () {
      self.newSlide.tv = self.currentTv.id;
      self.currentTv.slides.push(self.newSlide);
    }, function () {
      alert('Sorry, something went wrong.');
    });
  };
}]);
