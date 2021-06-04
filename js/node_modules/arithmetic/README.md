# arithmetic
[![Build Status](https://travis-ci.org/bsiddiqui/arithmetic.svg?branch=master)](https://travis-ci.org/bsiddiqui/arithmetic) [![Code Climate](https://codeclimate.com/github/bsiddiqui/arithmetic/badges/gpa.svg)](https://codeclimate.com/github/bsiddiqui/arithmetic) [![Version](https://badge.fury.io/js/arithmetic.svg)](http://badge.fury.io/js/arithmetic) [![Downloads](http://img.shields.io/npm/dm/arithmetic.svg)](https://www.npmjs.com/package/arithmetic)

Arithmetic safely conducts arithmetic operations by ensuring the values are valid numbers and typecasting them prior to evaluation.

## Install
``
$ npm install --save arithmetic
``

## Usage
```js
var arithmetic = require('arithmetic')

arithmetic.add(4, 2)
// => 6
```

## API

#### `arithmetic.add(num1, num2)` -> `number`

##### num1/num2
*Required* <br>
Type: `number`

#### `arithmetic.sum(numbers)` -> `number`

##### numbers
*Required* <br>
Type: `number array`

#### `arithmetic.subtract(num1, num2)` -> `number`

##### num1/num2
*Required* <br>
Type: `number`

#### `arithmetic.difference(numbers)` -> `number`

##### numbers
*Required* <br>
Type: `number array`

#### `arithmetic.multiply(num1, num2)` -> `number`

##### num1/num2
*Required* <br>
Type: `number`

#### `arithmetic.product(numbers)` -> `number`

##### numbers
*Required* <br>
Type: `number array`

#### `arithmetic.divide(num1, num2)` -> `number`

##### num1/num2
*Required* <br>
Type: `number`

#### `arithmetic.quotient(numbers)` -> `number`

##### numbers
*Required* <br>
Type: `number array`
