(function(root) {
  'use strict';

  function isNumeric(v) {
    if (typeof v === 'number') return true;
    var s = (v||'').toString();
    if (!s) return false;
    return !isNaN(s);
  }

  if (typeof exports !== 'undefined') {
    if (typeof module !== 'undefined' && module.exports) {
      exports = module.exports = isNumeric;
    }
    exports.isNumeric = isNumeric;
  } else if (typeof define === 'function' && define.amd) {
    define([], function() {
      return isNumeric;
    });
  } else {
    root.isNumeric = isNumeric;
  }

})(this);
