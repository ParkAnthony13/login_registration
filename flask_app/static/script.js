const nums1 = [-2, 5, 7, 0, 3];
const expected1 = 2;

const nums2 = [9, 9];
const expected2 = -1;

const nums3 = [-2, 0, 7, 0, 5];
const expected3 = 3

const nums4 = [-2, 0, 0, 0, 0];
const expected4 = -1

const nums5 = [0, 0, 0, 0, 2];
const expected5 = -1


function balanceIndex1(nums) {
    for (var i = 0; i < nums.length; i++) {
        var balance = {
        }
        for (var j = 0; j < i; j++) {
            if (balance['left']) {
                balance['left'] += nums[j];
            } else {
                balance['left'] = nums[j];
            }
        }
        for (var k = nums.length - 1; k > i; k--) {
            if (balance['right']) {
                balance['right'] += nums[k];
            } else {
                balance['right'] = nums[k];
            }
        }
        if (left === right) {
            return i
        }
    }
    return -1
}


console.log(balanceIndex1(nums1))
console.log(balanceIndex1(nums2))
console.log(balanceIndex1(nums3))
console.log(balanceIndex1(nums4))
console.log(balanceIndex1(nums5))
