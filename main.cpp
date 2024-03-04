#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstring>

// Function declarations
std::vector<std::vector<unsigned char>> key_expansion(const std::string& key);
std::vector<unsigned char> encrypt(const std::vector<unsigned char>& input, const std::string& key);
std::vector<unsigned char> decrypt(const std::vector<unsigned char>& input, const std::string& key);
std::vector<std::vector<unsigned char>> add_round_key(const std::vector<std::vector<unsigned char>>& state, const std::vector<std::vector<unsigned char>>& key_schedule, int round);

std::vector<std::vector<unsigned char>> sub_bytes(const std::vector<std::vector<unsigned char>>& state, bool inv);
std::vector<std::vector<unsigned char>> shift_rows(const std::vector<std::vector<unsigned char>>& state, bool inv);
std::vector<std::vector<unsigned char>> mix_columns(const std::vector<std::vector<unsigned char>>& state, bool inv);

std::vector<unsigned char> right_shift(std::vector<unsigned char> vec, int shift);
std::vector<unsigned char> left_shift(std::vector<unsigned char> vec, int shift);
std::vector<unsigned char> sub_word(const std::vector<unsigned char>& word);
std::vector<unsigned char> rot_word(const std::vector<unsigned char>& word);

unsigned char mul_by_02(unsigned char num);
unsigned char mul_by_03(unsigned char num);
unsigned char mul_by_09(unsigned char num);
unsigned char mul_by_0b(unsigned char num);
unsigned char mul_by_0d(unsigned char num);
unsigned char mul_by_0e(unsigned char num);

const unsigned char sbox[256] = {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
};

const unsigned char inv_sbox[256] = {
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
};

const int nb = 4;  // number of columns in the state (for AES = 4)
const int nr = 14;  // number of rounds in cipher cycle (if nb = 4 and nk = 8)
const int nk = 8;  // the key length (in 32-bit words)

// Define the round constants for a 256-bit key
const unsigned char rcon[10] = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36};

std::vector<unsigned char> encrypt(const std::vector<unsigned char>& input_bytes, const std::string& key) {
    std::vector<std::vector<unsigned char>> state(4, std::vector<unsigned char>(nb));
    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < nb; c++) {
            state[r][c] = input_bytes[r + 4 * c];
        }
    }

    std::vector<std::vector<unsigned char>> key_schedule = key_expansion(key);

    state = add_round_key(state, key_schedule, 0);

    for (int rnd = 1; rnd < nr; rnd++) {
        state = sub_bytes(state, false);
        state = shift_rows(state, false);
        state = mix_columns(state, false);
        state = add_round_key(state, key_schedule, rnd);
    }

    state = sub_bytes(state, false);
    state = shift_rows(state, false);
    state = add_round_key(state, key_schedule, nr);

    std::vector<unsigned char> output(4 * nb);
    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < nb; c++) {
            output[r + 4 * c] = state[r][c];
        }
    }

    return output;
}

std::vector<unsigned char> decrypt(const std::vector<unsigned char>& cipher, const std::string& key) {
    std::vector<std::vector<unsigned char>> state(nb, std::vector<unsigned char>(4));
    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < nb; c++) {
            state[r][c] = cipher[r + 4 * c];
        }
    }

    std::vector<std::vector<unsigned char>> key_schedule = key_expansion(key);

    state = add_round_key(state, key_schedule, nr);

    for (int rnd = nr-1; rnd > 0; rnd--) {
        state = shift_rows(state, true);
        state = sub_bytes(state, true);
        state = add_round_key(state, key_schedule, rnd);
        state = mix_columns(state, true);
    }

    state = shift_rows(state, true);
    state = sub_bytes(state, true);
    state = add_round_key(state, key_schedule, 0);

    std::vector<unsigned char> output(4 * nb);
    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < nb; c++) {
            output[r + 4 * c] = state[r][c];
        }
    }

    return output;
}

std::vector<std::vector<unsigned char>> sub_bytes(const std::vector<std::vector<unsigned char>>& state, bool inv) {
    const unsigned char* box = inv ? inv_sbox : sbox;
    std::vector<std::vector<unsigned char>> result(state);
    for (int i = 0; i < result.size(); i++) {
        for (int j = 0; j < result[i].size(); j++) {
            int row = result[i][j] / 0x10;
            int col = result[i][j] % 0x10;
            result[i][j] = box[16 * row + col];
        }
    }
    return result;
}

