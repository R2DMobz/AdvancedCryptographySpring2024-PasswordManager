import unittest
Sha3 = __import__("SHA-3")

# Some test cases for SHA3-224 from https://csrc.nist.gov/Projects/Cryptographic-Algorithm-Validation-Program
test224 = {
    "00":"6b4e03423667dbb73b6e15454f0eb1abd4597f9a1b078e3f5b5a6bc7",
    "01":"488286d9d32716e5881ea1ee51f36d3660d70f0db03b3f612ce9eda4",
    "69cb":"94bd25c4cf6ca889126df37ddd9c36e6a9b28a4fe15cc3da6debcdd7",
    "bf5831":"1bb36bebde5f3cb6d8e4672acf6eec8728f31a54dacc2560da2a00cc",
    "d148ce6d":"0b521dac1efe292e20dfb585c8bff481899df72d59983315958391ba",
    "91c71068f8":"989f017709f50bd0230623c417f3daf194507f7b90a11127ba1638fa"
}

class TestSHA3(unittest.TestCase):
        
    def test_SHA_3_224(self):
        for k, v in test224.items():
            test_message = bytes.fromhex(k)
            test_message_digest = bytes.fromhex(v)
            
            message_digest = Sha3.sha3(test_message, 224)
            with self.subTest():
                self.assertEqual(message_digest.hex(), test_message_digest.hex())

if __name__ == '__main__':
    unittest.main()
