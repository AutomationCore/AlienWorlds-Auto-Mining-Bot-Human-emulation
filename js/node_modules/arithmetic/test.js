'use strict'

var test = require('tape')
var arithmetic = require('./')

test(function (t) {
  t.equal(arithmetic.add('2', 1), 3)
  t.equal(arithmetic.add(4, 1), 5)
  t.equal(arithmetic.sum([4, '1', 2]), 7)
  t.equal(arithmetic.subtract(4, 1), 3)
  t.equal(arithmetic.difference([4, '1', 2]), 1)
  t.equal(arithmetic.multiply(10, 2), 20)
  t.equal(arithmetic.product([4, 3, 2]), 24)
  t.equal(arithmetic.divide(10, 2), 5)
  t.equal(arithmetic.quotient([32, 4, 2]), 4)
  t.end()
})