std::vector<std::vector<unsigned char>> shift_rows(const std::vector<std::vector<unsigned char>>& state, bool inv) {
    std::vector<std::vector<unsigned char>> result(state);
    for (int i = 0; i < nb; i++) {
        if (inv) {
            result[i] = right_shift(result[i], i); // Use right_shift for inverse
        }
        else {
            result[i] = left_shift(result[i], i); // Use left_shift for normal
        }
    }
    return result;
}
std::vector<unsigned char> right_shift(std::vector<unsigned char> vec, int shift) {
    std::vector<unsigned char> result(vec.size());
    for (int i = 0; i < vec.size(); i++) {
        result[i] = vec[(i - shift + vec.size()) % vec.size()];
    }
    return result;
}

std::vector<unsigned char> left_shift(std::vector<unsigned char> vec, int shift) {
    std::vector<unsigned char> result(vec.size());
    for (int i = 0; i < vec.size(); i++) {
        result[i] = vec[(i + shift) % vec.size()];
    }
    return result;
}

std::vector<std::vector<unsigned char>> mix_columns(const std::vector<std::vector<unsigned char>>& state, bool inv) {
    std::vector<std::vector<unsigned char>> result(state);
    for (int i = 0; i < nb; i++) {
        if (inv) {
            unsigned char s0 = mul_by_0e(result[0][i]) ^ mul_by_0b(result[1][i]) ^ mul_by_0d(result[2][i]) ^ mul_by_09(result[3][i]);
            unsigned char s1 = mul_by_09(result[0][i]) ^ mul_by_0e(result[1][i]) ^ mul_by_0b(result[2][i]) ^ mul_by_0d(result[3][i]);
            unsigned char s2 = mul_by_0d(result[0][i]) ^ mul_by_09(result[1][i]) ^ mul_by_0e(result[2][i]) ^ mul_by_0b(result[3][i]);
            unsigned char s3 = mul_by_0b(result[0][i]) ^ mul_by_0d(result[1][i]) ^ mul_by_09(result[2][i]) ^ mul_by_0e(result[3][i]);
            result[0][i] = s0;
            result[1][i] = s1;
            result[2][i] = s2;
            result[3][i] = s3;
        } else {
            unsigned char s0 = mul_by_02(result[0][i]) ^ mul_by_03(result[1][i]) ^ result[2][i] ^ result[3][i];
            unsigned char s1 = result[0][i] ^ mul_by_02(result[1][i]) ^ mul_by_03(result[2][i]) ^ result[3][i];
            unsigned char s2 = result[0][i] ^ result[1][i] ^ mul_by_02(result[2][i]) ^ mul_by_03(result[3][i]);
            unsigned char s3 = mul_by_03(result[0][i]) ^ result[1][i] ^ result[2][i] ^ mul_by_02(result[3][i]);
            result[0][i] = s0;
            result[1][i] = s1;
            result[2][i] = s2;
            result[3][i] = s3;
        }
    }
    return result;
}

std::vector<std::vector<unsigned char>> key_expansion(const std::string& key) {
    std::vector<unsigned char> key_symbols(key.begin(), key.end());

    if (key_symbols.size() <= 4 * nk) {
        for (int i = 4 * nk - key_symbols.size(); i > 0; i--) {
            key_symbols.push_back(0x01);
        }
    }

    if (key_symbols.size() < 32) {
        throw std::invalid_argument("Key length must be at least 32 bytes for AES-256.");
    }

    std::vector<std::vector<unsigned char>> key_schedule(4, std::vector<unsigned char>(nb));
    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < nk; c++) {
            key_schedule[r][c] = key_symbols[r + 4 * c];
        }
    }

    for (int col = nk; col < nb * (nr + 1); col++) {
        std::vector<unsigned char> tmp(key_schedule.size());
        for (int row = 0; row < 4; row++) {
            tmp[row] = key_schedule[row][col - 1];
        }
        if (col % nk == 0) {
            tmp = sub_word(rot_word(tmp));
            tmp[0] ^= rcon[col / nk - 1];
        } else if (nk > 6 && col % nk == 4) {
            tmp = sub_word(tmp);
        }
        for (int row = 0; row < 4; row++) {
            key_schedule[row].push_back(key_schedule[row][col - nk] ^ tmp[row]);
        }
    }

    return key_schedule;
}

std::vector<unsigned char> sub_word(const std::vector<unsigned char>& word) {
    std::vector<unsigned char> result(word.size());
    for (int i = 0; i < word.size(); i++) {
        result[i] = sbox[word[i]];
    }
    return result;
}

