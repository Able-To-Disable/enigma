from string import ascii_lowercase
import json


class enigma:
    def __init__(self, steckerbrett=None, settings_file=None, alpha=None, beta=None, gama=None):
        if steckerbrett is None:
            steckerbrett = {" ": " "}
        self.alphabet = list(ascii_lowercase)
        self.steckerbrett = steckerbrett
        if settings_file is not None:
            try:
                self.settings = json.load(open(settings_file, 'r'))[0]
            except IOError:
                print("Enigma Error 1: There is no such setting file")
            finally:
                self.steckerbrett = self.settings['steckerbrett']
                self.alpha = self.settings['alpha']
                self.beta = self.settings['beta']
                self.gama = self.settings['gama']
        elif alpha is not None and beta is not None and gama is not None and steckerbrett is not None:
            if type(steckerbrett) is not dict:
                self.steckerbrett = {" ": " "}
            self.alpha = alpha
            self.beta = beta
            self.gama = gama
        else:
            if type(steckerbrett) is not dict:
                self.steckerbrett = {" ": " "}
            rotors = [self.alpha, self.beta, self.gama]
            for rotor in rotors:
                if rotor is None or type(rotor) is not int or type(rotor) is not float:
                    rotor = 0
                else:
                    rotor = rotor % 26
            self.alpha = rotors[0]
            self.beta = rotors[1]
            self.gama = rotors[2]
        for letter in list(self.steckerbrett.keys()):
            if letter in self.alphabet:
                self.alphabet.remove(letter)
                self.alphabet.remove(self.steckerbrett[letter])
                self.steckerbrett.update({self.steckerbrett[letter]: letter})
        self.reflector = [leter for leter in reversed(self.alphabet)]

    def permutate(self, rotor):
        new_alphabet = ''.join(self.alphabet)
        new_alphabet = list(new_alphabet)
        for iter in range(rotor):
            new_alphabet.insert(0, new_alphabet[-1])
            new_alphabet.pop(-1)
        print(self.alphabet)
        print(new_alphabet)
        return new_alphabet

    def inverse_permutation(self, rotor):
        new_alphabet = ''.join(self.alphabet)
        new_alphabet = list(new_alphabet)
        for iter in range(rotor):
            new_alphabet.append(new_alphabet[0])
            new_alphabet.pop(0)
        print(self.alphabet)
        print(new_alphabet)
        return new_alphabet

    def encrypt_text(self, text):
        encrypted_text = []
        text = text.lower()
        text.split()
        for letter in text:
            if letter in self.steckerbrett:
                encrypted_text.append(self.steckerbrett[letter])
                self.alpha += 1
                if self.alpha % len(self.alphabet) == 0:
                    self.beta += 1
                    self.alpha = 0
                if self.beta % len(self.alphabet) == 0 and self.alpha % len(self.alphabet) != 0 and self.beta >= len(
                        self.alphabet) - 1:
                    self.gama += 1
                    self.beta = 1
            else:
                temp_letter = self.permutate(self.alpha)[self.alphabet.index(letter)]
                print("alpha - {}".format(temp_letter))
                temp_letter = self.permutate(self.beta)[self.alphabet.index(temp_letter)]
                print("beta - {}".format(temp_letter))
                temp_letter = self.permutate(self.gama)[self.alphabet.index(temp_letter)]
                print("gama - {}".format(temp_letter))
                print(temp_letter)
                temp_letter = self.reflector[self.alphabet.index(temp_letter)]
                print("reflector - > {}".format(temp_letter))
                temp_letter = self.inverse_permutation(self.gama)[self.alphabet.index(temp_letter)]
                print("gama - {}".format(temp_letter))
                temp_letter = self.inverse_permutation(self.beta)[self.alphabet.index(temp_letter)]
                print("beta - {}".format(temp_letter))
                temp_letter = self.inverse_permutation(self.alpha)[self.alphabet.index(temp_letter)]
                print("alpha - {}".format(temp_letter))
                encrypted_text.append(temp_letter)
                print(temp_letter)
                self.alpha += 1
                if self.alpha % len(self.alphabet) == 0:
                    self.beta += 1
                    self.alpha = 0
                if self.beta % len(self.alphabet) == 0 and self.alpha % len(self.alphabet) != 0 and self.beta >= len(
                        self.alphabet) - 1:
                    self.gama += 1
                    self.beta = 1
                print('alpha - {}'.format(self.alpha))
        return ''.join(encrypted_text)

    def encrypt_txt(self, original_path, encrypted_path=None):
        global file
        try:
            file = open(original_path, 'r')
        except IOError as e:
            print("Enigma Error 2: There is no such file to encrypt")
            return None
        finally:
            if encrypted_path == None :
                encrypted_path = "encrypted_" + original_path
            encrypted_file = open(encrypted_path, 'w')
            for line in file:
                encrypted_file.write(self.encrypt_text(line.rstrip()) + '\n')
            file.close()
            encrypted_file.close()
