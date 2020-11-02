function Decoder(bytes, port) {
    var result = "";
    for (var byte in bytes) {

        incomplete_binary = (bytes[byte] >>> 0).toString(2);
        console.log(incomplete_binary.length);
        let number_of_zeros_to_add = 8 - incomplete_binary.length;
        console.log(number_of_zeros_to_add);
        let zeros = ""
        for (let index = 0; index < number_of_zeros_to_add; index++) {
            zeros += '0';
        }
        complete_binary = zeros+incomplete_binary;
        result += complete_binary
    }
    return {
        "string": result
    };
}

console.log(Decoder("046"));