std::vector<unsigned char> rot_word(const std::vector<unsigned char>& word) {
    std::vector<unsigned char> result(word.size());
    for (int i = 0; i < word.size() - 1; i++) {
        result[i] = word[i + 1];
    }
    result[word.size() - 1] = word[0];
    return result;
}

std::vector<std::vector<unsigned char>> add_round_key(const std::vector<std::vector<unsigned char>>& state, const std::vector<std::vector<unsigned char>>& key_schedule, int round = 0) {
    std::vector<std::vector<unsigned char>> result(state);
    for (int j = 0; j < state[0].size(); j++) {
        for (int i = 0; i < state.size(); i++) {
            result[i][j] ^= key_schedule[i][nb * round + j];
        }
    }
    return result;
}

unsigned char mul_by_02(unsigned char num) {
    char res;
    if (num < 0x80){
        res = num << 1;
    }
    else{
        res = (num << 1)^0x1b;
    }
    return res;
}

unsigned char mul_by_03(unsigned char num) {
    return mul_by_02(num) ^ num;
}

unsigned char mul_by_09(unsigned char num) {
    return mul_by_02(mul_by_02(mul_by_02(num))) ^ num;
}

unsigned char mul_by_0b(unsigned char num) {
    return mul_by_02(mul_by_02(mul_by_02(num))) ^ mul_by_02(num) ^ num;
}

unsigned char mul_by_0d(unsigned char num) {
    return mul_by_02(mul_by_02(mul_by_02(num))) ^ mul_by_02(mul_by_02(num)) ^ num;
}

unsigned char mul_by_0e(unsigned char num) {
    return mul_by_02(mul_by_02(mul_by_02(num))) ^ mul_by_02(mul_by_02(num)) ^ mul_by_02(num);
}

std::vector<unsigned char> pad(const std::vector<unsigned char>& data) {
    int padding_length = 32 - data.size() % 32;
    std::vector<unsigned char> padding(padding_length, padding_length);
    std::vector<unsigned char> padded_data(data);
    padded_data.insert(padded_data.end(), padding.begin(), padding.end());
    return padded_data;
}

std::vector<unsigned char> unpad(const std::vector<unsigned char>& data) {
    int padding_length = data[data.size() - 1];
    std::vector<unsigned char> unpadded_data(data.begin(), data.end() - padding_length);
    return unpadded_data;
}

void main_func(const std::string& input_path, const std::string& key) {
    std::ifstream input_file(input_path, std::ios::binary);
    if (!input_file) {
        std::cout << "Failed to open input file." << std::endl;
        return;
    }

    std::vector<unsigned char> data(std::istreambuf_iterator<char>(input_file), {});
    input_file.close();

    std::vector<unsigned char> padded_data = pad(data);

    std::vector<unsigned char> crypted_data;
    std::vector<unsigned char> temp;
    for (unsigned char byte : padded_data) {
        temp.push_back(byte);
        if (temp.size() == 16) {
            std::vector<unsigned char> encrypted_temp = encrypt(temp, key);
            crypted_data.insert(crypted_data.end(), encrypted_temp.begin(), encrypted_temp.end());
            temp.clear();
        }
    }

    std::string out_path = "crypted_" + input_path;
    std::ofstream output_file(out_path, std::ios::binary);
    if (!output_file) {
        std::cout << "Failed to create output file." << std::endl;
        return;
    }
    output_file.write(reinterpret_cast<const char*>(crypted_data.data()), crypted_data.size());
    output_file.close();

    std::vector<unsigned char> decrypted_data;
    temp.clear();
    for (unsigned char byte : crypted_data) {
        temp.push_back(byte);
        if (temp.size() == 16) {
            std::vector<unsigned char> decrypted_temp = decrypt(temp, key);
            decrypted_data.insert(decrypted_data.end(), decrypted_temp.begin(), decrypted_temp.end());
            temp.clear();
        }
    }

    std::vector<unsigned char> unpadded_data = unpad(decrypted_data);

    std::string decrypted_out_path = "decrypted_" + input_path;
    std::ofstream decrypted_output_file(decrypted_out_path, std::ios::binary);
    if (!decrypted_output_file) {
        std::cout << "Failed to create decrypted output file." << std::endl;
        return;
    }
    decrypted_output_file.write(reinterpret_cast<const char*>(unpadded_data.data()), unpadded_data.size());
    decrypted_output_file.close();

    std::cout << "New encrypted file here: " << out_path << std::endl;
    std::cout << "New decrypted file here: " << decrypted_out_path << std::endl;
}

int main() {
    std::string input_path = "moby10b.txt";
    std::string key = "192837465192837465";
    main_func(input_path, key);
    return 0;
}
