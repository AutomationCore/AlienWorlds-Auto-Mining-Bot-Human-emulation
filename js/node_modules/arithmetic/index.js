'use strict'

var isNumeric = require('is-numeric')

exports.add = function add (num1, num2) {
  areNumbers(num1, num2)

  return (+num1) + (+num2)
}

exports.sum = function sum (numbers) {
  return numbers.reduce(exports.add)
}

exports.subtract = function subtract (num1, num2) {
  areNumbers(num1, num2)

  return (+num1) - (+num2)
}

exports.difference = function difference (numbers) {
  return numbers.reduce(exports.subtract)
}

exports.multiply = function multiply (num1, num2) {
  areNumbers(num1, num2)

  return (+num1) * (+num2)
}

exports.product = function product (numbers) {
  return numbers.reduce(exports.multiply)
}

exports.divide = function divide (num1, num2) {
  areNumbers(num1, num2)

  return (+num1) / (+num2)
}

exports.quotient = function (numbers) {
  return numbers.reduce(exports.divide)
}

function areNumbers (num1, num2) {
  if (!isNumeric(num1) || !isNumeric(num2)) {
    throw new Error('num1 and num2 must be a number')
  }
}
